
# Copyright (c) 2011 Nokia Corporation and/or its subsidiary(-ies).
# All rights reserved.
# This component and the accompanying materials are made available
# under the terms of the License "Eclipse Public License v1.0"
# which accompanies this distribution, and is available
# at the URL "http://www.eclipse.org/legal/epl-v10.html".

"""
Gathers performance metrics from the logs of a complex multi-step build.
Supports Helium 9-12 at the moment with support for the new logging format of 
Helium 13 coming soon [?].

Can also extract useful data from emake annotation files.
"""

import sys
import os
import re
import datetime

import allo.annofile
import allo.utils

class UndeterminedBuildID(Exception):
	pass

class LogfileNotFound(Exception):
	pass

class HeliumLog(object):
	""" Some common properties of any log file in a helium build """
	filenamesuffix = None

	def __init__(self, logpath, buildid, options=None):

		self.logfilename = os.path.join(logpath, buildid + self.filenamesuffix)
		self.buildid = buildid
		self.options = options

	@classmethod
	def findall(c, logpath):
		""" Find all the logs that are of this type - essentially also finds all builds 
		    which dumped their output in the same place """
		filename_re = re.compile('(.*/)?(?P<buildid>[^\\\/]*)' + c.filenamesuffix)
		logs = {}
		for f in os.listdir(logpath):
			m = filename_re.match(f)
			if m:
				file_buildid = m.groupdict()['buildid']
				logs[file_buildid] = os.path.join(logpath,f)
		return logs


	def __str__(self):
		return "<metric name='buildid'  value='{0}'>\n".format(self.buildid)

class MainAntLog(HeliumLog):
	""" This is the primary log of the helium build.  Useful for obtaining the total build time. Not good for this if the build failed. """
	# output/logs/92_7952_201020_003_main.ant.log
	filenamesuffix = "_main.ant.log"
	timeformat = "%Y/%m/%d %H:%M:%S:%f" # e.g. Thu 2010/06/24 09:15:42:625 AM

	def __init__(self, logpath, buildid, options=None):
		super(MainAntLog,self).__init__(logpath, buildid, options)

		# Starting logging into y:\output\logs\mcl_7901_201024_20100623181534_main.ant.log at Wed 2010/06/23 21:16:12:972 PM
		# Stopping logging into y:\output\logs\mcl_7901_201024_20100623181534_main.ant.log from hlm:record task at Thu 2010/06/24 09:15:42:625 AM

		start_re = re.compile("Starting logging into [^ ]+ at ... ([^ ]+ +[^ ]+) .*")
		stop_re = re.compile("Stopping logging into [^ ]+ from [^ ]+ task at ... ([^ ]+ +[^ ]+) (AM)|(PM).*")
		start_time = None
		stop_time = None
		with open(self.logfilename) as f:
			for l in f:
				if start_time is None:
					m = start_re.match(l)
					if m:
						start_time = datetime.datetime.strptime(m.groups()[0], self.timeformat)
						
				else: # if there are many stop lines then make sure the last one overrides the others
					m = stop_re.match(l)
					if m:
						stop_time = datetime.datetime.strptime(m.groups()[0], self.timeformat)

		if start_time and stop_time:
			build_duration = stop_time - start_time  # returns a timedelta object
			self.build_duration = build_duration.seconds +  86400 * build_duration.days  # seconds
		else:
			sys.stderr.write("start time and/or stop time not available.\n")
			self.build_duration = 0
			
	def __str__(self):
		return "<metric name='build_duration' value='{0}'>\n".format(self.build_duration)
		
class AntEnvLog(HeliumLog):
	# output/logs/92_7952_201020_003_ant_env.log
	filenamesuffix = "_ant_env.log"

	def __init__(self, logpath, buildid):
		super(AntEnvLog,self).__init__(logpath, buildid)

class TargetTimesLog(HeliumLog):
	"""Very useful timing data from Ant but does not get created in all builds by default (must be configured)"""
	# output/logs/92_7952_custom_dilbert_201022_dilbert_targetTimesLog.csv
	filenamesuffix = "_targetTimesLog.csv"

	def __init__(self, logpath, buildid):
		super(TargetTimesLog,self).__init__(logpath, buildid)
		self.raptorsecs = 0
		self.totalsecs = 0

		with open(self.logfilename) as f:
			for ll in f:
				l = ll.rstrip("\n")
				(rname, rsecs) = l.split(",")
				rsecs = int(rsecs)
				self.totalsecs += rsecs
				if rname == "compile-sbs":
					self.raptorsecs += rsecs

	def __str__(self):
		s = "<metric name='build_duration' value='{0}'>\n" \
			"<metric name='raptor_duration' value='{1}'>\n".format(self.totalsecs, self.raptorsecs)
		return s

class RaptorAnnofile(object):
	"""Thin wrapper around the annofile class to make it relevant to
	this utility.  Parses anno files lazily so that one can use it
	to represent an annotation file that one knows about without
	committing to the potentially time consuming task of parsing it.
	Referencing the annofile attribute triggers parsing."""
	# Examples:
	# 92_7952_custom_dilbert_201022_dilbert_dfs_build_sf_tools_all.resource.emake.anno
	# 92_7952_custom_dilbert_201022_dilbert_dfs_build_sf_dfs_variants.default.emake.anno
	# 92_7952_201022_003_dfs_build_ncp_dfs_variants.resource_deps.emake.anno
	def __init__(self, filename, buildid, maxagents):
		self.phase = ""
		self.filename = filename
		self.buildid = buildid

		# self.annofile respond with this value "lazily" 
		self.maxagents = maxagents

	def __getattr__(self, name):
		if name=='annofile':
			self.annofile = allo.annofile.Annofile(self.filename, self.maxagents)
			return self.annofile
		else:
			raise AttributeError("'RaptorAnnofile' object has no attribute '{0}'".format(name))
			

	def __str__(self):
		return "<annofile name='{0}' phase='{1}'>\n{2}</annofile>\n" \
	           .format(os.path.basename(self.filename), self.phase, str(self.annofile))


class RaptorBuild(HeliumLog):
	"""Any Raptor logfile.  Mainly used for getting the names of the 
	annotation files which the annofile parser will use. Also gets
	the version of raptor and the total time taken by this particular
	invocation of Raptor"""
	def __init__(self, logpath, buildid, build, options=None):
		self.filenamesuffix = '_' + build
		super(RaptorBuild,self).__init__(os.path.join(logpath, "compile"), buildid, options)
		self.build = build

		if not os.path.isfile(self.logfilename):
			raise LogfileNotFound("missing log file: {0}\n".format(self.logfilename))
		
		self.annofile_refs = []	
		self.build_duration = None 
		
		status_re = re.compile("<status exit='([a-z]+)'")
		compilation_re = re.compile("<recipe name='[^']*compile[^']*'")
		emake_invocation_re = re.compile("<info>Executing.*--emake-annofile=([^ ]+)")
		emake_maxagents_re = re.compile("--emake-maxagents=(\d+)")
		sbs_version_re = re.compile("<info>sbs: version ([^\n\r<]*)")
		run_time_re = re.compile("<info>Run time ([0-9]+) seconds</info>")
		
		self.recipes = { 'TOTAL':0, 'ok':0, 'failed':0, 'retry':0, 'COMPILE':0 }
		
		with open(self.logfilename) as f:
			sys.stderr.write("      parsing build log {0}\n".format(os.path.split(self.logfilename)[1]))
			for l in f:
				# match in order of likelihood (most probable first)
				
				m = status_re.match(l)
				if m:
					self.recipes['TOTAL'] += 1
					status = m.group(1)
					try:
						self.recipes[status] += 1
					except KeyError:
						sys.stderr.write("unknown recipe status '{0}'".format(status))
					continue
				
				m = compilation_re.match(l)
				if m:
					self.recipes['COMPILE'] += 1
					continue
				
				m = emake_invocation_re.match(l)
				if m:
					(adir, aname) = os.path.split(m.group(1))
					if aname.find("_pp_")==-1: # no parallel parsing ones preferably
						sys.stderr.write("        found annotation file {0}\n".format(aname))
						
						# if --emake-maxagents is present then use that, otherwise use
						# the value passed in through the options.
						m = emake_maxagents_re.match(l)
						if m:
							maxagents = int(m.group(1))
						elif options:
							maxagents = options.maxagents
							sys.stderr.write("          using maxagents {0} as there is no record in the logs\n".format(maxagents))
						else:
							maxagents = 30
							sys.stderr.write("          using maxagents {0} as there is no record in the logs and no other reasonable guess\n".format(maxagents))
							
						self.annofile_refs.append( (os.path.join(logpath, "makefile", aname), maxagents) )
					continue
				
				m = run_time_re.match(l)
				if m:
					self.build_duration = int(m.group(1))
					continue
					
				m = sbs_version_re.match(l)
				if m:
					self.version = m.group(1)

		self.annofiles = []
		for p in self.annofile_refs:
			self.annofiles.append(RaptorAnnofile(p[0], buildid, p[1]))
		if self.build_duration==None:
			self.build_duration = 0
			sys.stderr.write(" build duration was not found in raptor log: {0}".format(self.logfilename))

	def __str__(self):
		recipes = [" <metric name='raptor_{0}_recipes' value='{1}'/>\n".format(*x) for x in self.recipes.items()]
		
		return 	"<raptorbuild logfile='{0}'>\n" \
			    " <metric name='raptor_version' value='{1}' />\n" \
			    " <metric name='raptor_duration_{2}' value='{3}' />\n" \
			    .format(os.path.split(self.logfilename)[-1], 
					    self.version,
					    self.build, self.build_duration) + \
			    "".join(recipes) + \
			    "".join([str(a) for a in self.annofiles]) + \
			    "</raptorbuild>\n"
		

class HeliumBuild(object):
	"""A build with any version of Helium"""
	def __init__(self, logpath, buildid, options=None):
		self.options = options
		self.buildid = buildid
		self.logpath = logpath
		self.logfiles=[]

	def __str__(self):
		return  self.buildid + \
			"\n"+[str(a) for a in self.annofiles] + "\n"

class Helium9Build(HeliumBuild):
	""" Filenames, structure etc conform to Helium 9 """
	def __init__(self, logpath, buildid, options=None):
		super(Helium9Build,self).__init__(logpath, buildid, options)
		self.mainantlog = MainAntLog(logpath, buildid, options)
		self.raptorbuilds = []

		# mcl_7901_201024_20100623181534_dfs_build_ncp_variants.build_input_compile.log
		# mcl_7901_201024_20100623181534_dfs_build_sf_variants.build_input_compile.log
		# mcl_7901_201024_20100623181534_dfs_build_winscw_dfs_build_winscw_input_compile.log
		#
		# ....but the problem is that the anno files have a slightly differing convention:
		#        92_7952_201022_003_dfs_build_ncp_dfs_variants.resource_deps.emake.anno
		#  _dfs_build_ncp_variants
		#  _dfs_build_ncp_dfs_variants
                # read the annofile names from inside the raptor log output
		for r in ["dfs_build_ncp_variants.build_input_compile.log","dfs_build_sf_variants.build_input_compile.log","dfs_build_winscw_dfs_build_winscw_input_compile.log", "ncp_symbian_build_symtb_input_compile.log"]:
			try:
				self.raptorbuilds.append(RaptorBuild(logpath, buildid, r, options))
			except LogfileNotFound as ex:
				sys.stderr.write(str(ex))

	def __str__(self):

		raptor_duration = reduce(lambda x, y: x + y,[y.build_duration for y in self.raptorbuilds],0)
		return "<heliumbuild ver='9' id='{0}'>\n" \
			   "<metric name='total_duration' value='{1}' />\n" \
			   "<metric name='raptor_duration' value='{2}' />\n" \
			   .format(self.buildid,  self.mainantlog.build_duration, raptor_duration) + \
	 		   "".join([str(a) for a in self.raptorbuilds ]) + \
	 		   "</heliumbuild>\n"
		
class Helium13Build(HeliumBuild):
	""" Filenames, structure etc conform to Helium 13 """
	def __init__(self, logpath, buildid, options=None):
		super(Helium13Build,self).__init__(logpath, buildid, options)
		self.mainantlog = MainAntLog(logpath, buildid, options)
		self.raptorbuilds = []
		#  mcl_201124_hw79u_04_ncp_main_build_ncpvariants.build_input_compile.log
		#  ^^^^^^^^^^^^^^^^^^^ ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
		#  | the buildid     | | the buildstage                                 |
		#
		# we have no way of knowing the buildstage names until the build team
		# use the Helium option to turn on that logging. So we have to search
		# for all the raptor logs in the compile folder that match the buildid.
		
		compiledir = os.path.join(logpath, "compile")
		start = len(buildid) + 1
		builds = []
		for log in os.listdir(compiledir):
			if log.startswith(buildid) \
			and allo.utils.is_raptor_log(os.path.join(compiledir, log)):
				builds.append(log[start:])
				
		for r in builds: 
			try:
				self.raptorbuilds.append(RaptorBuild(logpath, buildid, r, options))
			except LogfileNotFound as ex:
				sys.stderr.write(str(ex))

	def __str__(self):

		raptor_duration = reduce(lambda x, y: x + y,[y.build_duration for y in self.raptorbuilds],0)
		return "<heliumbuild ver='13' id='{0}'>\n" \
			   "<metric name='total_duration' value='{1}' />\n" \
			   "<metric name='raptor_duration' value='{2}' />\n" \
			   .format(self.buildid,  self.mainantlog.build_duration, raptor_duration) + \
	 		   "".join([str(a) for a in self.raptorbuilds ]) + \
	 		   "</heliumbuild>\n"


class HeliumLogDir(object):
	"""Multiple builds can be done one after another (usually when rebuilding 
	   things that failed, apparently) and their logs left in the output dir.
	   The naming convention ensures that they don't overwrite each other.
	   This class identifies each build and tries to analyse them one by one."""
	def __init__(self, epocroot, options=None):
		self.logpath = os.path.join(epocroot, "output/logs")
		logs = MainAntLog.findall(self.logpath)
		self.builds = []
		
		for b in logs.keys():
			try:
				sys.stderr.write("  Found build with id {0}\n".format(b))
				build = Helium13Build(self.logpath, b, options)
				self.builds.append(build)
			except IOError as e:
				sys.stderr.write("  Buildid {0} found but does not refer to a complete build\n".format(b))
				sys.stderr.write(str(e)+"\n")

	def write(self, stream):
		for b in self.builds:
			stream.write(str(b)+"\n")
 

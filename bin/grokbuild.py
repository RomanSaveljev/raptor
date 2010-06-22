#!/usr/bin/env python
#
# Copyright (c) 2010 Nokia Corporation and/or its subsidiary(-ies).
# All rights reserved.
# This component and the accompanying materials are made available
# under the terms of the License "Eclipse Public License v1.0"
# which accompanies this distribution, and is available
# at the URL "http://www.eclipse.org/legal/epl-v10.html".
#
# Initial Contributors:
# Nokia Corporation - initial contribution.
#
# Contributors:
#
# Description: 
# fixmeta
#

"""

"""

import sys
import os
import re
from  optparse import OptionParser
import annofile


def checkconvert(dirname, filename):
	fromfilename = dirname + "/" + filename

def visit(arg, dirname, names):
	#print "dir: %s\n" % (dirname)
	for f in names:
		pass

class UndeterminedBuildID(Exception):
	pass

class LogfileNotFound(Exception):
	pass

class HeliumLog(object):
	filenamesuffix = None

	def __init__(self, logpath, buildid):

		self.logfilename = os.path.join(logpath, buildid + self.filenamesuffix)
		self.buildid = buildid

#		else:
#			raise LogfileNotFound("logpath = %s, match=%s" %  (logpath, str(filename_re)))

#		if self.buildid == None:
#			raise UndeterminedBuildID("logpath = %s, match=%s" %  (logpath, str(filename_re)))
#
#		if self.logfilename is None:

	@classmethod
	def findall(c, logpath):
		""" Find all the logs that are of this type - essentially also finds all builds 
		    which dumped their output in the same place """
		filename_re = re.compile('(.*/)?(?P<buildid>[^\\\/]*)' + c.filenamesuffix)
		logs = {}
		for f in os.listdir(logpath):
			m = filename_re.match(f)
			# print f
			if m:
				file_buildid = m.groupdict()['buildid']
				logs[file_buildid] = os.path.join(logpath,f)
		return logs


	def __str__(self):
		return "<metric name='buildid'  value='%s'>\n" % self.buildid

class MainAntLog(HeliumLog):
	# output/logs/92_7952_201020_003_main.ant.log
	filenamesuffix = "_main.ant.log"

	def __init__(self, logpath, buildid):
		super(MainAntLog,self).__init__(logpath, buildid)

		
class AntEnvLog(HeliumLog):
	# output/logs/92_7952_201020_003_ant_env.log
	filenamesuffix = "_ant_env.log"

	def __init__(self, logpath, buildid):
		super(AntEnvLog,self).__init__(logpath, buildid)

class TargetTimesLog(HeliumLog):
	# output/logs/92_7952_custom_dilbert_201022_dilbert_targetTimesLog.csv
	filenamesuffix = "_targetTimesLog.csv"

	def __init__(self, logpath, buildid):
		super(TargetTimesLog,self).__init__(logpath, buildid)
		self.raptorsecs = 0
		self.totalsecs = 0

		with open(self.logfilename) as f:
			for ll in f:
				l = ll.rstrip("\n")
				#print self.logfilename
				#print "L:",l
				(rname, rsecs) = l.split(",")
				rsecs = int(rsecs)
				#print "rname, rsecs: %s %d"%(rname,rsecs)
				self.totalsecs += rsecs
				if rname == "compile-sbs":
					self.raptorsecs += rsecs

	def __str__(self):
		s = "<metric name='build_duration'  value='%s'>" % self.totalsecs  \
			+ "\n<metric name='raptor_duration'  value='%s'>\n" % self.raptorsecs
		return s

class RaptorAnnofile(HeliumLog):
	# Examples:
	# 92_7952_custom_dilbert_201022_dilbert_dfs_build_sf_tools_all.resource.emake.anno
	# 92_7952_custom_dilbert_201022_dilbert_dfs_build_sf_dfs_variants.default.emake.anno
	# 92_7952_201022_003_dfs_build_ncp_dfs_variants.resource_deps.emake.anno
	def __init__(self, logpath, buildid, build, phase):
		self.filenamesuffix = '_%s.%s.emake.anno' % (build, phase)
		super(RaptorAnnofile,self).__init__(logpath, buildid)
		self.phase = phase
		self.build = build

		self.annofile = annofile.Annofile(self.logfilename)

	def __str__(self):
		return "<annofile id='%s'\n" % self.buildid + "build='%s'" % self.build + "phase='%s'" % self.phase + "'>\n" + str(self.annofile) + "\n</build>\n"


class DFSAnnofile(RaptorAnnofile):
	def __init__(self, logpath, buildid, phase):
		super(DFSAnnofile, self).__init__(logpath, buildid, "dfs_build_ncp_dfs_variants", phase)


class HeliumBuild(object):
	def __init__(self, logpath, buildid):
		self.buildid = buildid
		self.targettimes = 0
		self.logpath = logpath
		self.annofiles=[]

	def __str__(self):
		return  self.buildid + str(self.targettimes) + \
			"\n"+[str(a) for a in self.annofiles]

class Helium9Build(HeliumBuild):
	def __init__(self, logpath, buildid):
		super(Helium9Build,self).__init__(logpath, buildid)
		self.mainantlog = MainAntLog(logpath, buildid)
		self.targettimes = TargetTimesLog(logpath, buildid)
		for p in ['export', 'bitmap', 'resource', 'resource_deps', 'default']:
			self.annofiles.append(DFSAnnofile(os.path.join(logpath,"makefile"), buildid, p))

	def __str__(self):
		return "<heliumbuild ver='9' id='%s'>\n" % self.buildid + str(self.mainantlog) + \
			str(self.targettimes) + \
	 		"".join([str(a) for a in self.annofiles ]) + "</heliumbuild>\n"
		

class HeliumLogDir(object):
	def __init__(self, epocroot):
		self.logpath = os.path.join(epocroot, "output/logs")
		logs = MainAntLog.findall(self.logpath)
		self.builds = []
		
		for b in logs.keys():
			try:
				print "found build with id %s" % b
				build = Helium9Build(self.logpath, b)
				self.builds.append(build)
			except IOError,e:
				print "Buildid %s found but does not refer to a compete build " % b
				print e

	def write(self, stream):
		for b in self.builds:
			stream.write(str(b)+"\n")
 

parser = OptionParser(prog = "grokbuild",
        usage = "%prog [-h | options] path to $EPOCROOT (logs usually are in $EPOCROOT/output/logs)")

(options, args) = parser.parse_args()

if len(args) == 0:
	print "Need at least one argument: a path to the logs."
	sys.exit(-1)

print "Gathering\n"
#os.path.walk(args[0],visit,None)
epocroot = args[0]

b = HeliumLogDir(epocroot)
b.write(sys.stdout)

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
	def __init__(self, filename_re, outputpath):
		logpath = os.path.join(outputpath,"logs")
		self.buildid = "undetermined"
		self.logfilename = None
		for f in os.listdir(logpath):
			m = filename_re.match(f)
			# print f
			if m:
				self.buildid = m.groupdict()['buildid']
				self.logfilename = os.path.join(logpath,f)
				# print "logfilename: %s" %self.logfilename
				break
		if self.buildid == None:
			raise UndeterminedBuildID("logpath = %s, match=%s" %  (logpath, str(filename_re)))

		if self.logfilename is None:
			raise LogfileNotFound("logpath = %s, match=%s" %  (logpath, str(filename_re)))

	def __str__(self):
		return "<metric name='buildid'  value='%s'>" % self.buildid

class MainAntLog(HeliumLog):
	# output/logs/92_7952_201020_003_main.ant.log
	mainant_re = re.compile('(.*i)?(?P<buildid>[^\\\/]*)_main.ant.log$')

	def __init__(self, outputpath):
		super(MainAntLog,self).__init__(MainAntLog.mainant_re, outputpath)

		
class AntEnvLog(HeliumLog):
	# output/logs/92_7952_201020_003_main.ant.log
	antenv_re = re.compile('(.*i)?(?P<buildid>[^\\\/]*)_ant_env.log$')

	def __init__(self, outputpath):
		super(AntEnvLog,self).__init__(AntEnvLog.antenv_re, outputpath)

class TargetTimesLog(HeliumLog):
	# output/logs/92_7952_custom_dilbert_201022_dilbert_targetTimesLog.csv
	targettimeslog_re = re.compile("(.*/)?(?P<buildid>[^\\\/]*)_targetTimesLog.csv$", re.I)

	def __init__(self, outputpath):
		super(TargetTimesLog,self).__init__(TargetTimesLog.targettimeslog_re, outputpath)
		self.raptorsecs = 0
		self.totalsecs = 0

		with open(self.logfilename) as f:
			for l in f:
				(rname, rsecs) = l.split(",")
				rsecs = int(rsecs)
				#print "rname, rsecs: %s %d"%(rname,rsecs)
				self.totalsecs += rsecs
				if rname == "compile-sbs":
					self.raptorsecs += rsecs

	def __str__(self):
		s = "<metric name='build_duration'  value='%s'>" % self.totalsecs 
		s += "\n<metric name='raptor_duration'  value='%s'>" % self.raptorsecs
		return s

class HeliumBuild(object):
	def __init__(self, outputpath):
		self.buildid = "unknown"
		self.targettimes = 0

	def __str__(self):
		return "<build id='\n" + self.buildid+"'>\n" + str(self.targettimes) + "\n</build>"

class Helium9Build(HeliumBuild):
	def __init__(self, outputpath):
		super(Helium9Build,self).__init__(outputpath)
		self.mainantlog = MainAntLog(outputpath)
		self.buildid = self.mainantlog.buildid
		self.targettimes = TargetTimesLog(outputpath)

parser = OptionParser(prog = "grokbuild",
        usage = "%prog [-h | options] path to log directory (usually $EPOCROOT/output)")

(options, args) = parser.parse_args()

if len(args) == 0:
	print "Need at least one argument: a path to the logs."
	sys.exit(-1)

print "Gathering\n"
#os.path.walk(args[0],visit,None)
outputpath = args[0]

b = Helium9Build(outputpath)
print b

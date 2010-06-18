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

class HlmLog(object)
	g_re = re.compile('(.*i)?(?P<buildid>[^\\\/]*)_main.ant.log$')
	def __init__(self, outputpath):
		logpath = os.path.join(outputpath,"logs")
		self.logfilename = None
		for f in os.listdir(logpath):
			m = self.log_re.match(f)
			if m:
				self.buildid = m.groupdict()['buildid']
				self.logfilename = os.path.join(logpath,f)
				print "logfilename: %s" %self.logfilename
				break

class MainAntLog(object):
	# output/logs/92_7952_201020_003_main.ant.log

	def __init__(self, outputpath):
		self.log_re=mainantlog_re

		with open(self.logfilename) as f:
			for l in f:
				print "l: ",l


class TargetTimesLog(object):
	# output/logs/92_7952_custom_dilbert_201022_dilbert_targetTimesLog.csv
	targettimeslog_re = re.compile("(.*/)?([^\\\/]*)_targetTimesLog.csv$", re.I)

	def __init__(self, outputpath):

class Build(object):
	def __init__(self, outputpath):
		self.mainantlog = MainAntLog(outputpath)
		self.buildid = self.mainantlog.buildid



parser = OptionParser(prog = "grokbuild",
        usage = "%prog [-h | options] path to log directory (usually $EPOCROOT/output)")

(options, args) = parser.parse_args()

if len(args) == 0:
	print "Need at least one argument: a path to the logs."
	sys.exit(-1)

print "Gathering\n"
#os.path.walk(args[0],visit,None)
outputpath = args[0]

b = Build(outputpath)
print b.buildid


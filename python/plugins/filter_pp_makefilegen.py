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

"""This module provides the PPMakefileGenFilter class for filtering log output 
from sub-invocations of Raptor in builds where parallel parsing is used."""

import errno
import os
import sys
import raptor
import raptor_timing
import filter_interface

class PPMakefileGenFilter(filter_interface.Filter):
	"""A class for filtering log output from sub-invocations of Raptor 
	in builds where parallel parsing is used. This class may not be useful
	for generating log files on its own."""

	def __init__(self):
		super(PPMakefileGenFilter, self).__init__()
		self.unwanted_lines = [
							"<?xml version=",
							"<buildlog",
							"</buildlog>",
							"<info>Environment", 
							"<info>SBS_HOME",
							"<info>Set-up",
							"<info>Current working directory",
							"<info>sbs: version",
							"<info>Duplicate variant",
							"<info>Buildable configuration",
							"<info>Run time"]
		self.task = "makefile_generation"
		self.object_type = "makefile"
		self.key = ""

	def open(self, raptor_instance):
		"""Open a log file for the various I/O methods to write to."""

		self.raptor = raptor_instance
		self.logFileName = self.raptor.logFileName
		self.key = self.raptor.topMakefile
		# insert the time into the log file name
		if self.logFileName:
			self.logFileName.path = self.logFileName.path.replace("%TIME",
					self.raptor.timestring)
	
			try:
				dirname = str(self.raptor.logFileName.Dir())
				if dirname and not os.path.isdir(dirname):
					os.makedirs(dirname)
			except os.error, e:
				if e.errno != errno.EEXIST:
					msg = "{0} : error: cannot create directory {1}\n"
					sys.stderr.write(msg.format(str(raptor.name), dirname))
					return False
			try:
				self.out = open(str(self.logFileName), "w")
			except:
				self.out = None
				msg = "{0} : error: cannot write log {1}\n"
				sys.stderr.write(msg.format(str(raptor.name), self.logFileName.GetShellPath()))
				return False
		else:
			self.out = sys.stdout

		if self.out:
			timing_info = raptor_timing.Timing.start_string(key = self.key, task = self.task, object_type = self.object_type)
			self.out.write(timing_info)
		
		return True
	
	def is_wanted(self, line):
		for fragment in self.unwanted_lines:
			if line.startswith(fragment):
				return False
		return True

	def write(self, text):
		"""Write text into the log file"""
		if self.out:
			lines = text.splitlines(True)
			for line in lines:
				if self.is_wanted(line):
					self.out.write(line)
		return True

	def summary(self):
		"""Write Summary"""
		if self.logFileName and not self.raptor.quiet:
			sys.stdout.write("sbs: build log in %s\n" % str(self.logFileName))
		return False

	def close(self):
		"""Close the log file"""

		try:
			if self.out:
				timing_info = raptor_timing.Timing.end_string(key = self.key, task = self.task, object_type = self.object_type)
				self.out.write(timing_info)
				self.out.close()
			return True
		except:
			self.out = None
		return False

#
# Copyright (c) 2010-2011 Nokia Corporation and/or its subsidiary(-ies).
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

import raptor.timing
from raptor import filter_interface

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

		# submakefiles may only output to stdout - otherwise radical confusion might ensue
		self.out = sys.stdout

		if self.out:
			timing_info = raptor.timing.Timing.start_string(key = self.key, task = self.task, object_type = self.object_type)
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
		return False

	def close(self):
		"""Close the log file"""

		try:
			if self.out:
				timing_info = raptor.timing.Timing.end_string(key = self.key, task = self.task, object_type = self.object_type)
				self.out.write(timing_info)
			return True
		except:
			self.out = None
		return False

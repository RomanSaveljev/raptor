
# Copyright (c) 2010-2011 Nokia Corporation and/or its subsidiary(-ies).
# All rights reserved.
# This component and the accompanying materials are made available
# under the terms of the License "Eclipse Public License v1.0"
# which accompanies this distribution, and is available
# at the URL "http://www.eclipse.org/legal/epl-v10.html".

"""Filter class for generating comma-separated-value summary files."""

import os
import re
import sys

from raptor import filter_interface

class CSV(filter_interface.LogMessageClassifier):
	"""write out a raptor log as a comma-separated-values (.csv) file.
	
	The output format is:
	type,component,configuration,text
	
	where:
	type is one of (ok, error, critical, warning, remark, missing)
	component is the full path to the related bld.inf
	configuration is the raptor build config name (e.g. armv5_urel)
	text is the contents of the <recipe> element
	"""
	
	def __init__(self, params = []):
		"""parameters to this filter are a list of message types to ignore.
		
		For example, csv[ok,remark] will not include any 'ok' or 'remark'
		entries in the output csv data.
		
		If no parameter is given then any of the following may appear:
		ok, error, critical, warning, remark, missing
		"""
		super(CSV, self).__init__()
		self.name = "CSV filter"
		self.ignore = params
		
	# LogMessageClassifier method overrides
	
	def open_summary(self):
		
		if self.params.logFileName == None:
			self.out = sys.stdout # Default to stdout if no log file is given
		else:
			logname = self.params.logFileName.path.replace("%TIME", self.params.timestring)
			
			# Ensure that filename has the right extension; append ".csv" if required
			if not logname.lower().endswith(".csv"):
				logname += ".csv"

			try:
				dirname = os.path.dirname(logname)
				if dirname and not os.path.isdir(dirname):
					os.makedirs(dirname)
			except:
				return self.err("could not create directory '%s'" % dirname)
			
			try:
				self.out = open(logname, "w")
			except:
				self.out = None
				return self.err("could not create file '%s'" % logname)
		return self.ok	
		
	def close_summary(self):
		if self.out and self.out != sys.stdout:
			try:
				self.out.close()
			except Exception as e:
				self.err("could not close CSV " + str(e))
		return self.ok
	
	def sbs_version(self, version_string):
		try:
			self.out.write('info,sbs,version,"' + version_string + '"\n')
		except Exception as e:
			self.err("could not write CSV " + str(e))
		return self.ok
	
	def record(self, taggedtext, type):
		thing = filter_interface.Records.CLASSES[type]
		if thing in self.ignore:
			return self.ok
		
		component = taggedtext.bldinf
		configuration = taggedtext.config
		
		# we know that the text is likely to span multiple lines and to
		# contain " and , characters. The most common way to deal with this
		# (since there is no CSV standard) is to put double quotes around the
		# text and to double-up any contained double quote characters in the
		# text itself. However, we want to be able to sort lines easily using
		# line-based tools so we additionally replace all newline sequences
		# with the string NEWLINE. 
		text = taggedtext.text.strip()
		text = re.sub("[\r\n]+", "NEWLINE", text)
		text = '"' + text.replace('"', '""') + '"'
		
		try:
			self.out.write(",".join([thing,component,configuration,text]) + "\n")
		except Exception as e:
			self.err("could not write CSV " + str(e))
		return self.ok
	
# the end

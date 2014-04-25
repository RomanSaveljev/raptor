
# Copyright (c) 2010-2014 Microsoft Mobile and/or its subsidiary(-ies).
# All rights reserved.
# This component and the accompanying materials are made available
# under the terms of the License "Eclipse Public License v1.0"
# which accompanies this distribution, and is available
# at the URL "http://www.eclipse.org/legal/epl-v10.html".

"""Filter class for generating HTML summary pages."""

import os
import re
import shutil
import time

from raptor import filter_interface

class HTML(filter_interface.LogMessageClassifier):

	def __init__(self, params = []):
		"""parameters to this filter are..."""
		super(HTML, self).__init__()
		self.name = "HTML filter"
		
	# LogMessageClassifier method overrides
	
	def open_summary(self):
		
		if self.params.logFileName:
			self.dirname = str(self.params.logFileName).replace("%TIME", self.params.timestring) + "_html"
		else:
			self.dirname = "html" # writing to stdout doesn't make sense
		
		# create all the directories
		for s in filter_interface.Records.CLASSES:
			dir = os.path.join(self.dirname, s)
			if not os.path.isdir(dir):
				try:
					os.makedirs(dir)
				except:
					return self.err("could not create directory '%s'" % dir)
				
		# create an index.html
		try:
			indexname = os.path.join(self.dirname, "index.html")
			
			self.index = open(indexname, "w")
			self.index.write("""<html>
<head>
<title>Raptor Build Summary</title>
<link type="text/css" rel="stylesheet" href="style.css">
</head>
<body>
<h1>Raptor Build Summary</h1>
""")				
		except:
			return self.err("could not create file '%s'" % indexname)
		
		# copy over a style file if none exists in the output already
		css = os.path.join(self.dirname, "style.css")
		if not os.path.isfile(css):
			try:
				style = str(self.params.home.Append("style/filter_html.css"))
				shutil.copyfile(style, css)
			except:
				self.moan("could not copy '%s' to '%s'" % (style, css))
				
		return self.ok
		
	def close_summary(self):
		
		self.dumptotals()
		try:
			if self.progress_started > 0:
				t_from = time.asctime(time.localtime(self.progress_started))
				t_to = time.asctime(time.localtime(self.progress_stopped))
				self.index.write("<p>start: " + t_from + "\n")
				self.index.write("<br>end&nbsp;&nbsp;: " + t_to + "\n")
				
			self.index.write("<p><table><tr><th></th>")
			
			for title in filter_interface.Records.TITLES:
				self.index.write('<th class="numbers">%s</th>' % title)
			
			self.index.write("</tr>")
			self.index.write(self.totals.tablerow("total"))
			self.index.write("</table>")
			
			
			self.index.write("<h2>by configuration</h2>")
			self.index.write("<p><table><tr><th></th>")
			
			for title in filter_interface.Records.TITLES:
				self.index.write('<th class="numbers">%s</th>' % title)
			
			self.index.write("</tr>")
			
			# the list of configuration names in alphabetical order
			names = list(self.configurations.keys())
			names.sort()
			
			# print the "unknown" configuration results first
			if 'unknown' in names:
				self.index.write(self.configurations['unknown'].tablerow("no specific configuration"))
				names.remove('unknown')
				
			# print the rest
			for name in names:
				self.index.write(self.configurations[name].tablerow(name))
			
			self.index.write("</table>")
			
			
			self.index.write("<h2>by component</h2>")
			self.index.write("<p><table><tr><th></th>")
			
			for title in filter_interface.Records.TITLES:
				self.index.write('<th class="numbers">%s</th>' % title)
			
			self.index.write("</tr>")
			
			# the list of component names in alphabetical order
			names = list(self.components.keys())
			names.sort()
			
			# print the "unknown" component results first
			if 'unknown' in names:
				self.index.write(self.components['unknown'].tablerow("no specific component"))
				names.remove('unknown')
				
			# print the rest
			for name in names:
				self.index.write(self.components[name].tablerow(name))
			
			self.index.write("</table>")	
			self.index.write("</body></html>")
			self.index.close()
		except Exception as e:
			self.err("could not close index " + str(e))
		return self.ok
	
	def sbs_version(self, version_string):
		try:
			self.index.write("<p><tt>sbs " + version_string + "</tt>")
		except Exception as e:
			self.err("could not write to index " + str(e))
		return self.ok
	
	def record(self, taggedtext, type):
		if self.totals.isempty(type):
			self.createoverallfile(type)
		self.appendoverallfile(type, taggedtext)
		
		configuration = taggedtext.config
		
		if configuration in self.configurations:
			if self.configurations[configuration].isempty(type):
				self.createconfigurationfile(configuration, type)
				
			self.appendconfigurationfile(configuration, type, taggedtext)
		else:
			# first time for configuration
			self.configurations[configuration] = filter_interface.Records()
			self.createconfigurationfile(configuration, type)
			self.appendconfigurationfile(configuration, type, taggedtext)
			
		component = taggedtext.bldinf
		
		if component in self.components:
			if self.components[component].isempty(type):
				self.createcomponentfile(component, type)
				
			self.appendcomponentfile(component, type, taggedtext)
		else:
			# first time for component
			self.components[component] = filter_interface.Records()
			self.createcomponentfile(component, type)
			self.appendcomponentfile(component, type, taggedtext)
		return self.ok
	
	# our HTML file creation and appending functions
	
	def createoverallfile(self, type):
		if type == filter_interface.Records.OK:
			# we don't want to show successes, just count them
			return
		
		linkname = os.path.join(filter_interface.Records.CLASSES[type], "overall.html")
		filename = os.path.join(self.dirname, linkname)
		title = filter_interface.Records.TITLES[type] + " for all configurations"
		try:
			file = open(filename, "w")
			file.write("<html><head><title>%s</title>" % title)
			file.write('<link type="text/css" rel="stylesheet" href="../style.css"></head><body>')
			file.write("<h1>%s</h1>" % title)
			file.close()
		except:
			return self.err("cannot create file '%s'" % filename)
		
		self.totals.set_filename(type, filename)
		self.totals.set_linkname(type, linkname)
	
	def appendoverallfile(self, type, taggedtext):
		self.totals.inc(type)   # one more and counting
		self.totals.inc(filter_interface.Records.TIME, taggedtext.time)
		
		if type == filter_interface.Records.OK:
			# we don't want to show successes, just count them
			return
		
		filename = self.totals.get_filename(type)
		try:
			file = open(filename, "a")
			file.write("<p>component: %s " % taggedtext.bldinf)
			file.write("config: %s\n" % taggedtext.config)
			file.write("<pre>" + taggedtext.text.strip() + "</pre>")
			file.close()
		except:
			return self.err("cannot append to file '%s'" % filename)
		
	def createconfigurationfile(self, configuration, type):
		if type == filter_interface.Records.OK:
			# we don't want to show successes, just count them
			return
		
		linkname = os.path.join(filter_interface.Records.CLASSES[type], "cfg_" + configuration + ".html")
		filename = os.path.join(self.dirname, linkname)
		title = filter_interface.Records.TITLES[type] + " for configuration " + configuration
		try:
			file = open(filename, "w")
			file.write("<html><head><title>%s</title>" % title)
			file.write('<link type="text/css" rel="stylesheet" href="../style.css"></head><body>')
			file.write("<h1>%s</h1>" % title)
			file.close()
		except:
			return self.err("cannot create file '%s'" % filename)
		
		self.configurations[configuration].set_filename(type, filename)
		self.configurations[configuration].set_linkname(type, linkname)
	
	def appendconfigurationfile(self, configuration, type, taggedtext):
		self.configurations[configuration].inc(type)   # one more and counting
		self.configurations[configuration].inc(filter_interface.Records.TIME, taggedtext.time)
		
		if type == filter_interface.Records.OK:
			# we don't want to show successes, just count them
			return
		
		filename = self.configurations[configuration].get_filename(type)
		try:
			file = open(filename, "a")
			file.write("<p>component: %s\n" % taggedtext.bldinf)
			file.write("<pre>" + taggedtext.text.strip() + "</pre>")
			file.close()
		except:
			return self.err("cannot append to file '%s'" % filename)
		
	def createcomponentfile(self, component, type):
		if type == filter_interface.Records.OK:
			# we don't want to show successes, just count them
			return
		
		linkname = os.path.join(filter_interface.Records.CLASSES[type], "bld_" + re.sub("[/:]","_",component) + ".html")
		filename = os.path.join(self.dirname, linkname)
		title = filter_interface.Records.TITLES[type] + " for component " + component
		try:
			file = open(filename, "w")
			file.write("<html><head><title>%s</title>" % title)
			file.write('<link type="text/css" rel="stylesheet" href="../style.css"></head><body>')
			file.write("<h1>%s</h1>" % title)
			file.close()
		except:
			return self.err("cannot create file '%s'" % filename)
		
		self.components[component].set_filename(type, filename)
		self.components[component].set_linkname(type, linkname)
	
	def appendcomponentfile(self, component, type, taggedtext):
		self.components[component].inc(type)   # one more and counting
		self.components[component].inc(filter_interface.Records.TIME, taggedtext.time)
		
		if type == filter_interface.Records.OK:
			# we don't want to show successes, just count them
			return
		
		filename = self.components[component].get_filename(type)
		try:
			file = open(filename, "a")
			file.write("<p>config: %s\n" % taggedtext.config)
			file.write("<pre>" + taggedtext.text.strip() + "</pre>")
			file.close()
		except:
			return self.err("cannot append to file '%s'" % filename)

	def dumptotals(self):
		"""write the numbers of errors, warnings etc. into a text file.
		
		so that a grand summariser can tie together individual log summaries
		into one big summary page."""
		try:
			filename = os.path.join(self.dirname, "totals.txt")
			file = open(filename, "w")
			file.write(self.totals.textdump())
			file.close()
		except:
			self.err("cannot write totals file '%s'" % filename)
		
# the end

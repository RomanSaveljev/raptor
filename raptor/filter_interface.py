#
# Copyright (c) 2006-2011 Nokia Corporation and/or its subsidiary(-ies).
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
# Base Class for defining filter classes
# All filter classes that get defined should derive from this base class
#


class Filter(object):
	
	def open(self, params):
		return False
	
	def write(self, text):
		return False

	def summary(self):
		return False
	
	def close(self):
		return False
	
	def formatError(self, message):
		return "sbs: error: " + message + "\n"
		
	def formatWarning(self, message):
		return "sbs: warning: " + message + "\n"	

	def parseNamedParams(self, names, params):
		''' Match named parameters e.g. ['a=b','c=d'] against a list of expected
		names.  Allow for abbreviations.
		'''
		r = {}
		
		# Shorten all the names so they match abbreviations
		shortnames = []

		for name in names:
			shortname = ""
			conflict = True
			while len(shortname)<len(name) and conflict:
				shortname+=name[len(shortname)]
				conflict = False
				othernames = names[:] # Copy
				othernames.remove(name)
				for othername in othernames:
					if othername.startswith(shortname):
						conflict = True
						break
				if conflict == False:
					shortnames.append((shortname,name))
					r[name] = [] # Prime the hash key for this param
			if conflict:
				raise KeyError("Parameter name '{0}' duplicated".format(name))

		# Parse the params
		for param in params:
			if '=' in param:
				(key,value) = param.split('=')
				matched = False
				for (shortname, name) in shortnames:
					if key.strip().startswith(shortname):
						r[name].append(value.strip())
						matched = True
						break
				if not matched:
					raise ValueError("Named parameter '{0}' not valid in filter {1}".format(key,self.__class__.__name__))
			else:
				# Unnamed arg
				if not '' in names:
					raise ValueError("All parameters to the {0} filter must be named".format(self.__class__.__name__))
				else:
					r[''].append(param.strip())
		return r	
			
import sys
import xml.sax

class FilterSAX(Filter, xml.sax.handler.ContentHandler, xml.sax.handler.ErrorHandler):
	"base class for filters using a SAX parser"
	
	# define these methods in your subclass
	
	def startDocument(self):
		"called once before any elements are seen"
		pass
		
	def startElement(self, name, attributes):
		"called on the opening of any element"
		pass
	
	def characters(self, char):
		"called one or more times with body text from an element"
		pass
		
	def endElement(self, name):
		"called on the closing of any element"
		pass
	
	def endDocument(self):
		"called once when all elements are closed"
		pass

	def error(self, exception):
		"the parse found an error which is (possibly) recoverable"
		pass
		
	def fatalError(self, exception):
		"the parser thinks an error occurred which should stop everything"
		pass
		
	def warning(self, exception):
		"the parser found something to complain about that might not matter"
		pass
		
	# these methods are from the Filter base class
	
	def open(self, params):
		"initialise"
		
		self.params = params

		self.parser = xml.sax.make_parser(['xml.sax.expatreader'])
		self.parser.setContentHandler(self)
		self.parser.setErrorHandler(self)
		
		self.ok = True

		return self.ok
			
	def write(self, text):
		"process some log text"
		if self.ok:
			self.parser.feed(text)
		return self.ok

	def close(self):
		"finish off"
		try:
			self.parser.close()
		except Exception as ex:
			sys.stderr.write(self.formatError(str(ex)))
			self.ok = False
			
		return self.ok

class RaptorLogNotValid(Exception):
	pass

class PerRecipeFilter(FilterSAX):
	# Define this in your class
	def handleRecipe(self):
		# These variables are available to you:
		# self.name
		# self.target
		# self.host
		# self.layer
		# self.component
		# self.bldinf
		# self.mmp
		# self.config
		# self.platform
		# self.phase
		# self.source
		# self.prereqs
		# self.text
		# self.exit
		# self.attempt (final attempt number)
		# self.flags
		# self.start
		# self.elapsed

		return False
	
	# Helper functions
	def formatData(self, key, hash='self'):
		'''Output prettifier - return the attribute value, or just return 'undef' if the attribute is not set.'''

		if hash=='self':
			hash=self.__dict__
		if key in hash:
			return hash[key]
		else:
			return 'undef'
	
	# data keys
	recipeData = set(['name','target','host','layer','component','bldinf','mmp','config','platform','phase','source','prereqs'])
	statusData = set(['exit','attempt','flags'])
	timeData = set(['start','elapsed'])

	# methods from the SAX parser
	def startDocument(self):
		self.inRecipe = False
		self.text = ""

	def startElement(self, name, attributes):
		if name == "recipe":
			if self.inRecipe:
				self.error(RaptorLogNotValid("Nested recipes; {0} recipe for {1} inside {2} recipe for {3}".format(self.formatData('name', hash=attributes), self.formatData('target',hash=attributes), self.formatData('name'), self.formatData('target') )))
			else:
				self.inRecipe = True
				self.__setHashElements(attributes, self.__dict__, self.recipeData )		
		elif self.inRecipe:
			if name == "status":
				self.__setHashElements(attributes, self.__dict__, self.statusData)
			elif name == "time":
				self.__setHashElements(attributes, self.__dict__, self.timeData)
			else:
				self.error(RaptorLogNotValid("Unexpected <{0}> tag in {1} recipe for {2}".format(name, self.formatData('name'), self.formatData('target'))))
	
	def endElement(self, name):
		if name == "recipe":
			if not self.inRecipe:
				self.error(RaptorLogNotValid("Extra recipe close tag"))
			else:
				if not self.handleRecipe():
					self.error(RaptorLogNotValid('Handling of {0} recipe for {1} failed'.format(self.formatData('name'), self.formatData('target'))))
				self.inRecipe = False
				
				self.__delData(self.recipeData|self.statusData|self.timeData)
				self.text=""

	def characters(self, char):
		if self.inRecipe:
			self.text += char

	def error(self, exception):
		"the parse found an error which is (possibly) recoverable"
		pass
		
	def fatalError(self, exception):
		"the parser thinks an error occurred which should stop everything"
		pass
		
	def warning(self, exception):
		"the parser found something to complain about that might not matter"
		pass

	# Private methods
	def __setHashElements(self, fro, to, keys):
		for key in keys:
			if key in fro:
				to[key] = fro[key]

	def __delData(self, keys):
		for key in keys:
			if key in self.__dict__:
				del self.__dict__[key]

import csv
import os
import re
import shutil
import tempfile
import time

def noOp(*args, **kwargs):
	pass

class LogMessageClassifier(FilterSAX):
	"""A base class SAX parser which classifies text as Error, Warning etc.
	and calls overridable reporting methods which generate the appropriate
	summary output. Example sub-classes are CSV and HTML.
	
	The classification is based on a list of regular expressions stored in a
	file called logfile_regex.csv which is sought on the Raptor configuration
	path. The format of that file is:-
	
	TYPE,REGEX,DESCRIPTION
	
	TYPE is one of (ERROR, CRITICAL, WARNING, REMARK). Other types are
	silently ignored.
	
	REGEX is a (Python) regular expression. Expressions that don't compile
	will produce a warning.
		
	DESCRIPTION is usually blank, but if the description is "ignorecase"
	then the regular expression is compiled with re.IGNORECASE and will
	therefore match case-insensitively.
	"""
	def __init__(self):
		super(LogMessageClassifier, self).__init__()
		self.name = ""
		
	# FilterSAX method overrides
	
	def startDocument(self):
		
		# read regular expressions from the first file on the config path
		self.regex = []
		for p in self.params.configPath:
			if not p.isAbsolute():
				p = self.params.home.Append(p)
				
			csv = p.Append("logfile_regex.csv")
			if csv.isFile():
				self.regex = self.readregex(str(csv))
				break
		
		# regexes for important "make" errors
		self.noruletomake = re.compile("No rule to make target `(.+)', needed by `(.+)'")
		
		# all our lists are empty
		self.elements = []
		self.recipe_tag = None
		self.error_tag = None
		self.warning_tag = None
		
		self.components = {}
		self.configurations = {}
		self.missed_depends = {}
		self.parse_start = {}
		self.totals = Records()

		self.progress_started = 0
		self.progress_stopped = 0
		
		# create a temporary file to record all the "what" files in. We can
		# only test the files for existence after "make" has finished running.
		try:
			self.tmp = tempfile.TemporaryFile()
		except:
			return self.err("could not create temporary file")
		
		# now give a derived class a chance to set itself up
		return self.open_summary()
		
	def startElement(self, name, attributes):
		"call the start handler for this element if we defined one."
		
		ns_name = name.replace(":", "_")
		self.generic_start(ns_name)    # tracks element nesting
		
		function_name = "start_" + ns_name
		getattr(self, function_name, noOp)(attributes)
			
	def characters(self, char):
		"process [some of] the body text for the current element."
		
		function_name = "char_" + self.elements[-1]
		getattr(self, function_name, noOp)(char)
		
	def endElement(self, name):
		"call the end handler for this element if we defined one."
		
		function_name = "end_" + name.replace(":", "_")
		getattr(self, function_name, noOp)()
		
		self.generic_end()    # tracks element nesting
	
	def endDocument(self):
		self.existencechecks()
		# let the derived class finish off its summary now
		return self.close_summary()
		
	# error and warning exception handlers for FilterSAX
	
	def error(self, exception):
		self.fatalError(exception) # all errors are fatal
		
	def fatalError(self, exception):
		self.err("exception " + str(exception))
		
	def warning(self, exception):
		"""only print warnings if no errors have occurred yet.
		
		because after an error everything goes mad."""
		if self.ok:
			sys.stderr.write(self.formatWarning(self.name + " " + str(exception)))
	
	# our error handling functions
	
	def err(self, text):
		"""only print the first error, then go quiet.
		
		because after a fatal error there are usually hundreds of
		meaningless repeats and/or garbage that doesn't help anyone."""
		if self.ok:
			sys.stderr.write(self.formatError(self.name + " " + text))
		self.ok = False
		return self.ok
	
	def moan(self, text):
		"""print a warning about something that is annoying but not fatal."""
		if self.ok:
			sys.stderr.write(self.formatWarning(self.name + " " + text))
		return self.ok
	
	# our content handling functions
	
	def start_buildlog(self, attributes):
		try:
			self.sbs_version(attributes['sbs_version'])
		except KeyError:
			pass
	
	def char_buildlog(self, char):
		'''process text in the top-level element.
		
		ideally all text will be inside <recipe> tags, but some will not.
		"make" errors in particular appear inside the buildlog tag itself.'''
		
		text = char.strip()
		if text:
			match = self.noruletomake.search(text)
			if match:
				target = match.group(2)
				depend = match.group(1)
				if target in self.missed_depends:
					self.missed_depends[target].append(depend)
				else:
					self.missed_depends[target] = [depend]
		
	def end_buildlog(self):
		pass
		
	def start_recipe(self, attributes):
		self.recipe_tag = TaggedText(attributes)
		
	def char_recipe(self, char):
		self.recipe_tag.text += char
		
	def end_recipe(self):
		# an "ok" recipe may contain warnings / remarks
		if self.recipe_tag.exit == 'ok':
			self.record(self.recipe_tag, self.classify(self.recipe_tag.text))
		
		# a "failed" recipe is always an error
		elif self.recipe_tag.exit == 'failed':
			self.record(self.recipe_tag, Records.ERROR)
		
		# "retry" should just be ignored (for now)
		# but will be recorded in a later version.
		
		self.recipe_tag = None
	
	def start_status(self, attributes):
		try:
			if self.recipe_tag:
				self.recipe_tag.exit = attributes['exit']
				self.recipe_tag.code = attributes['code']
			else:
				self.err("status element not inside a recipe element")
		except KeyError:
			pass
	
	def start_time(self, attributes):
		try:
			if self.recipe_tag:
				self.recipe_tag.time = float(attributes['elapsed'])
			else:
				self.err("time element not inside a recipe element")
		except KeyError:
			pass
	
	def start_progress_start(self, attributes):
		'''on progress:start note the parse starting timestamp.
		
		and keep track of the earliest timestamp of all as that shows
		us when the sbs command was run.'''
		try:
			t = float(attributes['time'])
			if self.progress_started == 0 or t < self.progress_started:
				self.progress_started = t
				
			if attributes['task'] == 'parse':
				self.parse_start[attributes['key']] = t
		except KeyError:
			pass
		
	def start_progress_end(self, attributes):
		'''on progress:end add the elapsed parse time to the total time.
		
		also keep track of the latest timestamp of all as that shows
		us when the sbs command finished.'''
		try:
			t = float(attributes['time'])
			if t > self.progress_stopped:
				self.progress_stopped = t
				
			if attributes['task'] == 'parse':
				elapsed = t - self.parse_start[attributes['key']]
				self.totals.inc(Records.TIME, elapsed)
		except KeyError:
			pass
		
	def start_error(self, attributes):
		self.error_tag = TaggedText(attributes)
	
	def char_error(self, char):
		self.error_tag.text += char
		
	def end_error(self):
		self.record(self.error_tag, Records.ERROR)
		self.error_tag = None
		
	def start_warning(self, attributes):
		self.warning_tag = TaggedText(attributes)
	
	def char_warning(self, char):
		self.warning_tag.text += char
		
	def end_warning(self):
		self.record(self.warning_tag, Records.WARNING)
		self.warning_tag = None
	
	def start_whatlog(self, attributes):
		try:
			for attrib in ['bldinf', 'config']:
				self.tmp.write("|")
				if attrib in attributes:
					self.tmp.write(attributes[attrib])
			self.tmp.write("\n")
		except:
			return self.err("could not write to temporary file")
	
	def start_export(self, attributes):
		try:
			self.tmp.write(attributes['destination'] + "\n")
		except:
			return self.err("could not write to temporary file")
		
	def start_resource(self, attributes):
		self.resource_tag = ""
		
	def char_resource(self, char):
		self.resource_tag += char
		
	def end_resource(self):
		try:
			self.tmp.write(self.resource_tag.strip() + "\n")
		except:
			return self.err("could not write to temporary file")

	def start_bitmap(self, attributes):
		self.bitmap_tag = ""
		
	def char_bitmap(self, char):
		self.bitmap_tag += char
		
	def end_bitmap(self):
		try:
			self.tmp.write(self.bitmap_tag.strip() + "\n")
		except:
			return self.err("could not write to temporary file")
	
	def start_stringtable(self, attributes):
		self.stringtable_tag = ""
		
	def char_stringtable(self, char):
		self.stringtable_tag += char
		
	def end_stringtable(self):
		try:
			self.tmp.write(self.stringtable_tag.strip() + "\n")
		except:
			return self.err("could not write to temporary file")

	def start_member(self, attributes):
		self.member_tag = ""
		
	def char_member(self, char):
		self.member_tag += char
		
	def end_member(self):
		try:
			self.tmp.write(self.member_tag.strip() + "\n")
		except:
			return self.err("could not write to temporary file")
	
	def start_build(self, attributes):
		self.build_tag = ""
		
	def char_build(self, char):
		self.build_tag += char
		
	def end_build(self):
		try:
			self.tmp.write(self.build_tag.strip() + "\n")
		except:
			return self.err("could not write to temporary file")
	
	def start_clean(self, attributes):
		try:
			for attrib in ['bldinf', 'config']:
				self.tmp.write("|")
				if attrib in attributes:
					self.tmp.write(attributes[attrib])
			self.tmp.write("\n")
		except:
			return self.err("could not write to temporary file")
	
	def start_file(self, attributes):
		'''opening file tag.
		
		in the temporary file we need to mark the "clean" targets with a
		leading ">" character so they can be treated differently from 
		the "releasable" targets'''
		self.file_tag = ">"
		
	def char_file(self, char):
		self.file_tag += char
		
	def end_file(self):
		try:
			self.tmp.write(self.file_tag.strip() + "\n")
		except:
			return self.err("could not write to temporary file")
						
	# even if we ignore an element we need to mark its coming and going
	# so that we know which element any character data belongs to.
	
	def generic_start(self, name):
		self.elements.append(name)
	
	def generic_end(self):
		self.elements.pop()

	# text classification
	
	def classify(self, text):
		"test the text for errors, warnings and remarks."
		
		# there shouldn't actually be any errors in here because we
		# are only looking at "ok" recipes... BUT there are bad tools
		# out there which don't set an error code when they fail, so
		# we should look out for those cases.
		
		for line in text.splitlines():
			if not line or line.startswith("+"):
				continue    # it is a blank line or a command, not its output
			
			# the first expression that matches wins
			for r in self.regex:
				if r[0].search(line):
					return r[1]
		
		return Records.OK
	
	def existencechecks(self):
		''' use the temporary list of "what" and "clean" files to generate
		reports of missing files and to attribute missing dependencies to
		the component which appears to require them.'''
		try:
			self.tmp.flush()	# write what is left in the buffer
			self.tmp.seek(0)	# rewind to the beginning
			
			missing_tag = TaggedText({})
			missed = set()    # only report missing files once
			
			for line in self.tmp.readlines():
				if line.startswith("|"):
					parts = line.split("|")
					attribs = { 'bldinf' : parts[1].strip(),
							    'config' : parts[2].strip() }
					missing_tag = TaggedText(attribs)
				else:
					filename = line.strip()
					if filename.startswith(">"):
						# a clean target, so we don't care if it exists
						# but we care if it has a missing dependency
						filename = filename[1:]
					else:
						# a releasable target so it must exist
						if not filename in missed and not os.path.isfile(filename):
							missing_tag.text = filename
							self.record(missing_tag, Records.MISSING)
							missed.add(filename)
						
					if filename in self.missed_depends:
						missing_tag.text = filename + \
						"\n\nrequired the following files which could not be found,\n\n"
						for dep in self.missed_depends[filename]:
							missing_tag.text += dep + "\n"
						self.record(missing_tag, Records.ERROR)
						del self.missed_depends[filename]
					
			self.tmp.close()	# this also deletes the temporary file
			
			# any missed dependencies left over are not attributable to any
			# specific component but should still be reported
			missing_tag = TaggedText({})
			for filename in self.missed_depends:
				missing_tag.text = filename + \
				"\n\nrequired the following files which could not be found,\n\n"
				for dep in self.missed_depends[filename]:
					missing_tag.text += dep + "\n"
				self.record(missing_tag, Records.ERROR)
						
		except Exception as e:
			return self.err("could not close temporary file " + str(e))
	
	def readregex(self, csvfile):
		"""read the list of regular expressions from a csv file.
		
		the file format is TYPE,REGEX,DESCRIPTION
		
		If the description is "ignorecase" then the regular expression is
		compiled with re.IGNORECASE and will match case-insensitively.
		"""
		regexlist = []
		try:
			reader = csv.reader(open(csvfile, "r"))
			for row in reader:
				try:
					type = None
					
					if row[0] == "ERROR":
						type = Records.ERROR
					elif row[0] == "CRITICAL":
						type = Records.CRITICAL
					elif row[0] == "WARNING":
						type = Records.WARNING
					elif row[0] == "REMARK":
						type = Records.REMARK
						
					# there are other types like INFO that we don't
					# care about so silently ignore them.
					if type:
						if row[2].lower() == "ignorecase":
							regex = re.compile(row[1], re.I)
						else:
							regex = re.compile(row[1])
						regexlist.append((regex, type))
				except:
					self.moan("ignored bad regex '%s' in file '%s'" % (row[1], csvfile))
		except Exception as ex:
			self.err("cannot read regex file '%s': %s" % (csvfile, str(ex)))
			return []
		
		return regexlist

	# methods for derived classes
	
	def open_summary(self):
		'''called by parent before any records are seen.'''
		return True
	
	def sbs_version(self, version_string):
		'''called by parent with the sbs version string.'''
		return True
	
	def record(self, taggedtext, type):
		'''called by parent for each record seen.'''
		return True
	
	def close_summary(self):
		'''called by parent after all records have been seen.'''
		return True
	
class CountItem(object):
	def __init__(self):
		self.N = 0
		self.filename = None
		self.linkname = None

	def num_str(self):
		return str(self.N)
	
class TimeItem(CountItem):
	def num_str(self):
		return time.strftime("%H:%M:%S", time.gmtime(self.N + 0.5))
		
class Records(object):
	"a group of related records e.g. errors, warnings and remarks."
	
	# the different types of record we want to group together
	TIME     = 0
	OK       = 1
	ERROR    = 2
	CRITICAL = 3
	WARNING  = 4
	REMARK   = 5
	MISSING  = 6
	
	CLASSES = [ "time", "ok", "error", "critical", "warning", "remark", "missing" ]
	TITLES = [ "CPU Time", "OK", "Errors", "Criticals", "Warnings", "Remarks", "Missing files" ]
	
	def __init__(self):
		self.data = [ TimeItem(), CountItem(), CountItem(), CountItem(), CountItem(), CountItem(), CountItem() ]
		
	def get_filename(self, index):
		return self.data[index].filename
		
	def inc(self, index, increment=1):
		self.data[index].N += increment

	def isempty(self, index):
		return (self.data[index].N == 0)
		
	def set_filename(self, index, value):
		self.data[index].filename = value
	
	def set_linkname(self, index, value):
		self.data[index].linkname = value
		
	def tablerow(self, name):
		row = '<tr><td class="name">%s</td>' % name
		
		for i,datum in enumerate(self.data):
			if datum.N == 0:
				row += '<td class="zero">0</td>'
			else:
				row += '<td class="' + Records.CLASSES[i] + '">'
				if datum.linkname:
					row += '<a href="%s">%s</a></td>' % (datum.linkname,datum.num_str())
				else:
					row += '%s</td>' % datum.num_str()
							
		row += "</tr>"
		return row
	
	def textdump(self):
		text = ""
		for i,datum in enumerate(self.data):
			if datum.N == 0:
				style = "zero"
			else:
				style = Records.CLASSES[i]
			text += str(i) + ',' + style + "," + str(datum.N) + "\n"
		return text
				
class TaggedText(object):
	def __init__(self, attributes):
		
		for attrib in ['bldinf', 'config']:
			self.__dict__[attrib] = "unknown"
			if attrib in attributes:
				value = attributes[attrib]
				if value:
					self.__dict__[attrib] = value
		self.text = ""
		self.time = 0.0
		
# the end

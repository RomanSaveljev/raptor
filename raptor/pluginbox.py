#
# Copyright (c) 2008-2014 Microsoft Mobile and/or its subsidiary(-ies).
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
# PluginBox module - finds classes 
#

from os import listdir, environ, path
import re
from types import ModuleType
import sys

class BadPlugin(Exception):
	def __init__(self, message, filename):
		self.filename = filename
		full_message = "failed to load plugin '{0}' - {1}".format(self.filename, message)
		super(BadPlugin,self).__init__(full_message)

class PluginModule(object):
	"""Represents a module containing plugin classes """
	def __init__(self, file):
		# put raptor module dir in path so that 3rd party plugins don't need to 
		# all be changed to import "raptor.filter_interface" instead of "import filter_interface"
		try:
			self.module = __import__(file)
		except SyntaxError as e:
			if sys.version_info[0] >= 3:
				raise BadPlugin("Check plugin is python3 compatible or try python2: {0}\n".format(e), file)
			else:
				raise BadPlugin(format(str(e)), file)
		except Exception as e:
			raise BadPlugin(str(e), file)
		self.classes = []
		self.__findclasses(self.module)

	def __findclasses(self,module):
		for c in module.__dict__:
			mbr = module.__dict__[c]
			if type(mbr) == type(type):
				self.classes.append(mbr)

import traceback
class PluginBox(object):
	"""
	A container that locates all the classes in a directory.
	Example usage:

		from person import Person
		ps = PluginBox("plugins")
		people = []
		for i in ps.classesof(Person):
			people.append(i())

	"""
	plugfilenamere=re.compile('^(.*)\.py$',re.I)
	def __init__(self, plugindirectory):
		self.pluginlist = []
		self.plugindirs = []
		self.add_plugins(plugindirectory)
		
	def add_plugins(self, plugindirectory):
		self.plugindirs.append(str(plugindirectory))
		sys.path.append(self.plugindirs[-1])
		for f in listdir(self.plugindirs[-1]):
			if f == "__init__.py":
				continue	
			m = PluginBox.plugfilenamere.match(f)
			if m is not None:
				self.pluginlist.append(PluginModule(m.groups()[0]))
		sys.path = sys.path[:-1]

	def classesof(self, classtype):
		"""return a list of all classes that are subclasses of <classtype>"""
		classes = []
		for p in self.pluginlist:
			for c in p.classes:
				if issubclass(c,classtype):
					if c.__name__ != classtype.__name__:
						classes.append(c)
				else:
					# to work around a module naming problem 
					# with filters that were created before
					# the era of the raptor module:  
					# allows us to say filter_interface.Filter
					# and raptor.filter_interface.Filter
					# are effectively "the same"
					# We can remove this when all filters
					# import raptor.filter_interfacre
					# It won't work for filters that 
					# are not directly derived from
					# the Filter class because it's not
					# recursive and doesn't walk the entire tree.

					# These print() calls are still rather handy
					# but do eventually need to go:
					# print("is {0} derived from {1}".format(c.__name__,classtype.__name__))
					is_sub = False
					for b in c.__bases__:
						#print("base: {0} ".format(b.__name__))
						if b.__name__.endswith(classtype.__name__):
							#print("{0} is OK".format(c.__name__))
							is_sub = True
							break

					if is_sub:
						classes.append(c)
		return classes

	def getdetails(self):
		""" return a dictionary of plugins name:docstring """
		details = {}
		for plugin in self.pluginlist:
			for c in plugin.classes:
				details[c.__name__] = c.__doc__
		return details

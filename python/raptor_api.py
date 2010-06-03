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
#
# raptor_api module
#
# Python API for Raptor. External code should interact with Raptor via this
# module only, as it is the only programatic interface considered public. The
# command line --query option is also implemented using this module.

# constants
ALL = 1

# objects

class Reply(object):
	"""object to return values from API calls.
	"""
	def __init__(self, text=""):
		self.text = text
	
	def __str__(self):
		name = type(self).__name__.lower()
		
		string = "<" + name
		children = []
		longend = False
		
		for attribute,value in self.__dict__.items():
			if attribute != "text":
				if isinstance(value, Reply):
					children.append(value)
				elif isinstance(value, list):
					for item in value: 
						children.append(item)
				else:
					if value != None: # skip attributes whose value is None
						string += " %s='%s'" % (attribute, value)
		
		if children or self.text:
			string += ">"
			longend = True
		
		if self.text:
			string += self.text
		
		if children:
			string += "\n"
				
		for c in children:
			string += str(c)
			
		if longend:
			string += "</%s>\n" % name
		else:	
			string += "/>\n"
		
		return string

class Alias(Reply):
	def __init__(self, name, meaning):
		super(Alias,self).__init__()
		self.name = name
		self.meaning = meaning
	
	def __cmp__(self, other):
		""" Add __cmp__ to enable comparisons between two Alias objects based upon name."""
		return cmp(self.name, other.name)

class Config(Reply):
	def __init__(self, meaning, outputpath, text = None):
		super(Config,self).__init__(text)
		self.meaning = meaning
		self.outputpath = outputpath

class Product(Reply):
	def __init__(self, name):
		super(Product,self).__init__()
		self.name = name
	
	def __cmp__(self, other):
		""" Add __cmp__ to enable comparisons between two Product objects based upon name."""
		return cmp(self.name, other.name)

class Include(Reply):
	def __init__(self, path):
		super(Include,self).__init__()
		self.path = path

class PreInclude(Reply):
	def __init__(self, file):
		super(PreInclude,self).__init__()
		self.file = file

class Macro(Reply):
	def __init__(self, name):
		super(Macro,self).__init__()
		self.name = name

class TargetType(Reply):
	def __init__(self, name):
		super(TargetType,self).__init__()
		self.name = name

import generic_path
import raptor
import raptor_data
import raptor_meta
import re

class Context(object):
	"""object to contain state information for API calls.
	
	For example,
	
	api = raptor_api.Context()
	val = api.getaliases("X")
	"""
	def __init__(self, initialiser=None):
		# this object has a private Raptor object that can either be
		# passed in or created internally.
		
		if initialiser == None:
			self.__raptor = raptor.Raptor()
		else:
			self.__raptor = initialiser
			
	def stringquery(self, query):
		"""turn a string into an API call and execute it.
		
		This is a convenience method for "lazy" callers.
		
		The return value is also converted into a well-formed XML string.
		"""
		
		if query == "aliases":
			aliases = self.getaliases()
			return "".join(map(str, aliases)).strip()
		
		elif query == "products":
			variants = self.getproducts()
			return "".join(map(str, variants)).strip()
		
		elif query.startswith("config"):
			match = re.match("config\[(.*)\]", query)
			if match:
				config = self.getconfig(match.group(1))
				return str(config).strip()
			else:
				raise BadQuery("syntax error")
		
		raise BadQuery("unknown query")

	def getaliases(self, type=""):
		"""extract all aliases of a given type.
		
		the default type is "".
		to get all aliases pass type=ALL
		"""
		aliases = []
		
		for a in self.__raptor.cache.aliases.values():
			if type == ALL or a.type == type:
				# copy the members we want to expose
				aliases.append( Alias(a.name, a.meaning) )
		aliases.sort()	
		return aliases
	
	def getconfig(self, name):
		"""extract the values for a given configuration.
		
		'name' should be an alias or variant followed optionally by a
		dot-separated list of variants. For example "armv5_urel" or
		"armv5_urel.savespace.vasco".
		"""
		names = name.split(".")
		if names[0] in self.__raptor.cache.aliases:
			x = self.__raptor.cache.FindNamedAlias(names[0])
			
			if len(names) > 1:
				meaning = x.meaning + "." + ".".join(names[1:])
			else:
				meaning = x.meaning
				
		elif names[0] in self.__raptor.cache.variants:
			meaning = name
			
		else:
			raise BadQuery("'%s' is not an alias or a variant" % names[0])
		
		# create an evaluator for the named configuration
		tmp = raptor_data.Alias("tmp")
		tmp.SetProperty("meaning", meaning)
		
		units = tmp.GenerateBuildUnits(self.__raptor.cache)
		
		# catch exceptions from creation of evaluator object	
		text = None
		includepaths = []
		preincludeheader = ""
		platmacros = []
		try:
			evaluator = self.__raptor.GetEvaluator(None, units[0])
			
			# get the outputpath
			# this is messy as some configs construct the path inside the FLM
			# rather than talking it from the XML: usually because of some
			# conditional logic... but maybe some refactoring could avoid that.
			releasepath = evaluator.Get("RELEASEPATH")
			if not releasepath:
				raise BadQuery("could not get RELEASEPATH for config '%s'" % name)
					
			variantplatform = evaluator.Get("VARIANTPLATFORM")
			varianttype = evaluator.Get("VARIANTTYPE")
			featurevariantname = evaluator.Get("FEATUREVARIANTNAME")
			
			platform = evaluator.Get("TRADITIONAL_PLATFORM")
			
			# Initialise data and metadata objects
			buildunits = raptor_data.GetBuildUnits([meaning], self.__raptor.cache, self.__raptor)
			metareader = raptor_meta.MetaReader(self.__raptor, buildunits)
			metadatafile = raptor_meta.MetaDataFile(generic_path.Path("bld.inf"), "cpp", [], None, self.__raptor)
			
			# There is only one build platform here; obtain the pre-processing include paths,
			# pre-include file, and macros.			
			includepaths = metadatafile.preparePreProcessorIncludePaths(metareader.BuildPlatforms[0])
			preincludeheader = metareader.BuildPlatforms[0]['VARIANT_HRH']
			
			# The macros arrive as a list of strings of the form "name=value". 
			# This removes the equals sign and everything to the right of it.
			macrolist = metadatafile.preparePreProcessorMacros(metareader.BuildPlatforms[0])
			platmacros.extend(map(lambda macrodef: macrodef[0:macrodef.find("=")], macrolist))
			
			if platform == "TOOLS2":
				outputpath = releasepath
			else:
				if not variantplatform:
					raise BadQuery("could not get VARIANTPLATFORM for config '%s'" % name)
				
				if featurevariantname:
					variantplatform += featurevariantname
					
				if not varianttype:
					raise BadQuery("could not get VARIANTTYPE for config '%s'" % name)
				
				outputpath = str(generic_path.Join(releasepath, variantplatform, varianttype))
			
		except Exception, e: # unable to determine output path
			outputpath = None
			text = str(e)
		
		config = Config(meaning, outputpath, text)
		
		# Add child elements if they were calculated
		if len(includepaths) > 0:
			config.includepaths = map(lambda x: Include(str(x)), includepaths)
		
		if preincludeheader != "":
			config.preincludeheader = PreInclude(str(preincludeheader))
		
		if len(platmacros) > 0:
			config.platmacros = map(lambda x: Macro(x), platmacros)
					
		return config 
		
	def getproducts(self):
		"""extract all product variants."""
		
		variants = []
		
		for v in self.__raptor.cache.variants.values():
			if v.type == "product":
				# copy the members we want to expose
				variants.append( Product(v.name) )
		variants.sort()	
		return variants
	
class BadQuery(Exception):
	pass

# end of the raptor_api module

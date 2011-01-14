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
# raptor module
# This module represents the running Raptor program. Raptor is started
# either by calling the Main() function, which creates an instance of
# the raptor.Raptor class and calls its methods to perform a build based
# on command-line parameters, or by explicitly creating a raptor.Raptor
# instance and calling its methods to set-up and perform a build.
#
name = "sbs"			# the public name for the raptor build tool
env  = "SBS_HOME"		# the environment variable that locates us
xml  = "sbs_init.xml"	# the primary initialisation file
env2 = "HOME"		 	# the environment variable that locates the user
xml2 = ".sbs_init.xml"	# the override initialisation file

import generic_path
import os
import stat
import raptor_cache
import raptor_cli
import raptor_data
import raptor_make
import raptor_makefile
import raptor_meta
import raptor_timing
import raptor_utilities
import raptor_version
import raptor_xml
import filter_list
import subprocess
import sys
import types
import time
import traceback
import pluginbox
from xml.sax.saxutils import escape
from buildrecord import BuildRecord
import json


if not "HOSTPLATFORM" in os.environ or not "HOSTPLATFORM_DIR" in os.environ or not "HOSTPLATFORM32_DIR" in os.environ:
	print "Error: HOSTPLATFORM, HOSTPLATFORM_DIR and HOSTPLATFORM32_DIR must be set in the environment (this is usually done automatically by the startup script)."
	sys.exit(1)

hostplatform = set(os.environ["HOSTPLATFORM"].split(" "))
unixplatforms = set(['linux','freebsd','darwin','sunos'])
isunix = not hostplatform.isdisjoint(unixplatforms)
hostplatform_dir = os.environ["HOSTPLATFORM_DIR"]
hostplatform32_dir = os.environ["HOSTPLATFORM32_DIR"]

# defaults can use EPOCROOT

if "EPOCROOT" in os.environ:
	incoming_epocroot = os.environ["EPOCROOT"]
	epocroot = incoming_epocroot.replace("\\","/")
else:
	if 'win' in hostplatform:
		incoming_epocroot = os.sep
		epocroot = "/"
		os.environ["EPOCROOT"] = os.sep
	else:
		epocroot=os.environ['HOME'] + os.sep + "epocroot"
		os.environ["EPOCROOT"] = epocroot
		incoming_epocroot = epocroot

if "SBS_BUILD_DIR" in os.environ:
	sbs_build_dir = os.environ["SBS_BUILD_DIR"]
else:
	sbs_build_dir = (epocroot + "/epoc32/build").replace("//","/")


# only use default XML from the epoc32 tree if it exists
defaultSystemConfig = "lib/config"
epoc32UserConfigDir = generic_path.Join(epocroot, "epoc32/sbs_config")
if epoc32UserConfigDir.isDir():
	defaultSystemConfig = str(epoc32UserConfigDir) + os.pathsep + defaultSystemConfig

# parameters that can be overriden by the sbs_init.xml file
# or by the command-line.
defaults = {
		"allowCommandLineOverrides" : True,
		"CLI" : "raptor_cli",
		"buildInformation" : generic_path.Path("bld.inf"),
		"defaultConfig" : "default",
		"jobs": 4,
		"keepGoing": False,
		"logFileName" : generic_path.Join(sbs_build_dir,"Makefile.%TIME.log"),
		"makeEngine" : "make",
		"preferBuildInfoToSystemDefinition" : False,
		"pruneDuplicateMakefiles": True,
		"quiet" : False,
		"systemConfig" :  defaultSystemConfig,
		"systemDefinition" : generic_path.Path("System_Definition.xml"),
		"systemDefinitionBase" : generic_path.Path("."),
		"systemFLM" : generic_path.Path("lib/flm"),
		"systemPlugins" : generic_path.Path("python/plugins"),
		"topMakefile" : generic_path.Join(sbs_build_dir,"Makefile.%TIME"),
		"tries": 1,
		"writeSingleMakefile": True,
		"ignoreOsDetection": False,
		"toolcheck": "on",
		"incremental_parsing": False,
		"ignore_zero_flmcall_makefiles": False,
		"filterList": "filterterminal,filterlogfile"
		}



class ModelNode(object):
	""" Represents any node in a a tree of build information
	    e.g. a tree of bld.infs, mmps and finally things like resource blocks and string table blocks.
	    This is before they are produced into "build" specs.
	"""


	def __init__(self, id, parent = None):
		self.id = id
		self.type = type
		self.specs = []
		self.deps = [] # files that this node depends on
		self.depfiles = [] # files with dependencies listed in them in GNU make format
		self.children = set()
		self.unfurled = False
		self.parent = parent

	# Allow one to make a set
	def __hash__(self):
		return hash(self.id)

	def __cmp__(self,other):
		return cmp(self.id, other)

	def __iter__(self):
		return iter(self.children)

	def __getitem__(self,x):
		if isinstance(x, slice):
			return self.children[x.start:x.stop]
		return self.children[x]

	def __setitem__(self,k, v):
		self.children[k] = v

	def __len__(self):
		return len(self.children)

	def add(self, item):
		return self.children.add(item)

	def isunfurled(self, c):
		return self.unfurled == False

	def unique_filename(self): 
		""" returns a string that is short enough to add to a filename that is believed to be unique
		    within a single build.  This really should be overridden by children """
		# not a great default but we're not supposed to know what self.id contains so we can't e.g. process it like a filename
		return raptor_utilities.sanitise(hash(id))

	def alldeps(self):
		""" All the known simple dependencies of the object represented by this Node.
		    This doesn't include dependencies that are generated by tools like CPP - alldepfiles() does that"""
		for d in self.deps:
			yield d	
		for c in self.children:
			for d in c.alldeps():
				yield d

	def alldepfiles(self):
		"""Dependencies are sometimes discovered by tools like CPP and then stored in files"""
		for d in self.depfiles:
			yield d	
		for c in self.children:
			for d in c.alldepfiles():
				yield d

	def unfurl(self, build):
		"""Find any children of this node by processing it, produces specs"""
		pass

	def unfurl_all(self, build):
		"""Unfurl self and all children - preparatory e.g for realisation"""
		if not self.unfurled:
			self.unfurl(build)

		self.realise_exports(build) # permit communication of dependencies between children

		for c in self.children:
			c.unfurl_all(build)


	def realise_exports(self, build):
		"""Do the things that are needed such that we can fully unfurl all
		   sibling nodes.  i.e. this step is here to "take care" of the dependencies
		   between siblings.
		"""
		pass

	def makefile_name(self, build):
		"""use data from the build object to determine the makefilename for this node"""
		postfix = "_" + self.unique_filename()
		makefilename_base = build.topMakefile.Absolute()
		return str(makefilename_base) + postfix
		

	def realise_makefile(self, build, specs):

		makefile = self.makefile_name(build)

		metadepsfilename = makefile + ".metadeps"
		try:
			os.makedirs(str(generic_path.Path(makefile).Dir()))
		except OSError,e:
			pass # if the dir is already there


		build.Debug("Layer Deps: {0} with {1} children depfile {2}".format(self.id, len(self.children),metadepsfilename))

		build.InfoDiscovery(object_type = "layers", count = 1)
		build.InfoStartTime(object_type = "layer", task = "parse",
				key = makefile)
		makefileset = build.maker.Write(generic_path.Path(makefile), specs, build.buildUnitsToBuild)

		makefileset.write_metadeps(self.alldeps(), self.alldepfiles()) # ensure that this makefileset's dependency file has been written out
		build.InfoEndTime(object_type = "layer", task = "parse",
				key = makefile)

		# Tell the buildrecord about this set of makefiles
		build.build_record.record_makefileset(makefileset)

		return makefileset




	def realise(self, build):
		"""Give the spec trees to the make engine and actually
		"build" the product represented by this model node"""

		# Must ensure that all children are unfurled at this point
		self.unfurl_all(build)
		sp = self.specs
		build.AssertBuildOK()
		makefileset = self.realise_makefile(build, sp)

		build.InfoStartTime(object_type = "layer", task = "build",
				key = (str(makefileset.directory) + "/" + str(makefileset.filenamebase)))
		result = build.Make(makefileset)
		build.InfoEndTime(object_type = "layer", task = "build",
				key = (str(makefileset.directory) + "/" + str(makefileset.filenamebase)))


		return result



class Project(ModelNode):
	"""A project or, in symbian-speak, an MMP
	"""
	def __init__(self, filename, parent = None):
		super(Project,self).__init__(filename, parent = parent)
		# Assume that components are specified in mmp files for now
		# One day that tyranny might end.
		self.mmp_name = str(generic_path.Path.Absolute(filename))
		self.id = self.mmp_name
		self.unfurled = False
		self.deps.append(self.mmp_name)

	def makefile(self, makefilename_base, engine, named = False):
		"""Makefiles for individual mmps not feasible at the moment"""
		pass 
		# Cannot, currently, "unfurl an mmp" directly but do want
		# to be able to simulate the overall recursive unfurling of a build.

class Component(ModelNode):
	""" An Abstract class for group of projects (where projects are
	    usually things that represent one program or libary) """
	def __init__(self, filename, layername="", componentname=""):
		super(Component,self).__init__(filename)

		self.filename = filename
		self.id = str(filename)
		self.exportspecs = []
		self.depfiles = []
		self.unfurled = False # We can parse this
		self.deps.append(str(self.filename))
		
		# Extra metadata optionally supplied with system definition file gathered components
		self.layername = layername
		self.name = componentname

	def render_bldinf(self, build):
		raise Exception("Can't render a bld.inf from component {0} - don't know how".format(self.filename))

class BldinfComponent(Component):
	"""A group of projects or, in symbian-speak, a bld.inf.
	"""
	def __init__(self, filename, layername="", componentname=""):
		super(BldinfComponent,self).__init__(filename, layername = layername, componentname=componentname)
		# Assume that components are specified in bld.inf files for now
		# One day that tyranny might end.
		self.bldinf = None # Slot for a bldinf object if we spot one later
		self.bldinf_filename = generic_path.Path(str(filename)).Absolute()

	def AddMMP(self, filename):
		self.children.add(Project(filename))

	def render_bldinf(self, build):
		return self

class QmakeErrorException(Exception):
	def __init__(self, text, output = "", errorcode=1,command=""):
		self.output = output
		self.errorcode = errorcode
		self.command=command
	def __str__(self):
		return "{0} - while running: {1}".format(self.output,self.command)

class QtProComponent(BldinfComponent):
	""" represents a component that is specified in a .pro file.  The intention is that it should 
	    be possible to translate it into a bld.inf as we don't intend to parse Qt files directly which 
	    would be an immense and pointless effort."""

	def __init__(self, filename, layername="", componentname=""):
		self.qtpro_filename = generic_path.Path(filename).Absolute()
		super(QtProComponent,self).__init__(filename,layername=layername, componentname=componentname)

		# automatically determine the related bld.inf name by putting it in the same dir as the qt file.
		self.bldinf_filename = generic_path.Join(self.qtpro_filename.Dir(), "bld.inf")
		self.bldinf_produced = False

	def render_bldinf(self, build):
		self.bldinf_produced = True
		qmake = build.metaeval.Get("QMAKE")
		moc = build.metaeval.Get("MOC")
		uic = build.metaeval.Get("UIC")
		rcc = build.metaeval.Get("RCC")

		# run qmake and produce the bld.inf immediately.
		shell = "/bin/sh" # only needed on linux.
		# should really get qmake(.exe)'s absolute location from somewhere
		global epocroot
		spec = build.metaeval.Get("QMAKESPEC")
		incdir = build.metaeval.Get("QMAKE_INCDIR_QT")
		headers = build.metaeval.Get("QT_HEADERS")

		command = "{0} -spec {1} {2} -o {3} QMAKE_INCDIR_QT={4} QMAKE_MOC={5} QMAKE_UIC={6} QMAKE_RCC={7}".format(qmake, spec, self.qtpro_filename, self.bldinf_filename, headers, moc,uic,rcc)
		makeenv = os.environ.copy()

		build.Debug("qmake command: {0}".format(command))
		if isunix:
			p = subprocess.Popen(
					args = [shell, '-c', command],
					bufsize = 65535,
					stdout = subprocess.PIPE,
					stderr = subprocess.STDOUT,
					shell = False,
					universal_newlines = True, 
					env = makeenv)
		else:
			p = subprocess.Popen(
					args = [command], 
					bufsize = 65535,
					stdout = subprocess.PIPE,
					stderr = subprocess.STDOUT,
					shell = True,
					env = makeenv)
		stream = p.stdout
		self.qmake_output = []
		for l in stream:
		      self.qmake_output.append(l)
		               
		returncode = p.wait()

		if returncode != 0:
			e = QmakeErrorException("{0} failed for '{1}'".format(qmake, self.qtpro_filename), output = "\n".join(self.qmake_output), errorcode = returncode, command = command)
			raise e
		return self



class Layer(ModelNode):
	""" Some components that should be built togther
		e.g. a Layer in the system definition.
		
		Components that come from system definition files can
		have extra surrounding metadata that we need to pass
		on for use in log output.
	"""

	def __init__(self, name, componentlist=[]):
		""" componentlist may be a list of items of type Component xor type raptor_xml.SystemModelComponent
		    @componentlist must be a list of objects that are derived from the Component class.
		"""
		super(Layer,self).__init__(name)
		self.name = name

		for c in componentlist:
			# this is a component from the plain old command-line and we expect it to be of type "Component" already.
			self.children.add(c)

	def unique_filename(self): 
		""" returns a string that is short enough to add to a filename that is believed to be unique
		    within a single build. """
		# the layer name should be unique
		return raptor_utilities.sanitise(self.name)


	@classmethod
	def from_system_model(cls, name, sysmodel_componentlist):
		""" A factory method to build a layer from a raptor_xml.SystemModelComponent
		    this eases the process of working with a "system_definition.xml" file. """
		l = cls(name) # Call our class' constructor
		for c in sysmodel_componentlist:
			l.children.add(BldinfComponent(c, c.GetContainerName("layer"), c.GetContainerName("component")))

		return l

	def unfurl(self, build):
		"""Discover the children of this layer. This involves parsing the component MetaData (bld.infs, mmps).
		Takes a raptor object as a parameter (build), together with a list of Configurations.

		We currently have parsers that work on collections of components/bld.infs and that cannot
		parse at a "finer" level.  So one can't 'unfurl' an mmp at the moment.

		Returns True if the object was successfully unfurled.
		"""

		# setup all our components
		for c in self.children:
			c.specs = []

		self.configs = build.buildUnitsToBuild

		# render the components down to bld.inf form (if possible)
		# since we don't understand any other component format
		components = []
		for c in self.children:
			try:
				components.append(c.render_bldinf(build))
			except QmakeErrorException, e:
				build.Error(str(e))

		if len(components) > 0:
			try:
				# create a MetaReader that is aware of the list of
				# configurations that we are trying to build.
				metaReader = raptor_meta.MetaReader(build, build.buildUnitsToBuild)

				# convert the list of bld.inf files into a specification
				# hierarchy suitable for all the configurations we are using.
				self.specs = list(build.generic_specs)
				self.specs.extend(metaReader.ReadBldInfFiles(components, doexport = build.doExport, dobuild = not build.doExportOnly))

			except raptor_meta.MetaDataError, e:
				build.Error(e.Text)

		self.unfurled = True




	def _split_into_blocks(self, build):
		""" Split layer's components into blocks for parallel parsing """
		nc = len(self.children)
		number_blocks = build.jobs
		block_size = (nc / number_blocks) + 1
		component_blocks = [] # list of mini-layers, split up for parallel parsing

		b = 0
		childlist = list(self.children)
		while b < nc:
			l = Layer(self.name, childlist[b:b+block_size])
			component_blocks.append(l)
			b += block_size

		while len(component_blocks[-1].children) <= 0:
			component_blocks.pop()
			number_blocks -= 1

		build.Info("Parallel Parsing: bld.infs split into %d blocks\n", number_blocks)

		return component_blocks


	def meta_realise(self, build):
		"""Generate specs that can be used to "take care of" finding out more
		about this metaunit - i.e. one doesn't want to parse it immediately
		but to create a makefile that will parse it.
		In this case it allows bld.infs to be parsed in parallel by make."""

		# insert the start time into the Makefile name?

		self.configs = build.buildUnitsToBuild

		# Pass certain CLI flags through to the makefile-generating sbs calls
		cli_options = ""

		if build.debugOutput == True:
			cli_options += " -d"

		if build.ignoreOsDetection == True:
			cli_options += " -i"

		if build.keepGoing == True:
			cli_options += " -k"

		if build.quiet == True:
			cli_options += " -q"

		if build.noDependInclude == True:
			cli_options += " --no-depend-include"

		if build.noDependGenerate == True:
			cli_options += " --no-depend-generate"

		tm = build.topMakefile.Absolute()

		# List of all confgurations apart from "build" which 
		# is used internally for generating makefiles for 
		# parallel parsing
		configList = " ".join([c.name for c in self.configs if c.name != "build" ])
			
		# Cause the binding makefiles to have the toplevel makefile's
		# name.  The bindee's have __pp appended.
		binding_makefiles = raptor_makefile.MakefileSet(str(tm.Dir()), build.maker.selectors, makefiles=None, filenamebase=str(tm.File()))
		build.topMakefile = generic_path.Path(str(tm) + "_pp")
		
		component_blocks = self._split_into_blocks(build)

		spec_nodes = []
		loop_number = 0
		for block in component_blocks:
			loop_number += 1
			specNode = raptor_data.Specification("metadata_" + self.name)
			
			# root path for generated sysdef files and their partnering makefiles
			makefile_path = str(build.topMakefile) + "_" + str(loop_number)

			try:
				os.unlink(makefile_path)
			except Exception:
				pass
			
			pp_system_definition = makefile_path + ".sysdef.xml"
			
			try:
				sys_def_writer = raptor_xml.SystemModel(build, aDoRead=False)
				sys_def_writer.AddLayer(block)
				sys_def_writer.Write(pp_system_definition)
				build.Debug("Wrote intermediate parallel-parsing system definition file " + pp_system_definition)
			except Exception as e:
				build.Error("Failed to write intermediate parallel-parsing system definition file " + pp_system_definition)
				raise


			configList = " ".join([c.name for c in self.configs if c.name != "build" ])


			# add some basic data in a component-wide variant
			var = raptor_data.Variant()
			var.AddOperation(raptor_data.Set("PP_SYSTEM_DEFINITION", pp_system_definition))
			var.AddOperation(raptor_data.Set("MAKEFILE_PATH", makefile_path))
			var.AddOperation(raptor_data.Set("CONFIGS", configList))
			var.AddOperation(raptor_data.Set("CLI_OPTIONS", cli_options))


			# Allow the flm to skip exports. Note: this parameter
			doexport_str = '1'
			if not build.doExport:
				doexport_str = ''
			var.AddOperation(raptor_data.Set("DOEXPORT", doexport_str ))

			# Pass on '-n' (if specified) to the makefile-generating sbs calls
			if build.noBuild:
				var.AddOperation(raptor_data.Set("NO_BUILD", "1"))
			specNode.AddVariant(var)

			try:
				interface = build.cache.FindNamedInterface("build.makefiles")
				specNode.SetInterface(interface)
			except KeyError:
				build.Error("Can't find flm interface 'build.makefiles' ")

			spec_nodes.append(specNode)
			binding_makefiles.addInclude(str(makefile_path)+"_all")

		build.InfoDiscovery(object_type = "layers", count = 1)
		build.InfoStartTime(object_type = "layer", task = "parse",
				key = str(build.topMakefile))

		# Generate the makefileset and build it
		mset = self.realise_makefile(build, spec_nodes)
		mset.close()
		gen_result = build.Make(mset)

		build.InfoEndTime(object_type = "layer", task = "parse",
				key = str(build.topMakefile))
		build.InfoStartTime(object_type = "layer", task = "build",
				key = str(build.topMakefile))

		build.Debug("Binding Makefile base name is %s ", binding_makefiles.filenamebase)
		binding_makefiles.close()
		b = build.Make(binding_makefiles)
		build.InfoEndTime(object_type = "layer", task = "build",
				key = str(build.topMakefile))
		return b




class BuildCannotProgressException(Exception):
	pass

# raptor module classes

class Raptor(object):
	"""An instance of a running Raptor program.

	When operated from the command-line there is a single Raptor object
	created by the Main function. When operated by an IDE several Raptor
	objects may be created and operated at the same time.

	
	"""

	# mission enumeration
	M_BUILD = 1
	M_QUERY = 2
	M_VERSION = 3

	def __init__(self, home = None, commandline = [], dotargets = True, logger = None, load_defaults = True):
		"""
		Keyword Arguments:
		home - where to load xml settings from (default None indicated the current working directory)

		commandline - potentially a commandline full of options to set (default empty list)
		targets - when processing a commandline this ensures 
			that correct make targets are added e.g. "WHAT" if doing --what. (Default True)
		logger - a class that provides Debug, Info, Warning and Error 
			functions ( default is an internal logger )"""

		self.args = commandline
		self.dotargets = dotargets

		self.logger = logger
		if self.logger is not None:
			# Patching functions out here rather than putting
			# an if statement in each function seems 
			# a little more efficient although it may
			# be over optimisation.
			self.Info     = self.logger.Info
			self.Debug    = self.logger.Debug
			self.Warn     = self.logger.Warn

		self.load_defaults = load_defaults
		self._default_setup(home)

		# Load up the all the other XML configuration data:
		self.configPath = generic_path.NormalisePathList(self.systemConfig.split(os.pathsep))

		# If there are any commandline arguments then apply them
		if len(commandline) > 0:
			# remember the arguments for the log
			self.args = commandline

			# assuming self.CLI = "raptor_cli"
			if not raptor_cli.GetArgs(self, self.args):
				# raise exception quietly since the error
		 		# messages are already printed out from GetArgs
				raise BuildCannotProgressException("")

		# With incremental parsing which is itself an experimental feature
		# it is relatively safe to switch on a feature that doesn't execute
		# Makefiles if they have no flm calls in them
		if self.incremental_parsing:
			self.ignore_zero_flmcall_makefiles = True

		# Validate our current state
		if self.incremental_parsing and self.doParallelParsing:
			raise BuildCannotProgressException("The parallel parsing (--pp=on) and incremental parsing  (--ip=on) options cannot be used together at the moment")

		if (self.dotargets):
			self._check_and_set_build_targets()




	def _default_setup(self, home = None):
		"""the default set-up state"""
		self.errorCode = 0
		self.skipAll = False
		self.summary = True

		self.out = sys.stdout # Just until filters get started.

		# Create a bootstrap output system.
		self.out = filter_list.FilterList()


		if home == None:
			try:
				home = os.environ[env]
			except KeyError:
				home = os.getcwd()

		# make sure the home directory exists
		self.home = generic_path.Path(home).Absolute()

		if not self.home.isDir():
			self.Error("%s '%s' is not a directory", env, self.home)
			raise BuildCannotProgressException("{0} '{1}' is not a directory".format(env, str(self.home)))

		# the set-up file location.
		# use the override "env2/xml2" if it exists
		# else use the primary "env/xml" if it exists
		# else keep the hard-coded defaults.
		self.raptorXML = self.home.Append(xml)

		if env2 in os.environ:
			sbs_init = generic_path.Join(os.environ[env2], xml2)
			if sbs_init.isFile():
				self.raptorXML = sbs_init

		# things that can be overridden by the set-up file
		for key, value in defaults.items():
			self.__dict__[key] = value

		# things to initialise
		self.args = []

		self.layers = []
		self.orderLayers = False
		self.commandline_layer = Layer('commandline')

		self.systemModel = None
		self.systemDefinitionFile = None
		self.systemDefinitionRequestedLayers = []
		self.systemDefinitionOrderLayers = False

		self.specGroups = {}

		self.configNames = []
		self.configsToBuild = set()
		self.makeOptions = []
		self.maker = None
		self.debugOutput = False
		self.doExportOnly = False
		self.doExport = True
		self.noBuild = False
		self.noDependInclude = False
		self.noDependGenerate = False
		self.projects = set()
		self.queries = []
		
		self.cache = raptor_cache.Cache(self)

		self.override = {env: str(self.home)}
		self.targets = []
		self.defaultTargets = []

		self.doCheck = False
		self.doWhat = False
		self.doParallelParsing = False
		self.doCaseFolding_rsg = False
		self.mission = Raptor.M_BUILD

		# what platform and filesystem are we running on?
		self.filesystem = raptor_utilities.getOSFileSystem()

		self.timing = True # Needed by filters such as copy_file to monitor progress
		self.toolset = None

		self.starttime = time.time()
		# Create a unique time id that combines millisecond part of start time
		# and id of the process which Raptor python is running on 
		timeid = str(round(self.starttime, 3)).split('.')[1] + '-' + str(os.getpid())
		self.timestring = time.strftime("%Y-%m-%d-%H-%M-%S.") + timeid

		self.fatalErrorState = False

		if self.load_defaults:
			# Load up the raptor defaults from XML (formerly from the ConfigFile function)
			if self.raptorXML.isFile():
				self.cache.Load(self.raptorXML)

				# find the 'defaults.raptor' variant and extract the values
				try:
					var = self.cache.FindNamedVariant("defaults.init")
					evaluator = self.GetEvaluator( None, raptor_data.BuildUnit(var.name,[var]) )

					for key, value in defaults.items():
						newValue = evaluator.Resolve(key)

						if newValue != None:
							# got a string for the value
							if type(value) == types.BooleanType:
								newValue = (newValue.lower() != "false")
							elif type(value) == types.IntType:
								newValue = int(newValue)
							elif isinstance(value, generic_path.Path):
								newValue = generic_path.Path(newValue)

							self.__dict__[key] = newValue

				except KeyError:
					# it is OK to not have this but useful to say it wasn't there
					self.Info("No 'defaults.init' configuration found in " + str(self.raptorXML))

	def _load_cache(self):
		"""Before initiating any action like a build or query, we should load up all 
		   xml configuration. This function is not intended for use except by other
		   members of the Raptor class.
		"""

		def mkAbsolute(aGenericPath):
			""" internal function to make a generic_path.Path
			absolute if required"""
			if not aGenericPath.isAbsolute():
				return self.home.Append(aGenericPath)
			else:
				return aGenericPath

		# make generic paths absolute (if required)
		self.configPath = map(mkAbsolute, self.configPath)

		self.cache.Load(self.configPath)

		if not self.systemFLM.isAbsolute():
			self.systemFLM = self.home.Append(self.systemFLM)

		self.cache.Load(self.systemFLM)


		# Make it possible to ask this instance about default tools locations without
		# doing the evaluator creation repeatedly for no reason
		self.metavariant =  self.cache.FindNamedVariant("meta")
		self.metaeval    = self.GetEvaluator(None, raptor_data.BuildUnit(self.metavariant.name, [self.metavariant]) )


	def AddConfigList(self, configPathList):
		# this function converts cmd line option into a list
		# and prepends it to default config.
		self.configPath = generic_path.NormalisePathList(configPathList.split(os.pathsep)) + self.configPath
		return True

	def AddConfigName(self, name):
		if name == "build":
			traceback.print_stack((sys.stdout))
			sys.exit(1)
		self.configNames.append(name)
		return True

	def RunQuietly(self, TrueOrFalse):
		self.quiet = TrueOrFalse
		return True

	def SetCheck(self, TrueOrFalse):
		self.doCheck = TrueOrFalse
		return True

	def SetWhat(self, TrueOrFalse):
		self.doWhat = TrueOrFalse
		return True

	def SetEnv(self, name, value):
		self.override[name] = value

	def AddTarget(self, target):
		if self.doCheck or self.doWhat:
			self.Warn("ignoring target %s because --what or --check is specified.\n", target)
		else:
			self.targets.append(target)

	def AddSourceTarget(self, filename):
		# source targets are sanitised and then added as if they were a "normal" makefile target
		# in addition they have a default, empty, top-level target assigned in order that they can
		# be presented to any generated makefile without error
		sourceTarget = generic_path.Path(filename).Absolute()
		sourceTarget = 'SOURCETARGET_' + raptor_utilities.sanitise(str(sourceTarget))
		self.AddTarget(sourceTarget)
		self.defaultTargets.append(sourceTarget)
		return True

	def SetSysDefFile(self, filename):
		self.systemDefinitionFile = generic_path.Path(filename)
		return True

	def SetSysDefBase(self, path):
		self.systemDefinitionBase = generic_path.Path(path)
		return True

	def AddSysDefLayer(self, layer):
		self.systemDefinitionRequestedLayers.append(layer)
		return True

	def SetSysDefOrderLayers(self, TrueOrFalse):
		self.systemDefinitionOrderLayers = TrueOrFalse
		return True

	def AddBuildInfoFile(self, filename):
		bldinf = str(generic_path.Path(filename).Absolute())
		self.commandline_layer.add(BldinfComponent(bldinf))
		return True
	
	def AddQtProFile(self, filename):

		qt_pro_file = str(generic_path.Path(filename).Absolute())
		self.commandline_layer.add(QtProComponent(qt_pro_file))
		
		return True

	def SetTopMakefile(self, filename):
		self.topMakefile = generic_path.Path(filename)
		return True

	def SetDebugOutput(self, TrueOrFalse):
		self.debugOutput = TrueOrFalse
		return True

	def SetExportOnly(self, TrueOrFalse):
		self.doExportOnly = TrueOrFalse
		if not self.doExport:
			self.Error("The --noexport and --export-only options are incompatible - won't to do anything useful")
			return False
		return True

	def SetNoExport(self, TrueOrFalse):
		self.doExport = not TrueOrFalse
		if self.doExportOnly:
			self.Error("The --noexport and --export-only options are incompatible - won't to do anything useful")
			return False
		return True

	def SetNoBuild(self, TrueOrFalse):
		self.noBuild = TrueOrFalse
		return True

	def SetNoDependInclude(self, TrueOrFalse):
		self.noDependInclude = TrueOrFalse
		return True

	def SetNoDependGenerate(self, TrueOrFalse):
		self.noDependGenerate = TrueOrFalse
		return True

	def SetKeepGoing(self, TrueOrFalse):
		self.keepGoing = TrueOrFalse
		return True

	def SetLogFileName(self, logfile):
		if logfile == "-":
			self.logFileName = None  # stdout
		else:
			self.logFileName = generic_path.Path(logfile)
		return True

	def SetMakeEngine(self, makeEngine):
		self.makeEngine = makeEngine
		return True

	def AddMakeOption(self, makeOption):
		self.makeOptions.append(makeOption)
		return True

	def SetJobs(self, numberOfJobs):
		try:
			self.jobs = int(numberOfJobs)
		except ValueError:
			self.jobs = 0

		if self.jobs < 1:
			self.Warn("The number of jobs (%s) must be a positive integer\n", numberOfJobs)
			self.jobs = 1
			return False
		return True

	def SetTries(self, numberOfTries):
		try:
			self.tries = int(numberOfTries)
		except ValueError:
			self.tries = 0

		if self.tries < 1:
			self.Warn("The number of tries (%s) must be a positive integer\n", numberOfTries)
			self.tries = 1
			return False
		return True

	def SetToolCheck(self, type):
		type = type.lower()
		toolcheck_types= [ "forced", "on", "off" ]
		if type in toolcheck_types:
			self.toolcheck=type
		else:
			self.Warn("toolcheck option must be one of: %s" % toolcheck_types)
			return False

		return True

	def SetTiming(self, TrueOrFalse):
		self.Info("--timing switch no longer has any effect - build timing is now permanently on")
		return True

	def SetParallelParsing(self, type):
		type = type.lower()
		if type == "on":
			self.doParallelParsing = True
		elif type == "slave":
			self.isParallelParsingSlave = True
		elif type == "off":
			self.doParallelParsing = False
		else:
			self.Warn(" parallel parsing option must be either 'on' or 'off' (was %s)"  % type)
			return False

		return True
	def SetRsgCaseFolding(self, TrueOrFalse):
		self.doCaseFolding_rsg = TrueOrFalse
		return True

	def SetIncrementalParsing(self, type):
		if type == "on":
			self.incremental_parsing = True
		elif type == "off":
			self.incremental_parsing = False
		else:
			self.Warn(" incremental parsing option must be either 'on' or 'off' (was %s)"  % type)
			return False
		return  True

	def AddProject(self, projectName):
		self.projects.add(projectName.lower())
		return True

	def AddQuery(self, q):
		self.queries.append(q)
		self.mission = Raptor.M_QUERY
		return True
	
	def FilterList(self, value):
		self.filterList = value
		return True

	def IgnoreOsDetection(self, value):
		self.ignoreOsDetection = value
		return True

	def PrintVersion(self,dummy):
		global name
		print name, "version", raptor_version.fullversion()
		self.mission = Raptor.M_VERSION
		return True

	# worker methods

	def Introduction(self):
		"""Print a header of useful information about Raptor"""

		self.Info("%s: version %s", name, raptor_version.fullversion())

		self.Info("%s %s", env, str(self.home))
		self.Info("Set-up %s", str(self.raptorXML))
		self.Info("Command-line-arguments %s", " ".join(self.args))
		self.Info("Current working directory %s", os.getcwd())

		# the inherited environment
		for e, value in sorted( os.environ.items() ):
			self.Info("Environment %s=%s", e, value.replace("]]>", "]]&gt;"))

		# and some general debug stuff
		self.Debug("Platform %s", "-".join(hostplatform))
		self.Debug("Filesystem %s", self.filesystem)
		self.Debug("Python %d.%d.%d", *sys.version_info[:3])
		self.Debug("Command-line-parser %s", self.CLI)

		for e,value in self.override.items():
			self.Debug("Override %s = %s", e, value)

		for t in self.targets:
			self.Debug("Target %s", t)



	def _check_and_set_build_targets(self):
		# resolve inter-argument dependencies.
		# --what or --check implies the WHAT target and FilterWhat Filter
		if self.doWhat or self.doCheck:
			self.targets = ["WHAT"]
			self.filterList = "filterwhat"

		else:
			# 1. CLEAN/CLEANEXPORT/REALLYCLEAN needs the FilterClean filter.
			# 2. Targets that clean should not be combined with other targets.

			targets = [x.lower() for x in self.targets]

			CL = "clean"
			CE = "cleanexport"
			RC = "reallyclean"

			is_clean = 0
			is_suspicious_clean = 0

			if CL in targets and CE in targets:
				is_clean = 1
				if len(targets) > 2:
					is_suspicious_clean = 1
			elif RC in targets or CL in targets or CE in targets:
				is_clean = 1
				if len(targets) > 1:
					is_suspicious_clean = 1

			if is_clean:
				self.filterList += ",filterclean"
				if is_suspicious_clean:
					self.Warn('CLEAN, CLEANEXPORT and a REALLYCLEAN should not be combined with other targets as the result is unpredictable.')
			else:
				""" Copyfile implements the <copy> tag which is primarily useful with cluster builds.
				    It allows file copying to occur on the primary build host rather than on the cluster.
				    This is more efficient.
				"""
				self.filterList += ",filtercopyfile"



	def GetBuildUnitsToBuild(self, configNames):
		"""Return a list of the configuration objects that correspond to the
		   list of configuration names in the configNames parameter.

		raptor.GetBuildUnitsToBuild(["armv5", "winscw"])
		>>> [ config1, config2, ... , configN ]
		"""

		if len(configNames) == 0:
			# use default config
			if len(self.defaultConfig) == 0:
				self.Warn("No default configuration name")
			else:
				configNames.append(self.defaultConfig)

		buildUnitsToBuild = raptor_data.GetBuildUnits(configNames, self.cache, self)

		for b in buildUnitsToBuild:
			self.Info("Buildable configuration '%s'", b.name)

		if len(buildUnitsToBuild) == 0:
			self.Error("No build configurations given")

		return buildUnitsToBuild

	def CheckToolset(self, evaluator, configname):
		"""Check the toolset for a particular config, allow other objects access
		to the toolset for this build (e.g. the raptor_make class)."""
		if self.toolset is None:
			if self.toolcheck == 'on':
				self.toolset = raptor_data.ToolSet(log=self)
			elif self.toolcheck == 'forced' :
				self.toolset = raptor_data.ToolSet(log=self, forced=True)
			else:
				return True

		return self.toolset.check(evaluator, configname)

	def CheckConfigs(self, configs):
		"""	Tool checking for all the buildable configurations
			NB. We are allowed to use different tool versions for different
			configurations."""

		tools_ok = True
		tool_problems = []
		for b in configs:
			self.Debug("Tool check for %s", b.name)
			config_ok = False  #default
			try:
				evaluator = self.GetEvaluator(None, b, gathertools=True)
				config_ok = self.CheckToolset(evaluator, b.name)
			except raptor_data.UninitialisedVariableException,e:
				tool_problems.append(b.name)
				self.Error("{0} is a bad configuration: {1}".format(b.name,str(e)))

			tools_ok = tools_ok and config_ok

		if len(tool_problems) > 0:
			self.FatalError("Build stopped because the following requested configurations are incomplete or invalid: {0}".format(", ".join(tool_problems)))

		return tools_ok

	def GatherSysModelLayers(self, systemModel, systemDefinitionRequestedLayers):
		"""Return a list of lists of components to be built.

		components = GatherSysModelLayers(self, configurations)
		>>> set("abc/group/bld.inf","def/group/bld.inf, ....")
		"""
		layersToBuild = []

		if systemModel:
			# We either process all available layers in the system model, or a subset of
			# layers specified on the command line.  In both cases, the processing is the same,
			# and can be subject to ordering if explicitly requested.
			systemModel.DumpInfo()

			if systemDefinitionRequestedLayers:
				layersToProcess = systemDefinitionRequestedLayers
			else:
				layersToProcess = systemModel.GetLayerNames()

			for layer in layersToProcess:
				systemModel.DumpLayerInfo(layer)

				if systemModel.IsLayerBuildable(layer):
					layersToBuild.append(Layer.from_system_model(layer,
							systemModel.GetLayerComponents(layer)))

		return layersToBuild


	# Add bld.inf or system definition xml to command line layers (depending on preference)
	def FindSysDefIn(self, aDir = None):
		# Find a system definition file

		if aDir is None:
			dir = generic_path.CurrentDir()
		else:
			dir = generic_path.Path(aDir)

		sysDef = dir.Append(self.systemDefinition)
		if not sysDef.isFile():
			return None

		return sysDef


	def FindComponentIn(self, aDir = None):
		# look for a bld.inf

		if aDir is None:
			dir = generic_path.CurrentDir()
		else:
			dir = generic_path.Path(aDir)

		bldInf = dir.Append(self.buildInformation)

		if bldInf.isFile():
			return BldinfComponent(bldInf)

		return None

	def GenerateGenericSpecs(self, configsToBuild):
		# if a Configuration has any config-wide interfaces
		# then add a Specification node to call each of them.
		configWide = {}
		genericSpecs = []
		for c in configsToBuild:
			evaluator = self.GetEvaluator(None, c)
			iface = evaluator.Get("INTERFACE.config")
			if iface:
				if iface in configWide:
					# seen it already, so reuse the node
					filter = configWide[iface]
					filter.AddConfigCondition(c.name)
				else:
					# create a new node
					filter = raptor_data.Filter(name = "config_wide")
					filter.AddConfigCondition(c.name)
					for i in iface.split():
						spec = raptor_data.Specification(i)
						spec.SetInterface(i)
						filter.AddChildSpecification(spec)
					# remember it, use it
					configWide[iface] = filter
					genericSpecs.append(filter)

		return genericSpecs


	def GetEvaluator(self, specification, configuration, gathertools=False):
		""" this will perform some caching later """
		return raptor_data.Evaluator(specification, configuration, gathertools=gathertools, cache = self.cache)


	def Make(self, makefileset):
		if not self.noBuild and makefileset is not None:
			if self.maker.Make(makefileset, not self.ignore_zero_flmcall_makefiles):
				self.Info("The make-engine exited successfully.")
				return True
			else:
				self.Error("The make-engine exited with errors.")
				return False
		else:
			self.Info("No build performed")



	def Report(self):
		if self.quiet:
			return

		self.endtime = time.time()
		self.runtime = int(0.5 + self.endtime - self.starttime)
		self.raptor_params.runtime = self.runtime
		self.Info("Run time %s seconds" % self.runtime)

	def AssertBuildOK(self):
		"""Raise a BuildCannotProgressException if no further processing is required
		"""
		if self.Skip():
			raise BuildCannotProgressException("")

		return True

	def Skip(self):
		"""Indicate not to perform operation if:
		   fatalErrorState is set
		   an error code is set but we're not in keepgoing mode
		"""
		return self.fatalErrorState or ((self.errorCode != 0) and (not self.keepGoing))


	# log file open/close

	def OpenLog(self):
		"""Open a log file for the various I/O methods to write to."""

		try:
			# Find all the raptor plugins and put them into a pluginbox.
			if not self.systemPlugins.isAbsolute():
				self.systemPlugins = self.home.Append(self.systemPlugins)

			self.pbox = pluginbox.PluginBox(str(self.systemPlugins))

			self.raptor_params = BuildStats(self)

			# Open the requested plugins using the pluginbox
			self.out.open(self.raptor_params, self.filterList, self.pbox)

			# log header
			self.out.write("<?xml version=\"1.0\" encoding=\"ISO-8859-1\" ?>\n")

			namespace = "http://symbian.com/xml/build/log"
			progress_namespace = "http://symbian.com/xml/build/log/progress"
			schema = "http://symbian.com/xml/build/log/1_0.xsd"

			self.out.write("<buildlog sbs_version=\"%s\" xmlns=\"%s\" xmlns:progress=\"%s\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xsi:schemaLocation=\"%s %s\">\n"
						   % (raptor_version.fullversion(), namespace, progress_namespace, namespace, schema))
			self.logOpen = True
		except Exception,e:
			self.out = sys.stdout # make sure that we can actually get errors out.
			self.logOpen = False
			self.FatalError("Unable to open the output logs: %s" % str(e))

	def CloseLog(self):
		if self.logOpen:
			self.out.summary()
			self.out.write("</buildlog>\n")

			if not self.out.close():
				self.errorCode = 1


	def Cleanup(self):
		# ensure that the toolset cache is flushed.
		if self.toolset is not None:
			self.toolset.write()

	# I/O methods

	@staticmethod
	def attributeString(dictionary):
		"turn a dictionary into a string of XML attributes"
		atts = ""
		for a,v in dictionary.items():
			atts += " " + a + "='" + v + "'"
		return atts

	def Info(self, format, *extras, **attributes):
		"""Send an information message to the configured channel
				(XML control characters will be escaped)
		"""
		self.out.write("<info{0}>{1}</info>\n".format(self.attributeString(attributes), escape(format % extras)))

	def InfoDiscovery(self, object_type, count):
		if self.timing:
			try:
				self.out.write(raptor_timing.Timing.discovery_string(object_type = object_type,
						count = count))
			except Exception, exception:
				self.Error(exception.Text, function = "InfoDiscoveryTime")

	def InfoStartTime(self, object_type, task, key):
		if self.timing:
			try:
				self.out.write(raptor_timing.Timing.start_string(object_type = object_type,
						task = task, key = key))
			except Exception, exception:
				self.Error(exception.Text, function = "InfoStartTime")

	def InfoEndTime(self, object_type, task, key):
		if self.timing:
			try:
				self.out.write(raptor_timing.Timing.end_string(object_type = object_type,
						task = task, key = key))
			except Exception, exception:
				self.Error(exception.Text, function = "InfoEndTime")

	def Debug(self, format, *extras, **attributes):
		"Send a debugging message to the configured channel"

		# the debug text is out of our control so wrap it in a CDATA
		# in case it contains characters special to XML... like <>
		if self.debugOutput:
			self.out.write("<debug{0}><![CDATA[\n{1}\n]]></debug>\n".format(self.attributeString(attributes),(format % extras)))

	def Warn(self, format, *extras, **attributes):
		"""Send a warning message to the configured channel
				(XML control characters will be escaped)
		"""
		self.out.write("<warning{0}>{1}</warning>\n".format(self.attributeString(attributes), escape(format % extras)))

	def FatalError(self, format, *extras, **attributes):
		"""Send an error message to the configured channel. This implies such a serious
		   error that the entire build must be shut down asap whilst still finishing off
		   correctly whatever housekeeping is possible e.g. producing error reports.
		   Remains quiet if the raptor object is already in a fatal state since there
		   further errors are probably triggered by the first.
		"""
		if not self.fatalErrorState:
			self.out.write("<error{0}>{1}</error>\n".format(self.attributeString(attributes),(format % extras)))
			self.errorCode = 1
			self.fatalErrorState = True

	def Error(self, format, *extras, **attributes):
		"""Send an error message to the configured channel
				(XML control characters will be escaped)
		"""
		self.out.write("<error{0}>{1}</error>\n".format(self.attributeString(attributes), escape(format % extras)))
		self.errorCode = 1


	def PrintXML(self, format, *extras):
		"Print to configured channel (no newline is added) (assumes valid xml)"
		if format:
			self.out.write(format % extras)

	def GetLayersFromCLI(self):
		"""Returns the list of layers as specified by the
		   commandline interface to Raptor e.g. parameters
		   or the current directory"""
		layers=[]
		# Look for bld.infs or sysdefs in the current dir if none were specified
		if self.systemDefinitionFile == None and len(self.commandline_layer) == 0:
			if not self.preferBuildInfoToSystemDefinition:
				cwd = os.getcwd()
				self.systemDefinitionFile = self.FindSysDefIn(cwd)
				if self.systemDefinitionFile == None:
					aComponent = self.FindComponentIn(cwd)
					if aComponent is not None:
						layers.append(Layer('default',[aComponent]))
			else:
				aComponent = self.FindComponentIn(cwd)
				if aComponent is None:
					self.systemDefinitionFile = self.FindSysDefIn(cwd)
				else:
					layers.append(Layer('default',[aComponent]))

			if len(layers) <= 0 and  self.systemDefinitionFile == None:
				self.Warn("No default bld.inf or system definition file found in current directory (%s)", cwd)

		# If we now have a System Definition to parse then get the layers of components
		if self.systemDefinitionFile != None:
			systemModel = raptor_xml.SystemModel(self, self.systemDefinitionFile, self.systemDefinitionBase)
			layers = self.GatherSysModelLayers(systemModel, self.systemDefinitionRequestedLayers)

		# Now get components specified on a commandline - build them after any
		# layers in the system definition.
		if len(self.commandline_layer) > 0:
			layers.append(self.commandline_layer)

		# If we aren't building components in order then flatten down
		# the groups
		if not self.systemDefinitionOrderLayers:
			# Flatten the layers into one group of components if
			# we are not required to build them in order.
			newcg = Layer("all")
			for cg in layers:
				for c in cg:
					newcg.add(c)
			layers = [newcg]

		return layers

	def Query(self):
		"process command-line queries."
		
		if self.mission != Raptor.M_QUERY:
			return 0
		
		# establish an object cache based on the current settings
		self._load_cache()
			
		# our "self" is a valid object for initialising an API Context
		import raptor_api
		api = raptor_api.Context(self)
		
		print "<sbs version='%s'>" % raptor_version.numericversion()
		
		for q in self.queries:
			try:
				print api.stringquery(q)
				
			except Exception, e:
				self.Error("exception '%s' with query '%s'", str(e), q)
		
		print "</sbs>"	
		return self.errorCode
	
	def Build(self):

		if self.mission != Raptor.M_BUILD: # help or version requested instead.
			return 0

		# open the log file
		self.OpenLog()
		try:
			self.AssertBuildOK()
			# show the command and platform info
			self.Introduction()

			# load the cache of configurations etc
			self._load_cache()

			# establish an object cache
			self.AssertBuildOK()

			# find out what configurations to build
			buildUnitsToBuild = self.GetBuildUnitsToBuild(self.configNames)

			if len(buildUnitsToBuild) == 0:
				raise BuildCannotProgressException("No configurations to build.")
			
			self.buildUnitsToBuild = buildUnitsToBuild

			self.AssertBuildOK()

			###### insert the start time into the Makefile name
			makefile = self.topMakefile.Absolute()
			makefile.path = makefile.path.replace("%TIME", self.timestring)
			self.topMakefile = makefile
			######


			# Create a build record as non-parallel parsed builds can take advantage of incremental
			# makefile generation with some level of safety:
			tm_dir = str(makefile.Dir())
			tm_file = str(makefile.File())
			
			environment = ";".join(["{0}={1}".format(k,os.environ[k]) for k in BuildRecord.sensed_environment_variables])

			must_create_makefiles = True
			if self.incremental_parsing:
				self.build_record = BuildRecord.from_old(adir = str(self.topMakefile.Dir()), commandline=" ".join(self.args), environment = environment, topmakefile = str(makefile))
				must_create_makefiles = not self.build_record.reused
				if must_create_makefiles:
					if len(self.build_record.new_metadata) > 0:
						self.Info("incremental makefile generation: out of date items:  {0}".format("  ".join(set(self.build_record.new_metadata))))
			else:
				self.build_record = BuildRecord(commandline=" ".join(self.args), environment = environment, topmakefilename = str(makefile), makefilesets=[])

			if must_create_makefiles:
				if self.incremental_parsing:
					self.Info("incremental makefile generation: cannot reuse any pre-existing makefiles")

				# find out what components to build, and in what way
				layers = []

				self.AssertBuildOK()
				if len(buildUnitsToBuild) >= 0:
					layers = self.GetLayersFromCLI()

				componentCount = reduce(lambda x,y : x + y, [len(cg) for cg in layers])

				if not componentCount > 0:
					raise BuildCannotProgressException("No components to build.")

				# check the configurations (tools versions)
				self.AssertBuildOK()

				if self.toolcheck != 'off':
					self.CheckConfigs(buildUnitsToBuild)
				else:
					self.Info("Not Checking Tool Versions")

				self.AssertBuildOK()
			else:
				# Don't use the makefile name specified on the commmandline - use the one from the build record.
				self.Info("incremental makefile generation: pre-existing makefiles will be reused: {0}".format(self.build_record.topmakefilename))

			# Setup a make engine.
			if not self.maker:
				try:
					self.maker = raptor_make.MakeEngine(self, self.makeEngine)
				except raptor_make.BadMakeEngineException,e:
					self.Error("Unable to use make engine: %s " % str(e))
					

			self.AssertBuildOK()



			# if self.doParallelParsing and not (len(layers) == 1 and len(layers[0]) == 1):
			# rebuilding and parallel parsing are not compatible at the moment.  There is
			# a validation check for that earlier.
			if self.doParallelParsing:
				# Create a Makefile to parse components in parallel and build them
				self.build_record = BuildRecord(commandline=" ".join(self.args), environment=environment, topmakefilename=str(makefile), makefilesets=[])
				for l in layers:
					l.meta_realise(self)
			elif must_create_makefiles:
				# Parse components serially, creating one set of makefiles
				# create non-component specs
				self.generic_specs = self.GenerateGenericSpecs(buildUnitsToBuild)

				self.AssertBuildOK()



				self.build_record = BuildRecord(commandline=" ".join(self.args), environment=environment, topmakefilename=str(makefile), makefilesets=[])

				for l in layers:
					# create specs for a specific group of components
					try:
						l.realise(self)
					except raptor_make.CannotWriteMakefileException,e:
						pass # raptor_make will report these errors itself
						
				try:
					self.build_record.to_file()
				except Exception,e:
					self.Info("Couldn't write build record file: {0}".format(str(e)))

			else: 
				# Reusing old makefiles
				for makefileset in self.build_record.makefilesets:
					self.InfoStartTime(object_type = "makefileset", task = "build",
						key = makefileset.metadepsfilename)
					result = self.Make(makefileset)
					self.InfoEndTime(object_type = "makefileset", task = "build",
							key = makefileset.metadepsfilename)
				

		except BuildCannotProgressException,b:
			if str(b) != "":
				self.Info(str(b))

		# final report
		if not self.fatalErrorState:
			self.Report()

		self.Cleanup()

		# close the log file
		self.CloseLog()

		return self.errorCode

	@classmethod
	def CreateCommandlineAnalysis(cls, argv):
		""" Perform an analysis run where a build is not performed. 
		Don't parse command line targets - they don't make any sense if you're not doing a build"""
		build = Raptor(commandline=argv, dotargets = False)

		return build


# Class for passing constricted parameters to filters
class BuildStats(object):

	def __init__(self, raptor_instance):
		self.incoming_epocroot = incoming_epocroot
		self.epocroot = epocroot
		self.logFileName = raptor_instance.logFileName
		self.configPath = raptor_instance.configPath
		self.home = raptor_instance.home
		self.quiet = raptor_instance.quiet
		self.doCheck = raptor_instance.doCheck
		self.doWhat = raptor_instance.doWhat
		self.platform = hostplatform
		self.skipAll = raptor_instance.fatalErrorState
		self.timestring = raptor_instance.timestring
		self.targets = raptor_instance.targets
		self.runtime = 0
		self.name = name
		self.topMakefile = raptor_instance.topMakefile


# raptor module functions

def Main(argv):
	"""The main entry point for Raptor.

	argv is a list of command-line parameters,
	NOT including the name of the calling script.

	The return value is zero for success and non-zero for failure."""

	DisplayBanner()

	try:
		# object which represents a build
		b = Raptor(commandline=argv)

		if b.mission == Raptor.M_QUERY:
			return b.Query()
	
		return b.Build()
	except BuildCannotProgressException, e:
		t = str(e)
		if t != "":
			print("sbs error: {0:s}".format(t))
		return 1


def DisplayBanner():
	"""Stuff that needs printing out for every command."""
	pass




# end of the raptor module

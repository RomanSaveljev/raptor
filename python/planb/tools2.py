
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
# planb.tools2 module

'''
Python API for setting up TOOLS2 build actions in Raptor.
'''

import os
import planb.target
import sys

linux = sys.platform.lower().startswith("linux")

class Common(planb.target.Target):
	def __init__(self, agent):
		planb.target.Target.__init__(self, agent)
		
		self.user_includes = []
		self.system_includes = []
		self.source_files = []
		
		self.crosscompile = (agent['TOOLS2WIN32'] != "")
		
	def add_user_includes(self, dirs):
		self.user_includes.extend(dirs)
		
	def add_system_includes(self, dirs):
		self.system_includes.extend(dirs)
		
	def add_source_files(self, files):
		self.source_files.extend(files)
	
	def finalise(self):
		"""all the parameters are set so we can create ObjectFile targets."""

		if linux and not self.crosscompile:

			self.cdefs = self.agent['CDEFS.LINUX'] + " " + self.agent['CDEFS']
			self.cflags = self.agent['CFLAGS'] + " " + self.agent['OPTION_GCC']
			self.compiler_path = self.agent['COMPILER_PATH.LINUX']
		else:
			self.cdefs = self.agent['CDEFS.WIN32'] + " " + self.agent['CDEFS']
			self.cflags = self.agent['CFLAGS.WIN32'] + " " + self.agent['CFLAGS'] + " " + self.agent['OPTION_GCC']
			self.compiler_path = self.agent['COMPILER_PATH.WIN32']
	
		self.outputpath = self.agent['OUTPUTPATH'] + "/" + self.agent['TARGET'] + "_" + self.agent['TARGETTYPE'] + "/tools2/" + self.agent['VARIANTTYPE'] + self.agent['TOOLPLATFORMDIR']

# CDEFS_TOOLS2 = [agent['OPT.D'] + "'" + x + "'" for x in CDEFS_TOOLS2.split()]

		# tell the agent about directories we need to exist
		self.agent.add_directory(self.outputpath)
		self.agent.add_directory(self.agent['RELEASEPATH'])
		self.agent.add_directory(self.agent['TOOLSPATH'])

		# assemble the pre-include file and include search path
		include_flags = "".join([" " + self.agent['OPT.PREINCLUDE'] + i for i in self.agent['INC.COMPILER'].split()])

		include_flags += "".join([" " + self.agent['OPT.USERINCLUDE'] + i for i in self.user_includes])
		include_flags += "".join([" " + self.agent['OPT.SYSTEMINCLUDE'] + i for i in self.system_includes])
		
		# compose the common parts of the command-line
		command = ''
		
		if self.compiler_path:
			command += 'COMPILER_PATH="%s" ' % self.compiler_path

		command += ' ' + self.agent['COMPILER'] + ' ' + self.cflags
		command += ' ' + ''.join([' ' + self.agent['OPT.D'] + "'" + i + "'" for x in self.cdefs.split()])
		
	$(COMPILER) $(CFLAGS) $(CDEFS.TOOLS2) \
	$(if $(NO_DEPEND_GENERATE),,-MD -MT"$$@" -MF"$(DEPENDFILENAME)") \
	$(INCLUDES) $(OPT.O)"$$@" "$(1)" \
	$(call endrule,compile2object)
	
		# save  the list of object files as they are the inputs for EXE
		# and LIB targets that extend this general collection of .o files.
		self.object_files = []
		
		# create an object file target for each source file
		for src in self.source_files:
			base = os.path.basename(src)
			s = base.lower()
			if s.endswith(".cpp"):
				chop = -3
			elif s.endswith(".c"):
				chop = -1
			else:
				sys.stderr.write("warning: unknown SOURCE extension on '%s'\n" % s)
				continue
		
			obj = self.outputpath + "/" + base[0:chop] + "o"
			self.object_files.append(obj)

			object_target = planb.target.Target(self.agent)
			object_target.title = "compile2object"
			object_target.add_input(src)
			object_target.add_output(obj, False)    # not releasable
			
			# is there a generated dependency file?
			if self.agent.generate_dependencies:
				dep = obj + ".d"
				object_target.generated_dependencies(dep)
				
				command += ' -MD -MT"%s" -MF"%s"' % (obj, dep)

			# complete the command-line
			command += ' %s"%s" "%s"' % (self.agent['OPT.o'], obj, src)
			
			object_target.action(command) 
			


ifeq ($(NO_DEPEND_GENERATE),)
  CLEANTARGETS:=$$(CLEANTARGETS) $(DEPENDFILENAME)
endif

ifneq ($(DEPENDFILE),)
  ifeq ($(NO_DEPEND_INCLUDE),)
    ifeq ($(filter %CLEAN,$(call uppercase,$(MAKECMDGOALS))),)
      -include $(DEPENDFILE)
    endif
  endif
endif

endef

$(foreach SRC,$(CPPFILES),$(eval $(call compile2object,$(SRC),CPP)))
$(foreach SRC,$(cppFILES),$(eval $(call compile2object,$(SRC),cpp)))
$(foreach SRC,$(CFILES),$(eval $(call compile2object,$(SRC),C)))
$(foreach SRC,$(cFILES),$(eval $(call compile2object,$(SRC),c)))

### Conclusion - cleanup and introspection #######################

# make the output directories while reading makefile - some build engines prefer this
$(call makepath,$(CREATABLEPATHS))

## Clean up
$(call raptor_clean,$(CLEANTARGETS) $(OBJECTFILES))
## for the --what option and the log file
$(call raptor_release,$(RELEASABLES))

## The End


















class Exe(Common):
	def __init__(self, exename, agent):
		Common.__init__(self, agent)
		
		self.title = "tools2linkexe"
		self.exename = exename
		self.exepath = agent['RELEASEPATH'] + "/" + exename + agent['DOTEXE']
		
		self.static_libraries = []
		
		if linux and not self.crosscompile:
			self.system_libraries = agent['LIBS.LINUX'].split()
		else:
			self.system_libraries = agent['LIBS.WIN32'].split()
			
	def add_static_libraries(self, libs):
		self.static_libraries.extend(libs)
		
	def finalise(self):
		"""this gets called by the agent after all methods are done.
		
		so we can create all the targets we need now."""
		
		# finalise our parent class first to create all the ObjectFile targets
		Common.finalise(self)
		
		# the main output of this target
		self.add_output(self.exepath)
		
		# the object files from our parent class are inputs for this target
		self.add_inputs(self.object_files)
		
		# static libraries are inputs too
		static_lib_files = []
		static_lib_flags = self.agent['OPT.L'] + '"' + self.agent['RELEASEPATH'] + '"'
		
		for lib in self.static_libraries:
			static_lib_files.append(self.agent['RELEASEPATH'] + "/lib" + lib + ".a")
			static_lib_flags += " " + self.agent['OPT.l'] + lib
			
		self.add_inputs(static_lib_files)

		# static system libraries are not dependencies, as we cannot build them
		static_lib_flags += "".join([" " + self.agent['OPT.l'] + i for i in self.system_libraries])
		
		# piece together the link command
		command = self.agent['LINKER'] + " " + self.cflags + " " + self.agent['LFLAGS'] 
		command += " " + self.agent['OPT.O'] + '"' + self.exepath + '"'
		command += " " + "".join(['"' + i + '"' for i in self.object_files])
		command += " " + static_lib_flags + " " + self.agent['LINKER_OPTIONS']
	
		# copy the linked exe to the tools folder if required
		if self.agent['TOOLSPATH']:
			installed = self.agent['TOOLSPATH'] + "/" + self.exename + self.agent['DOTEXE']
			
			command += ' && %s "%s" "%s"' % (self.agent['GNUCP'], self.exepath, installed)
			command += ' && %s a+rwx "%s"' % (self.agent['GNUCHMOD'], installed)
			
		# remove all the intermediate files if required
		if self.agent['SAVESPACE']:
			command += '; %s -rf "%s"; true' % (self.agent['GNURM'], self.outputpath)

		# register the command as this target's action
		self.action(command)

#
# Copyright (c) 2006-2014 Microsoft Mobile and/or its subsidiary(-ies).
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
# build.cli module
# This module represents a Command Line Interpreter (CLI) for Raptor.
# The interface with Raptor is the GetArgs() function, which is called
# by a raptor.build object.
#

import sys
import types
from optparse import OptionParser # for parsing command line parameters

import raptor.version
from raptor.utilities import expand_command_options

# build.cli module attributes

parser = OptionParser(prog = raptor.version.name,
					  usage = """%prog [--help] [options] [target] ...

Targets:

BITMAP         Create bitmap files
CLEAN          Remove built files and intermediates, but not exported files
CLEANEXPORT    Remove exported files
EXPORT         Copy exported files to destinations
FINAL          Allow extension makefiles to execute final commands
FREEZE         Freeze exported functions in a .DEF file
LIBRARY        Create import libraries from frozen .DEF files
LISTING        Create assembler listing files for source files
PREPROCESS     Create preprocessor output files alongside source files
REALLYCLEAN    Same as CLEAN but also remove exported files
RESOURCE       Create resource files
ROMFILE        Create an IBY file to be included in a ROM
TARGET         Create main executables
WHAT           List all releaseable targets

Examples:

sbs -b my/group/bld.inf -c armv5        # build my component for target ARMV5
sbs -b my/group/bld.inf -c armv5.test   # build my tests for target ARMV5

sbs -c winscw CLEAN                     # clean emulator files
sbs REALLYCLEAN                         # delete everything""")

parser.add_option("-a","--sysdefbase",action="store",dest="sys_def_base",
				help="Root directory for relative paths in the System Definition XML file.")

parser.add_option("-b","--bldinf",action="append",dest="bld_inf_file",
				help="Build information filename. Multiple -b options can be given.")

parser.add_option("-c","--config",action="append",dest="config_name",
				help="Configuration name to build. Multiple -c options can be given. The standard configs are all, armv5, armv7, default, tools, tools2 and winscw.")

parser.add_option("--configpath", action="append",dest="config_list",
				help="Append a list of paths to the default list of XML configuration folders. Use ';' as the separator on Windows, and ':' on Linux. Multiple --configpath options can be given.")

parser.add_option("--check",action="store_true",dest="check",
				help="Test for the existence of files created by the build, printing the ones which are missing. Do not build anything.")

parser.add_option("--command",action="append",dest="command_file",
				help="Provide a set of command-line options in a file.")

parser.add_option("-d","--debug",action="store_true",dest="debugoutput",
				help="Display information useful for debugging.")

parser.add_option("-e","--engine",action="store",dest="make_engine",
				help="Name of the make engine which runs the build.")

parser.add_option("--export-only",action="store_true",dest="doExportOnly",
				help="Generate exports only and do not create any make files.")

parser.add_option("--noexport",action="store_true",dest="doExport",
				help="Don't export any files - useful in some builds when you know exports have already been done.")

parser.add_option("-f","--logfile",action="store",dest="logfile",
				help="Name of the log file, or '-' for stdout.")

parser.add_option("--filters",action="store",dest="filter_list",
				help="Comma-separated list of names of the filters to use (case sensitive).")

parser.add_option("-i","--ignore-os-detection",action="store_true",dest="ignore_os_detection",
				help="Disables automatic application of OS variant based upon the OS version detected from each epoc32 tree.")

parser.add_option("--ip",action="store",dest="incremental_parsing",
				help=
			"Reuse makefiles from previous builds if they are still "
			"relevant. i.e if no bld.infs/mmps or other metadata has "
			"changed and if the environment has not altered either. "
			"This option can improve raptor's performance but it "
			"is possible that it may sometimes be too optimistic "
			"and reuse makefiles that really should be regenerated. "
			"It cannot currently be used with the parallel parsing "
			"option (--pp=on). It is not likely to save time when "
			"the --qtpro option is used as there is no way to get the "
			"dependencies of a .pro file so qmake must always reparse "
			"them and regenerate their bld.inf files."
			)

parser.add_option("-j","--jobs",action="store",dest="number_of_jobs",
                help="The maximum number of jobs that make should try and run in parallel (on a single machine).")

parser.add_option("-k","--keepgoing",action="store_true",dest="keepgoing",
				help="Continue building, even if some build commands fail.")

parser.add_option("-l","--layer",action="append",dest="sys_def_layer",
                help="Build a specific layer in the System Definition XML File. Multiple -l options can be given.")

parser.add_option("-m","--makefile",action="store",dest="makefile",
				help="The basename of a set of makefiles.")

parser.add_option("--mo",action="append",dest="make_option",
				help="Option that must be passed through to the make engine. Multiple --mo options can be given.")

parser.add_option("-n","--nobuild",action="store_true",dest="nobuild",
				help="Just create makefiles, do not build anything.")

parser.add_option("--no-depend-include",action="store_true",dest="noDependInclude",
				help="Do not include generated dependency files. This is only useful for extremely large non-incremental builds.")

parser.add_option("--no-depend-generate",action="store_true",dest="noDependGenerate",
				help="Do not generate dependency files. This is only useful for extremely large non-incremental builds.  Implies --no-depend-include.")

parser.add_option("--no-metadata-depend",action="store_true",dest="no_metadata_depend",default=False,
				help="ADVANCED USERS ONLY: Assumes that MMP files are generated and removes the dependency between " 
				"the MMP file's target and the MMP file itself from Raptor's Makefile.")
				
parser.add_option("-o","--orderlayers",action="store_true",dest="sys_def_order_layers",
				help="Build layers in the System Definition XML file in the order listed or, if given, in the order of -l options.")

parser.add_option("-p","--project",action="append",dest="project_name",
                help="Build a specific project (mmp or extension) in the given bld.inf file. Multiple -p options can be given.")

parser.add_option("-q","--quiet",action="store_true",dest="quiet",
				help="Run quietly, not generating output messages.")

parser.add_option("--qtpro",action="append",dest="qt_pro_file",
				help="Qt project (.pro) file name. Multiple --qtpro options can be given.")

parser.add_option("--query",action="append",dest="query",
				help="""Access various build settings and options using a basic API. The current options are:
				
				* aliases - return all the values that can be sensibly used with the sbs -c option.
				
				* products - return all the values that can be "." appended to an alias to specialise it for a product build.
				
				* config[x] - return a set of values that represent the build configuration "x". Typically "x" will be an alias name or an alias followed by "." followed by a product.
				
				* filters - return a set of possible values for the --filters option.
				
				Multiple --query options can be given.
				""")

parser.add_option("-s","--sysdef",action="store",dest="sys_def_file",
				help="System Definition XML filename.")

parser.add_option("--source-target",action="append",dest="source_target",
				help="Build the listed source or resource file in isolation - do not perform any dependent processing. Multiple --source-target options can be given.")

parser.add_option("-t","--tries",action="store",dest="tries",
				help="How many times to run a command before recording an error. The default is 1. This is useful for builds where transient failures can occur.")

parser.add_option("--toolcheck",action="store",dest="toolcheck",
			help= \
				"""Possible values are:
				  "on"     -  Check the versions of tools that will be used in the build. Use cached results from previous builds to save time. This is the default.

  				  "off"    -  Do not check tool versions whatsoever.

				  "forced" -  Check all tool versions. Don't use cached results.
			""")

parser.add_option("--timing",action="store_true",dest="timing",
			help="Show extra timing information for various processes in the build.")

parser.add_option("--pp",action="store",dest="parallel_parsing",
				help="""Controls how metadata (e.g. bld.infs) are parsed in Parallel.
					Possible values are:
					"on"  - Parse bld.infs in parallel (should be faster on clusters/multicore machines)
					"slave" - used internally by Raptor 
					"off" - Parse bld.infs serially 
				     """)

parser.add_option("--use-rsg-casefolding", action="store_true", dest="resource_rsg_casefolding",
				help="""This option should not be used permanently to work around case issues on Linux. Case issues need to be fixed and this option should only be used before that has been done.

					Generate resource rsg files in lowercase regardless what is specified in mmp file.
				     """)

parser.add_option("-v","--version",action="store_true",dest="version",
				help="Print the version number and exit.")

parser.add_option("--what",action="store_true",dest="what",
				help="Print out the names of the files created by the build. Do not build anything.")




def GetArgs(build, args):
	"Process command line arguments for a Raptor object"
	return DoBuild(build,args)

class NonAsciiError(Exception):
	pass

def DoBuild(build, args):
	"Process build arguments"
	#
	# This should parse the args list and call methods on
	# the build object to store the appropriate data.

	# Expand --command=file options, replacing them with the contents of the
	# command file.

	non_ascii_error = "Non-ASCII character in argument or command file"

	try:
		expanded_args = expand_command_options(args)
		for arg in expanded_args:
			if arg.startswith("?"):
				u = NonAsciiError(non_ascii_error+" : found an argument starting with ? which can indicate that non-ascii characters were used in the commandline: "+arg) 
				raise u
			for c in arg:
				if ord(c) > 127:
					build.Error(non_ascii_error)
					return False
	except IOError as e:
		build.Error(str(e))
		return False
	except NonAsciiError as e:
		build.Error(str(e))
		return False
	except UnicodeDecodeError:
		build.Error(non_ascii_error)
		return False

	# parse the full set of arguments
	(options, leftover_args) = parser.parse_args(expanded_args)

	# the leftover_args are target names.
	for leftover in leftover_args:
		build.AddTarget(leftover)

	# Define the dictionary of functions to be used.
	# Attributes and function names can be added easily.
	# The calling attribute should be the same
	# as specified when creating the add_option
	functions = {'config_name': build.AddConfigName,
				 'config_list':build.AddConfigList,
				 'sys_def_file' : build.SetSysDefFile,
				 'sys_def_base' : build.SetSysDefBase,
				 'sys_def_layer' : build.AddSysDefLayer,
				 'sys_def_order_layers' : build.SetSysDefOrderLayers,
				 'bld_inf_file' : build.AddBuildInfoFile,
				 'logfile' : build.SetLogFileName,
				 'makefile' : build.SetTopMakefile,
				 'qt_pro_file' : build.AddQtProFile,
				 'quiet' : build.RunQuietly,
				 'debugoutput' : build.SetDebugOutput,
				 'doExportOnly' : build.SetExportOnly,
				 'doExport' : build.SetNoExport,
				 'keepgoing': build.SetKeepGoing,
				 'nobuild' : build.SetNoBuild,
				 'make_engine': build.SetMakeEngine,
				 'make_option': build.AddMakeOption,
				 'noDependInclude': build.SetNoDependInclude,
				 'noDependGenerate': build.SetNoDependGenerate,
				 'number_of_jobs': build.SetJobs,
				 'project_name' :  build.AddProject,
				 'query' : build.AddQuery,
				 'filter_list' : build.FilterList,
				 'ignore_os_detection': build.IgnoreOsDetection,
				 'check' :  build.SetCheck,
				 'what' :  build.SetWhat,
				 'tries' : build.SetTries,
				 'toolcheck' : build.SetToolCheck,
				 'timing' : build.SetTiming,
				 'source_target' : build.AddSourceTarget,
				 'command_file' : CommandFile,
				 'parallel_parsing' : build.SetParallelParsing,
				 'resource_rsg_casefolding' : build.SetRsgCaseFolding,
				 'incremental_parsing' : build.SetIncrementalParsing,
				 'no_metadata_depend' : build.SetNoMetadataDepend,
			 	 'version' : build.PrintVersion
				}

	# Check if Quiet mode has been specified (otherwise we will make noise)
	if parser.values.quiet:
		build.RunQuietly(True)

	# only return True if there are no command-line errors
	keepGoing = True

	# Parse through the command line arguments passed, and call the
	# corresponding function with the correct parameter.
	# Since options is a OptParse.Value instance, it can be iterated over.
	# This implementation helps avoid lengthy if-else statements
	for opt in options.__dict__.items():
		call_function = functions[str(opt[0])]
		values = opt[1]
		if not values:
			pass
		else:
			if type(values) is list: # Check if the argument type is a list or a string. If list, then iterate through it and call the functions
				for val in values:
					keepGoing = (call_function(val) and keepGoing)
			else:
					keepGoing = (call_function(values) and keepGoing)

	return keepGoing

def CommandFile(filename):
	"This should never be called because we expand --command in this module."
	print( "{0}: error: command file '{1}' was not expanded".format(build.name,filename))
	return False

# end of the build.cli module

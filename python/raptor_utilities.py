#
# Copyright (c) 2007-2011 Nokia Corporation and/or its subsidiary(-ies).
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
# raptor_utilities module
# Useful wrapper functions and classes used in Raptor processing
#

import generic_path
import os.path
import re
import sys
import stat
import shutil

dosDriveRegEx = re.compile("^([A-Za-z]{1}):")

def getOSPlatform():
	return sys.platform.lower()

def getOSFileSystem():
	if getOSPlatform().startswith("win"):
		return "cygwin"
	else:
		return "unix"

def absPathFromPath(aPathRoot, aReference):
	pathRoot = aPathRoot.replace('\\', '/')
	reference = aReference.replace('\\', '/')
	
	if os.path.isabs(reference):
		reference = reference.lstrip(r'/')
	
	joined = os.path.join(pathRoot, reference)
	
	return os.path.abspath(joined)

def make_bool_string(py_boolean):
	'''convert a python boolean value into a string "1" for True and "" for False.
	
	"1" is the Raptor convention for True in makefiles and
	"" is the Raptor convention for False in makefiles.'''
	if py_boolean:
		return "1"
	else:
		return ""

def absPathFromFile(aFileRoot, aReference):
	pathRoot = os.path.dirname(aFileRoot)
	return absPathFromPath(pathRoot, aReference)

def sanitise(aPotentialFilename):
	"Take a string and return a version suitable for use as a filename."
	return re.sub("(\\\\|\/|:|;| )", "_", aPotentialFilename)

def resolveSymbianPath(aFileRoot, aReference, aMainType="", aSubType="", aEPOCROOT="$(EPOCROOT)"):
	""" Convert raw Symbian metadata path/file references into absolute makefile references, or list of references

	<drive>-prefix	: maps to an emulated drive depending on the following cases:
							(a) If the drive is C:, it maps to the *two* locations
								$(EPOCROOT)/epoc32/data/<drive>/<path> and
								$(EPOCROOT)/epoc32/winscw/<drive>/<path>
							(b) If the drive is A:, B:, or D: to Z:, it maps to the *three* locations
								$(EPOCROOT)/epoc32/data/<drive>/<path> and
								$(EPOCROOT)/epoc32/release/winscw/udeb/<drive>/<path> and
								$(EPOCROOT)/epoc32/release/winscw/urel/<drive>/<path>
	Absolute 		: true absolute if:
							(a) PRJ_*EXPORTS destination or DEFFILE location and
							(b) not starting with an 'epoc32'
						otherwise relative to $(EPOCROOT)
	Relative 		: relative to $(EPOCROOT)/epoc32/include if:
							(a) PRJ_EXPORTS destination and
							(b) not a :zip statement,
					  relative to $(EPOCROOT) if:
							(a) PRJ_(TEST)EXPORTS destination and
							(b) a :zip statement,
						otherwise relative to aFileRoot
	|-prefix 		: relative to aFileRoot
	+-prefix 		: relative to $(EPOCROOT)/epoc32"""
	
	# Both reference and fileroot can have backslashes - so convert them.
	reference = aReference.replace('\\', '/')
	fileroot = aFileRoot.replace('\\', '/')
	
	# Remove Trailing backslashes so that the expansions doesnt mess up the shell
	if reference.endswith('/') and len(reference) > 1:
		reference = reference.rstrip('/')

	emulatedDrive = dosDriveRegEx.match(reference)	
	if emulatedDrive and aMainType in ("PRJ_EXPORTS", "PRJ_TESTEXPORTS"):
		# Interpret drive letters as emulator drives but only when dealing with exports
		# Emulated drive C:/ Z:/ and the like		
		resolvedPath = []
		driveLetter = emulatedDrive.group(1)
		if driveLetter.isupper():
			driveLetter = driveLetter.lower()
		
		# C: drive
		if driveLetter is "c":
			resolvedPath.append(dosDriveRegEx.sub(aEPOCROOT + '/epoc32/data/' + driveLetter, reference))
			resolvedPath.append(dosDriveRegEx.sub(aEPOCROOT + '/epoc32/winscw/' + driveLetter, reference))
		else: # Other letters: A, B and D to Z
			resolvedPath.append(dosDriveRegEx.sub(aEPOCROOT + '/epoc32/data/' + driveLetter, reference))
			resolvedPath.append(dosDriveRegEx.sub(aEPOCROOT + '/epoc32/release/winscw/udeb/' + driveLetter, reference))
			resolvedPath.append(dosDriveRegEx.sub(aEPOCROOT + '/epoc32/release/winscw/urel/' + driveLetter, reference))
	elif os.path.isabs(reference):
		# Absolute
		if re.search("(DEFFILE|PRJ_(TEST)?EXPORTS)", aMainType, re.I) and not re.search("^\/epoc32\/", reference, re.I):
			# Ensures prepending of drive if on Windows
			resolvedPath = os.path.abspath(reference)
		else:
			resolvedPath = aEPOCROOT + reference
		
	elif reference.startswith("+"):
		# '+' prefix
		reference = reference.lstrip(r'+')
		resolvedPath = aEPOCROOT + '/epoc32'+reference
	elif reference.startswith("|"):
		# '|' prefix
		reference = reference.lstrip(r'|')
		resolvedPath = absPathFromFile(fileroot, reference)
	else:
		# Relative
		if aMainType == "PRJ_EXPORTS" and aSubType != ":zip":
			resolvedPath = aEPOCROOT + '/epoc32/include/'+reference
		elif aSubType == ":zip":
			resolvedPath = aEPOCROOT + '/' + reference
		else:
			resolvedPath = absPathFromFile(fileroot, aReference)
	
	if isinstance(resolvedPath, list):
		# In this case, this is a list of export destinations, 
		makefilePath = map(lambda x: str(generic_path.Path(x)), resolvedPath)
	else:
		makefilePath = str(generic_path.Path(resolvedPath))
	
	return makefilePath # Note this is either a list of strings, or a single string


class ExternalTool(object):
	""" Generic wrapper for an external tool
	
	Provides the basic means to wrap up a tool that is external to Raptor with a
	consistent interface for both invocation and the capture of output."""
	
	def __init__(self, aTool):
		self.__Tool = aTool
		self.__Output = []

	def call(self, aArgs):		
		print "RUNNNING: {0} {1}".format(self.__Tool, aArgs)
		(input, output) = os.popen2(self.__Tool + " " + aArgs)
		self.__Output = output.read()
		return output.close() 
	
	def getTool(self):
		return self.__Tool

	def getOutput(self):
		return self.__Output
		
	def getOutputLines(self):
		return self.__Output.split("\n")


class NullLog(object):
	""" If your class has these methods then it can act as a log """
	def Info(self, format, *extras):
		"Send an information message to the configured channel"
		return

	def ClockInfo(self):
		"Print a timestamp in seconds"
		return

	def Debug(self, format, *extras):
		"Send a debugging message to the configured channel"
		return

	def Warn(self, format, *extras):
		"Send a warning message to the configured channel"
		return

	def Error(self, format, *extras):
		"Send an error message to the configured channel"
		return

nulllog = NullLog()

def copyfile(_source, _destination):
	"""Copy the source file to the destination file (create a directory
	   to copy into if it does not exist). Don't copy if the destination
	   file exists and has an equal or newer modification time."""
	source = generic_path.Path(str(_source).replace('%20',' '))
	destination = generic_path.Path(str(_destination).replace('%20',' '))
	dest_str = str(destination)
	source_str = str(source)

	try:


		destDir = destination.Dir()
		if not destDir.isDir():
			os.makedirs(str(destDir))
			# preserve permissions
			shutil.copy(source_str, dest_str)
			return 
		# Destination file exists so we have to think about updating it
		sourceMTime = 0
		destMTime = 0
		sourceStat = 0
		try:
			sourceStat = os.stat(source_str)
			sourceMTime = sourceStat[stat.ST_MTIME]
		except OSError, e:
			message = "Source of copyfile does not exist:  " + str(source)
			raise IOError(message)
		try:
			destMTime = os.stat(dest_str)[stat.ST_MTIME]
		except OSError, e:
			pass # destination doesn't have to exist

		if destMTime == 0 or destMTime < sourceMTime:
			# remove old version
			#	- not having ownership prevents chmod
			#	- avoid clobbering the original if it is a hard link
			if os.path.exists(dest_str):
				os.unlink(dest_str)
			# preserve permissions
			shutil.copy(source_str, dest_str)

	except Exception,e:
		message = "Could not update " + dest_str + " from " + source_str + " : " + str(e)
		raise IOError(message)

	return 



## Commandline processing utilities ##

fullCommandOption = "--command"
miniCommandOption = "--co"  # update this if another "co" option is added

def read_command_file(filename, used):
	"""Read commandline options in from a file"""
	if filename in used:
		raise IOError("command file '{0}' refers to itself".format(filename))

	args = []
	try:
		file = open(filename, "r")
		for line in file.readlines():
			args.extend(line.split())
		file.close()
	except:
		raise IOError("couldn't read command file '{0}'".format(filename))

	# expand any command files in the options we just read.
	# making sure we don't get stuck in a loop.
	usedPlusThis = used[:]
	usedPlusThis.append(filename)
	return expand_command_options(args, usedPlusThis)

def expand_command_options(args, files = []):
	"""process commandline options to recursively expand command files (--command options) into a full list of options."""
	expanded = []
	previousWasOpt = False

	for a in args:
		if previousWasOpt: # then this one is the filename
			expanded.extend(read_command_file(a, files))
			previousWasOpt = False
			continue

		if a.startswith(miniCommandOption):
			if "=" in a: # then this is opt=filename
				opt = a.split("=")
				if fullCommandOption.startswith(opt[0]):
					expanded.extend(read_command_file(opt[1], files))
					continue
			else: # the next one is the filename
				if fullCommandOption.startswith(a):
					previousWasOpt = True
					continue

		expanded.append(a) # an ordinary arg, nothing to do with command files

	return expanded

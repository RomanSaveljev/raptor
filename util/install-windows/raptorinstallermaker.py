# Copyright (c) 2009-2011 Nokia Corporation and/or its subsidiary(-ies).
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
# Raptor installer maker script - generates a Windows installer for Raptor using
# the NSIS package in the accompanying directory. Works on Windows and Linux.

import optparse
import os
import os.path
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import unzip
import zipfile



tempdir = ""
makensis_success = None
zipfile_success = None

def generateinstallerversion(sbshome = None):
	shellenv = os.environ.copy()
	shellenv["PYTHONPATH"] = os.path.join(sbshome, "python")
	
	raptorversioncommand = "python -c \"import raptor.version; print(raptor.version.numericversion())\""
	
	# Raptor version is obtained from raptor.version module's numericversion function.
	sbs_version_matcher = re.compile(".*(\d+\.\d+\.\d+).*", re.I)
	
	# Create Raptor subprocess
	versioncommand = subprocess.Popen(raptorversioncommand, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=shellenv)
	raptorversion = ""
	# Get all the lines matching the RE
	for line in versioncommand.stdout.readlines():
		res = sbs_version_matcher.match(line)
		if res:
			raptorversion = res.group(1)
			print("Successfully determined Raptor version {0}".format(raptorversion))

	versioncommand.wait() # Wait for process to end
	
	return raptorversion
	
def unzipnsis(pathtozip):
	global tempdir
	tempdir = tempfile.mkdtemp()
	un = unzip.unzip()
	print("Unzipping NSIS to {0}...".format(tempdir))
	un.extract(pathtozip, tempdir)
	print("Done.")

	# Ensure the correct executable is called	
	dotexe=""
	if "win" in sys.platform.lower():
		dotexe=".exe"
	
	makensispath = os.path.join(tempdir, "NSIS", "makensis" + dotexe)
	
	if not "win" in sys.platform.lower():
		os.chmod(makensispath, stat.S_IRWXU)

	return makensispath
	
def runmakensis(nsiscommand):
	# Create makensis subprocess
	print("Running NSIS command\n{0}".format(nsiscommand))
	makensis = subprocess.Popen(nsiscommand, shell=True)
	makensis.wait() # Wait for process to end
	return makensis.returncode

def cleanup():
	""" Clean up tempdir """
	global tempdir
	print("Cleaning up temporary directory {0}".format(tempdir))
	shutil.rmtree(tempdir,True)
	print("Done.")

def writeLicense(win32supportdirs):
	""" Create the license file from the raptor license, plus the NSIS
	license, plus the license for the tools we're using from the
	win32 support folders
	
	Returns the file object and the file name as a tuple"""
	licensetxt = tempfile.mkstemp()
	(licensetxtfile, licensetxtname) = licensetxt # Decode the tuple
	licensetxtfile = os.fdopen(licensetxtfile,"w") # Reopen as a writeable file object

	raptorlicense = os.path.join(options.sbshome,"license.txt")
	if os.path.exists(raptorlicense):
		with open(raptorlicense,"r") as f:
			shutil.copyfileobj(f,licensetxtfile)

	nsisdir = os.path.join(options.sbshome,"util","install-windows")
	nsisnotices = os.path.join(nsisdir,"notices.txt")
	if os.path.exists(nsisnotices):
		print("Using notices.txt from {0}".format(nsisdir))
		licensetxtfile.write("\n---\n\n")
		with open(nsisnotices,"r") as f:
			shutil.copyfileobj(f,licensetxtfile)
	
	for directory in win32supportdirs:
		dir = win32supportdirs[directory]

		# Check for a notices.txt file
		noticesfile = os.path.join(dir,"notices.txt")
		if os.path.exists(noticesfile):
			print("Using notices.txt from {0}".format(dir))
			licensetxtfile.write("\n---\n\n")
			with open(noticesfile,"r") as f:
				shutil.copyfileobj(f,licensetxtfile)

	licensetxtfile.close()
	
	return (licensetxtfile,licensetxtname) # (File object, filename)

def __writeDirTreeToArchive(zip, dirlist, sbshome, win32supportdirs=False):
	"""Auxilliary function to write all files in each directory tree of dirlist into the
	open archive "zip" assuming valid sbshome; destination path is tweaked for win32supportdirs, 
	so set this to true when writing files into $SBS_HOME/win32"""
	for name in dirlist:
		if name == None:
			continue
		files = os.walk(os.path.join(sbshome, name))
		for dirtuple in files:
			filenames = dirtuple[2]
			dirname = dirtuple[0]
			for file in filenames:
				# Filter out unwanted files
				if not file.lower().endswith(".pyc") and \
				not file.lower().endswith(".project") and \
				not file.lower().endswith(".cproject") and \
				not file.lower().endswith(".pydevproject"):
					origin = os.path.join(dirname, file)
					
					# For the win32 support directories, the destination is different
					if win32supportdirs:
						destination = os.path.join("sbs", "win32", os.path.basename(name.rstrip(os.sep)), 
												dirname.replace(name, "").strip(os.sep), file)
					else:
						destination = os.path.join("sbs", dirname.rstrip(os.sep).replace(sbshome, "").strip(os.sep), file)
					
					print("Compressing {0}\tto\t{1}".format(origin, destination))
					zip.write(origin, destination)

def writeZip(filename, sbshome, sbsbvdir, sbscygwindir, sbsmingwdir, sbspythondir, license):
	"""Write a zip archive with file name "filename" assuming SBS_HOME is sbshome, and  
	that sbsbvdir, sbscygwindir, sbsmingwdir, sbspythondir are the win32 support directories."""
	
	# *Files* in the top level SBS_HOME directory
	sbshome_files = ["RELEASE-NOTES.html"]
	
	# Directories in SBS_HOME
	sbshome_dirs = ["bin", "examples", "lib", "notes", "python", 
				"schema", "style", os.sep.join(["win32", "bin"])]
	
	# Win32 support directories
	win32_dirs = [sbsbvdir, sbscygwindir, sbsmingwdir, sbspythondir]
	
	try:
		# Open the zip archive for writing; if a file with the same
		# name exists, it will be truncated to zero bytes before 
		# writing commences
		zip = zipfile.ZipFile(filename, "w", zipfile.ZIP_DEFLATED)
		
		# Write the license file into the archive
		zip.write(license, os.path.join("sbs","license.txt"))
		# Write the files in the top-level of SBS_HOME into the archive
		for name in sbshome_files:
			origin = os.path.join(sbshome, name)
			destination = os.path.join("sbs", name)
			print("Compressing {0}\tto\t{1}".format(origin, destination))
			zip.write(origin, destination)
		
		# Write all files in the the directories in the top-level of SBS_HOME into the archive
		print("Reading the sbs directories...")
		__writeDirTreeToArchive(zip, sbshome_dirs, sbshome, win32supportdirs=False)
		print("Writing sbs directories to the archive is complete.")
		
		# Write all files in the the win32 support directories in the top-level of SBS_HOME into the archive
		print("Reading the win32 support directories")
		__writeDirTreeToArchive(zip, win32_dirs, sbshome, win32supportdirs=True)
		print("Writing win32 support directories to the archive is complete.")
		
		zip.close()
		print("Zipoutput: \"{0}\"".format(os.path.join(os.getcwd(), filename)))
		print("Zip file creation successful.")
		return 0
	except Exception, e:
		print("Error: failed to create zip file: {0}".format(str(e)))
		return 2


if __name__ == "__main__":
	# Create CLI and parse it
	parser = optparse.OptionParser()
	win32_msg = "Can be a full/relatitve path; prefix with \"WIN32SUPPORT\\\" to be relative to the Win32 support directory. Omitting this value will assume a default to a path inside the Win32 support directory."

	parser.add_option("-s", "--sbs-home", dest="sbshome", help="Path to use as SBS_HOME environment variable. If not present the script exits.")
	parser.add_option("-w", "--win32-support", dest="win32support", help="Path to Win32 support directory. If not present the script exits.")
	parser.add_option("-b", "--bv", dest="bv", help="Path to Binary variation CPP \"root\" directory. " + win32_msg)
	parser.add_option("--nobv", dest="nobv", help="Do not include the binary variation CPP (ignores any --bv option).", action="store_true" , default=False)
	parser.add_option("-c", "--cygwin", dest="cygwin", help="Path to Cygwin \"root\" directory. " + win32_msg)
	parser.add_option("-m", "--mingw", dest="mingw", help="Path to MinGW \"root\" directory. " + win32_msg)
	parser.add_option("-p", "--python", dest="python", help="Path to Python \"root\" directory. " + win32_msg)
	
	version_msg = "This will be present in the Raptor installer's file name and the installer's pages."
	parser.add_option("--prefix", dest="versionprefix", type="string", default="", help="A string to use as a prefix to the Raptor version string. " + version_msg)
	parser.add_option("--postfix", dest="versionpostfix", type="string", default="", help="A string to use as a postfix to the Raptor version string. " + version_msg)
	
	parser.add_option("--noclean", dest="noclean", help="Do not clean up the temporary directory created during the run.", action="store_true" , default=False)
	parser.add_option("--noexe", dest="noexe", help="Do not create a Windows .exe installer of the Raptor installation.", action="store_true" , default=False)
	parser.add_option("--nozip", dest="nozip", help="Do not create a zip archive of the Raptor installation.", action="store_true" , default=False)

	(options, args) = parser.parse_args()

	# Required directories inside the win32-support directory (i.e. the win32-support repository).
	win32supportdirs = {"cygwin":"cygwin", "mingw":"mingw", "python":"python27"}

	if not options.nobv:
		win32supportdirs["bv"] = "bv"

	if options.sbshome == None:
		print("ERROR: no SBS_HOME passed in. Exiting...")
		sys.exit(2)
	elif not os.path.isdir(options.sbshome):
		print("ERROR: the specified SBS_HOME directory \"{0}\" does not exist. Cannot build installer. Exiting...".format(options.sbshome))
		sys.exit(2)

	if options.win32support == None:
		print("ERROR: no win32support directory specified. Unable to proceed. Exiting...")
		sys.exit(2)
	else:
		# Check for command line overrides to defaults
		for directory in win32supportdirs:
			print("Checking for location \"{0}\"...".format(directory))
			value = getattr(options, directory)
			if value != None: # Command line override
				if value.lower().startswith("win32support"):
					# Strip off "WIN32SUPPORT\" and join to Win32 support location
					win32supportdirs[directory] = os.path.join(options.win32support, value[13:]) 
				else:
					# Relative to current directory
					win32supportdirs[directory] = value
				print("\tUsing commandline override value: \"{0}\"".format(str(value)))

			else: # Use default location
				win32supportdirs[directory] = os.path.join(options.win32support, win32supportdirs[directory])
				print("\tDefaulting to: \"{0}\"".format(str(win32supportdirs[directory])))
		
		# Check that all the specified directories exist and exit if any of them is missing.
		for directory in win32supportdirs:
			dir = win32supportdirs[directory]
			if os.path.isdir(dir):
				print("Found directory {0}".format(dir))

			else:
				print("ERROR: directory {0} does not exist. Cannot build installer. Exiting...".format(dir))
				sys.exit(2)

	# For grabbing a copy of nsis:
	sys.path.append(options.sbshome)
	from python import urlget

	# Create the license file
	(licensetxtfile,licensetxtname) = writeLicense(win32supportdirs)

	raptorversion = options.versionprefix + generateinstallerversion(options.sbshome) + options.versionpostfix

	print("Using Raptor version {0} ...".format(raptorversion))

	if not options.noexe:

		got_zip = False


		nsis_zip = "NSIS.zip"
		try:
			s = os.stat(nsis_zip)
			got_zip = True
		except OSError,e:
			for url in [ "http://rene.europe.nokia.com/~raptorbot/files/NSIS.zip",
						 "http://projects.developer.nokia.com/raptor/files/NSIS.zip" ]:
				try:
					print("Attempting to download {0} from {1}".format(nsis_zip,url))
					urlget.get_http(url,nsis_zip)
					got_zip = True
					print("Download ok")
				except Exception,e:
					print("WARNING: couldn't get {0} from {1}: {2}".format(nsis_zip, url, str(e)))
					continue

		if not got_zip:
			print("ERROR: don't have {0} and couldn't download it".format(nsis_zip))
			sys.exit(3)
			
		makensispath = unzipnsis("." + os.sep + "NSIS.zip")
		command_string = "{makensis} -DRAPTOR_LOCATION={sbs_home} " \
					"{bvopt} -DCYGWIN_LOCATION={cygwin} " \
					"-DMINGW_LOCATION={mingw} -DPYTHON_LOCATION={python} " \
					"-DLICENSE_FILE={license} " \
					"-DRAPTOR_VERSION={sbs_version} {nsis_script}"
		if options.nobv:
			bvopt = ""
		else:
			bvopt = "-DBV_LOCATION={bv}".format(bv = win32supportdirs["bv"])

		nsiscommand = command_string.format(makensis = makensispath,
					sbs_home = options.sbshome, 
					bvopt = bvopt, 
					cygwin = win32supportdirs["cygwin"],
					mingw = win32supportdirs["mingw"],
					python = win32supportdirs["python"],
					license = licensetxtname,
					sbs_version = raptorversion,
					nsis_script = os.path.join(options.sbshome, "util", "install-windows", "raptorinstallerscript.nsi")
				)
	
		# On Linux, we need to run makensis via Bash, so that it can find all its
		# internal libraries and header files etc. Makensis fails unless it 
		# is executed this way on Linux.
		if "lin" in sys.platform.lower():
			nsiscommand = "bash -c \"{0}\"".format(nsiscommand)
	
		makensis_success = runmakensis(nsiscommand)
	
		# Only clean NSIS installation in the temporary directory if requested
		if not options.noclean:
			cleanup()
		else:
			print("Not cleaning makensis in {0}".format(makensispath))
	
	else:
		print("Not creating .exe as requested.")

	# Only create zip archive if required
	if not options.nozip:
		filename = "sbs-" + raptorversion + ".zip"
		if options.nobv:
			bvopt = None
		else:
			bvopt = win32supportdirs["bv"]	
		zipfile_success = writeZip(filename, options.sbshome, bvopt, win32supportdirs["cygwin"], win32supportdirs["mingw"], win32supportdirs["python"], licensetxtname)
	else:
		print("Not creating zip archive as requested.")
	
	if not options.noclean:
		os.unlink(licensetxtname)
	
	if not options.noexe and makensis_success != None:
		print("Makensis Windows installer creation completed and exited with code {0}".format(makensis_success))

	if not options.nozip and zipfile_success != None:
		print("Zip file creation completed and exited with code {0}".format(zipfile_success))
	print("Finished.")

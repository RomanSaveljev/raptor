#
# Copyright (c) 2009 - 2011 Nokia Corporation and/or its subsidiary(-ies).
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

from raptor_tests import SmokeTest
from raptor_tests import ReplaceEnvs
import os
import sys

def run():
	t = SmokeTest()
	t.description =  """talon_test: three part test
	1) Test talon's -c option
	2) Test talon with a script file that has some blank lines and a single non-blank command line
	3) Test talon with a command that outputs control characters
	"""

	# Don't need these as we are not invoking Raptor
	t.logfileOption = lambda : ""
	t.makefileOption = lambda : ""

	# Set up variables for talon
	bindir = ReplaceEnvs("$(SBS_HOME)/$(HOSTPLATFORM_DIR)/bin")
	bash = "/bin/bash"
	talon = bindir + "/talon"

	# Adjust if on Windows - three "tries" for Bash on Windows.
	# 1 Default try
	if "win" in sys.platform.lower():
		bash = ReplaceEnvs("$(SBS_HOME)/win32/cygwin/bin/bash.exe")
		talon = ReplaceEnvs("$(SBS_HOME)/$(HOSTPLATFORM_DIR)/bin/talon.exe")
	
	# 2 Bash from a Cygwin
	if os.environ.has_key("SBS_CYGWIN"):
		bash = ReplaceEnvs("$(SBS_CYGWIN)/bin/bash.exe")
	
	# 3 Bash from an env. var.
	if os.environ.has_key("SBS_SHELL"):
		bash = os.environ["SBS_SHELL"]
	
	# Talon's command line
	commandline="\"|name=commandlinetest;COMPONENT_META=commandline/group/bld.inf;PROJECT_META=commandline.mmp;|echo Command line invocation output\""
	
	# Talon's "shell script"
	scriptfile=ReplaceEnvs("$(SBS_HOME)/test/smoke_suite/test_resources/talon_test/script")
	
	# Environment variables needed by talon - TALON_SHELL must be bash; the other two can be arbitrary.
	os.environ["TALON_SHELL"]=bash
	os.environ["TALON_BUILDID"]="{0}_{1}".format("talon_buildid", os.getpid())
	os.environ["TALON_RECIPEATTRIBUTES"]="component=talontest"

	# First part of test - command line
	t.name = "talon_test_command_line"
	t.command = "{0} -c {1}".format(talon, commandline)
	t.targets = []
	t.mustmatch_multiline = ["<recipe component=talontest>.*<!\[CDATA\[.*\+ echo Command line invocation output" + 
			".*\]\]><time start='\d+\.\d+' elapsed='\d+\.\d+' />" + 
			".*<status exit='ok' attempt='1' />.*</recipe>"]

	t.run()

	# Second part of test - script file
	t.name = "talon_test_script_file"
	t.command = "{0} {1}".format(talon, scriptfile)
	t.targets = []
	t.mustmatch_multiline = ["<recipe component=talontest>.*<!\[CDATA\[.*\+ echo Script file output" + 
			".*\]\]><time start='\d+\.\d+' elapsed='\d+\.\d+' />" + 
			".*<status exit='ok' attempt='1' />.*</recipe>"]

	t.run()
	
	# a script which outputs control characters
	scriptfile=ReplaceEnvs("$(SBS_HOME)/test/smoke_suite/test_resources/talon_test/ctrl.py")

	t.name = "talon_test_control_chars"
	t.command = '{0} -c "|name=ctrl;|python {1}"'.format(talon, scriptfile)
	t.targets = []
	# the script writes "AAA", then each control char from 0 to 31, then "ZZZ".
	# 0-31 decimal are not allowed in the output, except for 9, 10 and 13.
	# check that the CTRL codes are missing and also that CTRL-I, CTRL-J and
	# CTRL-M are not converted into ^I ^J ^M.
	t.mustnotmatch = [ '[\000-\010\013\014\016-\037]', '\^[IJM]' ]
	# do not try and match CTRL-J and CTRL-M explicitly because line ending
	# conversions between talon and here will mess things up.
	# the escaping hell at the end is to match ^[ ^\ ^] ^^ and ^_
	t.mustmatch_multiline = ["<recipe component=talontest>.*<!\[CDATA\[.*" +
							 "AAA\^@\^A\^B\^C\^D\^E\^F\^G\^H\011.*\^K\^L.*\^N\^O\^P\^\Q\^R\^S\^T\^U\^V\^W\^X\^Y\^Z\^\[\^\\\\\^\]\^\^\^_ZZZ" +
							 ".*\]\].*</recipe>"]
	
	t.run()
	
	# Print final result
	t.name = "talon_test"
	t.print_result()

	# Delete the added environment variables
	del os.environ["TALON_SHELL"]
	del os.environ["TALON_BUILDID"]
	del os.environ["TALON_RECIPEATTRIBUTES"]

	return t

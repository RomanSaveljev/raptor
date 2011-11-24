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
	if "SBS_CYGWIN" in os.environ:
		bash = ReplaceEnvs("$(SBS_CYGWIN)/bin/bash.exe")
	
	# 3 Bash from an env. var.
	if "SBS_SHELL" in os.environ:
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
	# the script writes "AAA", then each char from 0 to 255, then "ZZZ".
	# 0-31 and 127-255 decimal are not allowed in the output, except for 9, 10 and 13.
	# check that the non-printable codes are missing and also that CTRL-I, CTRL-J and
	# CTRL-M are not converted.
	t.mustnotmatch = [ '[\000-\010\013\014\016-\037\177-\377]', '&#x0[9ad];' ]
	# do not try and match CTRL-J and CTRL-M explicitly because line ending
	# conversions between talon and here will mess things up.
	t.mustmatch_multiline = ["<recipe component=talontest>.*<!\[CDATA\[.*" +
							 "AAA&#x00;&#x01;&#x02;&#x03;&#x04;&#x05;&#x06;&#x07;&#x08;\011.*&#x0b;&#x0c;.*&#x0e;&#x0f;&#x10;&#x11;&#x12;&#x13;&#x14;&#x15;&#x16;&#x17;&#x18;&#x19;&#x1a;&#x1b;&#x1c;&#x1d;&#x1e;&#x1f; !\"#\$%&'()\*\+,-\./0123456789:;<=>\?@ABCDEFGHIJKLMNOPQRSTUVWXYZ\[\\\]\^_`abcdefghijklmnopqrstuvwxyz{|}~&#x7f;&#x80;&#x81;&#x82;&#x83;&#x84;&#x85;&#x86;&#x87;&#x88;&#x89;&#x8a;&#x8b;&#x8c;&#x8d;&#x8e;&#x8f;&#x90;&#x91;&#x92;&#x93;&#x94;&#x95;&#x96;&#x97;&#x98;&#x99;&#x9a;&#x9b;&#x9c;&#x9d;&#x9e;&#x9f;&#xa0;&#xa1;&#xa2;&#xa3;&#xa4;&#xa5;&#xa6;&#xa7;&#xa8;&#xa9;&#xaa;&#xab;&#xac;&#xad;&#xae;&#xaf;&#xb0;&#xb1;&#xb2;&#xb3;&#xb4;&#xb5;&#xb6;&#xb7;&#xb8;&#xb9;&#xba;&#xbb;&#xbc;&#xbd;&#xbe;&#xbf;&#xc0;&#xc1;&#xc2;&#xc3;&#xc4;&#xc5;&#xc6;&#xc7;&#xc8;&#xc9;&#xca;&#xcb;&#xcc;&#xcd;&#xce;&#xcf;&#xd0;&#xd1;&#xd2;&#xd3;&#xd4;&#xd5;&#xd6;&#xd7;&#xd8;&#xd9;&#xda;&#xdb;&#xdc;&#xdd;&#xde;&#xdf;&#xe0;&#xe1;&#xe2;&#xe3;&#xe4;&#xe5;&#xe6;&#xe7;&#xe8;&#xe9;&#xea;&#xeb;&#xec;&#xed;&#xee;&#xef;&#xf0;&#xf1;&#xf2;&#xf3;&#xf4;&#xf5;&#xf6;&#xf7;&#xf8;&#xf9;&#xfa;&#xfb;&#xfc;&#xfd;&#xfe;&#xff;ZZZ" +
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

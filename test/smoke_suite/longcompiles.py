#
# Copyright (c) 2011-2014 Microsoft Mobile and/or its subsidiary(-ies).
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

def run():
	t = SmokeTest()
	
	command = "sbs -k -b smoke_suite/test_resources/simple/longcompiles.inf -c armv7_urel{variant} -c winscw_udeb{variant} -c arm.v5.urel.gcce4_4_1{variant}"
	talon_warning = ".*Command line length '\d+' exceeds the shell limit on this system of '\d+'.  If this recipe is a compile, try using the '.use_compilation_command_file' variant to reduce overall command line length."
	targets = [
				"$(EPOCROOT)/epoc32/release/armv7/urel/longcompiles.exe",
				"$(EPOCROOT)/epoc32/release/winscw/udeb/longcompiles.exe",
				"$(EPOCROOT)/epoc32/release/armv5/urel/longcompiles.exe"		
		]

	t.name = "longcompile_no_command_file"	
	t.description = """
		Confirm OS-specific behaviour on massive compilation command lines.
		On Linux, all should be well, but on Windows the compile will fail
		together with a talon warning with some potentially useful advice.
		"""			
	t.command = command.format(variant="")
	if t.onWindows:
		t.targets = []
		t.mustmatch_singleline = [talon_warning]
		t.warnings = 24
		t.errors = 1
		t.returncode = 1
	else:	
		t.targets = targets
		t.mustnotmatch_singleline = [talon_warning]
	t.run()
	
	
	t.name = "longcompile_command_file"	
	t.description = """
		Confirm that a command file is used with the .use_compilation_command_file
		variant, and that the build succeeds on all host OS platforms.
		"""
	t.command = command.format(variant=".use_compilation_command_file")
	t.targets = targets
	t.addbuildtargets('smoke_suite/test_resources/simple/longcompiles.inf', [
		"longcompiles_exe/armv7/urel/cc.cmdfile",
		"longcompiles_exe/winscw/udeb/cc.cmdfile",
		"longcompiles_exe/armv5/urel/cc.cmdfile"
		])
	t.mustmatch_singleline = []
	t.mustnotmatch_singleline = []
	t.warnings = 0
	t.errors = 0
	t.returncode = 0
	t.run()
	
	t.name = "longcompiles"
	t.print_result()
	return t

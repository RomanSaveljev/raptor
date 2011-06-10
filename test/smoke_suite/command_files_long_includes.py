#
# Copyright (c) 2011 Nokia Corporation and/or its subsidiary(-ies).
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
	t.name = "command_files_long_includes"	
	t.description = """Ensure that command files are used ."""
	t.command = "sbs -b smoke_suite/test_resources/simple/long_includes.inf -c armv7_urel -c winscw_udeb -c arm.v5.urel.gcce4_4_1"
	t.targets = [
				"$(EPOCROOT)/epoc32/release/armv7/urel/long_includes.exe",
				"$(EPOCROOT)/epoc32/release/winscw/udeb/long_includes.exe",
				"$(EPOCROOT)/epoc32/release/armv5/urel/long_includes.exe"		
				]
	t.addbuildtargets('smoke_suite/test_resources/simple/long_includes.inf', [
		"long_includes_exe/armv7/urel/cc_includes.cmdfile",
		"long_includes_exe/winscw/udeb/cc_includes.cmdfile",
		"long_includes_exe/armv5/urel/cc_includes.cmdfile"
	])
	t.run()
	return t

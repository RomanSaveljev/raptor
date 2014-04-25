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
	t.name="environment_native"

	t.description = """Checks that if you set SBS_HOME this is ignored"""
	
	t.command = "sbs -b smoke_suite/test_resources/simple/bld.inf -c arm.v5.udeb.gcce4_4_1"
	t.targets = [
		"$(EPOCROOT)/epoc32/release/armv5/udeb/test.exe"
		]

	t.environ['SBS_HOME'] = '/does/not/exist'
	t.run()

	if t.onWindows:
		t.name="environment_cygwin_bash"
		t.usebash = True
		t.description = """Checks that if you set SBS_HOME this is ignored on Cygwin"""
		t.run()

	t.name = "environment"
	t.print_result()
	return t

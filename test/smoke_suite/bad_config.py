#
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

from raptor_tests import SmokeTest

def run():
	t = SmokeTest()
	t.name="bad_config"

	t.description = """Checks that if you give an incomplete (unbuildable) configuration that raptor complains nicely without a traceback."""
	
	t.command = "sbs -b smoke_suite/test_resources/simple/bld.inf -c arm.v5.rvct4_0" # missing "urel" or "udeb"
	t.targets = [
		]	
	t.mustmatch = [
	"sbs: error: The selected configuration .-c option. 'arm\.v5\.rvct4_0' is incomplete or invalid and cannot result in a successful build: Unset variable 'VARIANTTYPE' used in spec 'none' with config 'none'"
	]
	t.mustnotmatch = [
		".*Traceback.*",
		".*UninitialisedVariableException.*"
	]
	t.errors = 1
	t.returncode = 1
	
	t.run()
	t.print_result()
	return t

#
# Copyright (c) 2009-2014 Microsoft Mobile and/or its subsidiary(-ies).
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
	t.name = "badconfigs"

	t.description = """Tests that Raptor does indicate errors but does not traceback when reading faulty config files"""
	t.command = "sbs -b smoke_suite/test_resources/simple/bld.inf --configpath=test/smoke_suite/test_resources/badconfigs --export-only -n -m ${SBSMAKEFILE} -f ${SBSLOGFILE}"
	t.mustmatch = [
		"sbs: warning: Failed to read XML file: .*missing_model_close_tag.xml:14:3: mismatched tag.*",
		"sbs: warning: Failed to read XML file: .*missing_build_close.xml:18:0: no element found.*",
		"sbs: warning: Unknown element bset.*",
		"sbs: warning: Failed to read XML file: .*testconfig.xml:17:2: mismatched tag.*",
		"sbs: warning: Unknown element bset.*",
		"sbs: warning: Failed to read XML file: .*uknowntag.xml:17:2: mismatched tag.*",
		"sbs: warning: Failed to read XML file:.*notxml1.xml:1:5:.*"
	]
	t.warnings = 7
	t.errors = 0
	t.returncode=0
	t.run()

	return t

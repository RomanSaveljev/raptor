#
# Copyright (c) 2009 Nokia Corporation and/or its subsidiary(-ies).
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
	
	t.name = "exported_flm_extension"
	t.command = "sbs -b smoke_suite/test_resources/simple_extension/flm_bld.inf -c armv5"
	t.targets = [
		"$(EPOCROOT)/epoc32/build/flm_test_1_2",
		"$(EPOCROOT)/epoc32/tools/makefile_templates/tools/flm_export.xml",
		"$(EPOCROOT)/epoc32/tools/makefile_templates/tools/flm_export.flm"
		]
	t.run()
	
	t.name = "per_component_flm"
	t.command = "sbs --configpath=test/smoke_suite/test_resources/docs" + \
	            " -b smoke_suite/test_resources/simple_dll/bld.inf" + \
	            " -b smoke_suite/test_resources/simple_lib/bld.inf" + \
	            " -c armv5.documentation"
	t.targets = [
		"$(EPOCROOT)/epoc32/build/flm_test_1_2",
		"$(EPOCROOT)/epoc32/tools/makefile_templates/tools/flm_export.xml",
		"$(EPOCROOT)/epoc32/tools/makefile_templates/tools/flm_export.flm"
		]
	t.run()
	
	t.name = "flm_extension"
	t.print_result()
	return t

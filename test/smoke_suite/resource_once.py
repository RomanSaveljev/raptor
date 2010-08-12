#
# Copyright (c) 2009-2010 Nokia Corporation and/or its subsidiary(-ies).
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
from raptor_meta import BldInfFile

def run():
	t = SmokeTest()
	t.id = "43562d"
	t.name =  "resource_build_header_onlyonce"
	t.description = "Ensure we only generate the resource header once even when there are many languages"
	t.command = "sbs  -b smoke_suite/test_resources/resource/group/simple.inf -c winscw_udeb -m ${SBSMAKEFILE} -f ${SBSLOGFILE}; XX=$?; cat ${SBSLOGFILE}; exit $XX" 
	t.usebash = True
	t.targets = [
		"$(EPOCROOT)/epoc32/include/testresource.hrh",
		"$(EPOCROOT)/epoc32/include/testresource_badef.rh",
		"$(EPOCROOT)/epoc32/data/z/resource/testresource/testresource.rsc",
		"$(EPOCROOT)/epoc32/release/winscw/udeb/z/resource/testresource/testresource.rsc",
		"$(EPOCROOT)/epoc32/release/winscw/urel/z/resource/testresource/testresource.rsc",
		"$(EPOCROOT)/epoc32/data/z/resource/testresource/testresource.r37",
		"$(EPOCROOT)/epoc32/release/winscw/udeb/z/resource/testresource/testresource.r37",
		"$(EPOCROOT)/epoc32/release/winscw/urel/z/resource/testresource/testresource.r37",
		"$(EPOCROOT)/epoc32/data/z/resource/testresource/testresource.r94",
		"$(EPOCROOT)/epoc32/release/winscw/udeb/z/resource/testresource/testresource.r94",
		"$(EPOCROOT)/epoc32/release/winscw/urel/z/resource/testresource/testresource.r94",
		"$(EPOCROOT)/epoc32/data/z/resource/testresource/testresource.r96",
		"$(EPOCROOT)/epoc32/release/winscw/udeb/z/resource/testresource/testresource.r96",
		"$(EPOCROOT)/epoc32/release/winscw/urel/z/resource/testresource/testresource.r96",
		"$(EPOCROOT)/epoc32/include/testresource.rsg",
		"$(EPOCROOT)/epoc32/release/winscw/udeb/testresource.exe"
		]
	t.countmatch = [["rcomp.*-h.*rsg",1]]
	t.mustnotmatch = []
	t.mustmatch = []
	t.run()

	t.name = 'resource_once'
	t.print_result()
	return t

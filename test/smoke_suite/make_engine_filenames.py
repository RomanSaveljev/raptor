#
# Copyright (c) 2010-2014 Microsoft Mobile and/or its subsidiary(-ies).
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
	t.name = "make_engine_filenames"
	t.description = "Can we pass the makefilename and stage name to emake options like --annofile etc?"
	
	t.mustmatch = [	".*Executing.*emake.*historyfile=.*default\.history.*",
			".*Executing.*emake.*annofile=.*\.default\.anno.*"]

	t.mustnotmatch = [".*Executing.*emake.*historyfile=.*#STAGE#\.history.*",
			  ".*Executing.*emake.*annofile=#MAKEFILE#\.anno.*"]
	
	t.usebash = True
	t.errors = 1
	t.returncode = 1
	base_command = "sbs generate -b smoke_suite/test_resources/simple/bld.inf -f-"
	
	t.command = base_command + " -e emake --mo=--emake-annofile=#MAKEFILE#.anno --mo=--emake-historyfile=$(EPOCROOT)/epoc32/build/#STAGE#.history -k NOTARGET"
	t.run()
		
	t.print_result()
	return t

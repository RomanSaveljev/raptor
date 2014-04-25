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
	t.usebash = True

	t.name = "var_test"
	t.command = "sbs -b smoke_suite/test_resources/variable_test/bld.inf -c armv7 -f ${SBSLOGFILE} -m ${SBSMAKEFILE} && cat ${SBSLOGFILE}"
	t.targets = []
	t.mustmatch = ["<debug>SBS=.*/bin/sbs\.bat</debug>"]
	t.run("windows")

	t.mustmatch = ["<debug>SBS=.*/bin/sbs</debug>"]
	t.run("linux")
	
	return t

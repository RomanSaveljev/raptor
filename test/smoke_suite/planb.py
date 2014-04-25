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
	t.name = "planb"
	t.description = "Basic planb test of the makefile mechanism."
	
	t.usebash = True
	t.command = "sbs -b smoke_suite/test_resources/planb/bld.inf -f-"
	t.countmatch = [
				["\+ echo bitmap-all", 4],    # 2 platforms * 2 variants
				["\+ echo resource-all", 4],
				["\+ echo target-all", 4],
				["\+ echo bitmap-no_var_dep", 2],    # 2 platforms
				["\+ echo resource-no_var_dep", 2],
				["\+ echo target-no_var_dep", 2],
				["\+ echo bitmap-no_plat_dep", 1],    # 1 build
				["\+ echo resource-no_plat_dep", 1],
				["\+ echo target-no_plat_dep", 1],
				]
	
	t.run()
	return t

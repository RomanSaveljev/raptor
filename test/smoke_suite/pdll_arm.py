#
# Copyright (c) 2009-2011 Nokia Corporation and/or its subsidiary(-ies).
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

from raptor_tests import AntiTargetSmokeTest

def run():
	t = AntiTargetSmokeTest()
	t.usebash = True
	
	command = "sbs -b smoke_suite/test_resources/simple_dll/pbld.inf -c {0} -f -"
	maintargets = [
		"$(EPOCROOT)/epoc32/release/{0}/udeb/createstaticpdll.dll.sym",
		"$(EPOCROOT)/epoc32/release/{0}/urel/createstaticpdll.dll.sym",
		"$(EPOCROOT)/epoc32/release/{0}/udeb/createstaticpdll.dll",
		"$(EPOCROOT)/epoc32/release/{0}/urel/createstaticpdll.dll"
		]
	armv5targets = [
		"$(EPOCROOT)/epoc32/release/{0}/lib/createstaticpdll.dso",
		"$(EPOCROOT)/epoc32/release/{0}/lib/createstaticpdll{000a0000}.dso"
		]
	buildtargets =  [
		"createstaticpdll_dll/{0}/udeb/CreateStaticDLL.o",
		"createstaticpdll_dll/{0}/urel/CreateStaticDLL.o"
		]
	mustmatch = [
		r".*\busrt\d_\d\.lib\b.*",
		r".*\bscppnwdl\.dso\b.*"
		]
	mustnotmatch = [
		".*ksrt.*"
		]
	
	t.name = "pdll_armv5_rvct"
	t.command = command.format("armv5")
	t.targets = [p.replace("{0}","armv5") for p in  maintargets + armv5targets][:]	# Shallow, as we optionally extend later and then re-use
	t.addbuildtargets('smoke_suite/test_resources/simple_dll/pbld.inf', [p.format("armv5") for p in buildtargets])
	t.mustmatch = mustmatch
	t.mustnotmatch = mustnotmatch
	t.run()
		
	t.name = "pdll_armv5_clean"
	t.command = command.format("armv5") + " clean"
	t.targets = []
	t.mustmatch = []
	t.mustnotmatch = []
	t.run()
	
	t.name = "pdll_armv5_gcce"
	t.command = command.format("gcce_armv5")
	t.targets = [p.replace("{0}","armv5") for p in maintargets + armv5targets]
	t.addbuildtargets('smoke_suite/test_resources/simple_dll/pbld.inf', [p.format("armv5") for p in buildtargets])
	t.mustmatch = mustmatch
	t.mustnotmatch = mustnotmatch
	t.run()

	t.name = "pdll_armv5_gcce_clean"
	t.command = command.format("gcce_armv5") + " clean"
	t.targets = []
	t.mustmatch = []
	t.mustnotmatch = []
	t.run()

	t.name = "pdll_armv7_rvct"
	t.command = command.format("armv7")
	t.targets = [p.replace("{0}","armv7") for p in maintargets][:]	# Shallow, as we optionally extend later and then re-use
	t.addbuildtargets('smoke_suite/test_resources/simple_dll/pbld.inf', [p.format("armv7") for p in buildtargets])
	t.mustmatch = mustmatch
	t.mustnotmatch = mustnotmatch
	t.run()
	
	t.name = "pdll_armv7_clean"
	t.command = command.format("armv7") + " clean"
	t.targets = []
	t.mustmatch = []
	t.mustnotmatch = []
	t.run()
	
	t.name = "pdll_armv7_gcce"
	t.command = command.format("arm.v7.udeb.gcce4_5_1 -c arm.v7.urel.gcce4_3_2")
	t.targets = [p.replace("{0}","armv7") for p in maintargets]
	t.addbuildtargets('smoke_suite/test_resources/simple_dll/pbld.inf', [p.format("armv7") for p in buildtargets])
	t.mustmatch = mustmatch
	t.mustnotmatch = mustnotmatch
	t.run()

	t.name = "pdll_arm"
	t.print_result()
	return t

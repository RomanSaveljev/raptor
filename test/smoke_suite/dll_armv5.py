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

from raptor_tests import AntiTargetSmokeTest

def run():
	t = AntiTargetSmokeTest()
	t.usebash = True
	
	command = "sbs -b smoke_suite/test_resources/simple_dll/bld.inf -c {0} -f-"
	maintargets = [
		"$(EPOCROOT)/epoc32/release/armv5/udeb/createstaticdll.dll.sym",
		"$(EPOCROOT)/epoc32/release/armv5/urel/createstaticdll.dll.sym",
		"$(EPOCROOT)/epoc32/release/armv5/lib/createstaticdll.dso",
		"$(EPOCROOT)/epoc32/release/armv5/lib/createstaticdll{000a0000}.dso",
		"$(EPOCROOT)/epoc32/release/armv5/udeb/createstaticdll.dll",
		"$(EPOCROOT)/epoc32/release/armv5/urel/createstaticdll.dll"
		]
	abiv1libtargets = [
		"$(EPOCROOT)/epoc32/release/armv5/lib/createstaticdll.lib",
		"$(EPOCROOT)/epoc32/release/armv5/lib/createstaticdll{000a0000}.lib"
		]	
	buildtargets =  [
		"createstaticdll_dll/armv5/udeb/CreateStaticDLL.o",
		"createstaticdll_dll/armv5/urel/CreateStaticDLL.o"
		]
	mustmatch = [
		r".*\busrt\d_\d\.lib\b.*",
		r".*\bscppnwdl\.dso\b.*"
			]
	mustnotmatch = [
		".*ksrt.*"
		]
	
	# Note that ABIv1 import libraries are only generated for RVCT-based armv5
	# builds on Windows if the kit asks for it (off by default)
	
	t.name = "dll_armv5_rvct"
	t.command = command.format("armv5")
	t.targets = maintargets[:]	# Shallow, as we optionally extend later and then re-use
	t.addbuildtargets('smoke_suite/test_resources/simple_dll/bld.inf', buildtargets)
	t.mustmatch = mustmatch
	t.mustnotmatch = mustnotmatch
	t.run()
	
	t.name = "dll_armv5_rvct_abiv1"
	t.command += " --configpath=test/config/abiv1kit"
	t.targets.extend(abiv1libtargets)
	t.run("windows")
		
	t.name = "dll_armv5_clean"
	t.command = "sbs -b smoke_suite/test_resources/simple_dll/bld.inf -c armv5 clean"
	t.targets = []
	t.mustmatch = []
	t.mustnotmatch = []
	t.run()	
		
	t.name = "dll_armv5_gcce"
	t.command = command.format("gcce_armv5")
	t.targets = maintargets
	t.antitargets = abiv1libtargets
	t.addbuildtargets('smoke_suite/test_resources/simple_dll/bld.inf', buildtargets)
	t.mustmatch = mustmatch
	t.mustmatch.append("-funsigned-bitfields")
	t.mustnotmatch = mustnotmatch
	t.run()	
	
	t.name = "dll_armv5"
	t.print_result()
	return t

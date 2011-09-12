#
# Copyright (c) 2010-2011 Nokia Corporation and/or its subsidiary(-ies).
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


from raptor_tests import SmokeTest

def run():

	t = SmokeTest()
	t.usebash = True

	BLD_INF = "smoke_suite/test_resources/custom_dll/bld.inf"
	OLD_ELF2E32 = "$(SBS_HOME)/test/smoke_suite/test_resources/custom_dll/elf2e32_old"
	if t.onWindows:
		OLD_ELF2E32 += ".exe"

	# Commands for using the new (i.e. the one with the --asm option) and old
	# version of elf2e32.
	new_cmd = "sbs -b {0} -c {{0}}".format(BLD_INF)
	old_cmd = "SBS_ELF2E32={0}".format(OLD_ELF2E32) + " " + new_cmd

	t.targets = [
		"$(EPOCROOT)/epoc32/release/armv5/lib/customdll.dso",
		"$(EPOCROOT)/epoc32/release/armv5/lib/customdll{000a0000}.dso",
		"$(EPOCROOT)/epoc32/release/armv5/udeb/customdll.dll",
		"$(EPOCROOT)/epoc32/release/armv5/udeb/customdll.dll.map",
		"$(EPOCROOT)/epoc32/release/armv5/urel/customdll.dll",
		"$(EPOCROOT)/epoc32/release/armv5/urel/customdll.dll.map"
		]
	t.addbuildtargets(BLD_INF, [
		"customdll_dll/armv5/customdll{000a0000}.",
		"customdll_dll/armv5/customdll{000a0000}.exp"])

	t.name = "custom_dll_rvct_new_elf2e32"
	t.command = new_cmd.format("armv5")
	t.run()

	t.name = "custom_dll_rvct_old_elf2e32"
	t.command = old_cmd.format("armv5")
	t.run()

	t.name = "custom_dll_gcce_new_elf2e32"
	t.command = new_cmd.format("gcce_armv5")
	t.run()

	t.name = "custom_dll"
	return t

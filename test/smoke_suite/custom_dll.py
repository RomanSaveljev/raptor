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
	t.description = """Test the 'expgen' stage with different combinations of
				compiler (RVCT and GCC-E) and elf2e32 version (with and without
				--asm option)."""

	t.usebash = True

	bld_inf = "smoke_suite/test_resources/custom_dll/bld.inf"
	old_elf2e32 = "$(SBS_HOME)/test/smoke_suite/test_resources/custom_dll/elf2e32_old"
	if t.onWindows:
		old_elf2e32 += ".exe"

	# Command templates for using the new and the old version of elf2e32,
	# respectively. The new version supports the --asm option.
	new_cmd = "sbs -b " + bld_inf + " -c {0}"
	old_cmd = "SBS_ELF2E32=" + old_elf2e32 + " " + new_cmd

	t.targets = [
		"$(EPOCROOT)/epoc32/release/armv5/lib/customdll.dso",
		"$(EPOCROOT)/epoc32/release/armv5/lib/customdll{000a0000}.dso",
		"$(EPOCROOT)/epoc32/release/armv5/udeb/customdll.dll",
		"$(EPOCROOT)/epoc32/release/armv5/udeb/customdll.dll.map",
		"$(EPOCROOT)/epoc32/release/armv5/urel/customdll.dll",
		"$(EPOCROOT)/epoc32/release/armv5/urel/customdll.dll.map"
		]

	# This ensures that the "expgen" stage is executed for each call to run().
	t.addbuildtargets(bld_inf, [
		"customdll_dll/armv5/customdll{000a0000}.s",
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

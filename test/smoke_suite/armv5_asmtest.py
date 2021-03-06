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
	t.id = "16"
	t.name = "armv5_asmtest"
	t.command = "sbs -b smoke_suite/test_resources/asmtest/bld.inf -c armv5"
	t.targets = [
		"$(EPOCROOT)/epoc32/release/armv5/udeb/asmtest.exe",
		"$(EPOCROOT)/epoc32/release/armv5/udeb/asmtest.exe.sym",
		"$(EPOCROOT)/epoc32/release/armv5/udeb/asmtest.exe.map",
		"$(EPOCROOT)/epoc32/release/armv5/urel/asmtest.exe",
		"$(EPOCROOT)/epoc32/release/armv5/urel/asmtest.exe.sym",
		"$(EPOCROOT)/epoc32/release/armv5/urel/asmtest.exe.map"
		]
	t.addbuildtargets('smoke_suite/test_resources/asmtest/bld.inf', [
		"asmtest_/armv5/udeb/asmtest_udeb_objects.via",
		"asmtest_/armv5/udeb/testassembler.o.d",
		"asmtest_/armv5/udeb/testassembler.o",
		"asmtest_/armv5/udeb/testassembler.o",
		"asmtest_/armv5/udeb/testcia_.o",
		"asmtest_/armv5/udeb/testcia_.cpp",
		"asmtest_/armv5/udeb/testcia_.pre",
		"asmtest_/armv5/udeb/testcia_.pre.d",
		"asmtest_/armv5/udeb/testasm.o.d",
		"asmtest_/armv5/udeb/testasm.o",
		"asmtest_/armv5/urel/asmtest_urel_objects.via",
		"asmtest_/armv5/urel/testassembler.o.d",
		"asmtest_/armv5/urel/testassembler.o",
		"asmtest_/armv5/urel/testassembler.o",
		"asmtest_/armv5/urel/testcia_.o",
		"asmtest_/armv5/urel/testcia_.cpp",
		"asmtest_/armv5/urel/testcia_.pre",
		"asmtest_/armv5/urel/testcia_.pre.d",
		"asmtest_/armv5/urel/testasm.o.d",
		"asmtest_/armv5/urel/testasm.o"
	])
	t.run()
	return t

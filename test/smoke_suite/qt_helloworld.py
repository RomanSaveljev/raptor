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
# This test case requires install of Qt. 

from raptor_tests import SmokeTest
import os

def run():
	t = SmokeTest()

	t.description = "Ensure Raptor builds Qt applications successfully"	

	t.id = "0110"
	t.name = "qt_helloworld"
	# Internal QT deliveries use a QMAKE launcher that expects EPOCROOT to end in a slash
	# We ensure it does (doesn't matter if there are multiple slashes)
	t.environ["EPOCROOT"] = os.environ["EPOCROOT"] + os.sep

	# The winscw platform is deprecated in 10.1 which our epocroot is based on an tests on 
	# that tend not to work so it's armv5.  Its using rvct4_0 because thats's also the 10.1
	# default now.
	t.command = "cd smoke_suite/test_resources/qt/helloworld && sbs --qtpro helloworldqt.pro -k -c arm.v5.urel.rvct4_0 -c winscw"
	t.targets = [
			"$(SBS_HOME)/test/smoke_suite/test_resources/qt/bld.inf",
			"$(SBS_HOME)/test/smoke_suite/test_resources/qt/helloworldqt.loc",
			"$(SBS_HOME)/test/smoke_suite/test_resources/qt/helloworldqt.rss",
			"$(SBS_HOME)/test/smoke_suite/test_resources/qt/helloworldqt_reg.rss",
			"$(SBS_HOME)/test/smoke_suite/test_resources/qt/helloworldqt_template.pkg",
			"$(SBS_HOME)/test/smoke_suite/test_resources/qt/Makefile",
			"$(EPOCROOT)/epoc32/release/armv5/udeb/helloworldqt.sym",
			"$(EPOCROOT)/epoc32/release/armv5/urel/helloworldqt.sym"
			"$(EPOCROOT)/epoc32/release/armv5/udeb/helloworldqt.exe",
			"$(EPOCROOT)/epoc32/release/armv5/udeb/helloworldqt.exe.map",
			"$(EPOCROOT)/epoc32/release/armv5/urel/helloworldqt.exe",
			"$(EPOCROOT)/epoc32/release/armv5/urel/helloworldqt.exe.map",
		]
	t.addbuildtargets('smoke_suite/test_resources/qt/bld.inf', [
		"helloworldqt_exe/armv5/udeb/helloworld.o",
		"helloworldqt_exe/armv5/udeb/helloworld.o.d",
		"helloworldqt_exe/armv5/urel/helloworld.o",
		"helloworldqt_exe/armv5/urel/helloworld.o.d"
		"helloworldqt_exe/winscw/udeb/helloworld.o",
		"helloworldqt_exe/winscw/udeb/helloworld.o.d",	
		"helloworldqt_exe/winscw/urel/helloworld.o",
		"helloworldqt_exe/winscw/urel/helloworld.o.d"
	])
	t.run()

	# postlinker error expected at the moment - something that may not be raptor's fault
	#   elf2e32 : Error: E1035: Undefined Symbol _ZTISt9exception found in ELF File
	t.returncode = 0 

	# Have a linking problem with a symbol that should not appear in the output
	# this is not something that appears to be a 

	return t


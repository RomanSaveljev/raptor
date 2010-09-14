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

	# Its using rvct4_0 because thats's also the 10.1 default now.
	t.command = "sbs --qtpro smoke_suite/test_resources/qt/helloworld/helloworldqt.pro -k -c arm.v5.urel.rvct4_0 -c arm.v5.udeb.rvct4_0 -c winscw"
	t.targets = [
			"$(SBS_HOME)/test/smoke_suite/test_resources/qt/helloworld/bld.inf",
			"$(SBS_HOME)/test/smoke_suite/test_resources/qt/helloworld/helloworldqt.loc",
			"$(SBS_HOME)/test/smoke_suite/test_resources/qt/helloworld/helloworldqt.rss",
			"$(SBS_HOME)/test/smoke_suite/test_resources/qt/helloworld/helloworldqt_reg.rss",
			"$(SBS_HOME)/test/smoke_suite/test_resources/qt/helloworld/helloworldqt_template.pkg",
			"$(SBS_HOME)/test/smoke_suite/test_resources/qt/helloworld/Makefile",
			"$(EPOCROOT)/epoc32/release/armv5/udeb/helloworldqt.exe.sym",
			"$(EPOCROOT)/epoc32/release/armv5/urel/helloworldqt.exe.sym",
			"$(EPOCROOT)/epoc32/release/armv5/udeb/helloworldqt.exe",
			"$(EPOCROOT)/epoc32/release/armv5/udeb/helloworldqt.exe.map",
			"$(EPOCROOT)/epoc32/release/armv5/urel/helloworldqt.exe",
			"$(EPOCROOT)/epoc32/release/armv5/urel/helloworldqt.exe.map",
			"$(EPOCROOT)/epoc32/release/winscw/urel/helloworldqt.exe",
			"$(EPOCROOT)/epoc32/release/winscw/udeb/helloworldqt.exe"
		]
	t.addbuildtargets('smoke_suite/test_resources/qt/helloworld/bld.inf', [
		"helloworldqt_exe/helloworldqt_helloworldqt.rsc",
		"helloworldqt_exe/armv5/udeb/helloworld.o",
		"helloworldqt_exe/armv5/udeb/helloworld.o.d",
		"helloworldqt_exe/armv5/urel/helloworld.o",
		"helloworldqt_exe/armv5/urel/helloworld.o.d",
		"helloworldqt_exe/winscw/udeb/helloworld.o",
		"helloworldqt_exe/winscw/udeb/helloworld.o.d",	
		"helloworldqt_exe/winscw/urel/helloworld.o",
		"helloworldqt_exe/winscw/urel/helloworld.o.d"
	])
	t.run()

	return t


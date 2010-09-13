#
# Copyright (c) 2010 Nokia Corporation and/or its subsidiary(-ies).
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

	t.description = "Ensure Raptor builds Qt applications which use moc, uic and other tools"	

	t.id = "0110a"
	t.name = "qt_lotto"
	# Internal QT deliveries use a QMAKE launcher that expects EPOCROOT to end in a slash
	# We ensure it does (doesn't matter if there are multiple slashes)
	t.environ["EPOCROOT"] = os.environ["EPOCROOT"] + os.sep

	# Its using rvct4_0 because that's the 10.1 default.
	t.command = "cd smoke_suite/test_resources/qt/lotto && sbs --qtpro LottoNumberPicker.pro -k -c arm.v5.urel.rvct4_0 -c winscw"
	t.targets = [

			"$(EPOCROOT)/epoc32/data/z/private/10003a3f/import/apps/lottonumberpicker_reg.rsc",
			"$(EPOCROOT)/epoc32/data/z/resource/apps/lottonumberpicker.rsc",
			"$(EPOCROOT)/epoc32/include/lottonumberpicker.rsg",
			"$(EPOCROOT)/epoc32/release/armv5/urel/lottonumberpicker.exe",
			"$(EPOCROOT)/epoc32/release/armv5/urel/lottonumberpicker.exe.map",
			"$(EPOCROOT)/epoc32/release/winscw/udeb/lottonumberpicker.exe",
			"$(EPOCROOT)/epoc32/release/winscw/udeb/z/private/10003a3f/import/apps/lottonumberpicker_reg.rsc",
			"$(EPOCROOT)/epoc32/release/winscw/udeb/z/resource/apps/lottonumberpicker.rsc",
			"$(EPOCROOT)/epoc32/release/winscw/urel/lottonumberpicker.exe",
			"$(EPOCROOT)/epoc32/release/winscw/urel/lottonumberpicker.exe.map",
			"$(EPOCROOT)/epoc32/release/winscw/urel/z/private/10003a3f/import/apps/lottonumberpicker_reg.rsc",
			"$(EPOCROOT)/epoc32/release/winscw/urel/z/resource/apps/lottonumberpicker.rsc",
			"$(SBS_HOME)/test/smoke_suite/test_resources/qt/lotto/.make.cache",
			"$(SBS_HOME)/test/smoke_suite/test_resources/qt/lotto/LottoNumberPicker_0x20029F39.mmp",
			"$(SBS_HOME)/test/smoke_suite/test_resources/qt/lotto/Makefile",
			"$(SBS_HOME)/test/smoke_suite/test_resources/qt/lotto/bld.inf",
			"$(SBS_HOME)/test/smoke_suite/test_resources/qt/lotto/lottonumberpicker.loc",
			"$(SBS_HOME)/test/smoke_suite/test_resources/qt/lotto/lottonumberpicker.rss",
			"$(SBS_HOME)/test/smoke_suite/test_resources/qt/lotto/lottonumberpicker_installer.pkg",
			"$(SBS_HOME)/test/smoke_suite/test_resources/qt/lotto/lottonumberpicker_reg.rss",
			"$(SBS_HOME)/test/smoke_suite/test_resources/qt/lotto/lottonumberpicker_template.pkg",
			"$(SBS_HOME)/test/smoke_suite/test_resources/qt/lotto/moc_lottonumberpicker.cpp",
			"$(SBS_HOME)/test/smoke_suite/test_resources/qt/lotto/moc_lottonumberpicker.cpp",
			"$(SBS_HOME)/test/smoke_suite/test_resources/qt/lotto/ui_lottonumberpicker.h"
		]
	t.addbuildtargets('smoke_suite/test_resources/qt/lotto/bld.inf', [
			"lottonumberpicker_exe/armv5/urel/integerpair.o",
			"lottonumberpicker_exe/armv5/urel/integerpair.o.d",
			"lottonumberpicker_exe/armv5/urel/lottonumberpicker.o",
			"lottonumberpicker_exe/armv5/urel/lottonumberpicker.o.d",
			"lottonumberpicker_exe/armv5/urel/lottonumberpicker_urel_objects.via",
			"lottonumberpicker_exe/armv5/urel/main.o",
			"lottonumberpicker_exe/armv5/urel/main.o.d",
			"lottonumberpicker_exe/armv5/urel/moc_lottonumberpicker.o",
			"lottonumberpicker_exe/armv5/urel/moc_lottonumberpicker.o.d",
			"lottonumberpicker_exe/lottonumberpicker_lottonumberpicker.rsc",
			"lottonumberpicker_exe/lottonumberpicker_lottonumberpicker.rsc.d",
			"lottonumberpicker_exe/lottonumberpicker_lottonumberpicker.rsc.rpp",
			"lottonumberpicker_exe/winscw/udeb/integerpair.dep",
			"lottonumberpicker_exe/winscw/udeb/integerpair.o",
			"lottonumberpicker_exe/winscw/udeb/integerpair.o.d",
			"lottonumberpicker_exe/winscw/udeb/lottonumberpicker.UID.CPP",
			"lottonumberpicker_exe/winscw/udeb/lottonumberpicker.dep",
			"lottonumberpicker_exe/winscw/udeb/lottonumberpicker.o",
			"lottonumberpicker_exe/winscw/udeb/lottonumberpicker.o.d",
			"lottonumberpicker_exe/winscw/udeb/lottonumberpicker_UID_.dep",
			"lottonumberpicker_exe/winscw/udeb/lottonumberpicker_UID_.o",
			"lottonumberpicker_exe/winscw/udeb/lottonumberpicker_UID_.o.d",
			"lottonumberpicker_exe/winscw/udeb/main.dep",
			"lottonumberpicker_exe/winscw/udeb/main.o",
			"lottonumberpicker_exe/winscw/udeb/main.o.d",
			"lottonumberpicker_exe/winscw/udeb/moc_lottonumberpicker.dep",
			"lottonumberpicker_exe/winscw/udeb/moc_lottonumberpicker.o",
			"lottonumberpicker_exe/winscw/udeb/moc_lottonumberpicker.o.d",
			"lottonumberpicker_exe/winscw/urel/integerpair.dep",
			"lottonumberpicker_exe/winscw/urel/integerpair.o",
			"lottonumberpicker_exe/winscw/urel/integerpair.o.d",
			"lottonumberpicker_exe/winscw/urel/lottonumberpicker.UID.CPP",
			"lottonumberpicker_exe/winscw/urel/lottonumberpicker.dep",
			"lottonumberpicker_exe/winscw/urel/lottonumberpicker.o",
			"lottonumberpicker_exe/winscw/urel/lottonumberpicker.o.d",
			"lottonumberpicker_exe/winscw/urel/lottonumberpicker_UID_.dep",
			"lottonumberpicker_exe/winscw/urel/lottonumberpicker_UID_.o",
			"lottonumberpicker_exe/winscw/urel/lottonumberpicker_UID_.o.d",
			"lottonumberpicker_exe/winscw/urel/main.dep",
			"lottonumberpicker_exe/winscw/urel/main.o",
			"lottonumberpicker_exe/winscw/urel/main.o.d",
			"lottonumberpicker_exe/winscw/urel/moc_lottonumberpicker.dep",
			"lottonumberpicker_exe/winscw/urel/moc_lottonumberpicker.o",
			"lottonumberpicker_exe/winscw/urel/moc_lottonumberpicker.o.d",
			"lottonumberpicker_reg_exe/lottonumberpicker_reg_lottonumberpicker_reg.rsc",
			"lottonumberpicker_reg_exe/lottonumberpicker_reg_lottonumberpicker_reg.rsc.d",
			"lottonumberpicker_reg_exe/lottonumberpicker_reg_lottonumberpicker_reg.rsc.rpp"
	])
	t.run()

	return t


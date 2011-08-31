#
# Copyright (c) 2011 Nokia Corporation and/or its subsidiary(-ies).
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
import os

def run():
	t = SmokeTest()
	t.description = "Test the build and package of Raptor built applications using the createsis FLM"

	t.name = "native_package_vanilla"
	t.command = "sbs -b $(SBS_HOME)/test/smoke_suite/test_resources/simple_gui/build_and_package.inf -c armv5 -c winscw"
	t.targets = [
		"$(EPOCROOT)/epoc32/data/z/resource/apps/helloworld.mbm",
		"$(EPOCROOT)/epoc32/release/winscw/udeb/z/resource/apps/helloworld.mbm",
		"$(EPOCROOT)/epoc32/release/winscw/urel/z/resource/apps/helloworld.mbm",
		"$(EPOCROOT)/epoc32/include/HelloWorld.rsg",
		"$(EPOCROOT)/epoc32/data/z/resource/apps/HelloWorld.rsc",
		"$(EPOCROOT)/epoc32/release/winscw/udeb/z/resource/apps/HelloWorld.rsc",
		"$(EPOCROOT)/epoc32/release/winscw/urel/z/resource/apps/HelloWorld.rsc",
		"$(EPOCROOT)/epoc32/release/armv5/udeb/helloworld.exe",
		"$(EPOCROOT)/epoc32/release/armv5/udeb/helloworld.exe.map",
		"$(EPOCROOT)/epoc32/release/winscw/udeb/helloworld.exe",
		"$(EPOCROOT)/epoc32/release/armv5/urel/helloworld.exe",
		"$(EPOCROOT)/epoc32/release/armv5/urel/helloworld.exe.map",
		"$(EPOCROOT)/epoc32/release/winscw/urel/helloworld.exe",
		"$(EPOCROOT)/epoc32/release/winscw/urel/helloworld.exe.map",
		"$(SBS_HOME)/test/smoke_suite/test_resources/simple_gui/sis/helloworld_armv5.sis",
		"$(SBS_HOME)/test/smoke_suite/test_resources/simple_gui/sis/helloworld_armv5_debug.sis",
		"$(SBS_HOME)/test/smoke_suite/test_resources/simple_gui/sis/helloworld_winscw.sis",
		"$(SBS_HOME)/test/smoke_suite/test_resources/simple_gui/sis/helloworld_winscw_debug.sis",
		"$(EPOCROOT)/epoc32/data/z/system/install/helloworld_stub.sis",
		"$(EPOCROOT)/epoc32/release/winscw/urel/z/system/install/helloworld_stub.sis"
		]
	t.addbuildtargets('smoke_suite/test_resources/simple_gui/build_and_package.inf', [
		"helloworld_exe/helloworld.mbm_bmconvcommands",
		"HelloWorld_exe/HelloWorld_HelloWorld.rsc.rpp",
		"HelloWorld_exe/HelloWorld_HelloWorld.rsc.d",
		"helloworld_exe/armv5/udeb/HelloWorld_Application.o",
		"helloworld_exe/armv5/udeb/HelloWorld_Application.o.d",
		"helloworld_exe/armv5/udeb/HelloWorld_AppUi.o",
		"helloworld_exe/armv5/udeb/HelloWorld_AppUi.o.d",
		"helloworld_exe/armv5/udeb/HelloWorld_AppView.o",
		"helloworld_exe/armv5/udeb/HelloWorld_AppView.o.d",
		"helloworld_exe/armv5/udeb/HelloWorld_Document.o",
		"helloworld_exe/armv5/udeb/HelloWorld_Document.o.d",
		"helloworld_exe/armv5/udeb/HelloWorld_Main.o",
		"helloworld_exe/armv5/udeb/HelloWorld_Main.o.d",
		"helloworld_exe/armv5/udeb/helloworld_udeb_objects.via",
		"helloworld_exe/armv5/urel/HelloWorld_Application.o",
		"helloworld_exe/armv5/urel/HelloWorld_Application.o.d",
		"helloworld_exe/armv5/urel/HelloWorld_AppUi.o",
		"helloworld_exe/armv5/urel/HelloWorld_AppUi.o.d",
		"helloworld_exe/armv5/urel/HelloWorld_AppView.o",
		"helloworld_exe/armv5/urel/HelloWorld_AppView.o.d",
		"helloworld_exe/armv5/urel/HelloWorld_Document.o",
		"helloworld_exe/armv5/urel/HelloWorld_Document.o.d",
		"helloworld_exe/armv5/urel/HelloWorld_Main.o",
		"helloworld_exe/armv5/urel/HelloWorld_Main.o.d",
		"helloworld_exe/armv5/urel/helloworld_urel_objects.via",
		"helloworld_exe/winscw/udeb/helloworld.UID.CPP",
		"helloworld_exe/winscw/udeb/HelloWorld_Application.dep",
		"helloworld_exe/winscw/udeb/HelloWorld_Application.o",
		"helloworld_exe/winscw/udeb/HelloWorld_Application.o.d",
		"helloworld_exe/winscw/udeb/HelloWorld_AppUi.dep",
		"helloworld_exe/winscw/udeb/HelloWorld_AppUi.o",
		"helloworld_exe/winscw/udeb/HelloWorld_AppUi.o.d",
		"helloworld_exe/winscw/udeb/HelloWorld_AppView.dep",
		"helloworld_exe/winscw/udeb/HelloWorld_AppView.o",
		"helloworld_exe/winscw/udeb/HelloWorld_AppView.o.d",
		"helloworld_exe/winscw/udeb/HelloWorld_Document.dep",
		"helloworld_exe/winscw/udeb/HelloWorld_Document.o",
		"helloworld_exe/winscw/udeb/HelloWorld_Document.o.d",
		"helloworld_exe/winscw/udeb/HelloWorld_Main.dep",
		"helloworld_exe/winscw/udeb/HelloWorld_Main.o",
		"helloworld_exe/winscw/udeb/HelloWorld_Main.o.d",
		"helloworld_exe/winscw/udeb/helloworld_UID_.dep",
		"helloworld_exe/winscw/udeb/helloworld_UID_.o",
		"helloworld_exe/winscw/udeb/helloworld_UID_.o.d",
		"helloworld_exe/winscw/urel/helloworld.UID.CPP",
		"helloworld_exe/winscw/urel/HelloWorld_Application.dep",
		"helloworld_exe/winscw/urel/HelloWorld_Application.o",
		"helloworld_exe/winscw/urel/HelloWorld_Application.o.d",
		"helloworld_exe/winscw/urel/HelloWorld_AppUi.dep",
		"helloworld_exe/winscw/urel/HelloWorld_AppUi.o",
		"helloworld_exe/winscw/urel/HelloWorld_AppUi.o.d",
		"helloworld_exe/winscw/urel/HelloWorld_AppView.dep",
		"helloworld_exe/winscw/urel/HelloWorld_AppView.o",
		"helloworld_exe/winscw/urel/HelloWorld_AppView.o.d",
		"helloworld_exe/winscw/urel/HelloWorld_Document.dep",
		"helloworld_exe/winscw/urel/HelloWorld_Document.o",
		"helloworld_exe/winscw/urel/HelloWorld_Document.o.d",
		"helloworld_exe/winscw/urel/HelloWorld_Main.dep",
		"helloworld_exe/winscw/urel/HelloWorld_Main.o",
		"helloworld_exe/winscw/urel/HelloWorld_Main.o.d",
		"helloworld_exe/winscw/urel/helloworld_UID_.dep",
		"helloworld_exe/winscw/urel/helloworld_UID_.o",
		"helloworld_exe/winscw/urel/helloworld_UID_.o.d",
		"HelloWorld_reg_exe/HelloWorld_reg_HelloWorld_reg.rsc.d",
		"helloworld_armv5_debug_sis/armv5/udeb/armv5_udeb.pkg",
		"helloworld_armv5_debug_sis/armv5/udeb/helloworld_armv5_debug.sis",
		"helloworld_armv5_sis/armv5/urel/armv5_urel.pkg",
		"helloworld_armv5_sis/armv5/urel/helloworld_armv5.sis",
		"helloworld_winscw_debug_sis/winscw/udeb/winscw_udeb.pkg",
		"helloworld_winscw_debug_sis/winscw/udeb/helloworld_winscw_debug.sis",
		"helloworld_winscw_sis/winscw/urel/winscw_urel.pkg",
		"helloworld_winscw_sis/winscw/urel/helloworld_winscw.sis",
		"helloworld_stub_sis/armv5/urel/stub.pkg",
		"helloworld_stub_sis/armv5/urel/helloworld_stub.sis",
		"helloworld_stub_sis/winscw/urel/stub.pkg",
		"helloworld_stub_sis/winscw/urel/helloworld_stub.sis"
	])
	t.run()
	
	# back-up the targets to clean later - we want them as input for the next
	# test without having to re-build the component
	built_targets = t.targets[:]
	
	t.name = "native_package_custom"
	t.targets = [
		"$(EPOCROOT)/epoc32/packaging/helloworld/helloworld_winscw_custom.sis",
		"$(EPOCROOT)/epoc32/packaging/helloworld/helloworld_armv5_custom.sis"
		]
	t.command = "sbs -b $(SBS_HOME)/test/smoke_suite/test_resources/simple_gui/custom_package.inf -c armv5 -c winscw"
	t.run()
	
	t.targets.extend(built_targets)
	t.clean()

	qmake_call = "$(EPOCROOT)/epoc32/tools/qt/qmake{ext} " + \
		"-spec $(EPOCROOT)/epoc32/tools/qt/mkspecs/symbian-sbsv2 " + \
		"QMAKE_INCDIR_QT=$(EPOCROOT)/epoc32/include/mw " + \
		"QMAKE_MOC=$(EPOCROOT)/epoc32/tools/moc{ext} " + \
		"QMAKE_UIC=$(EPOCROOT)/epoc32/tools/uic{ext} " + \
		"QMAKE_RCC=$(EPOCROOT)/epoc32/tools/rcc{ext} " + \
		"smoke_suite/test_resources/qt/lotto/LottoNumberPicker.pro " + \
		"-o $(SBS_HOME)/test/smoke_suite/test_resources/qt/lotto/bld.inf"
	raptor_call = "sbs -b $(SBS_HOME)/test/smoke_suite/test_resources/qt/lotto/bld.inf -c arm.v5.urel.rvct4_0 -c winscw_urel"	
	patch_bldinf= """cat <<__ENDOFPATCH__ >> $(SBS_HOME)/test/smoke_suite/test_resources/qt/lotto/bld.inf
	
START EXTENSION utility.createsis
OPTION PKG_FILE lottonumberpicker_template.pkg
#ifdef WINSCW
OPTION SIS_FILE lottonumberpicker_winscw.sis
#else
OPTION SIS_FILE lottonumberpicker_armv5.sis
#endif
OPTION TARGET_FILE lottonumberpicker.exe
OPTION BUILD_TYPE urel
END
__ENDOFPATCH__

"""
	tool_ext = ""
	if t.onWindows:
		tool_ext = ".exe"
	
	t.name= "qt_package"
	t.usebash = True
	t.command = "{qmake} && {patch} {raptor}".format(qmake=qmake_call.format(ext=tool_ext), patch=patch_bldinf, raptor=raptor_call)
	t.targets = [
		"$(EPOCROOT)/epoc32/data/z/private/10003a3f/import/apps/lottonumberpicker_reg.rsc",
		"$(EPOCROOT)/epoc32/data/z/resource/apps/lottonumberpicker.rsc",
		"$(EPOCROOT)/epoc32/include/lottonumberpicker.rsg",
		"$(EPOCROOT)/epoc32/release/armv5/urel/lottonumberpicker.exe",
		"$(EPOCROOT)/epoc32/release/armv5/urel/lottonumberpicker.exe.map",
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
		"$(SBS_HOME)/test/smoke_suite/test_resources/qt/lotto/ui_lottonumberpicker.h",
		"$(SBS_HOME)/test/smoke_suite/test_resources/qt/lotto/lottonumberpicker_armv5.sis",
		"$(SBS_HOME)/test/smoke_suite/test_resources/qt/lotto/lottonumberpicker_winscw.sis",			
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
		"lottonumberpicker_reg_exe/lottonumberpicker_reg_lottonumberpicker_reg.rsc.rpp",
		"lottonumberpicker_armv5_sis/armv5/urel/lottonumberpicker_template.pkg",
		"lottonumberpicker_armv5_sis/armv5/urel/lottonumberpicker_armv5.sis",
		"lottonumberpicker_winscw_sis/winscw/urel/lottonumberpicker_template.pkg",
		"lottonumberpicker_winscw_sis/winscw/urel/lottonumberpicker_winscw.sis"
	])	
	t.run()
	t.clean()
	
	t.name="packaging"
	t.print_result()
	return t

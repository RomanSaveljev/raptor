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

	# Unordered layer logging tests
	unorderedcommand = 'sbs -f- -s smoke_suite/test_resources/sysdef/system_definition_simple.xml'
	unorderedtargets = [
		"$(EPOCROOT)/epoc32/release/armv5/udeb/simple1.exe",
		"$(EPOCROOT)/epoc32/release/armv5/udeb/simple1.exe.sym",
		"$(EPOCROOT)/epoc32/release/armv5/udeb/simple1.exe.map",
		"$(EPOCROOT)/epoc32/release/armv5/urel/simple1.exe",
		"$(EPOCROOT)/epoc32/release/armv5/urel/simple1.exe.sym",
		"$(EPOCROOT)/epoc32/release/armv5/urel/simple1.exe.map",
		"$(EPOCROOT)/epoc32/release/winscw/udeb/simple1.exe",
		"$(EPOCROOT)/epoc32/release/winscw/urel/simple1.exe",
		"$(EPOCROOT)/epoc32/release/winscw/urel/simple1.exe.map",
		"$(EPOCROOT)/epoc32/release/armv5/udeb/simple2.exe",
		"$(EPOCROOT)/epoc32/release/armv5/udeb/simple2.exe.sym",
		"$(EPOCROOT)/epoc32/release/armv5/udeb/simple2.exe.map",
		"$(EPOCROOT)/epoc32/release/armv5/urel/simple2.exe",
		"$(EPOCROOT)/epoc32/release/armv5/urel/simple2.exe.sym",
		"$(EPOCROOT)/epoc32/release/armv5/urel/simple2.exe.map",
		"$(EPOCROOT)/epoc32/release/winscw/udeb/simple2.exe",
		"$(EPOCROOT)/epoc32/release/winscw/urel/simple2.exe",
		"$(EPOCROOT)/epoc32/release/winscw/urel/simple2.exe.map",
		"$(EPOCROOT)/epoc32/release/armv5/udeb/simple3.exe",
		"$(EPOCROOT)/epoc32/release/armv5/udeb/simple3.exe.sym",
		"$(EPOCROOT)/epoc32/release/armv5/udeb/simple3.exe.map",
		"$(EPOCROOT)/epoc32/release/armv5/urel/simple3.exe",
		"$(EPOCROOT)/epoc32/release/armv5/urel/simple3.exe.sym",
		"$(EPOCROOT)/epoc32/release/armv5/urel/simple3.exe.map",
		"$(EPOCROOT)/epoc32/release/winscw/udeb/simple3.exe",
		"$(EPOCROOT)/epoc32/release/winscw/urel/simple3.exe",
		"$(EPOCROOT)/epoc32/release/winscw/urel/simple3.exe.map",
		"$(EPOCROOT)/epoc32/release/armv5/udeb/simple4.exe",
		"$(EPOCROOT)/epoc32/release/armv5/udeb/simple4.exe.sym",
		"$(EPOCROOT)/epoc32/release/armv5/udeb/simple4.exe.map",
		"$(EPOCROOT)/epoc32/release/armv5/urel/simple4.exe",
		"$(EPOCROOT)/epoc32/release/armv5/urel/simple4.exe.sym",
		"$(EPOCROOT)/epoc32/release/armv5/urel/simple4.exe.map",
		"$(EPOCROOT)/epoc32/release/winscw/udeb/simple4.exe",
		"$(EPOCROOT)/epoc32/release/winscw/urel/simple4.exe",
		"$(EPOCROOT)/epoc32/release/winscw/urel/simple4.exe.map"
		]

	t.name = "sysdef_layers"
	t.description = "Test system definition building and layer logging"
	t.command = unorderedcommand
	t.targets = unorderedtargets
	t.countmatch = [
		["<recipe .*layer='layer1' .*>", 24],
		["<recipe .*layer='layer2' .*>", 24]
		]
	t.run()

	# Clean the previous run
	t.name = "sysdef_layers_clean"
	t.description = "Clean the previous run"
	t.command = unorderedcommand + " REALLYCLEAN"
	t.targets = []
	t.countmatch = []
	t.run()

	# System definition layer test with PP on
	t.name = "sysdef_layers_pp"
	t.description = "Test system definition layer building and logging with parallel processing on"
	t.command = unorderedcommand + " --pp on"
	t.targets = unorderedtargets
	t.countmatch = [
		["<recipe .*layer='layer1' .*>", 24],
		["<recipe .*layer='layer2' .*>", 24]
		]
	t.run()

	# Ordered layer building and logging tests
	orderedcommand = 'sbs -f- -s smoke_suite/test_resources/sysdef/system_definition_order_layer_test.xml ' + \
			'-l "Metadata Export" -l "Build Generated Source" -l "Component with Layer Dependencies" -o'

	t.name = "sysdef_layers_ordered"
	t.description = "Test system definition ordered layer building and logging"
	t.command = orderedcommand
	t.targets = [
		"$(SBS_HOME)/test/smoke_suite/test_resources/sysdef/build_gen_source/exported.inf",
		"$(SBS_HOME)/test/smoke_suite/test_resources/sysdef/build_gen_source/exported.mmh",
		"$(EPOCROOT)/epoc32/data/z/resource/apps/helloworld.mbm",
		"$(EPOCROOT)/epoc32/data/z/private/10003a3f/apps/HelloWorld_reg.rsc",
		"$(EPOCROOT)/epoc32/data/z/resource/apps/HelloWorld.rsc",
		"$(EPOCROOT)/epoc32/include/HelloWorld.rsg",
		"$(EPOCROOT)/epoc32/release/armv5/udeb/helloworld.exe",
		"$(EPOCROOT)/epoc32/release/armv5/udeb/helloworld.exe.sym",
		"$(EPOCROOT)/epoc32/release/armv5/udeb/helloworld.exe.map",
		"$(EPOCROOT)/epoc32/release/armv5/urel/helloworld.exe",
		"$(EPOCROOT)/epoc32/release/armv5/urel/helloworld.exe.sym",
		"$(EPOCROOT)/epoc32/release/armv5/urel/helloworld.exe.map",
		"$(EPOCROOT)/epoc32/release/winscw/udeb/z/resource/apps/helloworld.mbm",
		"$(EPOCROOT)/epoc32/release/winscw/udeb/helloworld.exe",
		"$(EPOCROOT)/epoc32/release/winscw/udeb/z/private/10003a3f/apps/HelloWorld_reg.rsc",
		"$(EPOCROOT)/epoc32/release/winscw/udeb/z/resource/apps/HelloWorld.rsc",
		"$(EPOCROOT)/epoc32/release/winscw/urel/z/resource/apps/helloworld.mbm",
		"$(EPOCROOT)/epoc32/release/winscw/urel/helloworld.exe",
		"$(EPOCROOT)/epoc32/release/winscw/urel/helloworld.exe.map",
		"$(EPOCROOT)/epoc32/release/winscw/urel/z/private/10003a3f/apps/HelloWorld_reg.rsc",
		"$(EPOCROOT)/epoc32/release/winscw/urel/z/resource/apps/HelloWorld.rsc",
		]
	t.addbuildtargets('smoke_suite/test_resources/sysdef/build_gen_source/bld.inf', [
		"HelloWorld_/HelloWorld_HelloWorld.rsc.rpp",
		"HelloWorld_/HelloWorld_HelloWorld.rsc",
		"HelloWorld_/HelloWorld_HelloWorld.rsc.d"
		])
	t.addbuildtargets('smoke_suite/test_resources/sysdef/dependent/bld.inf', [
		"helloworld_exe/armv5/udeb/HelloWorld_Application.o",
		"helloworld_exe/armv5/udeb/HelloWorld_AppUi.o",
		"helloworld_exe/armv5/udeb/HelloWorld_AppView.o",
		"helloworld_exe/armv5/udeb/HelloWorld_Document.o",
		"helloworld_exe/armv5/udeb/HelloWorld_Main.o",
		"helloworld_exe/armv5/urel/HelloWorld_Application.o",
		"helloworld_exe/armv5/urel/HelloWorld_AppUi.o",
		"helloworld_exe/armv5/urel/HelloWorld_AppView.o",
		"helloworld_exe/armv5/urel/HelloWorld_Document.o",
		"helloworld_exe/armv5/urel/HelloWorld_Main.o",
		"helloworld_exe/winscw/udeb/HelloWorld_Application.o",
		"helloworld_exe/winscw/udeb/HelloWorld_AppUi.o",
		"helloworld_exe/winscw/udeb/HelloWorld_AppView.o",
		"helloworld_exe/winscw/udeb/HelloWorld_Document.o",
		"helloworld_exe/winscw/udeb/HelloWorld_Main.o",
		"helloworld_exe/winscw/udeb/helloworld.UID.CPP",
		"helloworld_exe/winscw/udeb/helloworld_UID_.o",
		"helloworld_exe/winscw/urel/HelloWorld_Application.o",
		"helloworld_exe/winscw/urel/HelloWorld_AppUi.o",
		"helloworld_exe/winscw/urel/HelloWorld_AppView.o",
		"helloworld_exe/winscw/urel/HelloWorld_Document.o",
		"helloworld_exe/winscw/urel/HelloWorld_Main.o",
		"helloworld_exe/winscw/urel/helloworld.UID.CPP",
		"helloworld_exe/winscw/urel/helloworld_UID_.o",
		"HelloWorld_reg_exe/HelloWorld_reg_HelloWorld_reg.rsc.rpp",
		"HelloWorld_reg_exe/HelloWorld_reg_HelloWorld_reg.rsc.d"
		])
	t.countmatch = [
		["<recipe .*layer='Component with Layer Dependencies' component='dependent'.*>", 33],
		["<recipe .*layer='Build Generated Source' component='build generated source'.*>", 3]		
		]
	t.run()

	t.name = "sysdef_layers_ordered_pp"
	t.description = "Test system definition ordered layer building and logging with parallel processing on"
	t.command = orderedcommand + " --pp on"
	t.run()

	# package definition building and logging tests
	packagecommand = 'sbs -f- -s smoke_suite/test_resources/sysdef/package_definition.xml'
	packagetargets = [
		"$(EPOCROOT)/epoc32/release/armv5/udeb/simple1.exe",
		"$(EPOCROOT)/epoc32/release/armv5/udeb/simple1.exe.map",
		"$(EPOCROOT)/epoc32/release/armv5/udeb/simple2.exe",
		"$(EPOCROOT)/epoc32/release/armv5/udeb/simple2.exe.map",
		"$(EPOCROOT)/epoc32/release/armv5/udeb/simple3.exe",
		"$(EPOCROOT)/epoc32/release/armv5/udeb/simple3.exe.map",
		"$(EPOCROOT)/epoc32/release/armv5/udeb/simple4.exe",
		"$(EPOCROOT)/epoc32/release/armv5/udeb/simple4.exe.map",
		"$(EPOCROOT)/epoc32/release/armv5/urel/simple1.exe",
		"$(EPOCROOT)/epoc32/release/armv5/urel/simple1.exe.map",
		"$(EPOCROOT)/epoc32/release/armv5/urel/simple2.exe",
		"$(EPOCROOT)/epoc32/release/armv5/urel/simple2.exe.map",
		"$(EPOCROOT)/epoc32/release/armv5/urel/simple3.exe",
		"$(EPOCROOT)/epoc32/release/armv5/urel/simple3.exe.map",
		"$(EPOCROOT)/epoc32/release/armv5/urel/simple4.exe",
		"$(EPOCROOT)/epoc32/release/armv5/urel/simple4.exe.map",
		"$(EPOCROOT)/epoc32/release/winscw/udeb/simple1.exe",
		"$(EPOCROOT)/epoc32/release/winscw/udeb/simple2.exe",
		"$(EPOCROOT)/epoc32/release/winscw/udeb/simple3.exe",
		"$(EPOCROOT)/epoc32/release/winscw/udeb/simple4.exe",
		"$(EPOCROOT)/epoc32/release/winscw/urel/simple1.exe",
		"$(EPOCROOT)/epoc32/release/winscw/urel/simple1.exe.map",
		"$(EPOCROOT)/epoc32/release/winscw/urel/simple2.exe",
		"$(EPOCROOT)/epoc32/release/winscw/urel/simple2.exe.map",
		"$(EPOCROOT)/epoc32/release/winscw/urel/simple3.exe",
		"$(EPOCROOT)/epoc32/release/winscw/urel/simple3.exe.map",
		"$(EPOCROOT)/epoc32/release/winscw/urel/simple4.exe",
		"$(EPOCROOT)/epoc32/release/winscw/urel/simple4.exe.map"
		]

	t.name = "sysdef_layers_pkgdef_clean_1"
	t.description = "Clean for testing package definition building and layer logging"
	t.command = packagecommand + " reallyclean"
	t.targets = []
	t.countmatch = []
	t.run()

	t.name = "sysdef_layers_pkgdef"
	t.description = "Test package definition building and layer logging"
	t.command = packagecommand
	t.targets = packagetargets
	t.countmatch = [
		["<recipe .*layer='package1' .*>", 24],
		["<recipe .*layer='package2' .*>", 24]
		]
	t.run()

	t.name = "sysdef_layers_pkgdef_clean_2"
	t.description = "Clean for testing package definition building and layer logging"
	t.command = packagecommand + " reallyclean"
	t.targets = []
	t.countmatch = []
	t.run()

	t.name = "sysdef_layers_pkgdef_pp"
	t.description = "Test package definition building and layer logging with parallel processing on"
	t.command = packagecommand + " --pp on"
	t.targets = packagetargets
	t.run()

	t.id = "48"
	t.name = "sysdef_layers"
	return t

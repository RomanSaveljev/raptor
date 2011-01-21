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
#

from raptor_tests import SmokeTest

def run():
	t = SmokeTest()
	t.name = "preprocess"
	t.usebash = True
	t.description = "Exercise the global PREPROCESS target"
	
	# Build component normally first for one config - resource generate  .rsg files are #included in "straight" source
	# The PREPROCESS target does not resolve resource dependencies, but the test component is selected on the basis
	# that it will support the generation of resource .pre files in the future.

	addConfigs = ""
	addTargets = []
	if t.onWindows:
		addConfigs = "-c x86_udeb"
		addTargets = [
			"$(SBS_HOME)/test/smoke_suite/test_resources/simple_gui/HelloWorld_Application.cpp.x86.udeb.helloworld.exe.pre",
			"$(SBS_HOME)/test/smoke_suite/test_resources/simple_gui/HelloWorld_AppUi.cpp.x86.udeb.helloworld.exe.pre",
			"$(SBS_HOME)/test/smoke_suite/test_resources/simple_gui/HelloWorld_AppView.cpp.x86.udeb.helloworld.exe.pre",
			"$(SBS_HOME)/test/smoke_suite/test_resources/simple_gui/HelloWorld_Document.cpp.x86.udeb.helloworld.exe.pre",
			"$(SBS_HOME)/test/smoke_suite/test_resources/simple_gui/HelloWorld_Main.cpp.x86.udeb.helloworld.exe.pre"
			]

	t.command = """
		sbs -b smoke_suite/test_resources/simple_gui/Bld.inf -c armv5_urel &&
		sbs -b smoke_suite/test_resources/simple_gui/Bld.inf -c armv5 -c winscw_urel -c armv7_udeb -c arm.v7.urel.gcce4_4_1 {0} preprocess
		""".format(addConfigs)
	
	t.targets = [
		"$(SBS_HOME)/test/smoke_suite/test_resources/simple_gui/HelloWorld_Application.cpp.armv5.udeb.helloworld.exe.pre",
		"$(SBS_HOME)/test/smoke_suite/test_resources/simple_gui/HelloWorld_Application.cpp.armv5.urel.helloworld.exe.pre",
		"$(SBS_HOME)/test/smoke_suite/test_resources/simple_gui/HelloWorld_AppUi.cpp.armv5.udeb.helloworld.exe.pre",
		"$(SBS_HOME)/test/smoke_suite/test_resources/simple_gui/HelloWorld_AppUi.cpp.armv5.urel.helloworld.exe.pre",
		"$(SBS_HOME)/test/smoke_suite/test_resources/simple_gui/HelloWorld_AppView.cpp.armv5.udeb.helloworld.exe.pre",
		"$(SBS_HOME)/test/smoke_suite/test_resources/simple_gui/HelloWorld_AppView.cpp.armv5.urel.helloworld.exe.pre",
		"$(SBS_HOME)/test/smoke_suite/test_resources/simple_gui/HelloWorld_Document.cpp.armv5.udeb.helloworld.exe.pre",
		"$(SBS_HOME)/test/smoke_suite/test_resources/simple_gui/HelloWorld_Document.cpp.armv5.urel.helloworld.exe.pre",
		"$(SBS_HOME)/test/smoke_suite/test_resources/simple_gui/HelloWorld_Main.cpp.armv5.udeb.helloworld.exe.pre",
		"$(SBS_HOME)/test/smoke_suite/test_resources/simple_gui/HelloWorld_Main.cpp.armv5.urel.helloworld.exe.pre",
		"$(SBS_HOME)/test/smoke_suite/test_resources/simple_gui/HelloWorld_Application.cpp.winscw.urel.helloworld.exe.pre",
		"$(SBS_HOME)/test/smoke_suite/test_resources/simple_gui/HelloWorld_AppUi.cpp.winscw.urel.helloworld.exe.pre",
		"$(SBS_HOME)/test/smoke_suite/test_resources/simple_gui/HelloWorld_AppView.cpp.winscw.urel.helloworld.exe.pre",
		"$(SBS_HOME)/test/smoke_suite/test_resources/simple_gui/HelloWorld_Document.cpp.winscw.urel.helloworld.exe.pre",
		"$(SBS_HOME)/test/smoke_suite/test_resources/simple_gui/HelloWorld_Main.cpp.winscw.urel.helloworld.exe.pre",
		"$(SBS_HOME)/test/smoke_suite/test_resources/simple_gui/HelloWorld_Application.cpp.armv7.udeb.helloworld.exe.pre",
		"$(SBS_HOME)/test/smoke_suite/test_resources/simple_gui/HelloWorld_AppUi.cpp.armv7.udeb.helloworld.exe.pre",
		"$(SBS_HOME)/test/smoke_suite/test_resources/simple_gui/HelloWorld_AppView.cpp.armv7.udeb.helloworld.exe.pre",
		"$(SBS_HOME)/test/smoke_suite/test_resources/simple_gui/HelloWorld_Document.cpp.armv7.udeb.helloworld.exe.pre",
		"$(SBS_HOME)/test/smoke_suite/test_resources/simple_gui/HelloWorld_Main.cpp.armv7.udeb.helloworld.exe.pre",		
		"$(SBS_HOME)/test/smoke_suite/test_resources/simple_gui/HelloWorld_Application.cpp.armv7.urel.helloworld.exe.pre",
		"$(SBS_HOME)/test/smoke_suite/test_resources/simple_gui/HelloWorld_AppUi.cpp.armv7.urel.helloworld.exe.pre",
		"$(SBS_HOME)/test/smoke_suite/test_resources/simple_gui/HelloWorld_AppView.cpp.armv7.urel.helloworld.exe.pre",
		"$(SBS_HOME)/test/smoke_suite/test_resources/simple_gui/HelloWorld_Document.cpp.armv7.urel.helloworld.exe.pre",
		"$(SBS_HOME)/test/smoke_suite/test_resources/simple_gui/HelloWorld_Main.cpp.armv7.urel.helloworld.exe.pre"
		] + addTargets

	t.run()
	
	# Explicit clean-up due to the source tree nature of the generated files
	t.clean()
	return t

#
# Copyright (c) 2011-2014 Microsoft Mobile and/or its subsidiary(-ies).
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
	t.usebash = True
	result = SmokeTest.PASS

	description = "Validates the --no-metadata-depend option"

	base_command = "sbs -b smoke_suite/test_resources/simple/bld.inf"

	targets = [
		"$(EPOCROOT)/epoc32/release/armv5/urel/test.exe",
		"$(EPOCROOT)/epoc32/release/armv5/urel/test.exe.map",
		"$(EPOCROOT)/epoc32/release/armv5/urel/test.exe.sym",
		]

	buildtargets = [
		"test_/armv5/urel/test.o",
		"test_/armv5/urel/test.o.d",
		"test_/armv5/urel/test3.o.d",
		"test_/armv5/urel/test4.o.d",
		"test_/armv5/urel/test5.o.d",
		"test_/armv5/urel/test1.o.d",
		"test_/armv5/urel/test6.o.d",
		"test_/armv5/urel/test2.o.d",
		"test_/armv5/urel/test3.o",
		"test_/armv5/urel/test4.o",
		"test_/armv5/urel/test5.o",
		"test_/armv5/urel/test1.o",
		"test_/armv5/urel/test6.o",
		"test_/armv5/urel/test2.o",
		"test_/armv5/urel/test_.o",
		"test_/armv5/urel/test_urel_objects.via"
		]

	mustmatch = [
	]
	
	# Initial build of simple.exe to get all the files in place
	t.name = "initial_build"
	t.description = "Initial build"
	t.command = "{0} -c arm.v5.urel.gcce4_4_1".format(base_command)
	t.targets = targets
	t.addbuildtargets("smoke_suite/test_resources/simple/bld.inf", buildtargets)
	t.mustmatch = [	"compile.*smoke_suite.test_resources.simple.test.cpp.*\[arm.v5.urel.gcce4_4_1\]",
					"compile.*smoke_suite.test_resources.simple.test.cia.*\[arm.v5.urel.gcce4_4_1\]",
					"compile.*smoke_suite.test_resources.simple.test1.c\+\+.*\[arm.v5.urel.gcce4_4_1\]",
					"compile.*smoke_suite.test_resources.simple.test2.cxx.*\[arm.v5.urel.gcce4_4_1\]",
					"compile.*smoke_suite.test_resources.simple.test3.Cpp.*\[arm.v5.urel.gcce4_4_1\]",
					"compile.*smoke_suite.test_resources.simple.test4.cc.*\[arm.v5.urel.gcce4_4_1\]",
					"compile.*smoke_suite.test_resources.simple.test5.CC.*\[arm.v5.urel.gcce4_4_1\]",
					"compile.*smoke_suite.test_resources.simple.test6.C\+\+.*\[arm.v5.urel.gcce4_4_1\]",
					"target.*epoc32.release.armv5.urel.test.exe.*\[arm.v5.urel.gcce4_4_1\]"
					]
	t.run()
	
	# Rebuild using the --no-metadata-depend option having touched the MMP
	# No build should happen.
	t.name = "rebuild_with_using_no_metadata_depend"
	t.description = "Touch an MMP and run build again using --no-metadata-depend"
	t.command = ("touch smoke_suite/test_resources/simple/simple.mmp; " +
				"{0} -c arm.v5.urel.gcce4_4_1 --no-metadata-depend ".format(base_command))
	t.targets = targets
	t.addbuildtargets("smoke_suite/test_resources/simple/bld.inf", buildtargets)
	t.mustmatch = [	"no warnings or errors",
					"built 'arm.v5.urel.gcce4_4_1'"
					]
	# Don't clean the build targets as that would force a rebuild of everything.
	# The aim is to validate that nothing gets rebuilt despite the fact that the
	# MMP might have been re-written
	t.run(noclean=True)
	
	# Rebuild using the --no-metadata-depend option having touched the MMP
	# No build should happen.
	t.name = "rebuild_without_using_no_metadata_depend"
	t.description = "Touch an MMP and run build again without using --no-metadata-depend"
	t.command = ("touch smoke_suite/test_resources/simple/simple.mmp; " +
				"{0} -c arm.v5.urel.gcce4_4_1".format(base_command))
	t.targets = targets
	t.addbuildtargets("smoke_suite/test_resources/simple/bld.inf", buildtargets)
	t.mustmatch = [	"compile.*smoke_suite.test_resources.simple.test.cpp.*\[arm.v5.urel.gcce4_4_1\]",
					"compile.*smoke_suite.test_resources.simple.test.cia.*\[arm.v5.urel.gcce4_4_1\]",
					"compile.*smoke_suite.test_resources.simple.test1.c\+\+.*\[arm.v5.urel.gcce4_4_1\]",
					"compile.*smoke_suite.test_resources.simple.test2.cxx.*\[arm.v5.urel.gcce4_4_1\]",
					"compile.*smoke_suite.test_resources.simple.test3.Cpp.*\[arm.v5.urel.gcce4_4_1\]",
					"compile.*smoke_suite.test_resources.simple.test4.cc.*\[arm.v5.urel.gcce4_4_1\]",
					"compile.*smoke_suite.test_resources.simple.test5.CC.*\[arm.v5.urel.gcce4_4_1\]",
					"compile.*smoke_suite.test_resources.simple.test6.C\+\+.*\[arm.v5.urel.gcce4_4_1\]",
					"target.*epoc32.release.armv5.urel.test.exe.*\[arm.v5.urel.gcce4_4_1\]"
					]
	
	# Don't clean the build targets as that would force a rebuild of everything. 
	# The aim is to validate the dependency of the .exe on its mmp file, so 
	# a "touch" on the MMP, forces a rebuild
	t.run(noclean=True)
	
	return t
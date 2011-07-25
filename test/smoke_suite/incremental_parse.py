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

from raptor_tests import SmokeTest, ReplaceEnvs
import shutil
import os

def run():
	t = SmokeTest()
	t.usebash = True
	result = SmokeTest.PASS

	description = """This test checks that the incremental parsing feature
		works and that it rebuilds makefiles if and only if the
		relevant metadata files or their pre-requisites have 
		changed.  ie. ig an mmp,bld.inf,mmh or included bld.inf
		have been altered.  Incremental parsing is also sensitive
		to the configurations that are being built and to the
		environment (tools may change for example which may 
		require that makefile be regenerated.)  """

	command = "sbs -b smoke_suite/test_resources/simple/bld.inf -f ${SBSLOGFILE} "
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
		"test_/armv5/urel/test_urel_objects.via"
		]
	mustmatch = [
	]
	

	# Make sure that the targets aren't there - quicker than doing a CLEAN
	for trg in targets:
		try:
			os.unlink(ReplaceEnvs(trg))
		except OSError as e:
			pass
	# Ensure that all makefiles, build records etc from the past are 
	# removed so that this test can run completely "cleanly"

	if "SBS_BUILD_DIR" in os.environ:
		old_sbs_build_dir = os.environ["SBS_BUILD_DIR"]
		os.environ["SBS_BUILD_DIR"] = os.path.join(old_sbs_build_dir, "incremental_parse")
	else:
		old_sbs_build_dir = None
		os.environ["SBS_BUILD_DIR"] = os.path.join(ReplaceEnvs("$(EPOCROOT)"), "epoc32", "build", "incremental_parse")
	t.sbs_build_dir = os.environ["SBS_BUILD_DIR"]

	shutil.rmtree(os.environ["SBS_BUILD_DIR"], ignore_errors=True)
	os.makedirs(os.environ["SBS_BUILD_DIR"])

	t.name = "incremental_force"
	t.description = """ do a straightforward non-incremental build """
	t.command = command + " -c arm.v5.urel.gcce4_4_1"
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
	t.run(noclean=True)

	t.name = "incremental_donothing"
	t.description = """ do a straightforward non-incremental build """
	t.command = command + " -c arm.v5.urel.gcce4_4_1 --ip=on"
	t.targets = targets
	t.addbuildtargets("smoke_suite/test_resources/simple/bld.inf", buildtargets)
	t.mustmatch = [	"incremental makefile generation: pre-existing makefiles will be reused:.*",
			]
	t.run(noclean=True)

	t.name = "incremental_touched_source_file"
	t.description = """ do a straightforward incremental build having changed a source file """
	t.command = "touch $SBS_HOME/test/smoke_suite/test_resources/simple/test.cpp; " + command + " -c arm.v5.urel.gcce4_4_1 --ip=on"
	t.targets = targets
	t.addbuildtargets("smoke_suite/test_resources/simple/bld.inf", buildtargets)

	t.mustmatch = [	
					"incremental makefile generation: pre-existing makefiles will be reused:.*",
					"compile.*smoke_suite.test_resources.simple.test.cpp.*\[arm.v5.urel.gcce4_4_1\]",
					"target.*epoc32.release.armv5.urel.test.exe.*\[arm.v5.urel.gcce4_4_1\]",
					]
	t.mustnotmatch = [	"compile.*smoke_suite.test_resources.simple.test.cia.*\[arm.v5.urel.gcce4_4_1\]",
						"compile.*smoke_suite.test_resources.simple.test1.c\+\+.*\[arm.v5.urel.gcce4_4_1\]",
						"compile.*smoke_suite.test_resources.simple.test2.cxx.*\[arm.v5.urel.gcce4_4_1\]",
						"compile.*smoke_suite.test_resources.simple.test3.Cpp.*\[arm.v5.urel.gcce4_4_1\]",
						"compile.*smoke_suite.test_resources.simple.test4.cc.*\[arm.v5.urel.gcce4_4_1\]",
						"compile.*smoke_suite.test_resources.simple.test5.CC.*\[arm.v5.urel.gcce4_4_1\]",
						"compile.*smoke_suite.test_resources.simple.test6.C\+\+.*\[arm.v5.urel.gcce4_4_1\]"
					]
	t.run(noclean=True)

	t.name = "incremental_touched_mmp_file"
	t.description = """ do a straightforward incremental build having changed an mmp file """
	t.command = "sleep 1; touch $SBS_HOME/test/smoke_suite/test_resources/simple/simple.mmp; sleep 1; " + command + " -c arm.v5.urel.gcce4_4_1 --ip=on"
	t.targets = targets
	t.addbuildtargets("smoke_suite/test_resources/simple/bld.inf", buildtargets)

	t.mustmatch = [	
					"incremental makefile generation: cannot reuse any pre-existing makefiles",
					"compile.*smoke_suite.test_resources.simple.test.cpp.*\[arm.v5.urel.gcce4_4_1\]",
					"compile.*smoke_suite.test_resources.simple.test1.c\+\+.*\[arm.v5.urel.gcce4_4_1\]",
					"compile.*smoke_suite.test_resources.simple.test.cia.*\[arm.v5.urel.gcce4_4_1\]",
					"compile.*smoke_suite.test_resources.simple.test2.cxx.*\[arm.v5.urel.gcce4_4_1\]",
					"compile.*smoke_suite.test_resources.simple.test3.Cpp.*\[arm.v5.urel.gcce4_4_1\]",
					"compile.*smoke_suite.test_resources.simple.test4.cc.*\[arm.v5.urel.gcce4_4_1\]",
					"compile.*smoke_suite.test_resources.simple.test5.CC.*\[arm.v5.urel.gcce4_4_1\]",
					"compile.*smoke_suite.test_resources.simple.test6.C\+\+.*\[arm.v5.urel.gcce4_4_1\]",
					"target.*epoc32.release.armv5.urel.test.exe.*\[arm.v5.urel.gcce4_4_1\]"
					]
	t.mustnotmatch = []
	t.run(noclean=True)

	t.name = "incremental_changed_configuration"
	t.description = """ do a straightforward incremental build having changed the configuration """
	t.command = command + " -c arm.v5.udeb.gcce4_4_1 --ip=on"
	# need udeb versions for this part of the test
	t.targets = [x.replace("urel", "udeb") for x in targets]
	t.addbuildtargets("smoke_suite/test_resources/simple/bld.inf", [x.replace("urel", "udeb") for x in buildtargets])

	t.mustmatch = [	
					"incremental makefile generation: cannot reuse any pre-existing makefiles",
					"compile.*smoke_suite.test_resources.simple.test.cpp.*\[arm.v5.udeb.gcce4_4_1\]",
					"compile.*smoke_suite.test_resources.simple.test1.c\+\+.*\[arm.v5.udeb.gcce4_4_1\]",
					"compile.*smoke_suite.test_resources.simple.test.cia.*\[arm.v5.udeb.gcce4_4_1\]",
					"compile.*smoke_suite.test_resources.simple.test2.cxx.*\[arm.v5.udeb.gcce4_4_1\]",
					"compile.*smoke_suite.test_resources.simple.test3.Cpp.*\[arm.v5.udeb.gcce4_4_1\]",
					"compile.*smoke_suite.test_resources.simple.test4.cc.*\[arm.v5.udeb.gcce4_4_1\]",
					"compile.*smoke_suite.test_resources.simple.test5.CC.*\[arm.v5.udeb.gcce4_4_1\]",
					"compile.*smoke_suite.test_resources.simple.test6.C\+\+.*\[arm.v5.udeb.gcce4_4_1\]",
					"target.*epoc32.release.armv5.udeb.test.exe.*\[arm.v5.udeb.gcce4_4_1\]"
					]
	t.mustnotmatch = []
	t.run()

	# Restore SBS_BUILD_DIR if needed
	if old_sbs_build_dir != None:
		os.environ["SBS_BUILD_DIR"] = old_sbs_build_dir
	else:
		del os.environ["SBS_BUILD_DIR"]
	t.name = "incremental_parsing"	
	return t

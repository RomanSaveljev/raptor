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
#

from raptor_tests import SmokeTest, ReplaceEnvs
import shutil
import os

def run():
	t = SmokeTest()
	t.usebash = True
	result = SmokeTest.PASS
	t.id="1000001"

	description = """This test checks that the incremental parsing feature
		works and that it rebuilds makefiles if and only if the
		relevant metadata files or their pre-requisites have 
		changed.  ie. ig an mmp,bld.inf,mmh or included bld.inf
		have been altered.  Incremental parsing is also sensitive
		to the configurations that are being built and to the
		environment (tools may change for example which may 
		require that makefiles be regenerated.  """

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
		except OSError,e:
			pass
	# Ensure that all makefiles, build records etc from the past are 
	# removed so that this test can run completely "cleanly"

	shutil.rmtree(ReplaceEnvs("$(EPOCROOT)/epoc32/build"), ignore_errors=True)
	os.makedirs(ReplaceEnvs("$(EPOCROOT)/epoc32/build"))

	t.name = "incremental_force"
	t.id="1000001a"
	t.description = """ do a straightforward non-incremental build """
	t.command = command + " -c arm.v5.urel.gcce4_4_1"
	t.targets = targets
	t.addbuildtargets("smoke_suite/test_resources/simple/bld.inf", buildtargets)
	t.run()

	t.name = "incremental_donothing"
	t.id="1000001b"
	t.description = """ do a straightforward non-incremental build """
	t.command = command + " -c arm.v5.urel.gcce4_4_1 --ip=on"
	t.targets = targets
	t.addbuildtargets("smoke_suite/test_resources/simple/bld.inf", buildtargets)
	t.run()
	return t

#
# Copyright (c) 2010-2014 Microsoft Mobile and/or its subsidiary(-ies).
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

import os
from raptor_tests import AntiTargetSmokeTest

def run():
	t = AntiTargetSmokeTest()
	t.name = "delete_on_failed_compile"
	t.description = "Test that object files are not present following a forced failed compile."
	
	t.usebash = True
	base_command = "sbs -b smoke_suite/test_resources/simple/bld.inf -c armv5 -k"
	
	# Ensure everything is reallyclean before the test
	t.name = "delete_on_failed_compile_reallyclean_01"
	t.returncode = 0
	t.antitargets = [ ]
	t.command = base_command + " reallyclean"
	t.run()
	
	# Object files should *not* be present after this forced failed compile
	t.name = "delete_on_failed_compile_build"
	t.errors = 1
	t.returncode = 1
	# None of these files should be present
	t.addbuildantitargets('smoke_suite/test_resources/simple/bld.inf', 
		[	"test_/armv5/udeb/test.o",
			"test_/armv5/udeb/test1.o",
			"test_/armv5/udeb/test2.o",
			"test_/armv5/udeb/test3.o",
			"test_/armv5/udeb/test4.o",
			"test_/armv5/udeb/test5.o",
			"test_/armv5/udeb/test6.o",
			"test_/armv5/urel/test.o",
			"test_/armv5/urel/test1.o",
			"test_/armv5/urel/test2.o",
			"test_/armv5/urel/test3.o",
			"test_/armv5/urel/test4.o",
			"test_/armv5/urel/test5.o",
			"test_/armv5/urel/test6.o"  ])
	sbshome = os.environ["SBS_HOME"].replace("\\","/").rstrip("/")
	t.command = base_command.replace("armv5", "armv5.fake_compiler") + \
	" --configpath={0}/test/smoke_suite/test_resources/simple/compilervariants".format(sbshome)
	t.run()
	
	t.name = "delete_on_failed_compile_reallyclean_02"
	t.errors = 0
	t.returncode = 0
	t.antitargets = [] # Remove the list of anti-targets
	t.command = base_command + " reallyclean"
	t.run()
	
	# Use a redefined make_engine variant - object files *should* be present
	t.name = "delete_on_failed_compile_build_redefined_make_engine"
	t.errors = 1
	t.returncode = 1
	t.antitargets = [] # Remove the list of anti-targets
	# All of these files should be present
	t.addbuildtargets('smoke_suite/test_resources/simple/bld.inf', 
		[	"test_/armv5/udeb/test.o",
			"test_/armv5/udeb/test1.o",
			"test_/armv5/udeb/test2.o",
			"test_/armv5/udeb/test3.o",
			"test_/armv5/udeb/test4.o",
			"test_/armv5/udeb/test5.o",
			"test_/armv5/udeb/test6.o",
			"test_/armv5/urel/test.o",
			"test_/armv5/urel/test1.o",
			"test_/armv5/urel/test2.o",
			"test_/armv5/urel/test3.o",
			"test_/armv5/urel/test4.o",
			"test_/armv5/urel/test5.o",
			"test_/armv5/urel/test6.o"  ])
	
	t.command = base_command.replace("armv5", "armv5.fake_compiler") + " -e make_test " \
	+ " --configpath={0}/test/smoke_suite/test_resources/simple/compilervariants ".format(sbshome) \
	+ " --configpath={0}/test/smoke_suite/test_resources/simple/makevariants".format(sbshome)
	t.run()
	
	t.name = "delete_on_failed_compile_reallyclean_03"
	t.errors = 0
	t.returncode = 0
	t.antitargets = [] # Remove the list of anti-targets
	t.targets = [] # Remove the list of targets
	t.command = base_command + " reallyclean"
	t.run()
	
	t.name = "delete_on_failed_compile"
	t.print_result()
	return t

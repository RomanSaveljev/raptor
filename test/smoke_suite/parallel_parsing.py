#
# Copyright (c) 2009 - 2011 Nokia Corporation and/or its subsidiary(-ies).
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

	mmpcount = 10 # how many mmps in this parallel parsing test
	
	target_templ = [
		"$(EPOCROOT)/epoc32/release/armv5/udeb/test_pp#.exe",
		"$(EPOCROOT)/epoc32/release/armv5/udeb/test_pp#.exe.map",
		"$(EPOCROOT)/epoc32/release/armv5/urel/test_pp#.exe",
		"$(EPOCROOT)/epoc32/release/armv5/urel/test_pp#.exe.map",
		"$(EPOCROOT)/epoc32/release/armv5/udeb/test_pp#.exe.sym",
		"$(EPOCROOT)/epoc32/release/armv5/urel/test_pp#.exe.sym"
	]

	targets = []

	# Test appropriate startup script for platform:
	sbs_script="sbs"
	if t.onWindows:
		sbs_script="sbs.bat"

	# Build up target list for 10 similar executables
	for num in range(1,mmpcount):
		for atarget in target_templ:
			targets.append(atarget.replace('pp#','pp'+ str(num)))

	t.name = "parallel_parsing"
	t.description = """This test covers parallel parsing."""
	t.command=("mkdir -p $(EPOCROOT)/epoc32/build && cd $(SBS_HOME)/test/smoke_suite/test_resources/pp/ && " 
	"{0} --command=$(SBS_HOME)/test/smoke_suite/test_resources/pp/ppbldinf_commandfile -c armv5 -c winscw " 
	"--pp=on --noexport -m {1} -f - | grep progress ".format(sbs_script, "${SBSMAKEFILE}"))
	t.targets = targets
	t.mustmatch =  [
		".*<progress:start object_type='makefile' task='makefile_generation'.*"
	]
	t.mustnotmatch = [
		".*<recipe .*name='makefile_generation_export.*",
		".*<error[^><]*>.*"
	]
	t.warnings = 0
	t.run()

	t.name = "parallel_parsing_missing_includes_in_bld_inf"
	t.description = """ Ensure errors from parallel parsing are recorded by the top level Raptor. """
	t.command=("{0} -s smoke_suite/test_resources/pp/sys_def.xml -c armv5 -k --pp=on reallyclean > /dev/null 2>&1; "
	"{0} -s smoke_suite/test_resources/pp/sys_def.xml -c armv5 -k --pp=on".format(sbs_script))
	t.targets = []
	t.mustmatch = [
		 "sbs: error: .*cpp.*test/smoke_suite/test_resources/pp/test01/bld.inf.*this_file_does_not_exist.inf: No such file or directory",
		("sbs: error: Preprocessor exception.*Errors in .*test/smoke_suite/test_resources/pp/test01/bld.inf'' " 
		 ": in command.*cpp.*component.*test/smoke_suite/test_resources/pp/test01/bld.inf")
									
					]
	t.mustnotmatch = []
	t.warnings = -1
	t.errors = -1
	t.returncode = 1
	t.run()

	t.name = "parallel_parsing"
	t.print_result()
	return t

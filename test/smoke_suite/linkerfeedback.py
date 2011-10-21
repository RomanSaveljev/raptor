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

def run():
	t = SmokeTest()
	t.usebash = True
	
	t.command = "sbs -b smoke_suite/test_resources/simple_dll/bld.inf -c arm.v5.udeb.rvct4_0.linkerfeedback -c arm.v5.urel.rvct4_0.linkerfeedback -f-"

	gen_fdb_match = [
		".*armlink.*-o.*epoc32/release/armv5/udeb/createstaticdll.dll.sym.*--feedback=.*createstaticdll_dll/armv5/udeb/createstaticdll_udeb_feedback.fdb.*",
		".*armlink.*-o.*epoc32/release/armv5/urel/createstaticdll.dll.sym.*--feedback=.*createstaticdll_dll/armv5/urel/createstaticdll_urel_feedback.fdb.*"
		]
	use_fdb_match = [
		".*armcc.*--feedback=.*createstaticdll_dll/armv5/udeb/createstaticdll_udeb_feedback.fdb.*test/smoke_suite/test_resources/simple_dll/CreateStaticDLL.cpp.*",
		".*armcc.*--feedback=.*createstaticdll_dll/armv5/urel/createstaticdll_urel_feedback.fdb.*test/smoke_suite/test_resources/simple_dll/CreateStaticDLL.cpp.*"
		]
	
	t.name = "linkerfeedback_initial_build"
	t.targets = [
		"$(EPOCROOT)/epoc32/release/armv5/udeb/createstaticdll.dll.sym",
		"$(EPOCROOT)/epoc32/release/armv5/urel/createstaticdll.dll.sym",
		"$(EPOCROOT)/epoc32/release/armv5/lib/createstaticdll.dso",
		"$(EPOCROOT)/epoc32/release/armv5/lib/createstaticdll{000a0000}.dso",
		"$(EPOCROOT)/epoc32/release/armv5/udeb/createstaticdll.dll",
		"$(EPOCROOT)/epoc32/release/armv5/urel/createstaticdll.dll"
		]
	t.addbuildtargets('smoke_suite/test_resources/simple_dll/bld.inf', [
		"createstaticdll_dll/armv5/udeb/createstaticdll_udeb_feedback.fdb",
		"createstaticdll_dll/armv5/urel/createstaticdll_urel_feedback.fdb",
		"createstaticdll_dll/armv5/udeb/CreateStaticDLL.o",
		"createstaticdll_dll/armv5/urel/CreateStaticDLL.o"		
		])
	t.mustmatch_singleline = gen_fdb_match
	t.mustnotmatch_singleline = use_fdb_match
	t.run()
	
	# Note: we neutralise the targets in the following in order to ensure
	# that they aren't cleaned from the initial build
	# Instead we confirm that the "right thing" happens in these next builds
	# in terms of tools calls based on the linker feedback files being present
	# and:
	# (a) newer than the object files (triggering re-compile and re-link)
	# (b) older than the object files (nothing to be done)

	t.name = "linkerfeedback_first_rebuild"
	t.targets = []
	t.mustmatch_singleline = gen_fdb_match + use_fdb_match
	t.mustnotmatch_singleline = []
	t.run()
	
	t.name = "linkerfeedback_second_rebuild"
	t.targets = []
	t.mustmatch_singleline = []
	t.mustnotmatch_singleline = gen_fdb_match + use_fdb_match
	t.run()
	
	t.name = "linkerfeedback"
	t.print_result()
	return t

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

from raptor_tests import SmokeTest
import string

def run():
	t = SmokeTest()
	t.description = "Check that ARM toolchain specific macros are used in both metadata and source processing."
	t.warnings = -1

	toolchains = {
				'rvct2_2':   ['ARMCC', 'ARMCC_2', 'ARMCC_2_2', '__ARMCC__', '__ARMCC_2__',  '__ARMCC_2_2__'],
				'rvct4_0':   ['ARMCC', 'ARMCC_4', 'ARMCC_4_0', '__ARMCC__', '__ARMCC_4__' , '__ARMCC_4_0__'],
				'gcce4_3_2': ['GCCE', 'GCCE_4', 'GCCE_4_3', '__GCCE__', '__GCCE_4__' , '__GCCE_4_3__'],
				'gcce4_3_3': ['GCCE', 'GCCE_4', 'GCCE_4_3', '__GCCE__', '__GCCE_4__' , '__GCCE_4_3__'],
				'gcce4_4_1': ['GCCE', 'GCCE_4', 'GCCE_4_4', '__GCCE__', '__GCCE_4__' , '__GCCE_4_4__'],
				'gcce4_5_1': ['GCCE', 'GCCE_4', 'GCCE_4_5', '__GCCE__', '__GCCE_4__' , '__GCCE_4_5__']
				}

	rootname = "toolchain_macros_armv5_{0}_{1}"
	rootcommand = "sbs -b smoke_suite/test_resources/toolchain_macros/bld.inf -c arm.v5.urel."
	macromatch = ": #warning( directive:)? {0}(</warning>)?$"

	for toolchain in sorted(toolchains.keys()):
		t.name = rootname.format(toolchain, "clean")
		t.command = rootcommand + toolchain + " clean"
		t.mustmatch_singleline = []
		t.run()

		t.name = rootname.format(toolchain, "build")
		t.command = rootcommand + toolchain
		mustmatch = []
		for macro in toolchains[toolchain]:
			mustmatch.append(macromatch.format(macro))
		t.mustmatch_singleline = mustmatch
		t.run()

	t.name = "toolchain_macros"
	t.print_result()
	return t

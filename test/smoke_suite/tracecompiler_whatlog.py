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

from raptor_tests import CheckWhatSmokeTest
import re

def run():
	t = CheckWhatSmokeTest()
	t.description = "Trace Compiler Whatlog Clean"
	t.name = "tracecompiler_whatlog_clean"
	t.usebash = True
	t.command = "sbs -b smoke_suite/test_resources/tracecompiler/testTC/group/bld2.inf -c armv5.tracecompiler CLEAN"
	t.regexlinefilter = re.compile("^<(whatlog|export|build>|resource>|bitmap>)")
	t.stdout = [] # There should be no whatlog rules when cleaning
	t.run()
	t.print_result()

	t.description = "Trace Compiler Whatlog test"
	t.name = "tracecompiler_whatlog"
	t.command = "sbs -b smoke_suite/test_resources/tracecompiler/testTC/group/bld2.inf -c armv5.tracecompiler -m ${SBSMAKEFILE} -f ${SBSLOGFILE} && cat ${SBSLOGFILE}"
	t.hostossensitive = False
	t.targets = [
		"$(EPOCROOT)/epoc32/release/armv5/lib/testTC.dso",
		"$(EPOCROOT)/epoc32/release/armv5/lib/testTC{000a0000}.dso",
		"$(EPOCROOT)/epoc32/release/armv5/udeb/testTC.dll",
		"$(EPOCROOT)/epoc32/release/armv5/udeb/testTC.dll.map",
		"$(EPOCROOT)/epoc32/release/armv5/urel/testTC.dll",
		"$(EPOCROOT)/epoc32/release/armv5/urel/testTC.dll.map",
		"$(SBS_HOME)/test/smoke_suite/test_resources/tracecompiler/testTC/traces/wlanhwinitTraces.h",
		"$(SBS_HOME)/test/smoke_suite/test_resources/tracecompiler/testTC/traces/wlanhwinitmainTraces.h",
		"$(SBS_HOME)/test/smoke_suite/test_resources/tracecompiler/testTC/traces/wlanhwinitpermparserTraces.h",	
		"$(SBS_HOME)/test/smoke_suite/test_resources/tracecompiler/testTC/traces/fixed_id.definitions",
		"$(EPOCROOT)/epoc32/ost_dictionaries/test_TC_0x1000008d_Dictionary.xml",
		"$(EPOCROOT)/epoc32/include/platform/symbiantraces/autogen/test_TC_0x1000008d_TraceDefinitions.h"
		]
	t.stdout = [
		"<whatlog bldinf='$(SBS_HOME)/test/smoke_suite/test_resources/tracecompiler/testTC/group/bld2.inf' mmp='$(SBS_HOME)/test/smoke_suite/test_resources/tracecompiler/testTC/group/test.TC.mmp' config='armv5_urel.tracecompiler'>",
		"<whatlog bldinf='$(SBS_HOME)/test/smoke_suite/test_resources/tracecompiler/testTC/group/bld2.inf' mmp='$(SBS_HOME)/test/smoke_suite/test_resources/tracecompiler/testTC/group/test.TC.mmp' config='armv5_udeb.tracecompiler'>",
		"<build>$(EPOCROOT)/epoc32/release/armv5/lib/testTC.dso</build>",
		"<build>$(EPOCROOT)/epoc32/release/armv5/lib/testTC{000a0000}.dso</build>",
		"<build>$(EPOCROOT)/epoc32/release/armv5/udeb/testTC.dll</build>",
		"<build>$(EPOCROOT)/epoc32/release/armv5/udeb/testTC.dll.map</build>",
		"<build>$(EPOCROOT)/epoc32/release/armv5/urel/testTC.dll</build>",
		"<build>$(EPOCROOT)/epoc32/release/armv5/urel/testTC.dll.map</build>",
		"<build>$(EPOCROOT)/epoc32/ost_dictionaries/test_TC_0x1000008d_Dictionary.xml</build>",
		"<build>$(EPOCROOT)/epoc32/include/platform/symbiantraces/autogen/test_TC_0x1000008d_TraceDefinitions.h</build>"
		]		
	t.run()
	t.print_result()
	
	t.name = "tracecompiler_whatlog_initnum_clean"
	t.targets = []
	t.stdout = []
	t.command = "sbs -b smoke_suite/test_resources/tracecompiler/TC_initnum/group/bld.inf -c armv5.tracecompiler CLEAN"
	t.run() 
	t.print_result()

	t.name = "tracecompiler_whatlog_initnum"
	t.command = "sbs -b smoke_suite/test_resources/tracecompiler/TC_initnum/group/bld.inf -c armv5.tracecompiler -m ${SBSMAKEFILE} -f ${SBSLOGFILE} && cat ${SBSLOGFILE}"
	t.targets = [
		"$(EPOCROOT)/epoc32/release/armv5/lib/5goldrings.dso",
		"$(EPOCROOT)/epoc32/release/armv5/lib/5goldrings{000a0000}.dso",
		"$(SBS_HOME)/test/smoke_suite/test_resources/tracecompiler/TC_initnum/traces/5goldrings_dll/fixed_id.definitions",
		"$(SBS_HOME)/test/smoke_suite/test_resources/tracecompiler/TC_initnum/traces/5goldrings_dll/num_testTraces.h",
		"$(EPOCROOT)/epoc32/release/armv5/udeb/5goldrings.dll",
		"$(EPOCROOT)/epoc32/release/armv5/udeb/5goldrings.dll.map",
		"$(EPOCROOT)/epoc32/release/armv5/urel/5goldrings.dll",
		"$(EPOCROOT)/epoc32/release/armv5/urel/5goldrings.dll.map",
		"$(EPOCROOT)/epoc32/ost_dictionaries/_5goldrings_dll_0xe800004d_Dictionary.xml",
		"$(EPOCROOT)/epoc32/include/platform/symbiantraces/autogen/_5goldrings_dll_0xe800004d_TraceDefinitions.h"
		]

	t.stdout = [
		"<whatlog bldinf='$(SBS_HOME)/test/smoke_suite/test_resources/tracecompiler/TC_initnum/group/bld.inf' mmp='$(SBS_HOME)/test/smoke_suite/test_resources/tracecompiler/TC_initnum/group/5goldrings.mmp' config='armv5_urel.tracecompiler'>",
		"<whatlog bldinf='$(SBS_HOME)/test/smoke_suite/test_resources/tracecompiler/TC_initnum/group/bld.inf' mmp='$(SBS_HOME)/test/smoke_suite/test_resources/tracecompiler/TC_initnum/group/5goldrings.mmp' config='armv5_udeb.tracecompiler'>",
		"<build>$(EPOCROOT)/epoc32/release/armv5/lib/5goldrings.dso</build>",
		"<build>$(EPOCROOT)/epoc32/release/armv5/lib/5goldrings{000a0000}.dso</build>",
		"<build>$(EPOCROOT)/epoc32/release/armv5/udeb/5goldrings.dll</build>",
		"<build>$(EPOCROOT)/epoc32/release/armv5/udeb/5goldrings.dll.map</build>",
		"<build>$(EPOCROOT)/epoc32/release/armv5/urel/5goldrings.dll</build>",
		"<build>$(EPOCROOT)/epoc32/release/armv5/urel/5goldrings.dll.map</build>",
		"<build>$(EPOCROOT)/epoc32/ost_dictionaries/_5goldrings_dll_0xe800004d_Dictionary.xml</build>",
		"<build>$(EPOCROOT)/epoc32/include/platform/symbiantraces/autogen/_5goldrings_dll_0xe800004d_TraceDefinitions.h</build>"
		]
	t.run()
	t.print_result()


	return t


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

from raptor_tests import AntiTargetSmokeTest

def run():
	t = AntiTargetSmokeTest()
	t.usebash = True
	
	command = "sbs -b smoke_suite/test_resources/rvct_multifile/group/bld.inf -c {} -f-"
	maintargets = [
		"$(EPOCROOT)/epoc32/release/armv5/udeb/rvct_multifile.dll.sym",
		"$(EPOCROOT)/epoc32/release/armv5/urel/rvct_multifile.dll.sym",
		"$(EPOCROOT)/epoc32/release/armv5/udeb/rvct_multifile.dll",
		"$(EPOCROOT)/epoc32/release/armv5/urel/rvct_multifile.dll"
		]
	abiv1libtargets = [
		"$(EPOCROOT)/epoc32/release/armv5/lib/rvct_multifile.lib",
		"$(EPOCROOT)/epoc32/release/armv5/lib/rvct_multifile{000a0000}.lib"
		]	
	buildtargets =  [
		"rvct_multifile_dll/armv5/udeb/rvct_multifile.dll_udeb_multifileobject_cpp.o",
		"rvct_multifile_dll/armv5/udeb/rvct_multifile.dll_udeb_multifileobject_c.o",
		"rvct_multifile_dll/armv5/udeb/rvct_multifile_udeb_multifile_cpp.via",
		"rvct_multifile_dll/armv5/udeb/rvct_multifile_udeb_multifile_c.via",
		"rvct_multifile_dll/armv5/urel/rvct_multifile.dll_urel_multifileobject_c.o",
		"rvct_multifile_dll/armv5/urel/rvct_multifile.dll_urel_multifileobject_cpp.o",
		"rvct_multifile_dll/armv5/urel/rvct_multifile_urel_multifile_cpp.via",
		"rvct_multifile_dll/armv5/urel/rvct_multifile_urel_multifile_c.via",
		]
	mustmatch = [
		r".*--multifile.*"
			]
	
	t.name = "rvct_multifile_build"
	t.command = command.format("armv5.multifile")
	t.targets = maintargets[:]	# Shallow, as we optionally extend later and then re-use
	t.addbuildtargets('smoke_suite/test_resources/rvct_multifile/group/bld.inf', buildtargets)
	t.mustmatch = mustmatch
	t.mustnotmatch = []
	t.run()
		
	t.name = "rvct_multifile_clean"
	t.command = "sbs -b smoke_suite/test_resources/rvct_multifile/group/bld.inf -c armv5.multifile clean"
	t.targets = []
	t.mustmatch = []
	t.mustnotmatch = []
	t.run()	
		
	t.name = "rvct_multifile"
	t.print_result()
	return t

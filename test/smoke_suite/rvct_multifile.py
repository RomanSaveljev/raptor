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

	t.description = "Build the MMP as a DLL and make sure multifile compilation groups CPP and C files separately"
	command = "sbs -b smoke_suite/test_resources/rvct_multifile/group/bld.inf -c armv5.multifile {0} -f-"
	abiv1libtargets = [
		"$(EPOCROOT)/epoc32/release/armv5/lib/rvct_multifile.lib",
		"$(EPOCROOT)/epoc32/release/armv5/lib/rvct_multifile{000a0000}.lib"
		]	
	buildtargets =  [
		"rvct_multifile_dll_dll/armv5/udeb/asm1.o",
		"rvct_multifile_dll_dll/armv5/udeb/asm2.o",
		"rvct_multifile_dll_dll/armv5/udeb/cia1_.o",
		"rvct_multifile_dll_dll/armv5/udeb/cia2_.o",
		"rvct_multifile_dll_dll/armv5/urel/asm1.o",
		"rvct_multifile_dll_dll/armv5/urel/asm2.o",
		"rvct_multifile_dll_dll/armv5/urel/cia1_.o",
		"rvct_multifile_dll_dll/armv5/urel/cia2_.o",
		"rvct_multifile_dll_dll/armv5/udeb/rvct_multifile_dll.dll_udeb_multifileobject_cpp.o",
		"rvct_multifile_dll_dll/armv5/udeb/rvct_multifile_dll.dll_udeb_multifileobject_c.o",
		"rvct_multifile_dll_dll/armv5/udeb/rvct_multifile_dll_udeb_multifile_cpp.via",
		"rvct_multifile_dll_dll/armv5/udeb/rvct_multifile_dll_udeb_multifile_c.via",
		"rvct_multifile_dll_dll/armv5/urel/rvct_multifile_dll.dll_urel_multifileobject_c.o",
		"rvct_multifile_dll_dll/armv5/urel/rvct_multifile_dll.dll_urel_multifileobject_cpp.o",
		"rvct_multifile_dll_dll/armv5/urel/rvct_multifile_dll_urel_multifile_cpp.via",
		"rvct_multifile_dll_dll/armv5/urel/rvct_multifile_dll_urel_multifile_c.via",
		]
	
	t.name = "rvct_multifile_dll_build"
	t.command = command.format("-p rvct_multifile_dll.mmp")
	t.targets = [ 
		"$(EPOCROOT)/epoc32/release/armv5/udeb/rvct_multifile_dll.dll.sym",
		"$(EPOCROOT)/epoc32/release/armv5/urel/rvct_multifile_dll.dll.sym",
		"$(EPOCROOT)/epoc32/release/armv5/udeb/rvct_multifile_dll.dll",
		"$(EPOCROOT)/epoc32/release/armv5/urel/rvct_multifile_dll.dll"
		]
	t.addbuildtargets('smoke_suite/test_resources/rvct_multifile/group/bld.inf',buildtargets)

	t.mustmatch = [r".*armcc.*--multifile.*"]
	t.mustnotmatch = []
	t.run()

	t.name = "rvct_multifile_staticlib_build"
	t.description = "Build the MMP as a static library and make sure multifile compilation is not invoked"
	t.command = command.format("-p rvct_multifile_staticlib.mmp")
	t.targets = [
		"$(EPOCROOT)/epoc32/release/armv5/udeb/rvct_multifile_staticlib.lib",
		"$(EPOCROOT)/epoc32/release/armv5/udeb/rvct_multifile_staticlib.lib"
		]
	buildtargets = [
		"rvct_multifile_staticlib_lib/armv5/udeb/asm1.o",
		"rvct_multifile_staticlib_lib/armv5/udeb/asm2.o",
		"rvct_multifile_staticlib_lib/armv5/udeb/cia1_.o",
		"rvct_multifile_staticlib_lib/armv5/udeb/cia2_.o",
		"rvct_multifile_staticlib_lib/armv5/urel/asm1.o",
		"rvct_multifile_staticlib_lib/armv5/urel/asm2.o",
		"rvct_multifile_staticlib_lib/armv5/urel/cia1_.o",
		"rvct_multifile_staticlib_lib/armv5/urel/cia2_.o",
		"rvct_multifile_staticlib_lib/armv5/urel/add.o.d",
		"rvct_multifile_staticlib_lib/armv5/urel/sub.o.d",
		"rvct_multifile_staticlib_lib/armv5/urel/use_add.o.d",
		"rvct_multifile_staticlib_lib/armv5/urel/use_sub.o.d",
		"rvct_multifile_staticlib_lib/armv5/urel/testassembler.o.d",
		"rvct_multifile_staticlib_lib/armv5/udeb/add.o",
		"rvct_multifile_staticlib_lib/armv5/udeb/sub.o",
		"rvct_multifile_staticlib_lib/armv5/udeb/use_add.o",
		"rvct_multifile_staticlib_lib/armv5/udeb/use_sub.o",
		"rvct_multifile_staticlib_lib/armv5/udeb/testassembler.o"
		]

	t.addbuildtargets('smoke_suite/test_resources/rvct_multifile/group/bld.inf',buildtargets)
	t.mustmatch = []
	t.mustnotmatch = [r".*armcc.*--multifile.*"]
	t.run()
		
	t.name = "rvct_multifile_clean"
	t.command =command.format("clean")
	t.targets = []
	t.mustmatch = []
	t.mustnotmatch = []
	t.run()	
		
	t.name = "rvct_multifile"
	t.print_result()
	return t

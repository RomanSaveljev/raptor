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
	t.description = "This testcase tests all mmp keywords including new implementation of 'paged/unpaged code/data'"
	t.usebash = True
	
	t.name = "mmp_paging_keywords"
	t.command = "sbs -b smoke_suite/test_resources/mmp/mmp1/group/bld.inf -c armv5 -f-"
	t.targets = [
		"$(EPOCROOT)/epoc32/release/armv5/udeb/shutdownsrv.dll",
		"$(EPOCROOT)/epoc32/release/armv5/udeb/shutdownsrv.dll.map",
		"$(EPOCROOT)/epoc32/release/armv5/urel/shutdownsrv.dll",
		"$(EPOCROOT)/epoc32/release/armv5/urel/shutdownsrv.dll.map",
		"$(EPOCROOT)/epoc32/release/armv5/lib/exportlibrary_shutdownsrv.dso",
		"$(EPOCROOT)/epoc32/release/armv5/lib/exportlibrary_shutdownsrv{000a0000}.dso",
	]
	t.addbuildtargets("smoke_suite/test_resources/mmp/mmp1/group/bld.inf", [
		"shutdownsrv_dll/armv5/udeb/shutdownsrv.o",
		"shutdownsrv_dll/armv5/urel/shutdownsrv.o",
		"shutdownsrv_dll/armv5/udeb/shutdownsrvpatchdata.o",
		"shutdownsrv_dll/armv5/urel/shutdownsrvpatchdata.o",
		"shutdownsrv_dll/armv5/udeb/shutdowntimer.o",
		"shutdownsrv_dll/armv5/urel/shutdowntimer.o"
		])
	t.mustmatch = [
		".*elf2e32.*(--defaultpaged|--codepaging=default.*--datapaging=default).*",
		".*armlink.*--verbose.*"
	]
	t.run()

	t.name = "mmp_option_armcc_and_armasm"
	t.command = "sbs -b smoke_suite/test_resources/mmp/mmp2/group/bld.inf -c armv5 -f-"
	t.targets = [
		"$(EPOCROOT)/epoc32/release/armv5/udeb/imageprocessorperf.lib",
		"$(EPOCROOT)/epoc32/release/armv5/urel/imageprocessorperf.lib"		
	]
	t.addbuildtargets("smoke_suite/test_resources/mmp/mmp2/group/bld.inf", [
		"imageprocessorperf_lib/armv5/udeb/ColorConverter.o",
		"imageprocessorperf_lib/armv5/urel/ColorConverter.o",
		"imageprocessorperf_lib/armv5/udeb/ImageProcessor.o",
		"imageprocessorperf_lib/armv5/urel/ImageProcessor.o"
		])
	t.mustmatch = [
		".*armcc.*-O0.*-g.*--cpu 6.*-Otime.*",
		".*armcc.*-O3.*--cpu 6.*-Otime.*",
		".*OPTION ARMASM has no effect.*",
		".*OPTION_REPLACE ARMASM has no effect.*"
	]
	t.mustnotmatch = [
		".*armcc.*--export_all_vtbl.*"
	]
	t.warnings = 2
	t.run()
	
	t.name = "mmp_option_gcce_linkeroption_gcce"
	t.command = "sbs -b smoke_suite/test_resources/mmp/options/bld.inf -c arm.v5.urel.gcce4_4_1.release_gcce -f-"
	t.targets = [
		"$(EPOCROOT)/epoc32/release/gcce/urel/test.exe",
	]
	t.mustmatch = []
	t.mustmatch_singleline = [
		".*g\+\+.*-c.*-O3.*-fvisibility-inlines-hidden.*",
		".*g\+\+.* -Wl,--verbose -Wl,-pie .*"
	]
	t.mustnotmatch = [
		".*g\+\+.*-c.* -Wl,--verbose -Wl,-pie .*"
	]
	t.warnings = 0 
	t.run()
	
	# LINKEROPTION CW can impact DLL (and variants), EXE and LIB TARGETTYPEs in different ways
	# We ensure we have enough build coverage to cover all linker calls constructed in the win32 FLM
	t.name = "mmp_option_cw_linkeroption_cw"
	t.command = "sbs -b smoke_suite/test_resources/mmp/options/bld.inf -c winscw_urel -f-"
	t.targets = [
		"$(EPOCROOT)/epoc32/release/winscw/urel/test.exe",
	]
	t.mustmatch = []
	t.mustmatch_singleline = []
	t.countmatch = [
		[".*mwccsym2.*-relax_pointers.*-O2", 5],
		[".*mwldsym2.*-zerobss.*-export none", 2],
		[".*mwldsym2.*-zerobss.*-fold all", 2]
	]	
	t.warnings = 0
	t.run()
	
	t.countmatch = []
	
	t.name = "mmp_debuglibrary"
	t.command = "sbs -b smoke_suite/test_resources/mmp/mmp3/bld.inf -c armv5 -c winscw -f-"
	t.targets = [
		"$(EPOCROOT)/epoc32/release/armv5/udeb/tbm.exe",
		"$(EPOCROOT)/epoc32/release/armv5/udeb/tbm.exe.map",
		"$(EPOCROOT)/epoc32/release/armv5/urel/tbm.exe",
		"$(EPOCROOT)/epoc32/release/armv5/urel/tbm.exe.map",
		"$(EPOCROOT)/epoc32/release/armv5/udeb/t_oom.exe",
		"$(EPOCROOT)/epoc32/release/armv5/udeb/t_oom.exe.map",
		"$(EPOCROOT)/epoc32/release/armv5/urel/t_oom.exe",
		"$(EPOCROOT)/epoc32/release/armv5/urel/t_oom.exe.map",
		"$(EPOCROOT)/epoc32/release/armv5/udeb/dfpaeabi_vfpv2.dll",
		"$(EPOCROOT)/epoc32/release/armv5/udeb/dfpaeabi_vfpv2.dll.map",
		"$(EPOCROOT)/epoc32/release/armv5/urel/dfpaeabi_vfpv2.dll",
		"$(EPOCROOT)/epoc32/release/armv5/urel/dfpaeabi_vfpv2.dll.map",
		"$(EPOCROOT)/epoc32/release/winscw/urel/t_oom.exe",
		"$(EPOCROOT)/epoc32/release/winscw/urel/t_oom.exe.map",
		"$(EPOCROOT)/epoc32/release/winscw/udeb/t_oom.exe"
		]
	t.addbuildtargets("smoke_suite/test_resources/mmp/mmp3/bld.inf", [
		"tbm_exe/armv5/udeb/tbm.o",
		"tbm_exe/armv5/urel/tbm.o",
		"t_oom_exe/armv5/udeb/t_oom.o",
		"t_oom_exe/armv5/urel/t_oom.o",
		"dfpaeabi_vfpv2_dll/armv5/udeb/dfpaeabi.o",
		"dfpaeabi_vfpv2_dll/armv5/urel/dfpaeabi.o",
		"t_oom_exe/winscw/udeb/t_oom.o",
		"t_oom_exe/winscw/udeb/t_oom_UID_.o",
		"t_oom_exe/winscw/urel/t_oom.o",
		"t_oom_exe/winscw/urel/t_oom_UID_.o"
		])
	t.mustmatch = [
		".*armlink.*udeb/eexe.lib.*-o.*armv5/udeb/t_oom.exe.sym.*euser.dso.*efsrv.dso.*estor.dso.*euser.dso.*",
		".*armlink.*urel/eexe.lib.*-o.*armv5/urel/t_oom.exe.sym.*euser.dso.*efsrv.dso.*euser.dso.*",
		".*mwldsym2.*udeb/eexe.lib.*euser.lib.*efsrv.lib.*estor.lib.*euser.lib.*-o.*winscw/udeb/t_oom.exe.*",
		".*mwldsym2.*urel/eexe.lib.*euser.lib.*efsrv.lib.*euser.lib.*-o.*winscw/urel/t_oom.exe.*"
		]
	t.mustnotmatch = []
	t.warnings = 0
	t.run()
	
	t.name = "mmp_basedefault"
	t.command = "sbs -b smoke_suite/test_resources/mmp/mmp4/group/bld.inf -c winscw"
	t.targets = [			
		"$(EPOCROOT)/epoc32/release/winscw/udeb/d_newldd.ldd",
		"$(EPOCROOT)/epoc32/release/winscw/urel/d_newldd.ldd",
		"$(EPOCROOT)/epoc32/release/winscw/udeb/d_lddturnaroundtimertest.ldd",
		"$(EPOCROOT)/epoc32/release/winscw/urel/d_lddturnaroundtimertest.ldd",
		"$(EPOCROOT)/epoc32/release/winscw/urel/d_lddturnaroundtimertest.ldd.map",
		"$(EPOCROOT)/epoc32/release/winscw/udeb/t_sharedio3.exe",
		"$(EPOCROOT)/epoc32/release/winscw/urel/t_sharedio3.exe",
		"$(EPOCROOT)/epoc32/release/winscw/urel/t_sharedio3.exe.map",
		"$(EPOCROOT)/epoc32/release/winscw/udeb/t_rbuf.exe",
		"$(EPOCROOT)/epoc32/release/winscw/urel/t_rbuf.exe",
		"$(EPOCROOT)/epoc32/release/winscw/urel/t_rbuf.exe.map"
		]
	t.addbuildtargets("smoke_suite/test_resources/mmp/mmp4/group/bld.inf", [
		"d_newldd_ldd/winscw/udeb/d_newldd.o",
		"d_newldd_ldd/winscw/udeb/d_newldd.UID.CPP",
		"d_newldd_ldd/winscw/udeb/d_newldd_UID_.o",
		"d_newldd_ldd/winscw/urel/d_newldd.o",
		"d_newldd_ldd/winscw/urel/d_newldd.UID.CPP",
		"d_newldd_ldd/winscw/urel/d_newldd_UID_.o",
		"d_newldd_ldd/winscw/udeb/t_new_classes.o",
		"d_newldd_ldd/winscw/urel/t_new_classes.o",
		"d_lddturnaroundtimertest_ldd/winscw/udeb/d_lddturnaroundtimertest.o",
		"d_lddturnaroundtimertest_ldd/winscw/udeb/d_lddturnaroundtimertest.UID.CPP",
		"d_lddturnaroundtimertest_ldd/winscw/udeb/d_lddturnaroundtimertest_UID_.o",
		"d_lddturnaroundtimertest_ldd/winscw/urel/d_lddturnaroundtimertest.o",
		"d_lddturnaroundtimertest_ldd/winscw/urel/d_lddturnaroundtimertest.UID.CPP",
		"d_lddturnaroundtimertest_ldd/winscw/urel/d_lddturnaroundtimertest_UID_.o",
		"t_sharedio3_exe/winscw/udeb/t_sharedio.o",
		"t_sharedio3_exe/winscw/udeb/t_sharedio3.UID.CPP",
		"t_sharedio3_exe/winscw/udeb/t_sharedio3_UID_.o",
		"t_sharedio3_exe/winscw/urel/t_sharedio.o",
		"t_sharedio3_exe/winscw/urel/t_sharedio3.UID.CPP",
		"t_sharedio3_exe/winscw/urel/t_sharedio3_UID_.o",
		"t_rbuf_exe/winscw/udeb/t_rbuf.o",
		"t_rbuf_exe/winscw/udeb/t_rbuf.UID.CPP",
		"t_rbuf_exe/winscw/udeb/t_rbuf_UID_.o",
		"t_rbuf_exe/winscw/urel/t_rbuf.o",
		"t_rbuf_exe/winscw/urel/t_rbuf.UID.CPP",
		"t_rbuf_exe/winscw/urel/t_rbuf_UID_.o"
		])
	t.mustmatch = []
	t.run()
	
	# Test keywords: version, firstlib, nocompresstarget
	t.name = "mmp_version_firstlib_nocompresstarget"
	t.command = "sbs -b smoke_suite/test_resources/mmp/mmp5/bld.inf -c armv5"
	t.targets = [
		"$(EPOCROOT)/epoc32/release/armv5/udeb/fuzzv5.exe",
		"$(EPOCROOT)/epoc32/release/armv5/urel/fuzzv5.exe",
		"$(EPOCROOT)/epoc32/release/armv5/udeb/fuzzlib.lib",
		"$(EPOCROOT)/epoc32/release/armv5/urel/fuzzlib.lib"
		]
	t.addbuildtargets("smoke_suite/test_resources/mmp/mmp5/bld.inf", [
		"fuzzv5_exe/armv5/udeb/fuzzv5.o",
		"fuzzv5_exe/armv5/urel/fuzzv5.o",
		"fuzzlib_lib/armv5/udeb/uc_exe_.cpp",
		"fuzzlib_lib/armv5/urel/uc_exe_.cpp",
		"fuzzlib_lib/armv5/udeb/uc_exe_.o",
		"fuzzlib_lib/armv5/urel/uc_exe_.o",
		])
	t.run()

	t.name = "mmp_diagsuppress_armlibs"
	t.command = "sbs -b smoke_suite/test_resources/mmp/mmp6_7/bld.inf -c armv5 -k -p diagsuppress.mmp -f-"
	t.targets = [
		"$(EPOCROOT)/epoc32/release/armv5/udeb/diagsuppress_test.dll",
		"$(EPOCROOT)/epoc32/release/armv5/urel/diagsuppress_test.dll",
		]
	t.mustmatch = [
					"--diag_suppress 6780",
					"--diag_suppress 6331"
					]
	t.run()
	
	t.name = "mmp_diagsuppress_no_armlibs"
	t.command = "sbs -b smoke_suite/test_resources/mmp/mmp6_7/bld.inf -c armv5 -k -p diagsuppress_noarmlibs.mmp -f-"
	t.targets = [
		"$(EPOCROOT)/epoc32/release/armv5/urel/diagsuppress_noarmlibs_test.dll",
		"$(EPOCROOT)/epoc32/release/armv5/udeb/diagsuppress_noarmlibs_test.dll"
		]
	t.mustmatch = ["--diag_suppress 6331"]
	t.mustnotmatch = ["--diag_suppress 6780"]
	t.run()

	# Test keyword: version
	t.name = "mmp_version_keyword"
	t.command = "sbs -b smoke_suite/test_resources/mmp/mmp8/bld.inf"
	t.targets = [
		"$(EPOCROOT)/epoc32/release/armv5/urel/test_mmp_version.exe",
		"$(EPOCROOT)/epoc32/release/armv5/udeb/test_mmp_version.exe",
		"$(EPOCROOT)/epoc32/release/winscw/urel/test_mmp_version.exe",
		"$(EPOCROOT)/epoc32/release/winscw/udeb/test_mmp_version.exe"
		]
	t.mustmatch = []
	t.mustnotmatch = []
	t.warnings = 2
	t.run()

	# Test keyword: armfpu softvfp|vfpv2
	# Both armv5 RVCT and GCCE builds are covered, as they differ in behaviour.
	t.name = "mmp_armfpu_softvfp_rvct"
	t.command = "sbs -b $(SBS_HOME)/test/smoke_suite/test_resources/mmp/mmp9_10/bld.inf -p armfpu_soft.mmp -c armv5_urel -f-"			
	t.targets = []
	t.mustmatch = ["--fpu softvfp", "--fpu=softvfp"]
	t.mustnotmatch = ["--fpu vfpv2", "--fpu softvfp\+", "--fpu=vfpv2", "--fpu=softvfp\+"]
	t.warnings = 0
	t.run()
		
	t.name = "mmp_armfpu_vfpv2_rvct"
	t.command = "sbs -b $(SBS_HOME)/test/smoke_suite/test_resources/mmp/mmp9_10/bld.inf -c armv5_urel REALLYCLEAN &&" \
			+ " sbs -b $(SBS_HOME)/test/smoke_suite/test_resources/mmp/mmp9_10/bld.inf -p armfpu_vfpv2.mmp -c armv5_urel -f-"

	t.mustmatch = ["--fpu vfpv2", "--fpu=vfpv2"]
	t.mustnotmatch = ["--fpu softvfp", "--fpu=softvfp"]	
	t.run()
	
	t.name = "mmp_armfpu_softvfp+vfpv2_rvct"
	t.command = "sbs -b $(SBS_HOME)/test/smoke_suite/test_resources/mmp/mmp9_10/bld.inf -c armv5_urel REALLYCLEAN &&" \
			+ " sbs -b $(SBS_HOME)/test/smoke_suite/test_resources/mmp/mmp9_10/bld.inf -p \"armfpu_soft+vfpv2.mmp\" -c armv5_urel -f-"

	t.mustmatch = ["--fpu softvfp\+vfpv2", "--fpu=vfpv2"]
	t.mustnotmatch = ["--fpu vfpv2", "--fpu softvfp ", "--fpu=softvfp"]
	t.run()

	t.name = "mmp_armfpu_softvfp+vfpv2_gcce"
	t.command = "sbs -b $(SBS_HOME)/test/smoke_suite/test_resources/mmp/mmp9_10/bld.inf  -c armv5_urel_gcce4_3_2 REALLYCLEAN &&" \
			+ " sbs -b $(SBS_HOME)/test/smoke_suite/test_resources/mmp/mmp9_10/bld.inf -c armv5_urel_gcce4_3_2 -f-"
	t.countmatch = [
		["-mfloat-abi=soft", 3],
		["--fpu=softvfp", 3] # gcce doesn't vary according to ARMFPU currently
	]
	t.mustmatch = []
	t.mustnotmatch = ["--fpu=vfpv2", "--fpu=softvfp\+"]
	t.run()
	
	t.name = "mmp_armfpu_softvfp+vfpv3_rvct"
	t.command = "sbs -b $(SBS_HOME)/test/smoke_suite/test_resources/mmp/mmp9_10/bld2.inf -c arm.v5.urel.rvct4_0 REALLYCLEAN &&" \
			+ " sbs -b $(SBS_HOME)/test/smoke_suite/test_resources/mmp/mmp9_10/bld2.inf -c arm.v5.urel.rvct4_0 -f- --mo=-n"
	t.countmatch = [
		["elf2e32.*--fpu=vfpv3", 1],
		["armcc.*--fpu.softvfp\+vfpv3", 1]
	]
	t.mustmatch = []
	t.mustnotmatch = ["--fpu=vfpv2", "--fpu=softvfp\+"]
	t.run()
	
	t.name = "mmp_armfpu_softvfp+vfpv3_gcce"
	t.command = "sbs -b $(SBS_HOME)/test/smoke_suite/test_resources/mmp/mmp9_10/bld2.inf  -c armv5_urel_gcce4_4_1 REALLYCLEAN &&" \
			+ " sbs -b $(SBS_HOME)/test/smoke_suite/test_resources/mmp/mmp9_10/bld2.inf -c armv5_urel_gcce4_4_1 -f- --mo=-n"
	t.countmatch = [
		["g\+\+.*-mfloat-abi=soft", 1],
		["elf2e32.*--fpu=softvfp", 1] # gcce doesn't vary according to ARMFPU currently
	]
	t.mustmatch = []
	t.mustnotmatch = ["--fpu=vfpv2", "--fpu=softvfp\+"]
	t.run()
	
	# Test keywords: compresstarget, nocompresstarget, bytepaircompresstarget, inflatecompresstarget
	t.name = "mmp_byte_compression_target_keywords"
	t.command = "sbs -b $(SBS_HOME)/test/smoke_suite/test_resources/mmp/mmp11/bld.inf -c armv5_urel -f-"
	t.mustmatch_singleline = [
		"elf2e32.*--output.*\/compress\.exe.*--compressionmethod=inflate",
		"elf2e32.*--output.*\/nocompress\.exe.*--uncompressed",
		"elf2e32.*--output.*\/bytepaircompress\.exe.*--compressionmethod=bytepair",
		"elf2e32.*--output.*\/inflatecompress\.exe.*--compressionmethod=inflate",
		"elf2e32.*--output.*\/combinedcompress\.exe.*--compressionmethod=bytepair",		
		"COMPRESSTARGET keyword in .*combinedcompresstarget.mmp overrides earlier use of NOCOMPRESSTARGET",
		"INFLATECOMPRESSTARGET keyword in .*combinedcompresstarget.mmp overrides earlier use of COMPRESSTARGET",
		"BYTEPAIRCOMPRESSTARGET keyword in .*combinedcompresstarget.mmp overrides earlier use of INFLATECOMPRESSTARGET"
	]
	t.countmatch = []
	t.mustnotmatch = []
	t.warnings = 3
	t.run()

	# Test keyword: APPLY
	t.name = "mmp_apply"
	t.command = "sbs -b smoke_suite/test_resources/mmp/apply/bld.inf -f- -k --configpath=test/config"
	t.targets = [
		"$(EPOCROOT)/epoc32/release/armv5/urel/test_mmp_apply.exe",
		"$(EPOCROOT)/epoc32/release/armv5/udeb/test_mmp_apply.exe",
		"$(EPOCROOT)/epoc32/release/winscw/urel/test_mmp_apply.exe",
		"$(EPOCROOT)/epoc32/release/winscw/udeb/test_mmp_apply.exe"
		]
	t.mustmatch_singleline = ["-DAPPLYTESTEXPORTEDVAR",
	                          "-DAPPLYTESTAPPENDCDEFS",
	                          "-DSINGLE=1",
	                          "-DDOUBLE"]
	t.countmatch = [["<error.*APPLY unknown variant 'no_such_var'", 2],
				    ["<error.*MACRO names cannot start with a digit '2'", 2]]
	t.errors = 2 # no_such_var for armv5 and winscw
	t.errors += 2 # macro '2' error for armv5 and winscw
	t.warnings = 0
	t.returncode = 1
	t.run()

	# Test keyword: EPOCNESTEDEXCEPTIONS
	t.name = "mmp_epocnestedexceptions"
	t.command = "sbs -b smoke_suite/test_resources/mmp/epocnestedexceptions/bld.inf -c armv5_udeb -f-"

	# When EPOCNESTEDEXCEPTIONS is specified in the MMP file, a different static
	# run-time library should be used.
	t.mustmatch_singleline = ["usrt_nx_\d_\d\.lib"]
	t.mustnotmatch = ["usrt._.."]

	t.countmatch = []

	# The new static run-time libraries don't yet exist.
	t.errors = 1
	t.warnings = 1
	t.targets = []

	t.run()
	
	# Test keyword: DOCUMENT
	t.name = "mmp_keyword_document"
	# Note: in t.command, the makefile is cat'd through sed to remove the .DEFAULT double-colon rule's <warning> tag to ensure that t.run succeeds.
	t.command = "sbs -b smoke_suite/test_resources/mmp/mmp1/group/bld.inf -c armv5 reallyclean; " + \
				"sbs -b smoke_suite/test_resources/mmp/mmp1/group/bld.inf --no-depend-generate -c armv5_urel -m ${SBSMAKEFILE}; " + \
				"cat ${SBSMAKEFILE}_all.default"
	
	t.mustmatch_singleline = ["DOCUMENT:=.*test/smoke_suite/test_resources/mmp/mmp1/src/file01\.txt\\s+.*test/smoke_suite/test_resources/mmp/mmp1/src/file02\.txt"]
	t.mustnotmatch = []
	t.countmatch = []
	
	t.errors = 0
	t.warnings = 0
	t.returncode = 0
	t.targets = []
	
	t.run()
	
	t.name = "mmp_keywords"
	t.print_result()
	return t

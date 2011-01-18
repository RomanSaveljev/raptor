#
# Copyright (c) 2009-2010 Nokia Corporation and/or its subsidiary(-ies).
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

	cmd_prefix = "sbs -b smoke_suite/test_resources/simple_paging/bld.inf -c armv5_urel "
	cmd_suffix = " -m ${SBSMAKEFILE} -f ${SBSLOGFILE} && cat ${SBSLOGFILE} "

	t.name = "paging_default"
	t.command = cmd_prefix + "-p default.mmp" + cmd_suffix
	t.mustmatch_singleline = [
			"--codepaging=default", 
			"--datapaging=default"
			]
	t.run()

	t.name = "paging_unpaged"
	t.command = cmd_prefix + "-p unpaged.mmp" + cmd_suffix
	t.mustmatch_singleline = [
			"--codepaging=unpaged", 
			"--datapaging=unpaged"
			]
	t.run()

	# these tests have no "compression" keywords so we are testing that the right
	# defaults are used.
	#
	# PAGEDCODE implies BYTEPAIRCOMPRESSTARGET
	# UNPAGEDCODE implies INFLATECOMPRESSTARGET
	
	t.name = "paging_paged"
	t.command = cmd_prefix + "-p paged.mmp" + cmd_suffix
	t.mustmatch_singleline = [
			"--codepaging=paged", 
			"--datapaging=default",
			"--compressionmethod=bytepair"
			]
	t.mustnotmatch = [
			"--compressionmethod=inflate",
			"--uncompressed"
			]
	t.run()

	t.name = "paging_unpagedcode_pageddata"
	t.command = cmd_prefix + "-p unpagedcode_pageddata.mmp" + cmd_suffix
	t.mustmatch_singleline = [
			"--codepaging=unpaged", 
			"--datapaging=paged",
			"--compressionmethod=inflate"
			]
	t.mustnotmatch = [
			"--compressionmethod=bytepair",
			"--uncompressed"
			]
	t.run()

	t.name = "paging_pagedcode_unpageddata"
	t.command = cmd_prefix + "-p pagedcode_unpageddata.mmp" + cmd_suffix
	t.mustmatch_singleline = [
			"--codepaging=paged", 
			"--datapaging=unpaged",
			"--compressionmethod=bytepair"
			]
	t.mustnotmatch = [
			"--compressionmethod=inflate",
			"--uncompressed"
			]
	t.run()

	t.name = "paging_pagedcode_defaultdata"
	t.command = cmd_prefix + "-p pagedcode_defaultdata.mmp" + cmd_suffix
	t.mustmatch_singleline = [
			"--codepaging=paged", 
			"--datapaging=default",
			"--compressionmethod=bytepair"
			]
	t.mustnotmatch = [
			"--compressionmethod=inflate",
			"--uncompressed"
			]
	t.run()

	t.name = "paging_paged_unpaged_no_bytepair"
	t.command = cmd_prefix + "-p paged_unpaged.mmp" + cmd_suffix
	t.mustmatch_singleline = [
			"--codepaging=unpaged", 
			"--datapaging=unpaged",
			"--compressionmethod=inflate"
			]
	t.mustnotmatch = [
			"--compressionmethod=bytepair",
			"--uncompressed"
			]
	t.warnings = 2 # 1 in the log and 1 on screen
	t.run()

	# now we test that the "compression" keywords interact correctly with
	# the "code paging" keywords.
	#
	# PAGEDCODE can only support BYTEPAIRCOMPRESSTARGET or UNCOMPRESSTARGET
	
	t.name = "paging_pagedcode_compress"
	t.command = cmd_prefix + "-p pagedcode_compress.mmp" + cmd_suffix
	t.mustmatch_singleline = [
			"--codepaging=paged", 
			"--datapaging=default",
			"--compressionmethod=bytepair"
			]
	t.mustnotmatch = [
			"--compressionmethod=inflate",
			"--uncompressed"
			]
	t.warnings = 2
	t.run()
	
	t.name = "paging_unpagedcode_compress"
	t.command = cmd_prefix + "-p unpagedcode_compress.mmp" + cmd_suffix
	t.mustmatch_singleline = [
			"--codepaging=unpaged", 
			"--datapaging=default",
			"--compressionmethod=inflate"
			]
	t.mustnotmatch = [
			"--compressionmethod=bytepair",
			"--uncompressed"
			]
	t.warnings = 0
	t.run()
	
	t.name = "paging_pagedcode_uncompress"
	t.command = cmd_prefix + "-p pagedcode_uncompress.mmp" + cmd_suffix
	t.mustmatch_singleline = [
			"--codepaging=paged", 
			"--datapaging=default",
			"--uncompressed"
			]
	t.mustnotmatch = [
			"--compressionmethod=bytepair",
			"--compressionmethod=inflate"
			]
	t.warnings = 0
	t.run()
	
	t.name = "paging_unpagedcode_uncompress"
	t.command = cmd_prefix + "-p unpagedcode_uncompress.mmp" + cmd_suffix
	t.mustmatch_singleline = [
			"--codepaging=unpaged", 
			"--datapaging=default",
			"--uncompressed"
			]
	t.mustnotmatch = [
			"--compressionmethod=bytepair",
			"--compressionmethod=inflate"
			]
	t.warnings = 0
	t.run()
	
	t.name = "paging_pagedcode_bytepair"
	t.command = cmd_prefix + "-p pagedcode_bytepair.mmp" + cmd_suffix
	t.mustmatch_singleline = [
			"--codepaging=paged", 
			"--datapaging=default",
			"--compressionmethod=bytepair"
			]
	t.mustnotmatch = [
			"--compressionmethod=inflate",
			"--uncompressed"
			]
	t.warnings = 0
	t.run()
	
	t.name = "paging_unpagedcode_bytepair"
	t.command = cmd_prefix + "-p unpagedcode_bytepair.mmp" + cmd_suffix
	t.mustmatch_singleline = [
			"--codepaging=unpaged", 
			"--datapaging=default",
			"--compressionmethod=bytepair"
			]
	t.mustnotmatch = [
			"--uncompressed",
			"--compressionmethod=inflate"
			]
	t.warnings = 0
	t.run()
	
	t.name = "paging_pagedcode_inflate"
	t.command = cmd_prefix + "-p pagedcode_inflate.mmp" + cmd_suffix
	t.mustmatch_singleline = [
			"--codepaging=paged", 
			"--datapaging=default",
			"--compressionmethod=bytepair"
			]
	t.mustnotmatch = [
			"--compressionmethod=inflate",
			"--uncompressed"
			]
	t.warnings = 2
	t.run()
	
	t.name = "paging_unpagedcode_inflate"
	t.command = cmd_prefix + "-p unpagedcode_inflate.mmp" + cmd_suffix
	t.mustmatch_singleline = [
			"--codepaging=unpaged", 
			"--datapaging=default",
			"--compressionmethod=inflate"
			]
	t.mustnotmatch = [
			"--uncompressed",
			"--compressionmethod=bytepair"
			]
	t.warnings = 0
	t.run()
	
	# test the pre-WDP paging options --paged and --unpaged
	# there is an os_properties.xml file in test/config that
	# turns POSTLINKER_SUPPORTS_WDP off
	
	t.name = "paging_paged_no_wdp"
	t.command = cmd_prefix + "-p paged.mmp --configpath=test/config" + cmd_suffix
	t.mustmatch_singleline = [
			"--paged", 
			"--compressionmethod=bytepair"
			]
	t.mustnotmatch = [
			"--compressionmethod=inflate"	
			]
	t.warnings = 0
	t.targets = [ "$(EPOCROOT)/epoc32/release/armv5/urel/paged.dll" ]
	t.run()
	
	t.name = "paging_unpaged_no_wdp"
	t.command = cmd_prefix + "-p unpaged.mmp --configpath=test/config" + cmd_suffix
	t.mustmatch_singleline = [
			"--unpaged", 
			"--compressionmethod=inflate"
			]
	t.mustnotmatch = [
			"--compressionmethod=bytepair"	
			]
	t.targets = [ "$(EPOCROOT)/epoc32/release/armv5/urel/unpaged.dll" ]
	t.run()
	
	t.name = "paging"
	t.print_result()
	return t


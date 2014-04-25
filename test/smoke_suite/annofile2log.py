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

from raptor_tests import SmokeTest

def run():
	t = SmokeTest()
	t.name = "annofile2log_copy_from_log"
	t.description = "test workaround for log corruption from a make engine whose name begins with 'e'"
	command = 'cd smoke_suite/test_resources/annofile2log && ( FROMANNO="`mktemp`" ; bzip2 -dc {test_file_basename}.anno.bz2 ' \
			  ' | python testanno2log.py  >"${{FROMANNO}}" && FROMSTDOUT="`mktemp`"; bzip2 -dc {test_file_basename}.stdout.bz2 > ' \
			  '"${{FROMSTDOUT}}" && diff -wB "${{FROMANNO}}" "${{FROMSTDOUT}}"; RET=$? ; rm "${{FROMANNO}}" "${{FROMSTDOUT}}"; exit $RET )'
	
	t.usebash = True
	t.errors = 0
	t.returncode = 0
	t.exceptions = 0
	t.command = command.format(test_file_basename = "scrubbed_ncp_dfs_resource") 
	
	t.run()
	
	t.name = "annofile2log_new_format_annofile"
	t.description = "test new format of annofile"
	t.usebash = True
	t.errors = 0
	t.returncode = 0
	t.exceptions = 0
	t.command = command.format(test_file_basename = "scrubbed_ncp_dfs_resource_new") 
	
	t.run()
	
	t.print_result()
	return t

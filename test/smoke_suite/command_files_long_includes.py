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
import os
import shutil
import sys

def run():
	# Templates for header files, source files and the MMP file. 
	header_file_template_file = "smoke_suite/test_resources/source_templates/header_file.h"	
	source_file_template_file = "smoke_suite/test_resources/source_templates/source_file.cpp"
	mmp_file_template_file = "smoke_suite/test_resources/source_templates/mmp_file.mmp"
	
	# Read the templates
	header_file_template = None	
	with open(header_file_template_file, "r") as f:
		header_file_template = "".join(f)
	
	source_file_template = None	
	with open(source_file_template_file, "r") as f:
		source_file_template = "".join(f)
	
	mmp_file_template = None	
	with open(mmp_file_template_file, "r") as f:
		mmp_file_template = "".join(f)
	
	# Form the include directory paths and make them
	inc_dirs = []
	mmp_inc_dirs = []
	source_files = []
	for i in range(0, 65): # 65 items is enough to break the limit
		inc_dir = os.path.join("smoke_suite", "test_resources", "source_templates", 
							"{0:02d}".format(i) * 10, "x" * 50, "y" * 50, "z" * 50)
		if not os.path.isdir(inc_dir):
			os.makedirs(inc_dir)
		inc_dirs.append(inc_dir)
		# The MMP inc dirs are relative to the bld.inf, not $SBS_HOME/test
		mmp_inc_dirs.append(os.path.join("{0:02d}".format(i) * 10, "x" * 50, "y" * 50, "z" * 50))
		
		header_path = os.path.join(inc_dir, "test{0:02d}.h".format(i))
		with open(header_path, "w") as f:
			s = header_file_template.format(i)
			f.write(header_file_template.format(i))
		
		# Write the source files
		source_path = os.path.join("smoke_suite", "test_resources", "source_templates", 
								"test{0:02d}.cpp".format(i))
		source_files.append(source_path)
		with open(source_path, "w") as f:
			f.write(source_file_template.format(i))
	
	
	# Add the generates source files and include directories to the
	# MMP file and write the template to a file
	mmp_file_template += "\n"
	for inc in mmp_inc_dirs:
		mmp_file_template += "SYSTEMINCLUDE\t{0}\n".format(inc)
	
	for src in source_files:
		mmp_file_template += "SOURCE\t{0}\n".format(os.path.basename(src))
	
	mmp_path = os.path.join("smoke_suite", "test_resources", "source_templates", "long_command_lines.mmp")
	with open(mmp_path, "w") as f:
		f.write(mmp_file_template)
	
	# The actual build test
	t = SmokeTest()
	t.name = "command_files_long_includes"	
	t.description = """Ensure that command files are used ."""
	t.command = "sbs -b smoke_suite/test_resources/source_templates/bld.inf -c armv7_urel -c winscw_udeb"	
	t.targets = [
				"$(EPOCROOT)/epoc32/release/winscw/udeb/test_long_command_lines.exe",
				"$(EPOCROOT)/epoc32/release/armv7/urel/test_long_command_lines.exe",
				]
	
	t.run()
		
	# Clean up all generated files and directories
	for dir in inc_dirs:
		top_level_dir = os.path.normpath(os.path.join(dir, "..", "..", ".."))
		shutil.rmtree(top_level_dir, ignore_errors = True)
	
	for src in source_files:
		try:
			os.remove(src)
		except:
			pass
	
	return t

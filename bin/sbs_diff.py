#!/usr/bin/env python

# Copyright (c) 2010-2011 Nokia Corporation and/or its subsidiary(-ies). 
# All rights reserved.
# This component and the accompanying materials are made available
# under the terms of "Eclipse Public License v1.0"
# which accompanies this distribution, and is available
# at the URL "http://www.eclipse.org/legal/epl-v10.html".
#
# Initial Contributors:
# Nokia Corporation - initial contribution.
#
# Contributors:
# 
# Description:

"""
Compare the raptor XML logs from two builds and produce a short report.

Works on Linux; and on Windows with Cygwin.
"""

import optparse
import os
import sys

parser = optparse.OptionParser(usage = """%prog [options] dir_or_file1 dir_or_file2

When a directory is specified, all the logs in that directory are combined into
a single file for comparison. If a single file is specified then only that one
file is compared.""")

parser.add_option("--force", action="store_true", default=False, help =
    "Re-read the original logs, do not use the intermediate files generated "
    "by a previous run of this script. The default is '%default'."
				)

parser.add_option("--verbose", action="store_true", default=False, help =
    "Print out information about the processing as we go. Some very big builds "
    "can take more than ten minutes to run over. The default is '%default'."
	   			)

# parse the command-line arguments
(options, leftover_args) = parser.parse_args()

# there should be exactly 2 leftover_args
if len(leftover_args) == 2:
	build_a = leftover_args[0]
	build_b = leftover_args[1]
else:
	sys.stderr.write("error: expected 2 names, got '{0}'\n".format(", ".join(leftover_args)))
	sys.exit(1)

# raptor packages are in ../python relative to this script
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "python"))
#
import allo.diff
	
# generate the intermediate .csv files which make it possible to compare
# the two builds.
log_a = allo.diff.DiffableLog(build_a, options.force, options.verbose)
log_b = allo.diff.DiffableLog(build_b, options.force, options.verbose)

# now do the comparison
log_diff = allo.diff.LogDiff(log_a, log_b)

if log_diff.has_differences():
	sys.exit(1) # the builds are different

sys.exit(0) # the builds are probably equivalent

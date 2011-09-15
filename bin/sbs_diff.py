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
"""

import optparse
import os
import sys

import sbs_env
import allo.diff

parser = optparse.OptionParser(usage = """%prog [options] dir_or_file1 dir_or_file2

When a directory is specified, all the logs in that directory are combined into
a single file for comparison. If a single file is specified then only that one
file is compared.""")

parser.add_option("--force", action="store_true", default=False, help =
    "Re-read the original logs, do not use the intermediate files generated "
    "by a previous run of this script. The default is '%default'."
				)
parser.add_option("--limit", action="store", type=int, default=0, help =
    "If you have particularly huge error or warning messages then the CSV "
    "reader may bomb out. This parameter, if greater than zero, can be used "
    "to increase the maximum field size to whatever you need. "
    "The default is '%default'."
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

# generate the intermediate files which make it possible to compare the builds
log_a = allo.diff.DiffableLog(build_a, **options.__dict__)
log_b = allo.diff.DiffableLog(build_b, **options.__dict__)

# now do the comparison
log_diff = allo.diff.LogDiff(log_a, log_b)

# print the short report. it gives a good idea of how similar the results are
print("\nComponent differences (if any) ======================================")
for (bldinf, counts) in log_diff.components.items():
	if counts[0] != counts[1]:
		print("{0:>8} {1:<8} {2}".format(counts[0], counts[1], bldinf))

print("\nOverall totals ======================================================")
for (event, counts) in log_diff.events.items():
	print("{0:>8} {1:<8} {2}".format(counts[0], counts[1], event))

# take the detailed diff and create diff_left.txt and diff_right.txt
# which should be manageable by a graphical diff tool. we trim the size
# by replacing blocks of matching lines with "== block 1", "== block 2" etc.
different = log_diff.dump_to_files("diff_left.txt", "diff_right.txt")

if different:
	print("\nThe build logs are different.")
	sys.exit(1)

print("\nThe build logs are probably equivalent.")
sys.exit(0)

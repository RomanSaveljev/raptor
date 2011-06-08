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

# raptor packages are in ../python relative to this script
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "python"))
#
import allo.diff

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

different = False    # are the logs different at all
sameblock = False    # are we on a run of matching lines
block = 0

with open("diff_left.txt", "wb") as file_a:
	with open("diff_right.txt", "wb") as file_b:

		for line in log_diff:
			if line[1] == allo.diff.LogDiff.FIRST:
				file_a.write(line[0])
				sameblock = False
				different = True
			elif line[1] == allo.diff.LogDiff.SECOND:
				file_b.write(line[0])
				sameblock = False
				different = True
			elif not sameblock:    # allo.diff.LogDiff.BOTH
				sameblock = True
				block += 1
				file_a.write("== block {0}\n".format(block))
				file_b.write("== block {0}\n".format(block))
		
if different:
	print("\nThe build logs are different.")
	sys.exit(1)

print("\nThe build logs are probably equivalent.")
sys.exit(0)

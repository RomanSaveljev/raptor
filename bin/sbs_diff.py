#!/usr/bin/env python

# Copyright (c) 2010 Nokia Corporation and/or its subsidiary(-ies). 
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
import shutil
import subprocess
import sys

parser = optparse.OptionParser(usage = """%prog [options] dir_or_file1 dir_or_file2

When a directory is specified, all the logs in that directory are combined into
a single file for comparison. If a single file is specified then only that one
file is compared.""")

parser.add_option("--debug", default=False, help =
    "Print out info on how the processing is done. The default is '%default'."
				)
	  
parser.add_option("--verbose", default=False, help =
    "Print out more rather than less information. The default is '%default'."
				)

# parse the command-line arguments
(options, leftover_args) = parser.parse_args()

# there should be exactly 2 leftover_args
if len(leftover_args) != 2:
	for leftover in leftover_args:
		sys.stderr.write("warning: unexpected argument '%s'\n" % leftover)
	sys.exit(1)
else:
	left_param = leftover_args[0]
	right_param = leftover_args[1]

def generate_csv(dir_or_file, prefix):
	pass

# generate all.csv and totals.csv for left and right builds.
generate_csv(left_param, "left_")
generate_csv(right_param, "right_")

sys.exit(0)

def is_raptor_log(path):
	try:
		with open(path, "r") as f:
			line1 = f.readline()
			line2 = f.readline()
			return line1.startswith("<?xml") and line2.startswith("<buildlog")
	except:
		return False

def join_dir(filename):
	return os.path.join(options.directory, filename)

# search the given directory for a list of raptor log files
logs = filter(is_raptor_log, map(join_dir, os.listdir(options.directory)))

print "found", len(logs), "raptor log files"
if len(logs) < 1:
	sys.exit(0)
	
# run the CSV filter on each log file
cmd_template = "sbs_filter --filters=csv[{0}] -f {1} < {2}"
tmp_template = "/tmp/csv_gather_{0}.csv"

csvs = []
for i,f in enumerate(logs):
	tmpfile = tmp_template.format(i)
	command = cmd_template.format(options.params, tmpfile, f)
	print command
	returncode = subprocess.call(command, shell=True)
	if returncode != 0:
		sys.stderr.write("FAILED: {0}\n".format(command))
		sys.exit(1)
	csvs.append(tmpfile)
	
# cat all the temporary CSV files together and output the sorted result
catsort = "cat {0} | sort > {1}".format(" ".join(csvs), options.output)
print catsort
				
returncode = subprocess.call(catsort, shell=True)
if returncode != 0:
	sys.stderr.write("FAILED: {0}\n".format(catsort))
	sys.exit(1)

# run csv_totals on the "big" file to create an easier starting point
csvtotals = "csv_totals.py < {0} | sort > {1}".format(options.output, options.totals)
print csvtotals
				
returncode = subprocess.call(csvtotals, shell=True)
if returncode != 0:
	sys.stderr.write("FAILED: {0}\n".format(csvtotals))
	sys.exit(1)
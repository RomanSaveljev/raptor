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

import csv
import optparse
import os
import subprocess
import sys

parser = optparse.OptionParser(usage = """%prog [options] dir_or_file1 dir_or_file2

When a directory is specified, all the logs in that directory are combined into
a single file for comparison. If a single file is specified then only that one
file is compared.""")

parser.add_option("--debug", action="store_true", default=False, help =
    "Print out info on how the processing is done. The default is '%default'."
				)

parser.add_option("--use_intermediate", action="store_true", default=False, help =
    "Do not re-read the original logs, use the intermediate files generated "
    "by a previous run of this script. Useful for debugging and for turning "
    "up the verbosity without rescanning all the logs. The default is '%default'."
				)
 
parser.add_option("--verbose", action="store_true", default=False, help =
    "Print out more rather than less information. The default is '%default'."
				)

# parse the command-line arguments
(options, leftover_args) = parser.parse_args()

# there should be exactly 2 leftover_args
if len(leftover_args) == 2:
	left_param = leftover_args[0]
	right_param = leftover_args[1]
elif not options.use_intermediate:
	sys.stderr.write("error: expected 2 names, got\n")
	for leftover in leftover_args:
		sys.stderr.write("       {0}\n".format(leftover))
	sys.exit(1)

def generate_csv(dir_or_file, prefix):
	sorted_file = prefix + "all.csv"
	totals_file = prefix + "totals.csv"
	
	if os.path.isfile(dir_or_file):
		input_file = dir_or_file
		
		# run the CSV filter on this one log file and sort the result
		csvfilter = "sbs_filter --filters=csv[ok] -f- < {0} | sort > {1}".format(input_file, sorted_file)
		if options.debug:
			print( csvfilter )
		returncode = subprocess.call(csvfilter, shell=True)
		if returncode != 0:
			sys.stderr.write("FAILED: {0}\n".format(csvfilter))
			return
		
		# run csv_totals on the sorted csv file to create a summary
		csvtotals = "csv_totals.py < {0} | sort > {1}".format(sorted_file, totals_file)
		if options.debug:
			print( csvtotals )
		returncode = subprocess.call(csvtotals, shell=True)
		if returncode != 0:
			sys.stderr.write("FAILED: {0}\n".format(csvtotals))
			return
	
	elif os.path.isdir(dir_or_file):
		input_dir = dir_or_file
		
		# for a directory, csv_gather can collect everything for us
		csvgather = "csv_gather.py --dir={0} --output={1} --totals={2}".format(input_dir, sorted_file, totals_file)
		if options.debug:
			print( csvgather )
		returncode = subprocess.call(csvgather, shell=True)
		if returncode != 0:
			sys.stderr.write("FAILED: {0}\n".format(csvgather))
			return
		
	else:
		sys.stderr.write("error: {0} is not a file or a directory\n".format(dir_or_file))
		return

# generate all.csv and totals.csv for left and right builds.
if not options.use_intermediate:
	generate_csv(left_param, "left_")
	generate_csv(right_param, "right_")

def summarise_totals(filename):
	events = {}
	reader = csv.reader(open(filename, "rb"))
	for row in reader:
		event = row[0]
		if event in events:
			events[event] += 1
		else:
			events[event] = 1
	return events
		
left_summary = summarise_totals("left_totals.csv")
right_summary = summarise_totals("right_totals.csv")

print("\nOverall totals\n=============")
for event in ["error", "critical", "warning", "remark", "missing"]:
	if event in left_summary:
		left_number = left_summary[event]
	else:
		left_number = 0
		
	if event in right_summary:
		right_number = right_summary[event]
	else:
		right_number = 0
			
	print("\t{0:<10}:{1:>10}{2:>10}".format(event, left_number, right_number))

sys.exit(0)

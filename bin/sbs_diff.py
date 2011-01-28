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

parser.add_option("--use-intermediate", action="store_true", dest="use_intermediate", default=False, help =
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
	sys.stderr.write("error: expected 2 names, got '{0}'\n".format(",".join(leftover_args)))
	sys.exit(1)

def generate_csv(dir_or_file, prefix):
	sorted_file = prefix + "all.csv"
	totals_file = prefix + "totals.csv"
	
	if os.path.isfile(dir_or_file):
		input_file = dir_or_file
		
		# run the CSV filter on this one log file and sort the result
		csvfilter = "sbs_filter --filters=csv[ok] -f- < {0} | sort | uniq > {1}".format(input_file, sorted_file)
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
	components = {}
	
	reader = csv.reader(open(filename, "rb"))
	for row in reader:
		count = int(row[3])
		
		event = row[0]
		if event in events:
			events[event] += count
		else:
			events[event] = count
			
		bldinf = row[1]
		if bldinf in components:
			components[bldinf] += count
		else:
			components[bldinf] = count
			
	return (events, components)
		
left_summary = summarise_totals("left_totals.csv")
right_summary = summarise_totals("right_totals.csv")

# Component differences (if any)
bldinfs = set(left_summary[1].keys()) | set(right_summary[1].keys())
different_components = {}
for bldinf in bldinfs:
	if bldinf in left_summary[1]:
		left_number = left_summary[1][bldinf]
	else:
		left_number = 0
		
	if bldinf in right_summary[1]:
		right_number = right_summary[1][bldinf]
	else:
		right_number = 0

	if left_number != right_number:	
		different_components[bldinf] = (left_number, right_number)

if different_components:
	print("\nComponent totals (where different)\n==================================")
	widest = max(different_components, key=len)

	for bldinf in sorted(different_components.keys()):
		print("{0:<{w}}:{v[0]:>8}{v[1]:>8}".format(bldinf, v=different_components[bldinf], w=len(widest)+1))

print("\nOverall totals\n==============")
for event in ["error", "critical", "warning", "remark", "missing"]:
	if event in left_summary[0]:
		left_number = left_summary[0][event]
	else:
		left_number = 0
		
	if event in right_summary[0]:
		right_number = right_summary[0][event]
	else:
		right_number = 0
			
	print("{0:<9}:{1:>8}{2:>8}".format(event, left_number, right_number))

# now create left_diff.txt and right_diff.txt which are all the errors, warnings
# etc. from left_all.csv which are not the same in right_all.csv and vice-versa.
#
# these are .txt because the lines are reformatted for easier reading in a 
# graphical tool (e.g. NEWLINE strings are replaced by \n)
#
# note that these files are not necessarily empty if the totals are all the
# same - because there may be the same number of errors in both builds by
# fluke and they could be totally different sets of errors.

left_file = open("left_all.csv", "r")
right_file = open("right_all.csv", "r")

left_diff = open("left_diff.txt", "w")
right_diff = open("right_diff.txt", "w")

# we know that the files are sorted, so we can step through both line by line
left_line = left_file.readline()
right_line = right_file.readline()
common = False
while left_line or right_line:
	if left_line == right_line:
		common = True
		left_diff.write("=")
		right_diff.write("=")
		left_line = left_file.readline()
		right_line = right_file.readline()
	elif left_line < right_line or not right_line:
		# close off the line of =
		if common:
			left_diff.write("\n") 
			right_diff.write("\n")
		common = False
		# left is missing from right
		left_diff.write(left_line.replace("NEWLINE","\n"))
		left_line = left_file.readline()
	else:
		# close off the line of =
		if common:
			left_diff.write("\n") 
			right_diff.write("\n")
		common = False
		# right is missing from left
		right_diff.write(right_line.replace("NEWLINE","\n"))
		right_line = right_file.readline()
		
left_diff.close()
right_diff.close()
	
left_file.close()
right_file.close()

sys.exit(0)

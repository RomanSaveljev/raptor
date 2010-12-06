#!/usr/bin/python

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
Gather up all the raptor XML logs in a given directory and convert them
into a single sorted .csv file.

Works on Linux; and on Windows with Cygwin.
"""

import optparse
import os
import shutil
import subprocess
import sys

parser = optparse.OptionParser()
	  
parser.add_option("--directory", default=".", help =
    "The directory to search for raptor log files. The default is '%default'."
				)
parser.add_option("--output", default="raptor_all.csv", help =
    "The output .csv file name for all the collected log data. "
    "This is the 'one big file' that probably needs further processing. "
    "The default is '%default'."
				)
parser.add_option("--params", default="ok", help =
    "The parameters to pass to the CSV filter. This is a comma-separated "
    "list of the event types to exclude from the .csv output. The common "
    "types are: ok, error, critical, warning, remark, missing. The default "
    "is '%default'."
				)
parser.add_option("--totals", default="raptor_totals.csv", help =
    "The output .csv file name for the result of running csv_totals on the "
    "main --output file. This gives a shorter summary of the build in terms "
    "of events per component, so gives you a clue as to how to process the "
    "'one big file' to get the details you need. The default is '%default'."
				)

# parse the command-line arguments
(options, leftover_args) = parser.parse_args()

# there should not be any leftover_args
for leftover in leftover_args:
	sys.stderr.write("warning: unexpected argument '%s'\n" % leftover)

# on windows we need to explicitly add "bash -c" to the command
add_shell = sys.platform.startswith("win")

def is_raptor_log(path):
	try:
		with open(path, "r") as f:
			line1 = f.readline()
			line2 = f.readline()
			return line1.startswith("<?xml") and line2.startswith("<buildlog")
	except:
		return False

def join_dir(filename):
	return os.path.join(options.directory, filename.replace("\\", "/"))

def bash_script(script):
	if add_shell:
		return 'bash -c "{0}"'.format(script)
	return script

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
	command = bash_script(cmd_template.format(options.params, tmpfile, f))
	print command
	returncode = subprocess.call(command, shell=not add_shell)
	if returncode != 0:
		sys.stderr.write("FAILED: {0}\n".format(command))
		sys.exit(1)
	csvs.append(tmpfile)
	
# cat all the temporary CSV files together and output the sorted result
catsort = bash_script("cat {0} | sort > {1}".format(" ".join(csvs), options.output))
print catsort
				
returncode = subprocess.call(catsort, shell=not add_shell)
if returncode != 0:
	sys.stderr.write("FAILED: {0}\n".format(catsort))
	sys.exit(1)

# run csv_totals on the "big" file to create an easier starting point
csvtotals = bash_script("csv_totals.py < {0} | sort > {1}".format(options.output, options.totals))
print csvtotals
				
returncode = subprocess.call(csvtotals, shell=not add_shell)
if returncode != 0:
	sys.stderr.write("FAILED: {0}\n".format(csvtotals))
	sys.exit(1)
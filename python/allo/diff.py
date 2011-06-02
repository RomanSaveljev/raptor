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
Compare the raptor XML logs from multiple builds.
"""

import csv
import generic_path
import os
import subprocess
import sys
import plugins.filter_csv


def is_raptor_log(path):
	try:
		with open(path, "r") as f:
			line1 = f.readline()
			line2 = f.readline()
			return line1.startswith("<?xml") and line2.startswith("<buildlog")
	except:
		return False
	

class NotADiffableLog(Exception):
	pass


class CSVFilterParams(object):
	def __init__(self, csv_file):
		self.logFileName = generic_path.Path(csv_file)
		self.timestring = ""
		self.configPath = ""
		

class DiffableLog(object):
	"""Represents a raptor log, or set of logs, in a way that can be compared
	to another nominally similar log (or set of logs) from a different build."""
	
	def __init__(self, dir_or_file, force=False, verbose=False):
		"""If force=True the class will not reuse any cached information that
		it finds in the specified directory: instead it will re-read the original
		logs and generate a new cache."""
		
		self.location = dir_or_file
		self.force = force
		self.verbose = verbose
		self.logs = []
		
		# find all the raptor logs that are in the running
		if os.path.isfile(dir_or_file):
			self.add_file(dir_or_file)
			
		elif os.path.isdir(dir_or_file):
			for file in os.listdir(dir_or_file):
				self.add_file(os.path.join(dir_or_file, file))
		else:
			raise NotADiffableLog("'{0}' is not a file or a directory\n".format(dir_or_file))
	
		if len(self.logs) > 0:
			if self.verbose:
				print("found {0} raptor logs".format(len(self.logs)))
		else:
			raise NotADiffableLog("no raptor logs found in '{0}'\n".format(dir_or_file))
		
		# generate all the .csv files that are missing or out of date
		for log_file in self.logs:
			csv_file = self.csv_for(log_file)
			if self.force or not os.path.isfile(csv_file) \
			or os.path.getmtime(log_file) > os.path.getmtime(csv_file):
				self.generate_csv(log_file, csv_file)

	def add_file(self, path):
		if is_raptor_log(path):
			self.logs.append(path)
			if self.verbose:
				print(path + " is a raptor log")
	
	def csv_for(self, path):
		return path + "_diff.csv"
	
	def generate_csv(self, log_file, csv_file):
		if self.verbose:
			print("generating " + csv_file)
			
		filter = plugins.filter_csv.CSV(["ok"])    # ignore "ok" recipes
		filter_params = CSVFilterParams(csv_file)
		
		try:
			filter.open(filter_params)
			
			with open(log_file, "r") as file:
				for line in file.readlines():
					filter.write(line)

			filter.summary()
			filter.close()

		except Exception,e:
			raise NotADiffableLog("problem filtering '{0}' : {1}\n".format(log_file, str(e)))


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

class LogDiff(object):
	def __init__(self, log_a, log_b):
		pass

	def has_differences(self):
		return True
	
skip = """
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

if different_components:
	sys.exit(1) # the builds are different

sys.exit(0) # the builds are probably equivalent
"""
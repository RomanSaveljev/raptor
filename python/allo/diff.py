#!/usr/bin/env python

# Copyright (c) 2011 Nokia Corporation and/or its subsidiary(-ies). 
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
import os
import sys

import allo.utils
import generic_path
import plugins.filter_csv


# we don't want to create a Raptor object just for these 2 variables
sbs_home = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
cfg_path = os.path.join("lib", "config")


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
		self.configPath = [ generic_path.Path(cfg_path) ]
		self.home = generic_path.Path(sbs_home)
		

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
		new_csv_files = False
		all_csv_files = []
		for log_file in self.logs:
			csv_file = log_file + ".csv"
			all_csv_files.append(csv_file)
			
			if self.force or not os.path.isfile(csv_file) \
			or os.path.getmtime(log_file) > os.path.getmtime(csv_file):
				self.generate_csv(log_file, csv_file)
				new_csv_files = True

		# combine multiple .csv files into one big one
		all_csv_files.sort()
		csv_cat = all_csv_files[0] + ".cat"
		if new_csv_files or not os.path.isfile(csv_cat):
			allo.utils.cat(all_csv_files, csv_cat)

		# sort the big .csv file
		csv_sort = csv_cat + ".sort"
		if new_csv_files or not os.path.isfile(csv_sort):
			allo.utils.sort(csv_cat, csv_sort)
		
		# remove duplicate lines from the big .csv file
		self.csv = csv_sort + ".uniq"
		if new_csv_files or not os.path.isfile(self.csv):
			allo.utils.uniq(csv_sort, self.csv)
		
		if self.verbose:
			print("combined log " + self.csv)

		# add up the per-component and per-event totals
		self.summarise()
		
	def add_file(self, path):
		if is_raptor_log(path):
			self.logs.append(path)
			if self.verbose:
				print(path + " is a raptor log")
	
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

	def summarise(self):
		self.events = {}
		self.components = {}
	
		reader = csv.reader(open(self.csv, "rb"))
		for row in reader:
		
			event = row[0]
			if event == "info" and row[2] == "version":
				self.raptor_version = row[3]
				continue
			
			if event in self.events:
				self.events[event] += 1
			else:
				self.events[event] = 1
			
			bldinf = row[1]
			if bldinf in self.components:
				self.components[bldinf] += 1
			else:
				self.components[bldinf] = 1
			
		if self.verbose:
			for (event, count) in self.events.items():
				print("{0} : {1}".format(event, count))
			print("{0} components".format(len(self.components)))

			
class LogDiff(object):
	FIRST  = 1
	SECOND = 2
	BOTH   = 3
	
	def __init__(self, log_a, log_b):
		self.log_a = log_a
		self.log_b = log_b
		
		# compare the summaries

		# component totals
		bldinfs = set(log_a.components.keys()) | set(log_b.components.keys())
		self.components = {}
		for bldinf in bldinfs:
			if bldinf in log_a.components:
				na = log_a.components[bldinf]
			else:
				na = 0
		
			if bldinf in log_b.components:
				nb = log_b.components[bldinf]
			else:
				nb = 0

			self.components[bldinf] = (na, nb)
			
		# event totals
		events = set(log_a.events.keys()) | set(log_b.events.keys())
		self.events = {}
		for event in events:
			if event in log_a.events:
				na = log_a.events[event]
			else:
				na = 0
		
			if event in log_b.events:
				nb = log_b.events[event]
			else:
				nb = 0

			self.events[event] = (na, nb)

	def __iter__(self):
		"""an iterator for stepping through the detailed differences."""
		return LogDiffIterator(self)


class LogDiffIterator(object):
	def __init__(self, log_diff):
		# we know that the files are sorted, so we can step through both line by line
		self.file_a = open(log_diff.log_a.csv, "rb")
		self.file_b = open(log_diff.log_b.csv, "rb")
		
		self.line_a = self.file_a.readline()
		self.line_b = self.file_b.readline()
		
	def __iter__(self):
		return self
	
	def next(self):
		if self.line_a:
			if self.line_b:
				if self.line_a == self.line_b:
					value_pair = (self.line_a, LogDiff.BOTH)
					self.line_a = self.file_a.readline()
					self.line_b = self.file_b.readline()
				elif self.line_a < self.line_b:
					value_pair = (self.line_a, LogDiff.FIRST)
					self.line_a = self.file_a.readline()
				else:
					value_pair = (self.line_b, LogDiff.SECOND)
					self.line_b = self.file_b.readline()
			else:
				value_pair = (self.line_a, LogDiff.FIRST)
				self.line_a = self.file_a.readline()
		elif self.line_b:
			value_pair = (self.line_b, LogDiff.SECOND)
			self.line_b = self.file_b.readline()
		else:
			self.file_a.close()
			self.file_b.close()
			raise StopIteration
			
		return value_pair

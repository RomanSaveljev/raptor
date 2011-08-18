#
# Copyright (c) 2009 - 2011 Nokia Corporation and/or its subsidiary(-ies).
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
# Runs the specified suite of raptor tests

import os
import sys
import re
import imp
import datetime
import stat
import traceback

raptor_tests = imp.load_source("raptor_tests", "common/raptor_tests.py")

test_run_start_time = datetime.datetime.now()

# Command line options ########################################################
from optparse import OptionParser

parser = OptionParser(
		prog = "run",
		usage = "%prog [Options]")

parser.add_option("-s", "--suite", action = "store", type = "string",
		dest = "suite", help = "regex to use for selecting test suites")
parser.add_option("-t", "--tests", action = "store", type = "string",
		dest = "tests", help = "regex to use for selecting tests")
parser.add_option("-d", "--debug", action = "store_true", dest = "debug_mode",
		default = False, help = "Turns on debug-mode")
parser.add_option("--test-home", action = "store", type = "string",
		dest = "test_home", default="default",
		help = "Location of custom .sbs_init.xml (name of directory in " +
		"'custom_options'): test/custom_options/<test_home>/.sbs_init.xml")
parser.add_option("--what-failed", action = "store_true", dest = "what_failed",
		help = "Re-run all the tests that failed in the previous test run")
parser.add_option("--clean", action = "store_true", dest = "clean",
		help = "Clean EPOCROOT after each test is run")


(options, args) = parser.parse_args()

# Allow flagless test regex
if (options.tests == None) and (len(args) > 0):
	options.tests = args[len(args) - 1]

if options.debug_mode:
	raptor_tests.activate_debug()


# Set $HOME environment variable for finding a custom .sbs_init.xml 
if options.test_home != None:
	home_dir = options.test_home
	if home_dir in os.listdir("./custom_options"):
		os.environ["HOME"] = os.environ["SBS_HOME"] + "/test/custom_options/" \
				+ home_dir + "/"
	else:
		print("Warning: Path to custom .sbs_init.xml file not found (" + \
				home_dir + ")\nUsing defaults...")
		options.test_home = None


def format_milliseconds(microseconds):
	""" format a microsecond time in milliseconds """
	milliseconds = (microseconds / 1000)
	if milliseconds == 0:
		return "000"
	elif milliseconds < 10:
		return "00" + str(milliseconds)
	elif milliseconds < 100:
		return "0" + str(milliseconds)
	return milliseconds



class TestRun(object):
	"""Represents any series of tests"""
	def __init__(self):
		self.test_suites = []
		self.passed_tests = []
		self.failed_tests = []
		self.error_tests = []
		self.pass_total = 0
		self.fail_total = 0
		self.skip_total = 0
		self.exception_total = 0
		self.test_total = 0

	def aggregate(self, test_suite):
		""" Aggregate other test results into this one """
		self.test_suites.append(test_suite)
		self.test_total += len(test_suite.test_set)
		self.pass_total += test_suite.pass_total
		self.fail_total += test_suite.fail_total
		self.skip_total += test_suite.skip_total
		self.exception_total += test_suite.exception_total

	def show(self):
		for test_suite in self.test_suites:
			print("\n\n{0:s}\n".format(str(test_suite.suite_dir)))
				
			if len(test_suite.test_set) < 1:
				print("No tests run")
			else:
				print("PASSED: {0:d}".format(test_suite.pass_total))
				print("FAILED: {0:d}".format(test_suite.fail_total))
				if test_suite.skip_total > 0:
					print("SKIPPED: {0:d}".format(test_suite.skip_total))
				if test_suite.exception_total > 0:
					print("EXCEPTIONS: {0:d}".format(test_suite.exception_total))
		
				if test_suite.fail_total > 0:
					print("\nFAILED TESTS:")
					
					# Add each failed test to what_failed and print it
					for test in test_suite.failed_tests:
						print("\t{0}".format(test))
		
				if test_suite.exception_total > 0:
					print("\nERRONEOUS TESTS:")
					
					# Add each erroneous test to what_failed and print it
					for test in test_suite.error_tests:
						print("\t{0}".format(test))

	def read_what_failed(self):
		""" Read and parse the what_failed file, to determine which tests
		failed last time round.

		Format of the what_failed file is:
		test-suite-name-1
			test-name-1
			test-name-2
			test-name-3
		test-suite-name-2
			test-name-4
			test-name-5
		Each test suite is listed unindented followed by the tests that belong
		to it and failed, each indented with a single tab.
		"""
		self.previous_failures = {}
		try:
			with open("what_failed", "r") as what_failed:
				# any tests specified before a suite is specified go in
				# unnamed_suite. This means the file is corrupt.
				unnamed_suite = set()
				suite = unnamed_suite
				for line in what_failed.readlines():
					line = line.rstrip();
					if line[0] == '\t':
						suite.add(line[1:])
					else:
						if line not in self.previous_failures:
							self.previous_failures[line] = set()
						suite = self.previous_failures[line]
				if unnamed_suite:
					print("ERROR: what_failed corrupt; does not begin with a suite name")
		except IOError as e:
			# If what_failed file is not present, that's OK.
			pass


	def write_what_failed(self):
		"Recreate the file for --what-failed"
		with open("what_failed", "w") as what_failed:
			updated_failures = self.previous_failures.copy()
			for test_suite in self.test_suites:
				dir = test_suite.suite_dir
				# calculate updated suite failures as previous_failures[dir]
				# minus newly-passing tests plus newly-failing tests
				suite_failures = set()
				if dir in self.previous_failures:
					suite_failures = set(self.previous_failures[dir])
				suite_failures.difference_update(set(test_suite.passed_tests))
				suite_failures.update(set(test_suite.failed_tests))
				suite_failures.update(set(test_suite.error_tests))
				updated_failures[dir] = suite_failures

			for dir in sorted(updated_failures.keys()):
				# write any failures that remain to what_failed
				suite_failures = updated_failures[dir]
				if suite_failures:
					what_failed.write(dir + "\n")
					for t in sorted(suite_failures):
						what_failed.write("\t" + t + "\n")
					
class TestFile(object):
	def __init__(self, name, module):
		self.name = name
		self.module = module
		self.ok = True
		if module == None:
			self.ok = False
		self.errormessage=""

class BadTestResult(object):
	"""Represent a test that failed """
	def __init__(self):
		self.result = raptor_tests.SmokeTest.FAIL

class Suite(TestRun):
	""" A set of tests (.py files) in a directory """

	python_file_regex = re.compile("(?P<base>.*)\.py$", re.I)

	def __init__(self, dir, test_file_regex = '.*', allowable_test_set = None):
		""" A suite of tests in self.suite_dir. The tests that are run are all
		those in allowable_test_set that also match test_file_regex.
		If allowable_test_set is None, then all tests that match test_file_regex
		are run.
		"""

		TestRun.__init__(self)
		self.suite_dir = dir

		# Regex for searching for tests
		self.test_file_regex = test_file_regex
		self.allowable_test_set = allowable_test_set
		

	def run(self):
		"""run the suite"""

		self.time_stamp = datetime.datetime.now()
		self.results = {}
		self.start_times = {}
		self.end_times = {}
		self.test_set = []

		print("\n\nRunning " + str(self.suite_dir) + "...")

		# Iterate through all files in specified directory
		for test in os.listdir(self.suite_dir):
			# Only check '*.py' files
			name_match = self.python_file_regex.match(test)
			if name_match is not None:
				# extract base name (without the .py)
				import_name = name_match.group('base')
				matches_regex = (self.test_file_regex is None
						or self.test_file_regex.match(test))
				is_allowable = (self.allowable_test_set is None
						or import_name in self.allowable_test_set)
				if matches_regex and is_allowable:
					try:
						self.test_set.append( TestFile(import_name,
								imp.load_source(
									import_name,
									(raptor_tests.ReplaceEnvs(
										self.suite_dir + "/" + test)))))
					except:
						# Still create a testfile entry - keeps the numbering
						# of tests consistent which is a small convenience
						tf = TestFile(import_name, None)
						self.test_set.append(tf)
						tf.errormessage = traceback.format_exc(None)
	
		test_number = 0
		test_total = len(self.test_set)
		# Run each test, capturing all its details and its results
		for test_file in self.test_set:
			test_number += 1

				
			# Save start/end times and save in dictionary for TMS
			start_time = datetime.datetime.now()
			try:
				test_number_text = ("\n\nTEST " + str(test_number) + "/" +
						str(test_total) + ":")
				
				if self.fail_total > 0:
					test_number_text += ("    So far " + str(self.fail_total) +
							" FAILED")
				if self.exception_total > 0:
					test_number_text += ("    So far " + str(self.exception_total) +
							" ERRONEOUS")
				
				print(test_number_text)
				
				# Remember tests that could not be loaded
				# or were bad from the start for some reason
				if not test_file.ok:
					test_object = BadTestResult();
					print(tf.errormessage)
					print("TEST FAILED\n")
				else:
					test_object = test_file.module.run()
				
				end_time = datetime.datetime.now()
				
				# No millisecond function, so need to use microseconds/1000	
				start_milliseconds = start_time.microsecond
				end_milliseconds = end_time.microsecond
		
				# Add trailing 0's if required
				start_milliseconds = \
						format_milliseconds(start_milliseconds)
				end_milliseconds = \
						format_milliseconds(end_milliseconds)
		
				self.start_times[test_file.name] = start_time.strftime("%H:%M:%S:" +
						str(start_milliseconds))
				self.end_times[test_file.name] = end_time.strftime("%H:%M:%S:" +
						str(end_milliseconds))
				
				run_time = (end_time - start_time)
				
				run_time_seconds = (str(run_time.seconds) + "." +
						str(format_milliseconds(run_time.microseconds)))
				print("RunTime: " + run_time_seconds + "s")
				# Add to pass/fail count and save result to dictionary
				if test_object.result == raptor_tests.SmokeTest.PASS:
					self.pass_total += 1
					self.results[test_file.name] = "Passed"
					self.passed_tests.append(test_file.name)
				elif test_object.result == raptor_tests.SmokeTest.FAIL:
					self.fail_total += 1
					self.results[test_file.name] = "Failed"
					self.failed_tests.append(test_file.name)
				elif test_object.result == raptor_tests.SmokeTest.SKIP:
					self.skip_total += 1
				# Clean epocroot after running each test if --clean option is specified
				if options.clean:
					print("\nCLEANING TEST RESULTS...")
					raptor_tests.clean_epocroot()
					
			except:
				print("\nTEST ERROR:")
				traceback.print_exc(None, sys.stdout)    # None => all levels
				self.exception_total += 1
				self.error_tests.append(test_file.name)

		end_time_stamp = datetime.datetime.now()

		runtime = end_time_stamp - self.time_stamp
		seconds = (str(runtime.seconds) + "." +
				str(format_milliseconds(runtime.microseconds)))

		print("\n" + str(self.suite_dir) + " RunTime: " + seconds + "s")



class SuiteRun(TestRun):
	""" Represents a 'run' of a number of test suites """

	def __init__(self, suitepattern = None, testpattern = None,
			what_failed = False):
		TestRun.__init__(self)
		
		# Add common directory to list of paths to search for modules
		sys.path.append(raptor_tests.ReplaceEnvs("$(SBS_HOME)/test/common"))
		
		
		if suitepattern:
			self.suite_regex = re.compile(".*" + suitepattern + ".*", re.I)
		else:
			self.suite_regex = re.compile(".*\_suite$", re.I)

		if testpattern:
			self.test_file_regex = re.compile(".*" + testpattern + ".*",
					re.I)
		else:
			self.test_file_regex = None

		self.suitepattern = suitepattern
		self.what_failed = what_failed


	def _run_suite(self, dir):
		""" runs suite 'dir' if it is in what_failed (returning 1)
		or returns 0 without running anything if it is not. """
		s = None
		if self.what_failed:
			if dir in self.previous_failures:
				# run all tests listed in what_failed
				s = Suite(dir, self.test_file_regex,
						self.previous_failures[dir])
			else:
				# this suite not in what_failed
				return 0
		else:
			# not using --what-failed; run them all
			s = Suite(dir, self.test_file_regex)
		s.run()
		self.aggregate(s)
		return 1


	def run_tests(self):
		"""
		Run all the tests in the specified suite (directory)
		"""

		self.read_what_failed()	
		suiteCount = 0;
		for dir in os.listdir("."):
			if os.path.isdir(dir) and self.suite_regex.match(dir):
				suiteCount += self._run_suite(dir)
		
		# Print which options were used
		if options.test_home == None:
			options_dir = "defaults)"
		else:
			options_dir = "'" + options.test_home + "' options file)"
		print("\nTests run using {0}".format(options_dir))

		# Summarise the entire test run
		if self.suitepattern and (suiteCount == 0):
			print("\nNo suites matched specification '" + self.suitepattern + \
					"'\n")
		else:
			print("Overall summary ({0:d} suites, {1:d} tests):".format(
					suiteCount, self.test_total))
			self.show()
			self.write_what_failed()


# Make SBS_HOME, EPOCROOT have uppercase drive letters to match os.getcwd() and
# thus stop all those insane test problems which result from one being uppercase
# and the other lowercase

if sys.platform.startswith("win"):
	sh = os.environ['SBS_HOME']
	if sh[1] == ':':
		os.environ['SBS_HOME'] = sh[0].upper() + sh[1:]
	er = os.environ['EPOCROOT']
	if er[1] == ':':
		os.environ['EPOCROOT'] = er[0].upper() + er[1:]

# Clean epocroot before running tests
raptor_tests.clean_epocroot()
run_tests = SuiteRun(suitepattern = options.suite, testpattern = options.tests,
		what_failed = options.what_failed)
run_tests.run_tests()

duration = datetime.datetime.now() - test_run_start_time
print("\nTotal test run time: {0}\n".format(duration))

if run_tests.fail_total + run_tests.exception_total != 0:
	sys.exit(1)

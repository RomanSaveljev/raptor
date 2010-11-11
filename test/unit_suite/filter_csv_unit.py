
# Copyright (c) 2010 Nokia Corporation and/or its subsidiary(-ies).
# All rights reserved.
# This component and the accompanying materials are made available
# under the terms of the License "Eclipse Public License v1.0"
# which accompanies this distribution, and is available
# at the URL "http://www.eclipse.org/legal/epl-v10.html".

'''
Test the CSV class in plugins/filter_html.py
'''

import os
import sys
import unittest

test_data = os.path.join(os.getcwd(),"unit_suite","data","html_filter")

# add the plugins directory to the python path
sys.path.append(os.path.join(os.environ['SBS_HOME'], "python", "plugins"))
# so that we can import the filter module directly
import filter_html
import generic_path

class Mock(object):
	'''empty object for attaching arbitrary attributes and functions.'''
	pass
	
class TestFilterCsv(unittest.TestCase):
	'''test cases for the CSV log filter.
	
	This is a minimal set of tests for starters. As people start using this
	filter and reporting bugs and niggles we can add test cases here to
	avoid regressions.'''
	
	def setUp(self):
		self.mock_params = Mock()
		self.mock_params.configPath = [generic_path.Path("config")]
		self.mock_params.home = generic_path.Path(test_data)
		self.mock_params.logFileName = generic_path.Path("tmp/foo")
		self.mock_params.timestring = "now"
		
		# where do we expect the output to be written
		self.csv_file = str(self.mock_params.logFileName) + ".csv"
		
	def tearDown(self):
		'''remove the generated output file.'''
		if os.path.isfile(self.csv_file):
			os.unlink(self.csv_file)
	
	def testPass(self):
		'''are the setUp and tearDown methods sane.'''
		pass
	
	def testConstructor(self):
		'''simply construct a a CSV object.'''
		csv = filter_html.CSV()
	
	def readcsv(self):
		csv = open(self.csv_file)
		self.lines = [i.strip() for i in csv.readlines()]
		print "LINES", self.lines
		csv.close()
		return len(self.lines)
	
	def checkfor(self, csvstring):
		return csvstring in self.lines
	
	def testMinimalLog(self):
		'''process a minimal log file.'''
		csv = filter_html.CSV()
		self.assertTrue( csv.open(self.mock_params) )
		self.assertTrue( csv.write('<?xml version="1.0" encoding="ISO-8859-1" ?>\n') )
		self.assertTrue( csv.write('<buildlog sbs_version="2.99.9 [hi]">') )
		self.assertTrue( csv.write('</buildlog>') )
		self.assertTrue( csv.close() )
		
		self.assertTrue( os.path.isfile(self.csv_file) )
		
		self.assertEqual(self.readcsv(), 1)
		self.assertTrue( self.checkfor('info,sbs,version,"2.99.9 [hi]"') )
		
	def testMultilineRecipe(self):
		'''recipes can have more than one line of text.'''
		csv = filter_html.CSV()
		self.assertTrue( csv.open(self.mock_params) )
		self.assertTrue( csv.write('<?xml version="1.0" encoding="ISO-8859-1" ?>\n') )
		self.assertTrue( csv.write('<buildlog sbs_version="2.99.9 [hi]">\n') )
		self.assertTrue( csv.write('<recipe bldinf="BLDINF" config="ARM">\n') )
		self.assertTrue( csv.write('+ cd /\n') )
		self.assertTrue( csv.write('+ rm -rf *\n') )
		self.assertTrue( csv.write('<status exit="ok" code="0"/>\n') )
		self.assertTrue( csv.write('</recipe>\n') )
		self.assertTrue( csv.write('</buildlog>\n') )
		self.assertTrue( csv.close() )
		
		self.assertTrue( os.path.isfile(self.csv_file) )
		
		self.assertEqual(self.readcsv(), 2)
		self.assertTrue( self.checkfor('ok,BLDINF,ARM,"+ cd /NEWLINE+ rm -rf *"') )
		
	def testBadExitCode(self):
		'''some tools print errors but exit with 0.'''
		csv = filter_html.CSV()
		self.assertTrue( csv.open(self.mock_params) )
		self.assertTrue( csv.write('<?xml version="1.0" encoding="ISO-8859-1" ?>\n') )
		self.assertTrue( csv.write('<buildlog sbs_version="2.99.9 [hi]">\n') )
		self.assertTrue( csv.write('<recipe bldinf="B" config="A">\n') )
		self.assertTrue( csv.write('+ evil.pl\n') )
		self.assertTrue( csv.write('ERROR: cannot do evil\n') )
		self.assertTrue( csv.write('<status exit="ok" code="0"/>\n') )
		self.assertTrue( csv.write('</recipe>\n') )
		self.assertTrue( csv.write('</buildlog>\n') )
		self.assertTrue( csv.close() )
		
		self.assertTrue( os.path.isfile(self.csv_file) )
		
		self.assertEqual(self.readcsv(), 2 )
		self.assertTrue( self.checkfor('error,B,A,"+ evil.plNEWLINEERROR: cannot do evil"') )
	
	def testErrorTag(self):
		'''error and warning elements should be included.'''
		csv = filter_html.CSV()
		self.assertTrue( csv.open(self.mock_params) )
		self.assertTrue( csv.write('<?xml version="1.0" encoding="ISO-8859-1" ?>\n') )
		self.assertTrue( csv.write('<buildlog sbs_version="2.99.9 [hi]">\n') )
		self.assertTrue( csv.write('<error bldinf="A">ouch</error>\n') )
		self.assertTrue( csv.write('<warning bldinf="B">that is odd</warning>\n') )
		self.assertTrue( csv.write('</buildlog>\n') )
		self.assertTrue( csv.close() )
		
		self.assertTrue( os.path.isfile(self.csv_file) )
		
		self.assertEqual(self.readcsv(), 3 )
		self.assertTrue( self.checkfor('error,A,unknown,"ouch"') )
		self.assertTrue( self.checkfor('warning,B,unknown,"that is odd"') )
		
	def testExclusions(self):
		'''parameters to exclude message types.'''
		csv = filter_html.CSV(['ok', 'remark'])
		self.assertTrue( csv.open(self.mock_params) )
		self.assertTrue( csv.write('<?xml version="1.0" encoding="ISO-8859-1" ?>\n') )
		self.assertTrue( csv.write('<buildlog sbs_version="2.99.9 [hi]">\n') )
		self.assertTrue( csv.write('<error bldinf="A">ouch</error>\n') )
		
		self.assertTrue( csv.write('<recipe bldinf="BLDINF" config="ARM">\n') )
		self.assertTrue( csv.write('+ true') )
		self.assertTrue( csv.write('<status exit="ok" code="0"/>\n') )
		self.assertTrue( csv.write('</recipe>\n') )
		
		self.assertTrue( csv.write('<recipe bldinf="BLDINF" config="ARM">\n') )
		self.assertTrue( csv.write('REMARK: what?') )
		self.assertTrue( csv.write('<status exit="ok" code="0"/>\n') )
		self.assertTrue( csv.write('</recipe>\n') )
		
		self.assertTrue( csv.write('<warning bldinf="B">that is odd</warning>\n') )
		self.assertTrue( csv.write('</buildlog>\n') )
		self.assertTrue( csv.close() )
		
		self.assertTrue( os.path.isfile(self.csv_file) )
		
		self.assertEqual(self.readcsv(), 3 )
		self.assertTrue( self.checkfor('error,A,unknown,"ouch"') )
		self.assertTrue( self.checkfor('warning,B,unknown,"that is odd"') )
		
# run all the tests

from raptor_tests import SmokeTest

def run():
	t = SmokeTest()
	t.name = "filter_csv_unit"

	tests = unittest.makeSuite(TestFilterCsv)
	result = unittest.TextTestRunner(verbosity=2).run(tests)

	if result.wasSuccessful():
		t.result = SmokeTest.PASS
	else:
		t.result = SmokeTest.FAIL

	return t

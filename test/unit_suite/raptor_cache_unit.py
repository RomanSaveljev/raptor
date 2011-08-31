#
# Copyright (c) 2009-2011 Nokia Corporation and/or its subsidiary(-ies).
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
# Unit test for raptor.cache module

import os.path
import unittest

import raptor.build
import raptor.cache
from raptor import generic_path

class TestRaptorCache(unittest.TestCase):

	def setUp(self):
		self.raptor = raptor.build.Raptor()
		self.cache = self.raptor.cache

		dir = self.raptor.home.Append("test", "config")
		self.cache.Load(dir)
		
	def testLoadSingle(self):
		# load a single XML file
		file = self.raptor.home.Append("test/unit_suite/data", raptor.build.xml)
		self.cache.Load(file)
		self.failUnless(len(self.cache.variants) > 0)
		self.failUnless(len(self.cache.aliases) > 0)
		self.failUnless(len(self.cache.groups) > 0)
		
	def testVariant(self):
		def _testSingleVariant(name):
			try:
				var = self.cache.FindNamedVariant(name)
			except KeyError:
				self.fail()
			else:
				self.failUnless(var)
				self.assertEqual(var.name, name)

		_testSingleVariant("ARMV5_BASE")
		_testSingleVariant("ARMV5_UREL")
		_testSingleVariant("ARMV5_UDEB")
		_testSingleVariant("MOD1")
		_testSingleVariant("MOD2")
		_testSingleVariant("var_redef")

		self.failUnlessRaises( KeyError, self.cache.FindNamedVariant, "XY_123" )
		self.failUnlessRaises( KeyError, self.cache.FindNamedVariant, "ARMV5" )

	def testAlias(self):
		def _testSingleAlias(name):
			try:
				alias = self.cache.FindNamedAlias(name)
			except KeyError:
				self.fail()
			else:
				self.failUnless(alias)
				self.assertEqual(alias.name, name)

		_testSingleAlias("ALIAS_1")
		_testSingleAlias("ALIAS_2")
		_testSingleAlias("alias_redef")

		self.failUnlessRaises( KeyError, self.cache.FindNamedAlias, "XY_123" )
		self.failUnlessRaises( KeyError, self.cache.FindNamedAlias, "ARMV5" )
		self.failUnlessRaises( KeyError, self.cache.FindNamedAlias, "ARMV5_UREL" )

	def testGroup(self):
		def _testSingleGroup(name):
			try:
				group = self.cache.FindNamedGroup(name)
			except KeyError:
				self.fail()
			else:
				self.failUnless(group)
				self.assertEqual(group.name, name)
				
		_testSingleGroup("ARMV5")
		_testSingleGroup("group_redef")

		self.failUnlessRaises( KeyError, self.cache.FindNamedGroup, "XY_123" )
		self.failUnlessRaises( KeyError, self.cache.FindNamedGroup, "ARMV5_UDEB" )
		self.failUnlessRaises( KeyError, self.cache.FindNamedGroup, "ARMV5_UREL" )

	def testInterface(self):
		def _testSingleInterface(name):
			try:
				interface = self.cache.FindNamedInterface(name)
			except KeyError:
				self.fail()
			else:
				self.failUnless(interface)
				self.assertEqual(interface.name, name)
				
		_testSingleInterface("interface_redef")

		self.failUnlessRaises( KeyError, self.cache.FindNamedInterface, "foo" )
		self.failUnlessRaises( KeyError, self.cache.FindNamedInterface, "bar" )
		self.failUnlessRaises( KeyError, self.cache.FindNamedInterface, "123" )

# run all the tests

from raptor_tests import SmokeTest

def run():
	t = SmokeTest()
	t.id = "999"
	t.name = "raptor_cache_unit"

	tests = unittest.makeSuite(TestRaptorCache)
	result = unittest.TextTestRunner(verbosity=2).run(tests)

	if result.wasSuccessful():
		t.result = SmokeTest.PASS
	else:
		t.result = SmokeTest.FAIL

	return t

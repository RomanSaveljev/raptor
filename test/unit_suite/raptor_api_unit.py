#
# Copyright (c) 2010-2011 Nokia Corporation and/or its subsidiary(-ies).
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
# raptor_api_unit module

import generic_path
import raptor
import raptor_api
import unittest
import raptor_tests

class TestRaptorApi(unittest.TestCase):
			
	def testContext(self):
		api = raptor_api.Context()
		
	def testContextInitialiser(self):
		r = raptor.Raptor(dotargets=False)
		api = raptor_api.Context(r)
		
	def testAliases(self):
		r = raptor.Raptor(dotargets=False)
		r.cache.Load( generic_path.Join(r.home, "test", "configapi", "api.xml") )

		api = raptor_api.Context(r)
	
		aliases = api.getaliases() # type == ""
		self.failUnlessEqual(len(aliases), 4)
		self.failUnlessEqual(set(["alias_A","alias_B","s1","s2"]),
							 set(a.name for a in aliases))
		
		aliaslist = [a.name for a in aliases] # verify that the list is sorted
		self.failUnlessEqual(["alias_A","alias_B","s1","s2"], aliaslist)
		
		aliases = api.getaliases(raptor_api.ALL) # ignore type
		self.failUnlessEqual(len(aliases), 6)
		
		aliases = api.getaliases("X") # type == "X"
		self.failUnlessEqual(len(aliases), 1)
		self.failUnlessEqual(aliases[0].name, "alias_D")
		self.failUnlessEqual(aliases[0].meaning, "a.b.c.d")
	
	def testConfig(self):
		r = raptor.Raptor(dotargets=False)
		r.cache.Load( generic_path.Join(r.home, "test", "configapi", "api.xml") )

		api = raptor_api.Context(r)
		
		if r.filesystem == "unix":
			path = "/home/raptor/foo/bar"
		else:
			path = "C:/home/raptor/foo/bar"
			
		config = api.getconfig("buildme")
		self.failUnlessEqual(config.meaning, "buildme")
		self.failUnlessEqual(config.outputpath, path)
		self.failIfEqual(config.metadata, None)
		
		# metadata
				
		metadatamacros = [str(x.name+"="+x.value) if x.value else str(x.name) for x in config.metadata.platmacros]
		metadatamacros.sort()
		results = ['SBSV2=_____SBSV2', '__GNUC__=3']
		results.sort()
		self.failUnlessEqual(metadatamacros, results)
		
		includepaths = [str(x.path) for x in config.metadata.includepaths]
		includepaths.sort()

		# This result is highly dependent on the epocroot being used to test against.
		# with an SF baseline or an old Symbian one one might see this:
		# expected_includepaths = [raptor_tests.ReplaceEnvs("$(EPOCROOT)/epoc32/include/variant"), 
		#						raptor_tests.ReplaceEnvs("$(EPOCROOT)/epoc32/include"), "."

		# With another one might see: 
		expected_includepaths = [raptor_tests.ReplaceEnvs("$(EPOCROOT)/epoc32/include"), 
								raptor_tests.ReplaceEnvs("$(EPOCROOT)/epoc32/include"), "."]

		expected_includepaths.sort()
		self.failUnlessEqual(includepaths, expected_includepaths)
		
		preincludefile = str(config.metadata.preincludeheader.file)

		# Another baseline dependent result
		# self.failUnlessEqual(preincludefile, raptor_tests.ReplaceEnvs("$(EPOCROOT)/epoc32/include/variant/Symbian_OS.hrh"))
		self.failUnlessEqual(preincludefile, raptor_tests.ReplaceEnvs("$(EPOCROOT)/epoc32/include/feature_settings.hrh"))
		
		# build
		
		sourcemacros = [str(x.name+"="+x.value) if x.value else str(x.name) for x in config.build.sourcemacros]
		results = ['__BBB__', '__AAA__', '__DDD__=first_value', '__CCC__', '__DDD__=second_value']
		self.failUnlessEqual(sourcemacros, results)
		
		compilerpreincludefile = str(config.build.compilerpreincludeheader.file)
		self.failUnlessEqual(compilerpreincludefile, raptor_tests.ReplaceEnvs("$(EPOCROOT)/epoc32/include/preinclude.h"))

		expectedtypes = ["one", "two"]
		expectedtypes.sort()
		types = [t.name for t in config.build.targettypes]
		types.sort()
		self.failUnlessEqual(types, expectedtypes)

		# general

		config = api.getconfig("buildme.foo")
		self.failUnlessEqual(config.meaning, "buildme.foo")
		self.failUnlessEqual(config.outputpath, path)
		
		config = api.getconfig("s1")
		self.failUnlessEqual(config.meaning, "buildme.foo")
		self.failUnlessEqual(config.outputpath, path)
		
		config = api.getconfig("s2.product_A")
		self.failUnlessEqual(config.meaning, "buildme.foo.bar.product_A")
		self.failUnlessEqual(config.outputpath, path)
		
	def testProducts(self):
		r = raptor.Raptor(dotargets=False)
		r.cache.Load( generic_path.Join(r.home, "test", "configapi", "api.xml") )

		api = raptor_api.Context(r)
		
		products = api.getproducts() # type == "product"
		self.failUnlessEqual(len(products), 2)
		self.failUnlessEqual(set(["product_A","product_C"]),
							 set(p.name for p in products))
		productlist = [p.name for p in products] # verify that the list is sorted
		self.failUnlessEqual(["product_A","product_C"], productlist)
		
# run all the tests

from raptor_tests import SmokeTest

def run():
	t = SmokeTest()
	t.name = "raptor_api_unit"

	tests = unittest.makeSuite(TestRaptorApi)
	result = unittest.TextTestRunner(verbosity=2).run(tests)

	if result.wasSuccessful():
		t.result = SmokeTest.PASS
	else:
		t.result = SmokeTest.FAIL

	return t

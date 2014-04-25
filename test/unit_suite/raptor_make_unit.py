#
# Copyright (c) 2006-2014 Microsoft Mobile and/or its subsidiary(-ies).
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
# raptor_make_unit module
# This module tests the classes that write Makefile wrappers.
#

import os
import unittest

import raptor.build
import raptor.data
import raptor.make

class TestRaptorMake(unittest.TestCase):

	def cleanMakefiles(self, fileList):
		for file in fileList:
			name = file.GetLocalString()
			if os.path.exists(name):
				os.remove(name)
			
	def checkMakefiles(self, fileList):
		for file in fileList:
			name = file.GetLocalString()
			if not os.path.exists(name):
				print("did not find", name)
				return False
		return True
	
	def checkNotMakefiles(self, fileList):
		for file in fileList:
			name = file.GetLocalString()
			if os.path.exists(name):
				print("found unwanted", name)
				return False
		return True
	
	def testSimpleMake(self):
		# use a bare Raptor object
		aRaptor = raptor.build.Raptor()
		aRaptor._load_cache()
		aRaptor.pruneDuplicateMakefiles = False
		aRaptor.writeSingleMakefile = False
		
		# find the test directory
		testDir = aRaptor.home.Append("test", "tmp")
		
		# set up a build with a single Specification node
		spec = raptor.data.Specification("myProject")
		
		interface = raptor.data.Interface("EXE")
		interface.SetProperty("flm", "/lib/flm/exe.flm")
		interface.AddParameter(raptor.data.Parameter("EXEPARAM1"))
		interface.AddParameter(raptor.data.Parameter("EXEPARAM2"))
		interface.AddParameter(raptor.data.Parameter("EXEPARAM3"))
		spec.SetInterface(interface)
		
		svar = raptor.data.Variant("SVAR")
		svar.AddOperation(raptor.data.Set("EXEPARAM1", "parameter 1"))
		svar.AddOperation(raptor.data.Set("EXEPARAM2", "parameter 2"))
		spec.AddVariant(svar)
		
		# use a minimal Configuration
		conf = raptor.data.Variant("myConfig")
		cvar = raptor.data.Variant("CVAR")
		cvar.AddOperation(raptor.data.Set("EXEPARAM3", "parameter 3"))
		bldunit = raptor.data.BuildUnit("myConfig.CVAR",[conf,cvar])
		
		# delete any old Makefiles
		m1 = testDir.Append("Makefile")
		m2 = testDir.Append("myConfig.CVAR", "myProject", "Makefile")
		makefiles = [m1, m2]
		self.cleanMakefiles(makefiles)
		
		# create new Makefiles
		maker = raptor.make.MakeEngine(aRaptor)
		maker.Write(m1, [spec], [bldunit])
		
		# test and clean
		self.failUnless(self.checkMakefiles(makefiles))
		self.cleanMakefiles(makefiles)


	def testMultiSpecMultiConfigMake(self):
		# use a bare Raptor object
		aRaptor = raptor.build.Raptor()
		aRaptor._load_cache()
		aRaptor.pruneDuplicateMakefiles = False
		aRaptor.writeSingleMakefile = False
		
		# find the test directory
		testDir = aRaptor.home.Append("test", "tmp")
		
		interface = raptor.data.Interface("EXE")
		interface.SetProperty("flm", "/lib/flm/exe.flm")
		interface.AddParameter(raptor.data.Parameter("EXEPARAM1"))
		interface.AddParameter(raptor.data.Parameter("EXEPARAM2"))
		
		# set up a build with 2 top-level Specification nodes
		
		# top 1 has 2 sub-nodes
		top1 = raptor.data.Specification("top1")
		top1.SetInterface(interface)
		top1v = raptor.data.Variant()
		top1v.AddOperation(raptor.data.Set("EXEPARAM1", "top1 p1"))
		top1.AddVariant(top1v)
		# top 1 child 1 has 1 sub-node
		top1c1 = raptor.data.Specification("top1c1")
		top1c1.SetInterface(interface)
		top1c1v = raptor.data.Variant()
		top1c1v.AddOperation(raptor.data.Set("EXEPARAM1", "top1c1 p1"))
		top1c1.AddVariant(top1c1v)
		# top 1 child 1 child
		top1c1c = raptor.data.Specification("top1c1c")
		top1c1c.SetInterface(interface)
		top1c1cv = raptor.data.Variant()
		top1c1cv.AddOperation(raptor.data.Set("EXEPARAM1", "top1c1c p1"))
		top1c1c.AddVariant(top1c1cv)
		top1c1.AddChildSpecification(top1c1c)
		# top 1 child 2 has 1 sub-node
		top1c2 = raptor.data.Specification("top1c2")
		top1c2.SetInterface(interface)
		top1c2v = raptor.data.Variant()
		top1c2v.AddOperation(raptor.data.Set("EXEPARAM1", "top1c2 p1"))
		top1c2.AddVariant(top1c2v)
		# top 1 child 2 child
		top1c2c = raptor.data.Specification("top1c2c")
		top1c2c.SetInterface(interface)
		top1c2cv = raptor.data.Variant()
		top1c2cv.AddOperation(raptor.data.Set("EXEPARAM1", "top1c2c p1"))
		top1c2c.AddVariant(top1c2cv)
		top1c2.AddChildSpecification(top1c2c)
		#
		top1.AddChildSpecification(top1c1)
		top1.AddChildSpecification(top1c2)
		
		# top 2 has no sub-nodes
		top2 = raptor.data.Specification("top2")
		top2.SetInterface(interface)
		top2v = raptor.data.Variant()
		top2v.AddOperation(raptor.data.Set("EXEPARAM1", "top2 p1"))
		top2.AddVariant(top2v)
		#
		
		# use a pair of minimal Configurations
		
		conf1 = raptor.data.Variant("conf1")
		c1var = raptor.data.Variant()
		c1var.AddOperation(raptor.data.Set("EXEPARAM2", "conf1 p2"))
		buildunit1 = raptor.data.BuildUnit("conf1.c1var",[conf1,c1var])
		
		conf2 = raptor.data.Variant("conf2")
		c2var = raptor.data.Variant()
		c2var.AddOperation(raptor.data.Set("EXEPARAM2", "conf2 p2"))
		buildunit2 = raptor.data.BuildUnit("conf2.c2var",[conf2,c2var])
		
		# delete any old Makefiles
		makefiles = [testDir.Append("Makefile")]
		makefiles.append(testDir.Append("conf1.c1var", "top1", "Makefile"))
		makefiles.append(testDir.Append("conf1.c1var", "top1", "top1c1", "Makefile"))
		makefiles.append(testDir.Append("conf1.c1var", "top1", "top1c1", "top1c1c", "Makefile"))
		makefiles.append(testDir.Append("conf1.c1var", "top1", "top1c2", "Makefile"))
		makefiles.append(testDir.Append("conf1.c1var", "top1", "top1c2", "top1c2c", "Makefile"))
		makefiles.append(testDir.Append("conf1.c1var", "top2", "Makefile"))
		makefiles.append(testDir.Append("conf2.c2var", "top1", "Makefile"))
		makefiles.append(testDir.Append("conf2.c2var", "top1", "top1c1", "Makefile"))
		makefiles.append(testDir.Append("conf2.c2var", "top1", "top1c1", "top1c1c", "Makefile"))
		makefiles.append(testDir.Append("conf2.c2var", "top1", "top1c2", "Makefile"))
		makefiles.append(testDir.Append("conf2.c2var", "top1", "top1c2", "top1c2c", "Makefile"))
		makefiles.append(testDir.Append("conf2.c2var", "top2", "Makefile"))
		self.cleanMakefiles(makefiles)
		
		# create new Makefiles
		maker = raptor.make.MakeEngine(aRaptor)
		maker.Write(makefiles[0], [top1, top2], [buildunit1, buildunit2])
		
		# test and clean
		self.failUnless(self.checkMakefiles(makefiles))
		self.cleanMakefiles(makefiles)
		
		
	def testFilteredMake(self):
		# use a bare Raptor object
		aRaptor = raptor.build.Raptor()
		aRaptor._load_cache()
		aRaptor.pruneDuplicateMakefiles = False
		aRaptor.writeSingleMakefile = False
		aRaptor.debugOutput = True
		
		# find the test directory
		testDir = aRaptor.home.Append("test", "tmp")
		
		# the root Specification is a Filter
		top = raptor.data.Filter("top")
		
		# the test condition
		top.SetVariableCondition("SWITCH", "ARM")
		top.AddVariableCondition("TOGGLE", ["A", "B", "C"])
		top.SetConfigCondition("confA.confAv")
		top.AddConfigCondition("confB.confBv")
		
		# True part
		ifaceT = raptor.data.Interface("T.EXE")
		ifaceT.SetProperty("flm", "/lib/flm/exeT.flm")
		ifaceT.AddParameter(raptor.data.Parameter("TEXEPARAM"))
		ifaceT.AddParameter(raptor.data.Parameter("SWITCH"))
		ifaceT.AddParameter(raptor.data.Parameter("TOGGLE"))
		top.SetInterface(ifaceT)
		#
		varT = raptor.data.Variant()
		varT.AddOperation(raptor.data.Set("TEXEPARAM", "top True"))
		top.AddVariant(varT)
		#
		childT = raptor.data.Specification("Tchild")
		childT.SetInterface(ifaceT)
		childTv = raptor.data.Variant()
		childTv.AddOperation(raptor.data.Set("TEXEPARAM", "child True"))
		childT.AddVariant(childTv)
		#
		top.AddChildSpecification(childT)
		
		# False part
		ifaceF = raptor.data.Interface("F.EXE")
		ifaceF.SetProperty("flm", "/lib/flm/exeF.flm")
		ifaceF.AddParameter(raptor.data.Parameter("FEXEPARAM"))
		ifaceF.AddParameter(raptor.data.Parameter("SWITCH"))
		ifaceF.AddParameter(raptor.data.Parameter("TOGGLE"))
		top.Else.SetInterface(ifaceF)
		#
		varF = raptor.data.Variant()
		varF.AddOperation(raptor.data.Set("FEXEPARAM", "top False"))
		top.Else.AddVariant(varF)
		#
		childF = raptor.data.Specification("Fchild")
		childF.SetInterface(ifaceF)
		childFv = raptor.data.Variant()
		childFv.AddOperation(raptor.data.Set("FEXEPARAM", "child False"))
		childF.AddVariant(childFv)
		#
		top.Else.AddChildSpecification(childF)
		
		
		# Configurations
		
		confA = raptor.data.Variant("confA")	# hit
		confAv = raptor.data.Variant()
		confAv.AddOperation(raptor.data.Set("SWITCH", "confA switch"))
		confAv.AddOperation(raptor.data.Set("TOGGLE", "confA toggle"))
		b1 = raptor.data.BuildUnit("confA.confAv",[confA,confAv])
		
		confB = raptor.data.Variant("confB")	# hit
		confBv = raptor.data.Variant()
		confBv.AddOperation(raptor.data.Set("SWITCH", "confB switch"))
		confBv.AddOperation(raptor.data.Set("TOGGLE", "confB toggle"))
		b2 = raptor.data.BuildUnit("confB.confBv",[confB,confBv])
		
		confC = raptor.data.Variant("confC")
		confCv = raptor.data.Variant()
		confCv.AddOperation(raptor.data.Set("SWITCH", "confC switch"))
		confCv.AddOperation(raptor.data.Set("TOGGLE", "confC toggle"))
		b3 = raptor.data.BuildUnit("confC.confCv",[confC,confCv])
		
		confD = raptor.data.Variant("confD")
		confDv = raptor.data.Variant()
		confDv.AddOperation(raptor.data.Set("SWITCH", "ARM"))	# hit
		confDv.AddOperation(raptor.data.Set("TOGGLE", "confD toggle"))
		b4 = raptor.data.BuildUnit("confD.confDv",[confD,confDv])
		
		confE = raptor.data.Variant("confE")
		confEv = raptor.data.Variant()
		confEv.AddOperation(raptor.data.Set("SWITCH", "confE switch"))
		confEv.AddOperation(raptor.data.Set("TOGGLE", "B"))		# hit
		b5 = raptor.data.BuildUnit("confE.confEv",[confE,confEv])
		
		confF = raptor.data.Variant("confF")
		confFv = raptor.data.Variant()
		confFv.AddOperation(raptor.data.Set("SWITCH", "confF switch"))
		confFv.AddOperation(raptor.data.Set("TOGGLE", "confF toggle"))
		b6 = raptor.data.BuildUnit("confF.confFv",[confF,confFv])
		
		# delete any old Makefiles
		makefiles = [testDir.Append("Makefile")]
		makefiles.append(testDir.Append("confA.confAv", "top", "Makefile"))
		makefiles.append(testDir.Append("confB.confBv", "top", "Makefile"))
		makefiles.append(testDir.Append("confC.confCv", "top", "Makefile"))
		makefiles.append(testDir.Append("confD.confDv", "top", "Makefile"))
		makefiles.append(testDir.Append("confE.confEv", "top", "Makefile"))
		makefiles.append(testDir.Append("confF.confFv", "top", "Makefile"))
		makefiles.append(testDir.Append("confA.confAv", "top", "Tchild", "Makefile"))
		makefiles.append(testDir.Append("confB.confBv", "top", "Tchild", "Makefile"))
		makefiles.append(testDir.Append("confC.confCv", "top", "Fchild", "Makefile"))
		makefiles.append(testDir.Append("confD.confDv", "top", "Tchild", "Makefile"))
		makefiles.append(testDir.Append("confE.confEv", "top", "Tchild", "Makefile"))
		makefiles.append(testDir.Append("confF.confFv", "top", "Fchild", "Makefile"))
		self.cleanMakefiles(makefiles)
		
		# create new Makefiles
		maker = raptor.make.MakeEngine(aRaptor)
		maker.Write(makefiles[0], specs=[top], configs=[b1,b2,b3,b4,b5,b6])
		
		# test and clean
		self.failUnless(self.checkMakefiles(makefiles))
		self.cleanMakefiles(makefiles)
		

	def testPruneDuplicates(self):
		# use a bare Raptor object
		aRaptor = raptor.build.Raptor()
		aRaptor._load_cache()
		aRaptor.pruneDuplicateMakefiles = True
		aRaptor.writeSingleMakefile = False
		
		# find the test directory
		testDir = aRaptor.home.Append("test", "tmp")
		
		# an interface with defaults
		iface = raptor.data.Interface("I.EXE")
		iface.SetProperty("flm", "/lib/flm/iexe.flm")
		iface.AddParameter(raptor.data.Parameter("A", "1"))
		iface.AddParameter(raptor.data.Parameter("B", "2"))
		iface.AddParameter(raptor.data.Parameter("C", "3"))
		
		# each Specification is a Filter
		# f1 is empty, f2 and f3 are equal
		# so f2 should be the only Makefile generated
		
		f1 = raptor.data.Filter("f1")
		f1.SetConfigCondition("c1")
		
		f2 = raptor.data.Filter("f2")
		f2.SetConfigCondition("c2")
		f2.SetInterface(iface)
		
		f3 = raptor.data.Filter("f3")
		f3.SetConfigCondition("c3")
		f3.SetInterface(iface)
		
		# Configurations
		c1 = raptor.data.Variant("c1")
		c2 = raptor.data.Variant("c2")
		c3 = raptor.data.Variant("c3")

		# Build Units
		b1 = raptor.data.BuildUnit("c1",[c1])
		b2 = raptor.data.BuildUnit("c2",[c2])
		b3 = raptor.data.BuildUnit("c3",[c3])
		
		# Makefiles we expect
		makefiles = [testDir.Append("Makefile")]
		makefiles.append(testDir.Append("c2", "f2", "Makefile"))
		self.cleanMakefiles(makefiles)
		
		# Makefiles we do not expect
		prunes = []
		prunes.append(testDir.Append("c1", "f1", "Makefile"))
		prunes.append(testDir.Append("c1", "f2", "Makefile"))
		prunes.append(testDir.Append("c1", "f3", "Makefile"))
		prunes.append(testDir.Append("c2", "f1", "Makefile"))
		prunes.append(testDir.Append("c2", "f3", "Makefile"))
		prunes.append(testDir.Append("c3", "f1", "Makefile"))
		prunes.append(testDir.Append("c3", "f2", "Makefile"))
		prunes.append(testDir.Append("c3", "f3", "Makefile"))
		self.cleanMakefiles(prunes)
		
		# create new Makefiles
		maker = raptor.make.MakeEngine(aRaptor)
		maker.Write(makefiles[0], [f1, f2, f3], [b1, b2, b3])
		
		# test and clean
		self.failUnless(self.checkMakefiles(makefiles))
		self.cleanMakefiles(makefiles)
		self.failUnless(self.checkNotMakefiles(prunes))
		self.cleanMakefiles(prunes)
		
		
# run all the tests

from raptor_tests import SmokeTest

def run():
	t = SmokeTest()
	t.id = "999"
	t.name = "raptor_make_unit"

	tests = unittest.makeSuite(TestRaptorMake)
	result = unittest.TextTestRunner(verbosity=2).run(tests)

	if result.wasSuccessful():
		t.result = SmokeTest.PASS
	else:
		t.result = SmokeTest.FAIL

	return t


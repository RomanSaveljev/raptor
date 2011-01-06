#
# Copyright (c) 2006-2010 Nokia Corporation and/or its subsidiary(-ies).
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
# makefile module
# This module is for writing calls to Function-Like Makefiles
#

import re
import os
import generic_path
import stat
import json

class MakefileSelector(object):
	"""A "query" which is used to separate some flm interface calls
	  into separate makefile trees."""
	def __init__(self, name="default", interfacepattern=None, defaulttarget=None, ignoretargets=None):
		self.name=name
		if interfacepattern is not None:
			self.interfacepattern=re.compile(interfacepattern, re.I)
		else:
			self.interfacepattern=None
		self.defaulttarget=defaulttarget
		self.ignoretargets=ignoretargets

class BaseMakefile(object):
	def __init__(self, filename, callcount = 0, defaulttargets=[], ignoretargets=None, name=''):
		self.filename = filename
		self.callcount = callcount # Number of flm calls in this makefile
		self.defaulttargets = defaulttargets
		self.ignoretargets = ignoretargets
		self.name = name

	def json(self):
		"""Enables json serialisation of this object. Returns a structure in a format that the json module can render to text easily"""
		return { 'makefile' : { 'filename': str(self.filename), 'defaulttargets': self.defaulttargets, 'ignoretargets': self.ignoretargets, 'name': self.name }}

	@classmethod
	def from_json(self,json_structure):
		"""Deserialise an instance of this class from a data structure produced by the json parser"""
		try:
			mf_ = json_structure['makefile']
			mf = BaseMakefile(mf_['filename'], mf_['callcount'], mf_['defaulttargets'])
		except KeyError, e:	
			raise Exception("Makefile deserialised from json was invalid: {0}".format(str(json_structure))) 

		return mf

class Makefile(BaseMakefile):
	"""Representation of the file that is created from the build specification 
	   tree.
	"""
	def __init__(self, directory, selector, parent=None, filenamebase="Makefile", prologue=None, epilogue=None, defaulttargets=None):
		self.filenamebase = filenamebase
		self.directory = directory
		if selector.name != "":
			extension = "." + selector.name
		else:
			extension = ""
		filename = generic_path.Join(directory,filenamebase + extension)
		

		super(Makefile,self).__init__(filename = filename, defaulttargets = defaulttargets, ignoretargets = selector.ignoretargets, name = selector.name)
		self.selector = selector
		self.parent = parent
		self.childlist = []
		self.file = None
		self.prologue = prologue
		self.epilogue = epilogue
		self.dead = False

	def open(self):
		if self.dead:
			raise Exception, "Attempt to reopen completed makefile %s " % (self.filename)

		if self.file is None:
			directory = self.filename.Dir()
			if not (str(directory) == "" or directory.Exists()):
				try:
					os.makedirs(directory.GetLocalString())
				except Exception,e:
					raise Exception, "Cannot make directory '%s' for file '%s' in '%s': %s " % (str(directory),str(self.filename),str(self.directory),str(e))

			self.file = open(str(self.filename),"w+")
			
			self.file.write('# GENERATED MAKEFILE : DO NOT EDIT\n\n')
			if self.selector.defaulttarget:
				self.file.write('MAKEFILE_GROUP:=%s\n.PHONY:: %s\n%s:: # Default target\n' \
							% (self.selector.defaulttarget, self.selector.defaulttarget, self.selector.defaulttarget))
			else:
				self.file.write('MAKEFILE_GROUP:=DEFAULT\n')
			if self.prologue != None:
				self.file.write(self.prologue)
				
			if self.defaulttargets != None:
				self.file.write('# dynamic default targets\n')
				for defaulttarget in self.defaulttargets:
					self.file.write('.PHONY:: %s\n' % defaulttarget)
					self.file.write('%s:\n' % defaulttarget)
				self.file.write('\n')
			
	def addChild(self, child):
		self.open()
		self.file.write("include %s\n" % child.filename)
		child.open()

	def createChild(self, subdir):
		child = Makefile(str(self.filename.Dir().Append(subdir)), self.selector, self, self.filenamebase, self.prologue, self.epilogue, self.defaulttargets)
		self.addChild(child)
		child.open()
		return child

	def addCall(self, specname, configname, ifname, useAllInterfaces, flmpath, parameters, guard = None):
		"""Add an FLM call to the makefile.
			specname is the name of the build specification (e.g. the mmp name)
			configname is the name of the configuration which this call is made for
			flmpath is the absolute path to the flm
			parameters is an array of tuples, (paramname, paramvalue)	
			guard is a hash value that should be unique to the FLM call

		   This call will return False if the ifname does not match the selector for 
		   the makefile. e.g. it prevents one from adding a resource FLM call to a
		   makefile which is selecting export FLM calls. Selection is overridden if
		   useAllInterfaces is True.
		"""
		# create the directory if it does not exist

		if self.selector.interfacepattern is not None:
			ifmatch = self.selector.interfacepattern.search(ifname)
			if ifmatch == None and useAllInterfaces == False:
				return False

		# A possibly justified way of telling if this is an flm call that
		# "matters" to an incremental build or if it's a supporting call
		# that's only needed when others are there.
		if not ifname.endswith(".config.default"):
			self.callcount += 1

		self.open()
		# now we can write the values into the makefile
		self.file.write("# call %s, count %s\n" % (flmpath,self.callcount))
		self.file.write("SBS_SPECIFICATION:=%s\n" % specname)
		self.file.write("SBS_CONFIGURATION:=%s\n\n" % configname)

		if guard:
			self.file.write("ifeq ($(%s),)\n%s:=1\n\n" % (guard, guard))
		
		for (p, value) in parameters:
			self.file.write("%s:=%s\n" % (p, value))
	
		self.file.write("include %s\n" % flmpath)
		self.file.write("MAKEFILE_LIST:= # work around potential gnu make stack overflow\n\n")
		
		if guard:
			self.file.write("endif\n\n")

		return True

	def addInclude(self, makefilename):
		"""
		"""
		# create the directory if it does not exist

		self.open()
		# now we can write the values into the makefile
		self.file.write("include %s\n" % (makefilename+"."+self.selector.name))

	def close(self):
		if self.file is not None:
			if self.epilogue != None:
				self.file.write(self.epilogue)
			self.file.write('# END OF GENERATED MAKEFILE : DO NOT EDIT\n')
			self.file.close()
			self.file = None
			self.dead = True

	def __del__(self):
		self.close()
			
		
class OutOfDateException(Exception):
	pass

class BaseMakefileSet(object):

	# Used in Metadeps files:
	dep_prefix="dep:"
	include_prefix="include "
	record_prefix="makefileset="

	def __init__(self, metadepsfilename):
		self.makefiles = [] # list of Makefile()
		self.metadepsfilename = metadepsfilename

	def json(self):
		"""Enables json serialisation of this object. Returns a structure in a format that the json module can render to text easily"""
		return { 'makefileset' : { 'metadeps': self.metadepsfilename, 'makefiles': [m.json() for m in self.makefiles]}}

	@classmethod
	def from_json(self,json_structure):
		"""Deserialise an instance of this class from a data structure produced by the json parser"""
		try:
			mfset_ = json_structure['makefileset']
			mfset = BaseMakefileSet(mfset_['metadeps'])
			for makefile_ in mfset_['makefiles']:
				self.makefiles.append(BaseMakefile.from_json(makefile_))
		except Exception,e:
			raise Exception("Makefile set deserialised from json was invalid: {0}".format(str(json_structure))) 

	def __len__(self):
		return len(self.makefiles)

	def __getitem__(self,b):
		return self.makefiles[b]

	def makefile_names(self):
		for mf in self.makefiles:
			print "MFCOUNT",str(mf.filename),mf.callcount
		return [str(mf.filename) for mf in self.makefiles]
	
	def nonempty_makefiles(self):
		for mf in self.makefiles:
			print "MFCOUNT",str(mf.filename),mf.callcount
		return [mf for mf in self.makefiles if mf.callcount > 0]

	def nonempty_makefile_names(self):
		return [str(mf.filename) for mf in self.nonempty_makefiles]

	def add_makefile(self, makefile):
		self.makefiles.append(makefile)

	def buildrec_str(self):
		return " ".join(["{0},{1}".format(str(mf.filename),str(mf.callcount)) for mf in self.makefiles])

	def write_metadeps(self, singledeps, depfiles):
		"""
		The metadeps format looks like this:
		
		dep: /tracecompiler/testTC/group/bld2.inf
		dep: /tracecompiler/testTC/group/test.TC.mmp
		include /er/epoc32/build/testtc/c_c4b9ca3feb66425f/bldinf.p_d61573b7b2d85d4bde10a540d5abab13.d
		include /er/epoc32/build/testtc/c_c4b9ca3feb66425f/bldinf.p_d61573b7b2d85d4bde10a540d5abab13.d

		it is a gnu make compatible format with 2 phony targets. "dep:" indicates a direct dependency and 
		"include" indicates that there is a gnu makefile format list of dependencies

		For make to interpret this correctly the variable PARSETARGET would need to be set to "dep"
		and dep itself would have to be a prerequisite of the makefile that would be generated by this
		build.
		"""

		try:
			os.makedirs(str(generic_path.Path(self.metadepsfilename).Dir()))
		except OSError,e:
			pass # if the dir is already there

		try:

			with open(self.metadepsfilename,"w") as f:
				for d in singledeps:
					f.write("{0}{1}\n".format(BaseMakefileSet.dep_prefix,d))
				for d in depfiles:
					f.write("{0}{1}\n".format(BaseMakefileSet.include_prefix,d[0]))
		except Exception,e:
			raise(IOError("Could not write metadepfile: {0} {1}".format(self.metadepsfilename, str(e))))


	def check_uptodate(self):
		""" Throw exceptions if the makefile set is out of date compared to the
		    metadata that it is generated from."""

		if len(self.makefiles) == 0:
			return

		# Don't check the entire makefile set - should all be 
		# treated as one entity and the times should be similar
		makefile = self.makefiles[0].filename
		makefile_mtime = 0
		makefile_stat = 0

		try:
			makefilestat = os.stat(makefile)
			makefile_mtime = makefilestat[stat.ST_MTIME]
		except OSError, e:
			raise(OutOfDateException("incremental makefile generation: metadata is not uptodate: {0} doesn't exist".format(e.filename)))

		try:
			with open(self.metadepsfilename,"r") as mdf:
				for l in mdf:
					if l.startswith(BaseMakefileSet.dep_prefix):
						depfile = l[len(BaseMakefileSet.dep_prefix):].strip("\n\r ")
						depstat = os.stat(depfile)
						deptime = depstat[stat.ST_MTIME]

						if deptime > makefile_mtime:
							raise(OutOfDateException("OUTOFDATE: metadata deps: {0}".format(depfile)))

					if l.startswith(BaseMakefileSet.include_prefix):
						gnudepfile = l[len(BaseMakefileSet.include_prefix):].strip("\r\n ")
						
						parsetarget = "$(PARSETARGET):"
						with open(gnudepfile,"r") as gf:
							for dl in gf:
								if dl.find(parsetarget) > -1:
									dl = dl[len(parsetarget):]
	 
								deplist = dl.strip("\n\r \t\\").split(" ")

								for depfile in deplist:	
									if depfile == '':
										continue
									depstat = os.stat(depfile)
									deptime = depstat[stat.ST_MTIME]

									if deptime > makefile_mtime:
										raise(OutOfDateException("incremental makefile generation: outofdate {0} is newer than ".format(e.filename)))

		except IOError,e:
			raise(OutOfDateException("incremental makefile generation: metadata is not uptodate: {0} doesn't exist or has been altered".format(e.filename)))


class MakefileSet(BaseMakefileSet):
	grouperselector = MakefileSelector(name="")
	defaultselectors = [ 
		MakefileSelector("export", '\.export$', "EXPORT"),
		MakefileSelector("bitmap", '\.bitmap$', "BITMAP"),
		MakefileSelector("resource", '\.resource$', "RESOURCE"),
		MakefileSelector("default", '\.(?!export$|bitmap$|resource$).*$', "ALL")
		]

	def __init__(self, directory, selectors=defaultselectors, makefiles=None, parent=None, filenamebase="Makefile", prologue=None, epilogue=None, defaulttargets=None, readonly=False):
		super(MakefileSet,self).__init__(metadepsfilename = filenamebase + ".metadeps")

		self.directory = generic_path.Path(directory)
		self.filenamebase = filenamebase
		self.parent = parent
		self.readonly = readonly

		if makefiles is not None:
			self.makefiles = makefiles
		else:
			self.makefiles = []
			for sel in selectors:
				mf = Makefile(directory, sel, None, filenamebase, prologue, epilogue, defaulttargets)
				if readonly:
					mf.dead = True
				self.makefiles.append(mf)
					
		self.groupermakefile = Makefile(directory, MakefileSet.grouperselector, None, filenamebase, "# GROUPER MAKEFILE\n\nALL::\n\n", "\n")
		

		if readonly:
			self.groupermakefile.dead = True 
		else:
			for mf in self.makefiles:
				self.groupermakefile.addChild(mf)

	def createChild(self, subdir):
		"""Create a set of "sub" makefiles that are included by this set."""
		if not self.readonly:
			newmakefiles = []
			for mf in self.makefiles:
				newmf = mf.createChild(subdir)
				newmakefiles.append(newmf)

		newset = MakefileSet(str(self.directory.Append(subdir)), None, newmakefiles, self, self.filenamebase, readonly=self.readonly)
		if not self.readonly:
			self.groupermakefile.addChild(newset.groupermakefile)

		return newset

	def addCall(self, specname, configname, ifname, useAllInterfaces, flmpath, parameters, guard = None):
		"""Find out which makefiles to write this FLM call to 
		   and write it to those (e.g. the exports makefile) """

		if self.readonly:
			return
		for f in self.makefiles:
			f.addCall(specname, configname, ifname, useAllInterfaces, flmpath, parameters, guard)

	def addInclude(self, makefilename):
		"""include a makefile from each of the makefiles in the set - has the selector name appended to it."""
		if self.readonly:
			return
		for f in self.makefiles:
			f.addInclude(makefilename)




	def close(self):
		if self.readonly:
			return
		for mf in self.makefiles:
			mf.close()
		self.groupermakefile.close()

	def __del__(self):
		if self.readonly:
			return
		self.close()

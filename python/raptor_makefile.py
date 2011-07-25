#
# Copyright (c) 2006-2011 Nokia Corporation and/or its subsidiary(-ies).
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
# This module is for writing makefiles containing calls to Function-Like Makefiles
#

import re
import os
import generic_path
import stat
import json

class JsonMakefileDecodeError(Exception):
	pass

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
	"""A class representing a makefile.  In general it's not meant to be used for creating makefiles
	   but for representing makefiles that already exist."""
	def __init__(self, filename, callcount = 0, defaulttargets=[], ignoretargets=None, name=''):
		""" filename -- should be a generic_path.Path()
		    callcount -- is the number of FLM calls in the makefile.
		    defaulttargets -- variable indicates what targets to supply when running the makefile without
			any user specified targets.
		    ignoretargets -- A regular expression string that can be used to indicate what makefile targets
			should be removed from the make commandline when building this makefile.
			It is essentially a way of saying that if an overall build is being done and the overall
			target is, for example, "EXPORT" that this particular makefile doesn't and never will 
			supply that target and that therefore one should not ask it to produce such a target.
			In some situations this allows one to avoid having errors in logfiles which 
			make the user think, incorrectly, that there was some problem.
		    name -- A name that might be used to identify this makefile within some list of makefiles 
			(e.g. the name of a build stage or similar).
		"""
		    
		self.filename = filename
		self.callcount = callcount # Number of flm calls in this makefile
		self.defaulttargets = defaulttargets
		self.ignoretargets = ignoretargets
		self.name = name

	def json(self):
		"""Enables json serialisation of this object. Returns a structure in a format that the json module can render to text easily"""
		return { 'makefile' : { 'filename': str(self.filename), 'defaulttargets': self.defaulttargets, 'ignoretargets': self.ignoretargets, 'name': self.name , 'callcount': self.callcount}}

	@classmethod
	def from_json(cls,json_structure):
		"""Deserialise an instance of this class from a data structure produced by the json parser
		   json_structure -- a python data structure that the json module has deserialised from a text file.
		"""
		try:
			mf_ = json_structure['makefile']
			mf = cls(mf_['filename'], mf_['callcount'], mf_['defaulttargets'])
		except KeyError as e:	
			raise JsonMakefileDecodeError("Makefile deserialised from json was invalid: keyerror on {0} :: {1}  ".format(str(e), str(json_structure))) 

		return mf

class Makefile(BaseMakefile):
	"""Representation of the file that is created from the build specification 
	   tree.  This is used for *creating* new makefiles and addinf FLM calls into them.
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
			raise Exception("Attempt to reopen completed makefile {0} ".format(self.filename))

		if self.file is None:
			directory = self.filename.Dir()
			if not (str(directory) == "" or directory.Exists()):
				try:
					os.makedirs(directory.GetLocalString())
				except Exception as e:
					raise Exception("Cannot make directory '{0}' for file '{1}' in '{2}': {3} ".format(str(directory),str(self.filename),str(self.directory),str(e)))

			self.file = open(str(self.filename),"w+")
			
			self.file.write('# GENERATED MAKEFILE : DO NOT EDIT\n\n')
			if self.selector.defaulttarget:
				self.file.write('MAKEFILE_GROUP:={0}\n.PHONY:: {1}\n{2}:: # Default target\n'.format( 
					self.selector.defaulttarget, self.selector.defaulttarget, self.selector.defaulttarget))
			else:
				self.file.write('MAKEFILE_GROUP:=DEFAULT\n')
			if self.prologue != None:
				self.file.write(self.prologue)
				
			if self.defaulttargets != None:
				self.file.write('# dynamic default targets\n')
				for defaulttarget in self.defaulttargets:
					self.file.write('.PHONY:: {0}\n'.format(defaulttarget))
					self.file.write('{0}:\n'.format(defaulttarget))
				self.file.write('\n')
			
	def addChild(self, child):
		self.open()
		self.file.write("include {0}\n".format(child.filename))
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
		self.file.write("# call {0}, count {1}\n".format(flmpath,self.callcount))
		self.file.write("SBS_SPECIFICATION:={0}\n".format(specname))
		self.file.write("SBS_CONFIGURATION:={0}\n\n".format(configname))

		if guard:
			self.file.write("ifeq ($({0}),)\n{1}:=1\n\n".format(guard, guard))
		
		for (p, value) in parameters:
			self.file.write("{0}:={1}\n".format(p, value))
	
		self.file.write("include {0}\n".format(flmpath))
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
		self.file.write("include {0}\n".format((makefilename+"."+self.selector.name)))

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
	def __init__(self, text="", items=[]):
		""" items - strings representing files or other items that are out of date"""
		super(OutOfDateException,self).__init__(text)
		self.items = items

class BaseMakefileSet(object):
	"""Represents a "sequence" of makefiles that make up a build (e.g. export, bitmap, resource, resource_deps, default).
	   It is used generally to represent existing makefiles - not as a way to create new ones.
	"""

	# Used in Metadeps files:
	dep_prefix="dep:"
	include_prefix="include "
	record_prefix="makefileset="

	def __init__(self, metadepsfilename):
		self.makefiles = [] # list of Makefile()
		self.metadepsfilename = str(metadepsfilename)

	def json(self):
		"""Enables json serialisation of this object. Returns a structure in a format that the json module can render to text easily"""
		return { 'makefileset' : { 'metadeps': self.metadepsfilename, 'makefiles': [m.json() for m in self.makefiles]}}

	@classmethod
	def from_json(cls,json_structure):
		"""Deserialise an instance of this class from a data structure produced by the json parser"""
		try:
			mfset_ = json_structure['makefileset']
			mfset = cls(mfset_['metadeps'])
			for makefile_ in mfset_['makefiles']:
				mfset.makefiles.append(BaseMakefile.from_json(makefile_))
		except Exception as e:
			raise JsonMakefileDecodeError("Makefile set deserialised from json was invalid: {0} {1}  ".format(str(e),str(json_structure))) 
		return mfset

	def __len__(self):
		return len(self.makefiles)

	def __getitem__(self,b):
		return self.makefiles[b]

	def makefile_names(self):
		return [str(mf.filename) for mf in self.makefiles]
	
	def nonempty_makefiles(self):
		return [mf for mf in self.makefiles if mf.callcount > 0]

	def nonempty_makefile_names(self):
		return [str(mf.filename) for mf in self.nonempty_makefiles]

	def add_makefile(self, makefile):
		self.makefiles.append(makefile)

	def buildrec_str(self):
		return " ".join(["{0},{1}".format(str(mf.filename),str(mf.callcount)) for mf in self.makefiles])

	def write_metadeps(self, singledeps, depfiles):
		"""
		Write out the dependencies of this set of makefiles - i.e. the filenames of all the 
		metadata from which the makefile was generated.

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
		except OSError as e:
			pass # if the dir is already there

		try:

			with open(self.metadepsfilename,"w") as f:
				for d in singledeps:
					f.write("{0}{1}\n".format(BaseMakefileSet.dep_prefix,d))
				for d in depfiles:
					f.write("{0}{1}\n".format(BaseMakefileSet.include_prefix,d[0]))
		except Exception as e:
			ioe = IOError("Could Not write metadepfile: {0} {1}".format(self.metadepsfilename,str(e)))
			raise ioe


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
		message_template = "incremental makefile generation: {0} is out-of-date"
		try:
			makefilestat = os.stat(makefile)
			makefile_mtime = makefilestat[stat.ST_MTIME]
		except OSError as e:
			o = OutOfDateException(message_template.format(e.filename,items=[e.filename]))
			raise o

		try:
			with open(self.metadepsfilename,"r") as mdf:
				for l in mdf:
					if l.startswith(BaseMakefileSet.dep_prefix):
						depfile = l[len(BaseMakefileSet.dep_prefix):].strip("\n\r ")
						depstat = os.stat(depfile)
						deptime = depstat[stat.ST_MTIME]

						if deptime > makefile_mtime:
							o = OutOfDateException(message_template.format(depfile,items=[depfile]))
							raise o

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
										o = OutOfDateException(message_template.format(depfile,items=[depfile]))
										raise o

		except IOError as e:
			o = OutOfDateException(message_template.format(e.filename,items=[e.filename]))
			raise o


class MakefileSet(BaseMakefileSet):
	""" A sequence of makefiles that make up a build of a "layer". """
	grouperselector = MakefileSelector(name="")
	defaultselectors = [ 
		MakefileSelector("export", '\.export$', "EXPORT"),
		MakefileSelector("bitmap", '\.bitmap$', "BITMAP"),
		MakefileSelector("resource", '\.resource$', "RESOURCE"),
		MakefileSelector("default", '\.(?!export$|bitmap$|resource$).*$', "ALL")
		]

	def __init__(self, directory, selectors=defaultselectors, makefiles=None, parent=None, filenamebase="Makefile", prologue=None, epilogue=None, defaulttargets=None, readonly=False):
		super(MakefileSet,self).__init__(metadepsfilename = generic_path.Join(directory, filenamebase + ".metadeps"))

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

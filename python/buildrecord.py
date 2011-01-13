#
# Copyright (c) 2011 Nokia Corporation and/or its subsidiary(-ies).
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


""" Module for creating/manipulating an "audit trail" of builds """

import raptor_makefile
import os
import stat
import json


class BuildRecord(object):
	"""Information about a build which can be used, amongst other purposes,
	to assist incremental makefile generation.
	
	A new file is created in every build with the name #MAKEFILE#.buildrecord.
	This file records of the names of the makefiles involved in a build and
	the corresponding commandline that was given to raptor when it created
	them.
	
	Raptor uses these records to determine if the current build can reuse
	existing makefiles.  If the current build attempt's commandline and
	'environment' match those of an existing record then the makefiles
	referenced by the record can be reused.
	
	Each layer in a build can produce a 'makefileset' with makefiles for
	all the stages of a build (export,bitmap,resource_deps,resource,default).
	Hence buildrecords contain a list with one 'set' for each layer and 
	each set is itself a list of makefiles, one per stage.
	
	Build records also store the filenames of 'metadeps' files (short for
	"Metadata Dependencies")  which list the metadata that each makefileset
	depends on (e.g. the bld.infs and mmps that correspond to that makefileset).
	"""
	
	stored_attrs = ['commandline', 'environment', 'topmakefilename']
	sensed_environment_variables = ["EPOCROOT","PATH"]
	history_size = 10
	parsefails = []
	def __init__(self, commandline=None, environment=None, topmakefilename=None, makefilesets=None):
		""" 	Create a new record of a build that is about to happen (in which case the default parameters
			may be used) or a build that is complete.  Parameters must all be strings. 
		"""

		self.commandline = commandline
		self.environment = environment
		self.topmakefilename = topmakefilename
		self.uptodate = False # Do we need to regenerate the makefiles to reuse this build?
		self.makefilesets=makefilesets #  an array of raptor_makefile.BaseMakefileset Object
		self.filename = self.topmakefilename + ".buildrecord"
		self.reused = False
		self.new_metadata = [] # record what was out of date

	def to_file(self):
		""" Write out the build record so that we can find it in future builds"""
		with open(self.filename,"w") as f:
			json_br = {}
			for a in BuildRecord.stored_attrs:
				json_br[a] = self.__dict__[a]

			json_makefilesets = []
			for ms in self.makefilesets:
				json_makefilesets.append(ms.json())

			json_br['makefilesets'] = json_makefilesets
			json_structure = {'buildrecord': json_br	 }

			json.dump(json_structure,f, indent = 4)	


	def record_makefileset(self, makefileset):
		""" Add a makefileset to the list of sets "executed" in the build. 
		    This can be called repeatedly - e.g. once to record
		    the makefiles for each layer in an ordered layers build.
		"""
		self.makefilesets.append(makefileset)

	@classmethod
	def from_file(cls, filename):
		""" Create a build record from a .buildrecord file"""
		with open(filename,"r") as f:
			try:
				json_structure  = json.load(f)
			except Exception,e:
				raise Exception("Bad build record format - json deserialisation failed.")

		try:
			kargs = json_structure['buildrecord']
		except Exception,e:
			raise Exception("Bad build record format - buildrecord property not found in buildrecord file.")

		# the json structure matches what must be passed into the constructor
		# quite well except for the makefilesets
		try:
			makefilesets = [ raptor_makefile.BaseMakefileSet.from_json(json_makefileset) 
					 for json_makefileset in kargs['makefilesets']]
		except raptor_makefile.JsonMakefileDecodeError,e:
			raise Exception("Bad build record format: makefilesets element did not decode: {0}".format(str(e)))
		

		# replace the json structure for makefilesets with real BaseMakefileSet() instances
		kargs['makefilesets'] = makefilesets

		try:
			br = BuildRecord(**kargs)
		except TypeError,e:
			raise Exception("Bad build record format: settings must be present for {0} but they were {1}: {2}: {3}".format(BuildRecord.stored_attrs, str(kargs), filename, str(e)))


		br.filename = filename

		return br


	def _commandline_key(self):
		"""Strip a commandline of things that don't affect the
		   makefiles e.g. the name of the logfile. This is used
		   to decide if we need new makefiles or if the old ones
		   are ok. Obviously this kind of method is "approximate" and
		   will make some commandlines that are really equivalent seem
		   different e.g. options in a different order. The main thing
		   though is that it is a kind of "overcautious" mechanism
		   which is ok for an initial implementation of incremental
		   makefile generation."""
		sc = self.commandline.split(" ")

		# cut out non-relevant stuff
		skipcount = 0
		nsc = []
		for s in sc:
			if skipcount > 0:
				skipcount -= 1
				continue
			elif s ==  "--ip=on" or s == "clean":
				continue
			elif s == "-f": # skip logfilenames
				skipcount = 1
				continue

			nsc.append(s)

		return " ".join(nsc)

			
	def __eq__(self, other):
		""" Were the two builds done in a compatible 
		    environment, similar targets and for the same platforms?
		    i.e. should the makefiles be interchangeable?
		"""
		sc =  self._commandline_key()
		oc = other._commandline_key()
		if sc == oc:
			if self.environment == other.environment:
				return True
		
		return False

	@classmethod
	def matching_records(cls, adir, matching):
		"""Find records of previous builds that are equivalent to this one,
		   sort them according to time order and yield first X of them to 
		   the caller """

		brfiles = []
		for b in os.listdir(adir):
			if b.endswith(".buildrecord"):
				brf  = os.path.join(adir,b)
				try:
					brfiles.append((brf, os.stat(brf)[stat.ST_MTIME]))
				except OSError, e:
					pass

		# sort so newest are first
		brfiles_s = sorted(brfiles,key=lambda f:f[1], reverse=True)

		# yield up build records if they are "equal".  Don't 
		# look infinitely far back as it might take a long time
		rcount = 0
		for brt in brfiles_s:
			b = brt[0]
			try:
				br = cls.from_file(os.path.join(adir,b))
				if br == matching:
					yield br
					rcount += 1
					if rcount > BuildRecord.history_size:
						break
			except Exception,e:
				print(e)
				BuildRecord.parsefails.append(e)	# parse errors should not be fatal - just means that the build record is from an old version of raptor.  There is no way to report the fact that they happened though and that's not so nice.  This exception list just makes it feasible to debug a problem if one occurs.

	@classmethod
	def from_old(cls,  adir, commandline, environment, topmakefile):
		"""Create a build record for this build. Try to make it from an older one 
		   and use its existing makefiles if they are uptodate."""

		newbr = cls(commandline, environment, topmakefile)
		
		# See if there is an old build record to reuse
		for oldbr in cls.matching_records(adir, newbr):
			if oldbr.check_uptodate(newbr.new_metadata):
				newbr.topmakefilename = oldbr.topmakefilename
				newbr.makefilesets = oldbr.makefilesets
				newbr.uptodate = True
				newbr.reused = True
		return newbr



	def check_uptodate(self,triggers=[]):
		""" Return False if any of the metadata is out of date
		    update the list of triggers parameter with any
	 	    items that are not uptodate. Logic is short-circuit.
		"""
		try:
			# Loop gives a chance for exception to be thrown
			for mset in self.makefilesets:
				mset.check_uptodate()

			# No exception so all must be uptodate
			return True
		except raptor_makefile.OutOfDateException,e:
			triggers.extend(e.items)

		return False

#
# Copyright (c) 2010 Nokia Corporation and/or its subsidiary(-ies).
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
# planb.agent module
#
# Python API for setting up build actions in Raptor.

import optparse
import os
import pickle
import sys

# constants

# objects

class Connect(object):
	"""object to contain state information for API calls.
	
	For example,
	
	agent = planb.agent.Connect()
	agent.add_target(x)
	agent.commit()
	"""
	def __init__(self):
		# ignore the user's flags, all ours start with --planb
		flags = filter(lambda x: x.startswith("--planb"), sys.argv)

		parser = optparse.OptionParser()
		parser.add_option("--planb-debug", action="store_true", dest="debug", default=False)
		parser.add_option("--planb-dir", action="store", dest="dir", default=".")

		(options, []) = parser.parse_args(flags)

		# save the options (writing direct into self doesn't work)
		self.dir = options.dir
		self.debug = options.debug
		
		# load a parameter dictionary if we can
		if self.dir:
			self.pickle = os.path.join(self.dir, "pickle")
			file = open(self.pickle, "rb")
			self.parameters = pickle.load(file)
			file.close()
		else:
			self.parameters = {}
		
		if 'FLMDEBUG' in self.parameters:
			self.debug = (self.parameters['FLMDEBUG'] == '1')
			
		if self.debug:
			print "parameter values"
			for (k,v) in self.parameters.items():
				print "\t", k, "=", v
					
		self.targets = {}
	
	def __getitem__(self, name):
		"""retrieve parameters as if this were a dictionary.
		
		For example,
		
		print agent['EPOCROOT']
		"""
		# in future we may have multiple private dictionaries or even
		# a connection to some other process.
		
		# and we may convert the bare strings into lists or some other
		# useful python types.
		
		# for now though we'll just return the same text string that the
		# FLM would get.
		
		return self.parameters[name]
				
	def add_target(self, target):
		if target.phase in self.targets:
			self.targets[target.phase].append(target)
		else:
			self.targets[target.phase] = [target]
		
	def commit(self):

		print "REMARK: dir =", self.dir
		
		if not os.path.isdir(self.dir):
			os.makedirs(self.dir)
		
		ok = True
		
		for phase in ['BITMAP', 'RESOURCE', 'ALL']:
			if phase in self.targets:
				try:
					filename = os.path.join(self.dir, phase)
					file = open(filename, "w")
				
					for t in self.targets[phase]:
						file.write("$(call raptor_phony_recipe,%s,%s,,%s)" % (t.title, phase, t.run))
				
					file.close()
					print "REMARK: file =", filename
				except:
					sys.stderr.write("error: cannot create file '%s'\n" % filename)
					ok = False
		
		# write out the dependency file
		done_target = os.path.join(self.dir, "done")
		try:
			depends = os.path.join(self.dir, "depend.mk")
			file = open(depends, "w")
			file.write("%s: %s\n" % (done_target, sys.argv[0]))
				
			if self.pickle:
				file.write("%s: %s\n" % (done_target, self.pickle))
					
			file.close()
		except:
			sys.stderr.write("error: cannot create file '%s'\n" % depends)
			ok = False
				
		# write out the target marker file if all was well
		if ok:
			try:
				file = open(done_target, "w")
				file.close()
			except:
				sys.stderr.write("error: cannot create file '%s'\n" % done_target)
				sys.exit(1)
		else:
			sys.exit(1)
					
# end of the planb.agent module

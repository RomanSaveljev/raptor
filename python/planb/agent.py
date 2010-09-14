
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

'''
Python API for setting up build actions in Raptor.
'''

import optparse
import os
import pickle
import sys

# constants

# objects

class PlanbException(Exception):
	pass
	
class Connect(object):
	"""object to contain state information for API calls.
	
	For example,
	
	agent = planb.agent.Connect()
	target = planb.target.Target(agent)
	target.action("echo this makes my target")
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
					
		self.targets = []
	
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
	
	def add_directory(self, directory):
		print "WARNING: add_directory doesn't do anything yet with", directory
				
	def add_target(self, target):
		self.targets.append(target)
		
	def commit(self):

		print "REMARK: dir =", self.dir
		
		if not os.path.isdir(self.dir):
			os.makedirs(self.dir)
		
		phases = {}
		for t in self.targets:	
			if t.phase in phases:
				phases[t.phase].append(t)
			else:
				phases[t.phase] = [t]
			
		for phase in ['BITMAP', 'RESOURCE', 'ALL']:
			if phase in phases:
				filename = os.path.join(self.dir, phase)
				file = open(filename, "w")
				
				for t in phases[phase]:
					pre_reqs = " ".join(t.inputs)
					if t.outputs:
						main_target = t.outputs[0][0]
						macro = "raptor_recipe"
					else:
						main_target = phase
						macro = "raptor_phony_recipe"
				
					file.write("$(call {0},{1},{2},{3},{4})\n\n".format(macro, t.title, main_target, pre_reqs, t.run))
					
				file.close()
				print "REMARK: file =", filename
		
		# write out the dependency file
		done_target = os.path.join(self.dir, "done")
		depends = os.path.join(self.dir, "depend.mk")
		file = open(depends, "w")
		file.write("%s: %s\n" % (done_target, sys.argv[0]))
				
		if self.pickle:
			file.write("%s: %s\n" % (done_target, self.pickle))
					
		file.close()
				
		# write out the target marker file if all was well
		file = open(done_target, "w")
		file.close()

# end of the planb.agent module

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
		parser.add_option("--planb-dir", action="store", dest="dir")

		(self.options, args) = parser.parse_args(flags)

		# load a parameter dictionary if we can
		if self.options.dir:
			filename = os.path.join(self.options.dir, "pickle")
			file = open(filename, "rb")
			self.parameters = pickle.load(file)
			file.close()
		else:
			self.parameters = {}
		
		if self.options.debug:
			for (k,v) in self.parameters.items():
				print k + "=" + v
					
		self.targets = {}
			
	def add_target(self, target):
		if target.phase in self.targets:
			self.targets[target.phase].append(target)
		else:
			self.targets[target.phase] = [target]
		
	def commit(self):

		print "REMARK: dir =", self.options.dir
		
		if not os.path.isdir(self.options.dir):
			os.makedirs(self.options.dir)
		
		ok = True
		
		for phase in ['BITMAP', 'RESOURCE', 'ALL']:
			try:
				filename = os.path.join(self.options.dir, phase)
				file = open(filename, "w")
				
				if phase in self.targets:
					for t in self.targets[phase]:
						file.write("$(call raptor_phony_recipe,%s,%s,,%s)" % (t.title, phase, t.run))
				else:
					# we create an empty file anyway
					pass
				
				file.close()
				print "REMARK: file =", filename
			except:
				sys.stderr.write("error: cannot create file '%s'\n" % filename)
				ok = False
		
		if not ok:
			sys.exit(1)
					
# end of the planb.agent module

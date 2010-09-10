
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
# planb.target module

'''
Python objects for setting up build actions in Raptor.
'''

# constants

# objects

class File(object):
	def __init__(self, agent):
		self.agent = agent
		agent.add_target(self)
		
		self.generated_dependency_file = None
		self.inputs = []
		self.outputs = []
		self.run = 'true'    # a command that always succeeds
		
	def add_input(self, input):
		self.inputs.append(input)
	
	def add_inputs(self, inputs):
		self.inputs.extend(inputs)
			
	def add_output(self, output, releasable=True):
		self.outputs.append( (output, releasable) )
	
	def add_outputs(self, outputs, releasable=True):
		self.outputs.extend( [ (i, releasable) for i in outputs] )
			
	def action(self, command):
		self.run = command
	
	def generated_dependencies(self, depfile):
		self.generated_dependency_file = depfile
		
	def finalise(self):
		'''the agent calls this just before it uses the object.'''
		pass
	
class Bitmap(File):
	def __init__(self, agent):
		File.__init__(self, agent)
		self.phase = 'BITMAP'
		self.title = 'planb.bitmap'

class Resource(File):
	def __init__(self, agent):
		File.__init__(self, agent)
		self.phase = 'RESOURCE'
		self.title = 'planb.resource'

class Target(File):
	def __init__(self, agent):
		File.__init__(self, agent)
		self.phase = 'ALL'
		self.title = 'planb.target'

# end of the planb.target module

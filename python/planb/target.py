
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

class Base(object):
	def __init__(self):
		self.generated_dependency_file = None
		self.inputs = []
		self.outputs = []
		self.run = 'true'    # a command that always succeeds
		
	def add_input(self, input):
		self.inputs.append(input)
	
	def add_inputs(self, inputs):
		self.inputs.extend(inputs)
			
	def add_output(self, output, releasable=True):
		self.outputs.append(Output(output, releasable))
			
	def action(self, command):
		self.run = command
	
	def generated_dependencies(self, depfile):
		self.generated_dependency_file = depfile
		
	def finalise(self):
		pass

class Input(object):
	pass

class Output(object):
	def __init__(self, filename, releasable=True):
		self.filename = filename
		self.releasable = releasable
		
class Bitmap(Base):
	def __init__(self):
		Base.__init__(self)
		self.phase = 'BITMAP'
		self.title = 'planb.bitmap'

class Resource(Base):
	def __init__(self):
		Base.__init__(self)
		self.phase = 'RESOURCE'
		self.title = 'planb.resource'

class Target(Base):
	def __init__(self):
		Base.__init__(self)
		self.phase = 'ALL'
		self.title = 'planb.target'

# end of the planb.target module

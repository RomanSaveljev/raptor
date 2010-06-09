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
# planb.target module
#
# Python objects for setting up build actions in Raptor.

# constants

# objects

class File(object):
	def action(self, command):
		self.run = command
	
class Bitmap(File):
	def __init__(self):
		self.phase = 'BITMAP'
		self.title = 'planb.bitmap'
		self.run = 'true'

class Resource(File):
	def __init__(self):
		self.phase = 'RESOURCE'
		self.title = 'planb.resource'
		self.run = 'true'

class Target(File):
	def __init__(self):
		self.phase = 'ALL'
		self.title = 'planb.target'
		self.run = 'true'

# end of the planb.target module

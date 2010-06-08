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
		pass
	
class Bitmap(File):
	pass

class Resource(File):
	pass

class Target(File):
	pass

# end of the planb.target module

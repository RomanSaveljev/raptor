#
# Copyright (c) 2008-2009 Nokia Corporation and/or its subsidiary(-ies).
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
# Filter class for doing --what and --check operations
#

import os
import sys
import re
import filter_interface
import filter_what

class FilterWhatComp(filter_what.FilterWhat):

	def write(self, text):
		"process some log text"
		
		for line in text.splitlines():
			ok =filter_what.FilterWhat.write(self, line)
			if not ok:
				break
				
		self.ok = ok
		return self.ok
	
	def start_bldinf(self,bldinf):
		if "win" in self.buildparameters.platform:
			dir = os.path.dirname(bldinf.replace("/","\\"))
		else:
			dir = os.path.dirname(bldinf)

		self.outfile.write("-- abld -w \nChdir %s \n" % dir)
		
	def end_bldinf(self):
		self.outfile.write("++ Finished\n")

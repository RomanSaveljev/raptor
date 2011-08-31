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
#
import os

from raptor_tests import SmokeTest

def run():
	t = SmokeTest()
	t.usebash = True
	
	t.name = "start_via_python"
	t.description =  """Test that we can start up raptor from the python script sbs.py without using a batch file or script"""

	python = "python"
	if 'SBS_PYTHON3' in os.environ:
		python = os.environ['SBS_PYTHON3']
	elif 'SBS_PYTHON' in os.environ:
		python = os.environ['SBS_PYTHON']

	python = python.replace("\\","/")
		
	t.command = r"unset SBS_HOME HOSTPLATFORM HOSTPLATFORM_DIR HOSTPLATFORM32_DIR; {0} ../bin/sbs.py -b smoke_suite/test_resources/simple/bld.inf -c armv5 -n".format(python)
	t.warnings = 0
	t.run()
	return t

#
# Copyright (c) 2011-2014 Microsoft Mobile and/or its subsidiary(-ies).
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
# set up environment for programs that want to use python

import os
import sys

if not 'SBS_HOME' in os.environ:
	# effectively this determines if the script is not being run from a wrapper
	# so that we can try to set up roughly what the wrapper would set up.
	# e.g. this should make it easier to run raptor from a python debugger
	sbh = os.path.abspath(os.path.join(os.path.split(sys.argv[0])[0],".."))
	os.environ['SBS_HOME'] = sbh
	if 'SBS_PYTHONPATH' in os.environ:
		pyp_index = 0
		if 'PYTHONPATH' in os.environ:
			pyp = os.environ['PYTHONPATH'].split(os.pathsep)
			# Try to remember where pythonpath appears in the overall path
			# Usually it's after all the default paths but we don't 
			# know where those are:
			pyp_index = sys.path.index(pyp[0]) 

			# delete the python path from the front of the system path
			# so that we can replace it with "SBS_PYTHONPATH"
			for p in pyp:
				try:
					sys.path.remove(p)
				except ValueError as e:
					pass

		# insert SBS_PYTHONPATH at the same point where PYTHONPATH appeared		
		sys.path[pyp_index:pyp_index] = os.environ['SBS_PYTHONPATH'].split(os.pathsep)

if not 'HOSTPLATFORM' in os.environ: # set platform details if not already done.
	plat = sys.platform.lower()
	if plat.startswith("win"):
		# Assume win32 for now since raptor has to operate at that level.
		os.environ['HOSTPLATFORM']='win 32'
		os.environ['HOSTPLATFORM32_DIR']='win32'
		os.environ['HOSTPLATFORM_DIR']='win32'
	else:
		# Call the gethost.sh script using the -e option to obtain platform details
		try:
			import subprocess # avoid doing this import if we don't have to
			p = subprocess.Popen(args=[os.path.join(os.environ['SBS_HOME'],"bin", "gethost.sh"),"-e"],stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
			(output,errors) = p.communicate()
			rc = p.wait()

			if type(output) is not str:
				output = output.decode()
		
			for term in output.split("\n"):
				try:
					left,right=term.split("=")
					left = left.split(" ")[1] # get rid of "export" 
					right = right.strip("'")
				except ValueError as e: 
					continue

				if left in ['HOSTPLATFORM', 'HOSTPLATFORM_DIR', 'HOSTPLATFORM32_DIR']:
					os.environ[left] = right

		except Exception as e:
			import traceback
			traceback.print_exc()
			print("sbs: error: while determining host platform details - {0}".format(e))
			sys.exit(1)

# The SBS_HOME dir is in pythonpath to support the raptor pacakge
# SBS_HOME/raptor is in the pythonpath to support planb and old filters.
raptor_pythondirs = [ os.path.join(os.environ['SBS_HOME'],'raptor'), os.environ['SBS_HOME'] ]
sys.path[0:0] = raptor_pythondirs  # going in before everything - even the default paths

# Transmit a similar path down to subprocesses - unavoidably slightly different because it will go in after
# the default paths rather than at the start.  One doesn't know where default paths start/end
# so there's not much one can do about that.  Subprocesses like planb need this to work.
if 'PYTHONPATH' in os.environ:
	pp_env = os.path.pathsep + os.environ['PYTHONPATH']
else:
	pp_env=''

os.environ['PYTHONPATH']= os.pathsep.join(raptor_pythondirs) + pp_env

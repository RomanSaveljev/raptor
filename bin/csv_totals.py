#!/usr/bin/env python

# Copyright (c) 2010 Nokia Corporation and/or its subsidiary(-ies).
# All rights reserved.
# This component and the accompanying materials are made available
# under the terms of the License "Symbian Foundation License v1.0"
# which accompanies this distribution, and is available
# at the URL "http://www.symbianfoundation.org/legal/sfl-v10.html".
#
# Initial Contributors:
# Nokia Corporation - initial contribution.
#
# Contributors:
#
# Description:

"""
Summarise a .csv file (from the CSV filter) by adding up the numbers of
errors, criticals, warnings and missing files for each component and each
configuration.

The output is another .csv file with the fourth field replaced by the total
number of that "type" of event seen for that component and configuration.
For example,

error,/src/a/bld.inf,armv5_urel,64
error,/src/a/bld.inf,armv5_udeb,64
error,/src/b/bld.inf,armv5_urel,65
error,/src/b/bld.inf,armv5_udeb,65
"""

import os
import sys
import traceback

# we don't expect arguments, so treat any as a call for help
if len(sys.argv) > 1:
	print "usage:", sys.argv[0]
	print """
  The input CSV is read from stdin. The expected format is,
	
    type,component,configuration,"commands and output text"
	
  The output CSV is written to sdtout. The output format is,
	
    type,component,configuration,number_of_occurences
"""
	sys.exit(0)

totals = {}
line = " "
while line:
	line = sys.stdin.readline().strip()
	if line:
		fields = line.split(",")
		key = ",".join(fields[0:3])
		if key in totals:
			totals[key] += 1
		else:
			totals[key] = 1
		
for key, value in totals.items():
	sys.stdout.write("{0},{1}\n".format(key, value))

sys.exit(0)


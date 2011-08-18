#!/usr/bin/env python

# Copyright (c) 2011 Nokia Corporation and/or its subsidiary(-ies).
# All rights reserved.
# This component and the accompanying materials are made available
# under the terms of the License "Eclipse Public License v1.0"
# which accompanies this distribution, and is available
# at the URL "http://www.eclipse.org/legal/epl-v10.html".

"""
gk2csv.py

Converts the stats output about a build from grokbuild.py (in an XML format)
and makes a csv format file from it.  Looks for <annofile> tags and outputs
all the value attributes of the <metric> tags within them.

Usage:
python gk2csv.py grokfilename.xml > output.csv

"""

import os
import sys
import re

# following might match: mcl_201123_hw79u_08_ncp_main_build_dfs_variants.resource_deps.emake.anno
name_re=re.compile("^([a-zA-Z0-9]*_[0-9]+_[a-zA-Z0-9]+_[0-9]+)_(.*?).emake.anno.*")

from xml.dom import minidom



try:
	inputfilename = sys.argv[1]
	xmldoc = minidom.parse(inputfilename)
except IndexError as e:
	sys.stderr.write("Need a filename parameter: {0}\n".format(__doc__))
	sys.exit(1)
except IOError as e:
	sys.stderr.write("parameter '{0}' could not be parsed must be an existing xml format file\n".format(inputfilename)) 
	sys.exit(1)

headlines=[]
headered=False
build_id = None
for node in xmldoc.getElementsByTagName('annofile'):
		fname = os.path.split(node.attributes['name'].value)[1]
		m = name_re.match(fname)

		if build_id == None:
			build_id = m.group(1)
			print("Build: {0}".format(build_id))

		stepname = m.group(2)

		line = [stepname]
		for c in node.getElementsByTagName('metric'):
			line.append(c.attributes['value'].value)
			if not headered:
				headlines.append(c.attributes['name'].value)

		if not headered:
			print("stepname,{0}".format(",".join(headlines)))
			headered = True
		
		print(",".join(line))

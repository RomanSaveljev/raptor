#!/usr/bin/env python

# Copyright (c) 2010-2014 Microsoft Mobile and/or its subsidiary(-ies).
# All rights reserved.
# This component and the accompanying materials are made available
# under the terms of the License "Eclipse Public License v1.0"
# which accompanies this distribution, and is available
# at the URL "http://www.eclipse.org/legal/epl-v10.html".

"""
Gathers performance metrics from the logs of a complex multi-step build.
Supports Helium 13 at the moment

Can also extract useful data from emake annotation files.
"""


import datetime
import optparse
import os
import re
import sys

# raptor packages are in ../python relative to this script
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "python"))

import allo.helium

parser = optparse.OptionParser(prog = "grokbuild",
                               usage = """%prog [-h | options] path_to_EPOCROOT 

The build logs are usually in $EPOCROOT/output/logs""")

parser.add_option("--maxagents", type="int", default=30,
       help="The number of simultaneous agents used in the build. You need to "
            "supply this if --emake-class was used rather than --emake-maxagents "
            "since this is then a property of the build cluster and is not usually "
            "recorded in the logs. The default is %default.")

parser.add_option("--output", default="-",
       help="The name of the output file to store the grok results in. A value "
            "of '-' can be used to write to the standard output. The default "
            "is '%default'.")

(options, args) = parser.parse_args()

if len(args) == 0:
	sys.stderr.write("Need at least one argument: a path to the logs.\n")
	sys.exit(-1)

epocroot = args[0]
sys.stderr.write("Gathering Performance Metrics for %s\n" % epocroot)

b = allo.helium.HeliumLogDir(epocroot, options)

if options.output == "-":
	b.write(sys.stdout)
else:
	with open(options.output, "w") as stream:
		b.write(stream)

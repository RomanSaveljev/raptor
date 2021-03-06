#!/bin/python
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
#
# Fetch a file via http
#

try:
	from urllib import request # python3
except ImportError:
	import urllib2 as request # python2

import sys
import os

def get_http(url, outfile):
	opener = request.build_opener()

	# ...and install it globally so it can be used with urlopen.
	request.install_opener(opener)

	fin = request.urlopen(url) 
	with open(outfile,"w")  as fout:
		inbytes = fin.read()
		while inbytes:
			fout.write(inbytes)
			inbytes = fin.read()


if __name__ == "__main__":
	usage="usage: urlget.py <url> [<outputfilename>]"
	if len(sys.argv) > 1:
		url = sys.argv[1]
		if len(sys.argv) == 3:
			outfile = sys.argv[2]
		else:
			sys.stderr.write("error: 1-2 arguments required, {0} supplied\n{1}\n".format(len(sys.argv)-1,usage))
			sys.exit(2)
	elif len(sys.argv)==2:
		outfile = url.split("/")[-1]
	else:
		sys.stderr.write("error: 1-2 arguments required but none supplied\n{1}\n".format(usage))
		sys.exit(2)


	try:
		get_http(url, outfile)
		print("downloaded {0}".format(outfile))
	except Exception as e:
		sys.stderr.write("error: download failed: {0}\n".format(str(e)))
		sys.exit(3)


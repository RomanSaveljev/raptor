#!/usr/bin/env python

# Copyright (c) 2011 Nokia Corporation and/or its subsidiary(-ies). 
# All rights reserved.
# This component and the accompanying materials are made available
# under the terms of "Eclipse Public License v1.0"
# which accompanies this distribution, and is available
# at the URL "http://www.eclipse.org/legal/epl-v10.html".
#
# Initial Contributors:
# Nokia Corporation - initial contribution.
#
# Contributors:
# 
# Description:

"""
File utilities like cat, sort, uniq
"""

import os
import tempfile
import itertools
import heapq

def cat(input_list, output):
	with open(output, "wb") as fout:
		for input in input_list:
			with open(input, "rb") as fin:
				for line in fin:
					fout.write(line)

def merge(*iterables):
    for element in heapq.merge(*iterables):
        yield element

def sort(input, output, buffer_size=32000):
	tempdir = tempfile.gettempdir()
	rw_buffer = 64 * 1024
	chunks = []
	try:
		with open(input, 'rb', rw_buffer) as input_file:
			input_iterator = iter(input_file)
			current_chunk = list(itertools.islice(input_iterator, buffer_size))
			if current_chunk:
				current_chunk.sort()
				output_chunk = open(os.path.join(tempdir, '%06i'%len(chunks)), 'w+b', rw_buffer)
				chunks.append(output_chunk)
				output_chunk.writelines(current_chunk)
				output_chunk.flush()
				output_chunk.seek(0)
		with open(output, 'wb', rw_buffer) as output_file:
			output_file.writelines(merge(*chunks))
	finally:
		for chunk in chunks:
			try:
				chunk.close()
				os.remove(chunk.name)
			except Exception:
				pass

def uniq(input, output):
	with open(output, "wb") as fout:
		with open(input, "rb") as fin:
			previous = ''
			for line in fin:
				if line != previous:
					fout.write(line)
					previous = line

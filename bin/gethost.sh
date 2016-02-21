#!/bin/bash


# Copyright (c) 2006-2011 Nokia Corporation and/or its subsidiary(-ies).
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
# Determine hosttype
#
#

# Print out a list of host information in order of significance.
# for use within Makefiles and other scripts.
# The idea is that it should be possible to use it for simple decisions
# e.g. windows/linux and more complex ones e.g. i386/x86_64

getopts de  OPT

if [[ "${OSTYPE}" =~ "linux" || "${HOSTPLATFORM}" =~ "linux" ]]; then
	ARCH=$(uname -i)
	# Find the libc binary and use a regular expression to slice
	# off the major and minor version numbers
	# e.g /lib/libc-2.12.1.so  => libc2_12

	# if 32 and 64 bit architectures are present then libc is usually
	# the same either way so pick one, in this case the last. If only
	# 1 architecture is present then this still works. 
	_clibs=($(echo /lib/*-linux-gnu/libc-*)) # Make an array
    LIBCPAT=${_clibs[${#_clibs[*]}-1]} # Arbitrarily select last item


	# Some systems have a simpler convention and we can 
	#  Just look at the 32-bit libc to get a version
	if [ ! -f "$LIBCPAT" ]; then
		LIBCPAT=$(echo /lib/libc-*)
	fi

	# Get the libc major and minor version numbers
	LIBC=$(echo "$LIBCPAT" | sed -r 's#.*/libc-([0-9]*)\.([0-9]*)(\.([0-9]*))?.so#libc\1_\2#')

	# The 32-bit platform is often compatible in the sense that
	# a) 32-bit programs can run on the 64-bit OS.
	# b) a 64-bit OS can tell the compiler to create 32-bit executables.

	ARCH32="i386"

	# deal with ubuntu/debian:
	if [ "$ARCH" == "unknown" ]; then
		ARCH=$(uname -m)
	fi

	HOSTPLATFORM="linux ${ARCH} ${LIBC}"
	HOSTPLATFORM_DIR="linux-${ARCH}-${LIBC}"
	HOSTPLATFORM32_DIR="linux-${ARCH32}-${LIBC}"
	
elif [[ "$OS" == "Windows_NT" ]]; then
	HOSTPLATFORM="win 32"
	HOSTPLATFORM_DIR="win32"
	HOSTPLATFORM32_DIR="win32"
else
	HOSTPLATFORM=unknown
	HOSTPLATFORM_DIR=unknown
fi

if [ "$OPT" == "e" ]; then 
	echo "export HOSTPLATFORM_DIR=$HOSTPLATFORM_DIR"
	echo "export HOSTPLATFORM32_DIR=$HOSTPLATFORM32_DIR"
	echo "export HOSTPLATFORM='$HOSTPLATFORM'"
elif [ "$OPT" == "d" ]; then 
	echo "$HOSTPLATFORM_DIR"
else
	echo "$HOSTPLATFORM"
fi

#!/bin/bash 

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
# A script that does a test run with simmmer upto some number of cores
# 



function dotest {
for i in {1..32}; do
j=$(( i *2 ))
rm -f testfile.*
(time make -j $j -f test.mk SIMMER_ARGS:="$SIMMER_ARGS"  ) 2>result.j$j
done
mkdir "$TESTNAME"
mv result.j* "$TESTNAME"
}

SIMMER_ARGS=--copylen=16384
TESTNAME=copylen_16384
dotest

SIMMER_ARGS=--copylen=8192
TESTNAME=copylen_8192
dotest

SIMMER_ARGS=--copylen=4096
TESTNAME=copylen_4096
dotest


SIMMER_ARGS=--filedata=425000L
TESTNAME=filedata_425000
dotest

SIMMER_ARGS=--filedata=850000L
TESTNAME=filedata_850000
dotest

SIMMER_ARGS=--filedata=1700000L
TESTNAME=filedata_1700000L
dotest

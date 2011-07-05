#
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
# Utility makefile 
#

BVCPP_TAR:=$(SBS_HOME)/util/ext/bv.tgz
BVCPP_TAR_URL:=http://rene.europe.nokia.com/~raptorbot/files/bv.tgz

# This rule is allowed to fail as it is possible that 
# a user might not be able to obtain the bv.tgz file
# and although this makes binary variation harder
# it is not impossible if one uses gcc > 4.4 
# by setting SBS_BVCPP

define b_bvcpp

.PHONY:: bvcpp

all:: bvcpp

bvcpp: $(INSTALLROOT)/bv/bin/cpp


$(INSTALLROOT)/bv/bin/cpp: $(BVCPP_TAR)
	-@if [ -f $(BVCPP_TAR) ]; then cd $(INSTALLROOT) && \
	rm -rf bv && \
	tar -xzf $(BVCPP_TAR)&& touch $$@ ; else \
	echo "Cannot find a prepackaged binary variation capabale CPP.  GCC 4.4 is usually sufficient - set SBS_BVCPP to point to it"; fi


$(BVCPP_TAR):
	-for url in $(BVCPP_TAR_URL); do \
	    wget $(BVCPP_TAR_URL) -O $(BVCPP_TAR);  \
	    if [ $$$$? -eq 0 ]; then break; else rm $(BVCPP_TAR); fi ; \
	done


endef

$(eval $(b_bvcpp))





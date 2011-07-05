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

RAPTOR_MAKE_VER:=3.81

MAKE_SOURCEDIR:=$(OUTPUTPATH)/make-$(RAPTOR_MAKE_VER)
MAKE_TAR:=$(SBS_HOME)/util/ext/make-$(RAPTOR_MAKE_VER).tar.bz2
MAKE_TAR_URL:=http://mirrors.kernel.org/gnu/make/make-$(RAPTOR_MAKE_VER).tar.bz2  http://www.nic.funet.fi/pub/gnu/ftp.gnu.org/pub/gnu/make/make-$(RAPTOR_MAKE_VER).tar.bz2


define b_make

.PHONY:: make

all:: make

make: $(INSTALLROOT)/bin/make

$(MAKE_TAR):
		for url in $(MAKE_TAR_URL); do \
		    wget $(MAKE_TAR_URL) -O $(MAKE_TAR); \
			if [ $$$$? -eq 0 ]; then break; fi ;\
		done
	
$(INSTALLROOT)/bin/make: $(MAKE_TAR) 
	rm -rf $(MAKE_SOURCEDIR) && \
	cd $(OUTPUTPATH) && \
	tar -xjf $(MAKE_TAR) && \
	(  \
	cd $(MAKE_SOURCEDIR) && \
	CFLAGS="-O2 $(GCCTUNE)" ./configure --prefix=$(INSTALLROOT) --disable-job-server && \
	$(MAKE) -j8 && $(MAKE) install \
	)
endef

$(eval $(b_make))

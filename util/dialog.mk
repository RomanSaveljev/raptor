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


# Build dialog for SBSv2 installer

RAPTOR_DIALOG_VER:=1.1-20080819

DIALOG_SOURCEDIR:=$(OUTPUTPATH)/dialog-$(RAPTOR_DIALOG_VER)
DIALOG_TAR:=$(SBS_HOME)/util/ext/dialog-$(RAPTOR_DIALOG_VER).tar.gz

DIALOG_TAR_URL:=http://projects.developer.nokia.com/raptor/files/dialog-$(RAPTOR_DIALOG_VER).tar.gz http://rene.europe.nokia.com/~raptorbot/files/dialog-$(RAPTOR_DIALOG_VER).tar.gz


define b_dialog

.PHONY:: dialog

all:: dialog

dialog: $(INSTALLROOT)/bin/dialog
	
$(INSTALLROOT)/bin/dialog: $(DIALOG_TAR) 
	rm -rf $(DIALOG_SOURCEDIR) && \
	cd $(OUTPUTPATH) && \
	tar -xzf $(DIALOG_TAR) && \
	(  \
	cd $(DIALOG_SOURCEDIR) && \
	CFLAGS="-O3 $(GCCTUNE) -s" ./configure --prefix=$(INSTALLROOT) && \
	$(MAKE) -j8 && $(MAKE) install \
	)

$(call fetch_gbzip,$(DIALOG_TAR),$(DIALOG_TAR_URL))

endef

$(eval $(b_dialog))





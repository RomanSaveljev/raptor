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

# Build Python for Raptor


define b_python
.PHONY:: python$(RAPTOR_PYTHON_DIRVERSION) python

python$(RAPTOR_PYTHON_DIRVERSION):: $(PYINSTALLROOT)/bin/python

all:: python$(RAPTOR_PYTHON_DIRVERSION)

python:: $(RAPTOR_PYTHON_DIRVERSION)
	
$(call fetch_gbzip,$(PYTHON_TAR),$(PYTHON_TAR_URL))
	
$(PYINSTALLROOT)/bin/python: $(PYTHON_TAR) 
	rm -rf $(PYTHON_SOURCEDIR) && \
	cd $(OUTPUTPATH) && \
	tar -xjf $(PYTHON_TAR) && \
	(  \
	cd $(PYTHON_SOURCEDIR) && \
	CFLAGS="-O3 $(GCCTUNE) -s" ./configure --prefix=$(PYINSTALLROOT) --enable-shared --with-threads --enable-bzip2 && \
	$(MAKE) -j8 && $(MAKE) install \
	)

CLEANFILES:=$(PYINSTALLROOT)/bin/python
$(cleanlog)

endef

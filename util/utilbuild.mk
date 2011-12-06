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

CHAR_BLANK:=
CHAR_SPACE:=$(CHAR_BLANK) $(CHAR_BLANK)

HOSTPLATFORM:=$(shell $(SBS_HOME)/bin/gethost.sh)
HOSTPLATFORM_DIR:=$(shell $(SBS_HOME)/bin/gethost.sh -d)

ifeq ($(filter $(HOSTPLATFORM),win),win)
PROGRAMEXT:=.exe
HOSTMACROS:=-DHOST_WIN -DHOST_DIR=$(HOSTPLATFORM_DIR)
else
PROGRAMEXT:=
HOSTMACROS:=-DHOST_LINUX -DHOST_DIR=$(HOSTPLATFORM_DIR)
endif

GCCTUNE:=
ifeq ($(filter $(HOSTPLATFORM),x86_64),x86_64)
else
GCCTUNE:=-mtune=i686
endif

BUILDDIR:=$(subst \,/,$(SBS_HOME))/util/build
INSTALLROOT:=$(subst \,/,$(SBS_HOME))/$(HOSTPLATFORM_DIR)
BINDIR:=$(INSTALLROOT)/bin
OUTPUTPATH:=$(BUILDDIR)/$(HOSTPLATFORM_DIR)

define cleanlog
ifneq ($(CLEANMODE),)
$$(info <clean>)
$$(foreach O,$$(CLEANFILES),$$(info <file>$$(O)</file>)) 
$$(info </clean>)
endif
endef

# fetch_gbzip - fetch a gzip/bzipped file using a list of alternate
# URLS. If the result is corrupt or incomplete then remove it.
# $1 - The ultimate location and filename in which to store the file 
#      Must end in "bz2" or "gz"
# $2 - urls separated by spaces for alternate download locations
define fetch_gbzip
$1:
	-for url in $2; do \
	    wget $$$$url -O $1; \
	    if [ $$$$? -eq 0 ]; then \
			filetype="$1"; \
			if [ "$$$${filetype##*bz2}" == "" ]; then \
				bzip2 -t $1; \
			else \
				gzip -t $1;\
			fi; \
	    	if [ $$$$? -eq 0 ]; then \
				break;\
			else \
				echo "Error - $1 could not be decompressed hence it is invalid - deleting it." 1>&2 ; \
		 		rm $1; \
			fi ; \
		else \
			echo "Error - $1 could not be fetched" 1>&2 ;\
		 	rm $1; \
		fi ; \
	done ; \
	test -f $1

endef

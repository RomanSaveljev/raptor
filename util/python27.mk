#
# Copyright (c) 2006-2010 Nokia Corporation and/or its subsidiary(-ies).
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

ifndef (b_python)
include python.mk
endif

RAPTOR_PYTHON_VER:=2.7
RAPTOR_PYTHON_DIRVERSION:=$(subst .,,$(RAPTOR_PYTHON_VER))
PYTHON_SOURCEDIR:=$(OUTPUTPATH)/Python-$(RAPTOR_PYTHON_VER)
PYTHON_TAR:=$(SBS_HOME)/util/ext/Python-$(RAPTOR_PYTHON_VER).tar.bz2
PYTHON_TAR_URL:=http://www.python.org/ftp/python/2.7/Python-2.7.tar.bz2
PYINSTALLROOT:=$(INSTALLROOT)/python$(RAPTOR_PYTHON_DIRVERSION)
$(eval $(b_python))

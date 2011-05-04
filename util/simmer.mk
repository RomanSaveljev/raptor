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
# Makefile for a compiler simulator
#
#
SOURCEDIR:=$(subst \,/,$(SBS_HOME))/util/simmer
TALONDIR:=$(subst \,/,$(SBS_HOME))/util/talon

TARGET:=simmer
CFLAGS:=$(CFLAGS) -g -I$(TALONDIR)
SOURCES:=$(addprefix $(SOURCEDIR)/,simmer.c) $(addprefix $(TALONDIR)/,log.c) $(addprefix $(SOURCEDIR)/,sim_mallocs.c)
$(eval $(cprogram))


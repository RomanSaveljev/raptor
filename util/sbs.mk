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
# Utility makefile 
#
#


SHELL:=bash

include $(SBS_HOME:\=/)/util/gccprogram.mk

ifeq ($(filter win,$(HOSTPLATFORM)),win)
PROCESS_C:=process_win.c
CFLAGS:=-DHOST_WIN
ifeq ($(SBS_MINGW),)
LDFLAGS:=$(subst \,/,$(SBS_HOME:\=/)\win32\mingw\lib\libiberty.a)
else
LDFLAGS:=$(subst \,/,$(SBS_MINGW:\=/)\lib\libiberty.a)
endif
LDFLAGS:=$(LDFLAGS) -Wl,-lws2_32
else
PROCESS_C:=process.c
CFLAGS:=-g
linux_PTHREADLIBS:=-lpthread
LDFLAGS:=$(linux_PTHREADLIBS) -lrt
endif


SOURCEDIR:=$(subst \,/,$(SBS_HOME))/util/talon


# remember how to clean up:
MANIFEST:=$(SOURCEDIR)/manifest

ifeq ($(filter win,$(HOSTPLATFORM)),win)
TARGET:=sbs
SOURCES:=$(addprefix $(SOURCEDIR)/,sbs.c buffer.c sema.c log.c env.c file.c $(PROCESS_C)) 
$(eval $(cprogram))
endif


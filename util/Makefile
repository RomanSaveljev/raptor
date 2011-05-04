
# Copyright (c) 2008-2011 Nokia Corporation and/or its subsidiary(-ies).
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
##


SHELL:=bash

ifeq ($(CLEANMODE),)
.PHONY:: all
all::
else
.PHONY:: clean
clean::

endif

include utilbuild.mk # need general settings e.g. INSTALLROOT

ifeq ($(filter CLEAN,$(MAKECMDGOALS))$(filter clean,$(MAKECMDGOALS)),)

include gccprogram.mk

#################################################
ifeq ($(TARGETS),)
  TARGETS:=descramble talon ransleep tmkdir simmer
  ifneq ($(filter $(HOSTPLATFORM),win),win)
    # Some tools not built for windows
    # Some of these don't support our special clean mode
    TARGETS:=$(TARGETS) make python27 bvcpp dialog 
    # TARGETS:=$(TARGETS) python32
  endif
  ifneq ($(filter $(HOSTPLATFORM),win),)
	TARGETS:=$(TARGETS) sbs
  endif
endif

$(foreach T,$(TARGETS),$(eval -include $(T).mk))

else

clean:
	@echo "Cleaning"
	$(MAKE) $(MAKEFILE) CLEANMODE:=1 | grep '<file>' |sed -r 's#.*<file>(.*)</file>.*#\1#' | (read F; while [ $$? -eq 0 ]; do rm -f "$$F"; echo " [rm] $$F"; read F; done; true )
endif

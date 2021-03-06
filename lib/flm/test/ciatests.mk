#
# Copyright (c) 2009 Nokia Corporation and/or its subsidiary(-ies).
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
#
##
# A grouping glue makefile that runs all tests

## Purpose: Run test makefiles in parallel to ensure that they all work
## Postconditions: All postconditions for all the makefiles are satisfied

include $(FLMHOME)/flmtools.mk

$(call vsave,ALLTARGET)
COMPONENT_ALLTARGETS:=$(RELEASEPATH)/$(FULLVARIANTPATH)/ciaabiv2_1.dll
COMPONENT_GLUEMAKEFILES:=ciaabiv2_1/ciaabiv2_1.mk
$(ALLTARGET):: ciatests
ALLTARGET:=ciatests

include $(FLMHOME)/grouping.flm
$(call vrestore)

# Copyright (c) 2010-2011 Nokia Corporation and/or its subsidiary(-ies).
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

TOBLDINF:=$(dir $(subst :,,$(subst $(EPOCROOT)/,,$(COMPONENT_META))))

ifeq ($(ROMFILE_$(call sanitise,$(TOBLDINF)$(TARGET).$(REQUESTEDTARGETEXT))),)
    ROMFILE_$(call sanitise,$(TOBLDINF)$(TARGET).$(REQUESTEDTARGETEXT)):=1
    ROMDIR:=$(EPOCROOT)/epoc32/rom/$(TOBLDINF)

    # Default values
    ROMFILETYPE:=file
    ROMFILETYPE_NOKIA:=file
    
    RELEASE_ROOT_DIR:=/epoc32/release
    RELEASE_ROOT_DIR_NOKIA:=
    
    ROMFILE:=$(TARGET).$(REQUESTEDTARGETEXT)
    ROMPATH:=$(if $(TARGETPATH),$(TARGETPATH)/,sys/bin/)
    ROMDECORATIONS:=
    ROMFILETYPE_RAM:=data
    ROMFILE_RAM:=$(TARGET).$(REQUESTEDTARGETEXT)
    ROMPATH_RAM:=sys/bin/
    BUILDROMTARGET:=1
    ABIDIR:=MAIN

    define DoRomSet
    ifeq ($(call uppercase,$(TARGETTYPE)),LIB)
    BUILDROMTARGET:=
    endif

    ifeq ($(call uppercase,$(TARGETTYPE)),KEXT)
    ROMFILETYPE:=extension[MAGIC]
    ROMFILETYPE_NOKIA:=extension[VARID]
    ABIDIR:=KMAIN
    endif
    ifeq ($(call uppercase,$(TARGETTYPE)),LDD)
    ROMFILETYPE:=device[MAGIC]
    ROMFILETYPE_NOKIA:=device[VARID]
    ABIDIR:=KMAIN
    endif
    ifeq ($(call uppercase,$(TARGETTYPE)),PDD)
    ROMFILETYPE:=device[MAGIC]
    ROMFILETYPE_NOKIA:=device[VARID]
    ABIDIR:=KMAIN
    endif
    ifeq ($(call uppercase,$(TARGETTYPE)),VAR)
    ROMFILETYPE:=variant[MAGIC]
    ROMFILETYPE_NOKIA:=variant[VARID]
    ABIDIR:=KMAIN
    endif
    ifeq ($(call uppercase,$(TARGETTYPE)),KDLL)
    ABIDIR:=KMAIN
    endif

    ifneq ($(CALLDLLENTRYPOINTS),)
    ROMFILETYPE:=dll
    ROMFILETYPE_NOKIA:=dll
    endif
    ifeq ($(ROMFILETYPE),primary)
    ABIDIR:=KMAIN
    endif
    endef

    $(eval $(call DoRomSet))

    ifneq ($(EPOCFIXEDPROCESS),)
        ROMDECORATIONS:=$(ROMDECORATIONS) fixed
    endif
    ifeq ($(PAGED),1)
        ROMDECORATIONS:=$(ROMDECORATIONS) paged
    endif
    ifeq ($(PAGED),0)
        ROMDECORATIONS:=$(ROMDECORATIONS) unpaged
    endif


    DATATEXT:=
    ifeq ($(TESTCODE),TRUE)
    	# Add 'TEST' to the .iby filename
    	ROMTEST:=test
        ifeq ($(TEST_OPTION),BOTH)
            DATATEXT:="data=/epoc32/data/z/test/$(MODULE_DIR)/$(VARIANTPLATFORM).auto.bat test/$(MODULE_NAME).auto.bat"\n"data=/epoc32/data/z/test/$(MODULE_DIR)/$(VARIANTPLATFORM).manual.bat test/$(MODULE_NAME).manual.bat"
        else
            ifneq ($(TEST_OPTION),NONE)
                DATATEXT:="data=/epoc32/data/z/test/$(MODULE_DIR)/$(VARIANTPLATFORM).$(TEST_OPTION).bat test/$(MODULE_NAME).$(TEST_OPTION).bat"
            endif
        endif
    endif

    # ROMTARGET
    ifneq ($(ROMTARGET),)
        ifneq ($(words $(ROMTARGET)),1)
            ROMTARGETALL:=$(ROMTARGET)
            ROMTARGET:=$(word 1,$(ROMTARGET))
        endif

        ifeq ($(ROMTARGET),<none>)
            BUILDROMTARGET:=
        else
            ifneq ($(ROMTARGET),+)
                ifneq ($(notdir $(ROMTARGET)),)
                    ROMFILE:=$(notdir $(ROMTARGET))
                endif
                ifneq ($(dir $(ROMTARGET)),./)
                    ROMPATH:=$(dir $(ROMTARGET))
                endif
            endif
        endif
    endif
endif

# Generate both old and new format .iby files by default
# These differ by ROMFILETYPE and the way that macros are used for the release tree location
ROMFILENAME:=$(ROMDIR)$(PLATFORM)$(ROMTEST).iby
ROMFILENAME_NOKIA:=$(ROMDIR)$(PLATFORM)$(ROMTEST)n.iby

# RAMTARGET
ifneq ($(RAMTARGET),)
    ROMDECORATIONS_RAM:=" attrib=r"
    ifneq ($(RAMTARGET),+)
        ifneq ($(notdir $(RAMTARGET)),)
            ROMFILE_RAM:=$(notdir $(RAMTARGET))
        endif
        ifneq ($(dir $(RAMTARGET)),./)
            ROMPATH_RAM:=$(dir $(RAMTARGET))
        endif
    endif
endif

define BuildRomfileTarget
$(ALLTARGET)::ROMFILE
ROMFILE::$(ROMFILENAME) $(ROMFILENAME_NOKIA)

$(ROMFILENAME)::
	$(call startrule,rombuild) \
	$(GNUMKDIR) -p $(ROMDIR) \
	$(if $(ROMFILE_CREATED_$(TOBLDINF)),,&& echo -e "// $(subst $(EPOCROOT)/,,$(ROMFILENAME))\n//\n$(DATATEXT)" > $(ROMFILENAME)) \
	$(if $(BUILDROMTARGET),&& echo "$(ROMFILETYPE)=$(RELEASE_ROOT_DIR)/##$(ABIDIR)##/##BUILD##/$(TARGET)$(if $(EXPLICITVERSION),{$(VERSIONHEX)},).$(REQUESTEDTARGETEXT)   $(1)$(ROMDECORATIONS)" >> $(ROMFILENAME)) \
	$(if $(RAMTARGET),&& echo "$(ROMFILETYPE_RAM)=$(RELEASE_ROOT_DIR)/##$(ABIDIR)##/##BUILD##/$(TARGET)$(if $(EXPLICITVERSION),{$(VERSIONHEX)},).$(REQUESTEDTARGETEXT)   $(ROMPATH_RAM)$(ROMFILE_RAM)$(ROMDECORATIONS_RAM)" >> $(ROMFILENAME))
	$(call endrule,rombuild)

$(ROMFILENAME_NOKIA)::
	$(call startrule,rombuild_nokia) \
	$(GNUMKDIR) -p $(ROMDIR) \
	$(if $(ROMFILE_CREATED_$(TOBLDINF)),,&& echo -e "// $(subst $(EPOCROOT)/,,$(ROMFILENAME_NOKIA))\n//\n$(DATATEXT)" > $(ROMFILENAME_NOKIA)) \
	$(if $(BUILDROMTARGET),&& echo "$(ROMFILETYPE_NOKIA)=ABI_DIR/BUILD_DIR/$(TARGET)$(if $(EXPLICITVERSION),{$(VERSIONHEX)},).$(REQUESTEDTARGETEXT)   $(1)$(ROMDECORATIONS)" >> $(ROMFILENAME_NOKIA)) \
	$(if $(RAMTARGET),&& echo "$(ROMFILETYPE_RAM)=ABI_DIR/BUILD_DIR/$(TARGET)$(if $(EXPLICITVERSION),{$(VERSIONHEX)},).$(REQUESTEDTARGETEXT)   $(ROMPATH_RAM)$(ROMFILE_RAM)$(ROMDECORATIONS_RAM)" >> $(ROMFILENAME_NOKIA)) \
	$(call endrule,rombuild_nokia)
endef

# When VARIANTTYPE changes, romfile is finished,
# apart from if this is a new component......
ifneq ($(PREVIOUSVARIANTTYPE),)
    ifneq ($(VARIANTTYPE),$(PREVIOUSVARIANTTYPE))
        ifneq ($(ROMFILE_CREATED_$(TOBLDINF)),)
            ROMFILEFINISHED:=1
        else
            ROMFILEFINISHED:=
        endif
    endif
endif

# When romfile is finished, don't continue to add to it
ifeq ($(ROMFILEFINISHED),)
    $(eval $(call BuildRomfileTarget,$(ROMPATH)$(ROMFILE)))
endif

# Don't allow romfile to be recreated for every MMP
ifeq ($(ROMFILE_CREATED_$(TOBLDINF)),)
    ROMFILE_CREATED_$(TOBLDINF):=1
endif

# Build other ROMTARGETs if there is more than one
ifneq ($(ROMTARGETALL),)
    RAMTARGET:=
    $(foreach ROMTARGET,$(wordlist 2,$(words $(ROMTARGETALL)),$(ROMTARGETALL)),$(eval $(call BuildRomfileTarget,$(ROMTARGET))))
    ROMTARGETALL:=
endif

# Keep track of variant type while romfile is being created
PREVIOUSVARIANTTYPE:=$(VARIANTTYPE)

WHATRELEASE:=$(WHATRELEASE) $(ROMFILENAME) $(ROMFILENAME_NOKIA)


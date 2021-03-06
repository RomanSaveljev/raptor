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
# Post-linking macros for supported e32 base architectures
#
#

define e32postlink_arm
	$(POSTLINKER) \
	  --sid=0x$(if $(SID),$(SID),$(if $(UID3),$(UID3),0)) \
	  --version=$(VERSION) \
	  --capability=$(FINAL_CAPABILITIES) \
	  --linkas=$(call dblquote,$(LINKASVERSIONED)) \
	  --fpu=$(POSTLINKER_FPU) \
	  --targettype=$(POSTLINKTARGETTYPE) \
	  --output=$$(call dblquote,$$@) \
	  --elfinput=$(call dblquote,$(LINK_TARGET)) \
	  $(if $(UID1),--uid1=0x$(UID1),) \
	  $(if $(UID2),--uid2=0x$(UID2),) \
	  $(if $(UID3),--uid3=0x$(UID3),) \
	  $(if $(VENDORID),--vid=0x$(VENDORID),) \
	  $(if $(EXPTARGET),--customdlltarget,) \
	  $(if $(ARMLIBS),--excludeunwantedexports,) \
	  $(if $(EPOCALLOWDLLDATA),--dlldata,) \
	  $(if $(EPOCPROCESSPRIORITY),--priority=$(EPOCPROCESSPRIORITY),) \
	  $(if $(EPOCSTACKSIZE),--stack=0x$(EPOCSTACKSIZE),) \
	  $(if $(EPOCHEAPSIZEMIN),--heap=0x$(EPOCHEAPSIZEMIN)$(CHAR_COMMA)0x$(EPOCHEAPSIZEMAX),) \
	  $(if $(EPOCFIXEDPROCESS),--fixedaddress,) \
	  $(if $(EPOCDATALINKADDRESS),--datalinkaddress=$(EPOCDATALINKADDRESS),) \
	  $(if $(NAMEDSYMLKUP),--namedlookup,) \
	  $(if $(SMPSAFE),--smpsafe,) \
	  $(if $(POSTLINKDEFFILE),--definput=$(POSTLINKDEFFILE),) \
	  $(if $(EXPORTUNFROZEN),--unfrozen,) \
	  $(if $(AUTOEXPORTS),--sysdef=$(call dblquote,$(AUTOEXPORTS)),) \
	  $(if $(CANIGNORENONCALLABLE), \
	    $(if $(IMPORTLIBRARYREQUIRED),,--ignorenoncallable),) \
	  $(if $(CANHAVEEXPORTS), --defoutput=$(call dblquote,$(GENERATED_DEFFILE)) --dso=$(GENERATED_DSO)) \
	  $(if $(filter $(VARIANTTYPE),$(DEBUGGABLE)),--debuggable,) \
	  $(if $(POSTLINKER_SUPPORTS_WDP), \
	    --codepaging=$(PAGEDCODE_OPTION) --datapaging=$(PAGEDDATA_OPTION), \
	    $(POSTLINKER_PAGEDOPTION)) \
	  $(if $(NOCOMPRESSTARGET),--uncompressed, \
	    $(if $(INFLATECOMPRESSTARGET),--compressionmethod=inflate, \
	      $(if $(BYTEPAIRCOMPRESSTARGET),--compressionmethod=bytepair, \
	        --compressionmethod=$(POSTLINKER_COMPRESSION_DEFAULT)))) \
	  --libpath="$(call concat,$(PATHSEP)$(CHAR_SEMIC),$(strip $(RUNTIME_LIBS_PATH) $(STATIC_LIBS_PATH)))"
endef

define e32postlink_x86
	$(POSTLINKER) \
	  -sid 0x$(if $(SID),$(SID),$(if $(UID3),$(UID3),0)) \
	  -version $(VERSION) \
	  -capability $(FINAL_CAPABILITIES) \
	  $(if $(UID1),-uid1 0x$(UID1),) \
	  $(if $(UID2),-uid2 0x$(UID2),) \
	  $(if $(UID3),-uid3 0x$(UID3),) \
	  $(if $(VENDORID),-vid 0x$(VENDORID),) \
	  $(if $(EPOCALLOWDLLDATA),-allow,) \
	  $(if $(EPOCPROCESSPRIORITY),-priority $(EPOCPROCESSPRIORITY),) \
	  $(if $(EPOCSTACKSIZE),-stack 0x$(EPOCSTACKSIZE),) \
	  $(if $(EPOCHEAPSIZEMIN),-heap 0x$(EPOCHEAPSIZEMIN) 0x$(EPOCHEAPSIZEMAX),) \
	  $(if $(EPOCFIXEDPROCESS),-fixed,) \
	  $(if $(EPOCDATALINKADDRESS),-datalinkaddress $(EPOCDATALINKADDRESS),) \
	  $(if $(SMPSAFE),-smpsafe,) \
	  $(if $(POSTLINKER_SUPPORTS_WDP), \
	    -codepaging $(PAGEDCODE_OPTION) -datapaging $(PAGEDDATA_OPTION), \
	    $(POSTLINKER_PAGEDOPTION)) \
	  $(if $(NOCOMPRESSTARGET),-uncompressed, \
	    $(if $(BYTEPAIRCOMPRESSTARGET),-compressionmethod bytepair, \
	      -compressionmethod $(POSTLINKER_COMPRESSION_DEFAULT))) \
	  $(call dblquote,$(LINK_TARGET)) \
	  $$(call dblquote,$$@)
endef

# e32linkerfeedback_*
#
# Currently only implemented for ARM builds using RVCT
#
# The process here amounts to:
# if a feedback file doesn't exist, or exists but is different to the one just
# generated by the linker, then:
# (a) copy the one just generated by the linker to a known location so it can
#     be used in the compile stage of later builds and
# (b) explicitly sleep and then update the copied file's time-stamp in order to
#     guarantee it is later than existing object files from which the linked
#     binary was built (thus ensuring dependency based re-compilation in later
#     builds where file system time-stamp granularity is otherwise insufficient).
#
# Note: as linker feedback files contain time-stamps, these are ignored in the diff.
#
define e32linkerfeedback_arm
	if [ ! -e $(FEEDBACKFILENAME) ] || [ -n "`$(GNUDIFF) --ignore-matching-lines='.*Last Updated:.*' --brief $(FEEDBACKFILENAME) $(FEEDBACKFILENAME)_temp`" ]; then \
	$(GNUCP) $(FEEDBACKFILENAME)_temp $(FEEDBACKFILENAME); \
	sleep 1; \
	$(GNUTOUCH) $(FEEDBACKFILENAME); \
	fi;
endef


# python FLM generator for TOOLS2 EXE

import planb.agent
import planb.target

agent = planb.agent.Connect()

print "TESTS:"
print "TARGET =", agent.TARGET
print "TEGRAT =", agent.TEGRAT

comments = """
tools2 common

## Input parameters

ifeq ($(filter win,$(HOSTPLATFORM)),win)
CDEFS.TOOLS2:=$(CDEFS.WIN32) $(CDEFS)
CFLAGS:=$(CFLAGS.WIN32) $(CFLAGS) $(OPTION_GCC)
COMPILER_PATH:=$(COMPILER_PATH.WIN32)
OUTPUTPATH:=$(OUTPUTPATH)/$(TARGET)_$(TARGETTYPE)/tools2/$(VARIANTTYPE)$(TOOLPLATFORMDIR)
else
ifneq ($(TOOLS2WIN32),)
# Build win32 tools in Linux
CDEFS.TOOLS2:=$(CDEFS.WIN32) $(CDEFS)
CFLAGS:=$(CFLAGS.WIN32) $(CFLAGS) $(OPTION_GCC)
COMPILER_PATH:=$(COMPILER_PATH.WIN32)
OUTPUTPATH:=$(OUTPUTPATH)/$(TARGET)_$(TARGETTYPE)/tools2/$(VARIANTTYPE)
else
# Build linux tools in Linux
CDEFS.TOOLS2:=$(CDEFS.LINUX) $(CDEFS)
CFLAGS:=$(CFLAGS) $(OPTION_GCC)
COMPILER_PATH=$(COMPILER_PATH.LINUX)
OUTPUTPATH:=$(OUTPUTPATH)/$(TARGET)_$(TARGETTYPE)/tools2/$(VARIANTTYPE)$(TOOLPLATFORMDIR)
endif
endif


CDEFS.TOOLS2:=$(call makemacrodef,$(OPT.D),$(CDEFS.TOOLS2))

## Locally used variables
CREATABLEPATHS:=$(OUTPUTPATH) $(RELEASEPATH) $(TOOLSPATH)

## Global targets
$(ALLTARGET):: $(TARGETS)
TARGET:: $(TARGETS)

## Pre-Include directories
ifneq ($(INC.COMPILER),)
PINCLUDE:=$(patsubst %,$(OPT.PREINCLUDE)%,$(INC.COMPILER))
endif

## User and System Include directories
ifneq ($(USERINCLUDE),)
UINCLUDE:=$(patsubst %,$(OPT.USERINCLUDE)%,$(USERINCLUDE))
endif
ifneq ($(SYSTEMINCLUDE),)
SINCLUDE:=$(patsubst %,$(OPT.SYSTEMINCLUDE)%,$(SYSTEMINCLUDE))
endif

INCLUDES:=$(PINCLUDE) $(UINCLUDE) $(SINCLUDE)

## Source files
CPPFILES:=$(filter %.CPP,$(SOURCE))
cppFILES:=$(filter %.cpp,$(SOURCE))
CFILES:=$(filter %.C,$(SOURCE))
cFILES:=$(filter %.c,$(SOURCE))

## Object files
CPPOBJFILES:=$(patsubst %,$(OUTPUTPATH)/%,$(notdir $(patsubst %.CPP,%.o,$(CPPFILES))))
cppOBJFILES:=$(patsubst %,$(OUTPUTPATH)/%,$(notdir $(patsubst %.cpp,%.o,$(cppFILES))))
COBJFILES:=$(patsubst %,$(OUTPUTPATH)/%,$(notdir $(patsubst %.C,%.o,$(CFILES))))
cOBJFILES:=$(patsubst %,$(OUTPUTPATH)/%,$(notdir $(patsubst %.c,%.o,$(cFILES))))
OBJECTFILES:=$(CPPOBJFILES) $(cppOBJFILES) $(cOBJFILES) $(COBJFILES)

CLEANTARGETS:=
## Compile CPP and cpp files
define compile2object
$(eval compile2object_TARGET:=$(OUTPUTPATH)/$(patsubst %.$(2),%.o,$(notdir $(1))))
$(eval DEPENDFILENAME:=$(compile2object_TARGET).d)
$(eval DEPENDFILE:=$(wildcard $(DEPENDFILENAME)))
$(compile2object_TARGET): $(1) $(if (DEPENDFILE),,EXPORT)
	$(call startrule,compile2object,,$(1)) \
	$(if $(COMPILER_PATH),COMPILER_PATH="$(COMPILER_PATH)",) \
	$(COMPILER) $(CFLAGS) $(CDEFS.TOOLS2) \
	$(if $(NO_DEPEND_GENERATE),,-MD -MT"$$@" -MF"$(DEPENDFILENAME)") \
	$(INCLUDES) $(OPT.O)"$$@" "$(1)" \
	$(call endrule,compile2object)

ifeq ($(NO_DEPEND_GENERATE),)
  CLEANTARGETS:=$$(CLEANTARGETS) $(DEPENDFILENAME)
endif

ifneq ($(DEPENDFILE),)
  ifeq ($(NO_DEPEND_INCLUDE),)
    ifeq ($(filter %CLEAN,$(call uppercase,$(MAKECMDGOALS))),)
      -include $(DEPENDFILE)
    endif
  endif
endif

endef

$(foreach SRC,$(CPPFILES),$(eval $(call compile2object,$(SRC),CPP)))
$(foreach SRC,$(cppFILES),$(eval $(call compile2object,$(SRC),cpp)))
$(foreach SRC,$(CFILES),$(eval $(call compile2object,$(SRC),C)))
$(foreach SRC,$(cFILES),$(eval $(call compile2object,$(SRC),c)))

### Conclusion - cleanup and introspection #######################

# make the output directories while reading makefile - some build engines prefer this
$(call makepath,$(CREATABLEPATHS))

## Clean up
$(call raptor_clean,$(CLEANTARGETS) $(OBJECTFILES))
## for the --what option and the log file
$(call raptor_release,$(RELEASABLES))

## The End



tools2.EXE



## Outputs - externally relevant targets that this FLM generates
ifeq ($(filter win,$(HOSTPLATFORM)),win)
SYSTEMLIBS:=$(LIBS.WIN32)
else
ifneq ($(TOOLS2WIN32),)
# Build win32 tools in Linux 
SYSTEMLIBS:=$(LIBS.WIN32)
else
# Build linux tools in Linux
SYSTEMLIBS:=$(LIBS.LINUX)
endif
endif


EXETARGET:=$(RELEASEPATH)/$(TARGET)$(DOTEXE)

INSTALLED:=
ifneq ($(TOOLSPATH),)
INSTALLED:=$(TOOLSPATH)/$(TARGET)$(DOTEXE)
endif

## Target groups
RELEASABLES:=$(INSTALLED)
TARGETS:=$(EXETARGET) $(INSTALLED)

## Common build steps (compiling and cleaning)
include $(FLMHOME)/tools2common.flm

## Static libraries
ifneq ($(STATICLIBRARY),)
STATICLIBS:=$(patsubst %,$(RELEASEPATH)/lib%.a,$(STATICLIBRARY))
LLIBS:=$(OPT.L)"$(RELEASEPATH)" $(patsubst %,$(OPT.l)%,$(STATICLIBRARY))
#
ifneq ($(SYSTEMLIBS),)
LLIBS:=$(LLIBS) $(patsubst %,$(OPT.l)%,$(SYSTEMLIBS))
endif
#
endif

## Link executable
# get OBJECTFILES from call to tools2common
define tools2linkexe
$(EXETARGET): $(OBJECTFILES) $(STATICLIBS)
	$(call startrule,tools2linkexe) \
	$(LINKER) $(CFLAGS) $(LFLAGS) $(OPT.O)"$(EXETARGET)" $(call dblquote,$(OBJECTFILES)) $(LLIBS) $(LINKER_OPTIONS) \
	$(if $(SAVESPACE),; $(GNURM) -rf $(OUTPUTPATH); true,) \
	$(call endrule,tools2linkexe)

endef

$(eval $(call tools2linkexe))

	
## Copy executable to the tools directory
ifneq ($(TOOLSPATH),)
define tools2install
$(INSTALLED): $(EXETARGET)
	$(call startrule,tools2install) \
	$(GNUCP) "$(EXETARGET)" "$(INSTALLED)" && \
	$(GNUCHMOD) a+rwx "$(INSTALLED)" \
	$(call endrule,tools2install)
endef

$(eval $(call tools2install))

endif

## The End
"""

agent.commit()
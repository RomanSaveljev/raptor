
# test a "real" raptor gluefile
# generated by Raptor 0.0.1

RAPTOR_HOME?=/localhome/tmurphy/pf/EPOC/development/tools/personal/tmurphy/tools/raptor
EPOCROOT?=/tmp/tim-epocroot/

# start simple 

# configuration ARMV5_UDEB
AAPCS_OPTION:=--apcs /inter
CAPABILITY:=LocalServices ReadDeviceData ReadUserData
CC:=armcc
CC_ERRORS_CONTROL_OPTION:=--diag_error 1267
CC_WARNINGS_CONTROL_OPTION:=--diag_suppress 161,611,654,997,1152,1300,1464,1488,6318
CDEFS:=__MARM_THUMB__ __MARM_INTERWORK__ _UNICODE __SYMBIAN32__ __ARMCC__ __EPOC32__ __MARM__ __EABI__ __PRODUCT_INCLUDE=\"$(EPOCROOT)/epoc32/include/variant/Symbian_OS_vFuture.hrh\" _EXE_
CFLAGS:=
COMMANDFILE_OPTION:=--via
COMPILE_ONLY_OPTION:=-c
CPP_LANG_OPTION:=--cpp
CREATABLEPATHS:=
SOURCEFILES:=$(RAPTOR_HOME)/test/simple/test.cpp
ELF2E32:=$(EPOCROOT)/epoc32/tools/elf2e32$(DOTEXE)
ENUM_OPTION:=--enum_is_int
EXCEPTIONS:=--exceptions --exceptions_unwind
EXEBASELIBS:=usrt2_2.lib euser.dso efsrv.dso bafl.dso commsdat.dso
EXENAME:=test
EXPORT_VTBL_OPTION:=--export_all_vtbl
FLMHOME:=$(RAPTOR_HOME)/lib/flm
FPMODE_OPTION:=--fpmode ieee_no_fenv
FULLVARIANTPATH:=ARMV5/UDEB
INCLUDES:=-J $(EPOCROOT)/epoc32/include -J $(EPOCROOT)/epoc32/include/variant
LD:=armlink
LIBPATH:=
LINKER_DEBUG_OPTION:=--debug
LINKER_ENTRY_OPTION:=--entry
LINKER_SYMBOLS_FILE_OPTION:=--list
LINKER_SYMBOLS_OPTION:=--symbols
OUTPUTPATH:=$(EPOCROOT)/epoc32/build
OUTPUT_OPTION:=-o
OWN_LIBRARY_OPTION:=-Ono_known_library
PREINCLUDE_OPTION:=--preinclude $(EPOCROOT)/epoc32/include/rvct2_2/rvct2_2.h
RELEASEPATH:=$(EPOCROOT)/epoc32/release
RUNTIME_LIBS_LIST:=drtaeabi.dso dfpaeabi.dso dfprvct2_2.dso scppnwdl.dso drtrvct2_2.dso
RUNTIME_LIBS_PATH:=$(EPOCROOT)/epoc32/release/ARMV5,$(EPOCROOT)/epoc32/release/ARMV5/LIB
RUNTIME_SYMBOL_VISIBILITY_OPTION:=--dllimport_runtime
RW_BASE_OPTION:=--rw-base
SHARED_OBJECT_OPTION:=--dll
SID:=0x10003a5c
SOFTVFPMODE_OPTION:=
SO_NAME_OPTION:=--soname
SPLIT_OPTION:=--split
STACKSIZE:=0x00005000
STATIC_LIBS_LIST:="h_t__uf.l(switch8.o)"
STATIC_LIBS_PATH:=/usr/local/ARM/RVCT/Data/2.2/308/lib/armlib
SYMBIAN_CCFLAGS:=-g -O0
SYMBIAN_LINK_FLAGS:=--diag_suppress 6331  --bpabi --reloc   --no_scanlib --datacompressor=off
SYMVER_OPTION:=--symver_soname
TARGETTYPE:=EXE
TARGET_ARCH_OPTION:=--cpu 5T
THUMB_INSTRUCTION_SET:=--thumb
UID1:=0x1000007a
UID2:=0x100039ce
UID3:=0x00000001
USER_LIBS_PATH_OPTION:=--userlibpath
VARIANTTYPE:=UDEB
VFE_OPTION:=--no_vfe
include $(FLMHOME)/e32abiv2exe.flm


# configuration ARMV5_UREL
AAPCS_OPTION:=--apcs /inter
CAPABILITY:=LocalServices ReadDeviceData ReadUserData
CC:=armcc
CC_ERRORS_CONTROL_OPTION:=--diag_error 1267
CC_WARNINGS_CONTROL_OPTION:=--diag_suppress 161,611,654,997,1152,1300,1464,1488,6318
CDEFS:=__MARM_THUMB__ __MARM_INTERWORK__ _UNICODE __SYMBIAN32__ __ARMCC__ __EPOC32__ __MARM__ __EABI__ __PRODUCT_INCLUDE=\"$(EPOCROOT)/epoc32/include/variant/Symbian_OS_vFuture.hrh\" _EXE_
CFLAGS:=
COMMANDFILE_OPTION:=--via
COMPILE_ONLY_OPTION:=-c
CPP_LANG_OPTION:=--cpp
CREATABLEPATHS:=
SOURCEFILES:=$(RAPTOR_HOME)/test/simple/test.cpp
ELF2E32:=$(EPOCROOT)/epoc32/tools/elf2e32$(DOTEXE)
ENUM_OPTION:=--enum_is_int
EXCEPTIONS:=--exceptions --exceptions_unwind
EXEBASELIBS:=usrt2_2.lib euser.dso efsrv.dso bafl.dso commsdat.dso
EXENAME:=test
EXPORT_VTBL_OPTION:=--export_all_vtbl
FLMHOME:=$(RAPTOR_HOME)/lib/flm
FPMODE_OPTION:=--fpmode ieee_no_fenv
FULLVARIANTPATH:=ARMV5/UREL
INCLUDES:=-J $(EPOCROOT)/epoc32/include -J $(EPOCROOT)/epoc32/include/variant
LD:=armlink
LIBPATH:=
LINKER_DEBUG_OPTION:=--debug
LINKER_ENTRY_OPTION:=--entry
LINKER_SYMBOLS_FILE_OPTION:=--list
LINKER_SYMBOLS_OPTION:=--symbols
OUTPUTPATH:=$(EPOCROOT)/epoc32/build
OUTPUT_OPTION:=-o
OWN_LIBRARY_OPTION:=-Ono_known_library
PREINCLUDE_OPTION:=--preinclude $(EPOCROOT)/epoc32/include/rvct2_2/rvct2_2.h
RELEASEPATH:=$(EPOCROOT)/epoc32/release
RUNTIME_LIBS_LIST:=drtaeabi.dso dfpaeabi.dso dfprvct2_2.dso scppnwdl.dso drtrvct2_2.dso
RUNTIME_LIBS_PATH:=$(EPOCROOT)/epoc32/release/ARMV5,$(EPOCROOT)/epoc32/release/ARMV5/LIB
RUNTIME_SYMBOL_VISIBILITY_OPTION:=--dllimport_runtime
RW_BASE_OPTION:=--rw-base
SHARED_OBJECT_OPTION:=--dll
SID:=0x10003a5c
SOFTVFPMODE_OPTION:=
SO_NAME_OPTION:=--soname
SPLIT_OPTION:=--split
STACKSIZE:=0x00005000
STATIC_LIBS_LIST:="h_t__uf.l(switch8.o)"
STATIC_LIBS_PATH:=/usr/local/ARM/RVCT/Data/2.2/308/lib/armlib
SYMBIAN_CCFLAGS:=-O2
SYMBIAN_LINK_FLAGS:=--diag_suppress 6331  --bpabi --reloc   --no_scanlib --datacompressor=off
SYMVER_OPTION:=--symver_soname
TARGETTYPE:=EXE
TARGET_ARCH_OPTION:=--cpu 5T
THUMB_INSTRUCTION_SET:=--thumb
UID1:=0x1000007a
UID2:=0x100039ce
UID3:=0x00000001
USER_LIBS_PATH_OPTION:=--userlibpath
VARIANTTYPE:=UREL
VFE_OPTION:=--no_vfe
include $(FLMHOME)/e32abiv2exe.flm

# end simple 

# END OF GENERATED MAKEFILE : DO NOT EDIT

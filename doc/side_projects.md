# Hobbies, side projects and work-in-progress #

= Using Raptor in pre-Symbian Foundation SDKs =

'''This page contains information that's nothing to do with the team developing Raptor, and isn't supported or endorsed by them. As such, you should use information from here at your own risk.  This is EXPERIMENTAL support and may not work.''' 

Raptor does not support the public SDKs that are available for pre-Symbian Foundation platforms that are available from Nokia (S60 5th edition, S60 3rd edition, etc.).  However, it is possible to make it work if you are willing to accept a few limitations:

# Raptor only works in ABIv2 mode.
# Some source code that builds with abld in ABIv1 mode may not build with Raptor (or abld in ABIv2 mode, for that matter)
# This is completely unsupported by the team that develop Raptor, and may produce broken binaries.
== S60 5th edition  ==
These instructions are based on a quick hacking session to get Raptor working.  They have not yet been verified to produce correct binaries in all cases.  They may also not work for you, in which case you're encouraged to leave feedback here describing the problem, or fix it.  '''Using Raptor in this environment should only be considered experimental at this time.'''

(To get this working, I took files from the Symbian^3 PDK.  '''That was not the correct thing to do.'''  The correct thing to do is to patch the versions of the tools that came with the SDKs originally, as later versions of tools will have additional functionality that may not be supported on the underlying platform.  However, the source for those versions of the tools is not currently available under an open source license, so it's not currently possible to do this. Until this is done properly, it's not recommended to use this for anything other than experimental purposes.)

 *  checklib.exe is needed
 *  an updated version of elf2e32 is needed, that fixes a problem where it returns error code 0 even on failure
 *  an updated version of def2dll. pl is needed
 *  /epoc32/sbs_config/os_properties.xml should be added to the SDK (you can use the example file in Raptor)
 *  /epoc32/tools/makefile_templates/s60/ is needed for the mifconv FLMs
 *  an updated version of mifconv is needed that supports the -f and -i flags
== S60 3rd edition, feature pack 2  ==
 *  efreeze.pl from the S60 5th edition SDK is also needed.
== S60 3rd edition, feature pack 1  ==
There are some additional steps needed for which I don't have complete instructions.  Certainly there are problems with bmconv, and svgtbinencode.  The warnings about using unsupported tools versions from later Symbian releases apply even more strongly here...
=  What still needs to be done  =
# abld needs to be run in ABIv2 mode, and the calls to the tools compared to what Raptor does, to understand if there are any new arguments being passed by Raptor that would not be passed by abld (this would occur because Raptor doesn't support these old OS versions, so may assume features in tools that were not present in older versions.  Since we've cheated and used newer tools, we wouldn't see this as an error)
# The binaries produced need to be tested extensively to ensure they work.
# The updated versions of the tools needs to be checked using abld (particularly with GCC-E) to make sure nothing has broken



= Bootstrapping the Symbian build tools on Ubuntu Linux =


I have populated a repository with a package that provides an Ubuntu hosted build of the Symbian build tools. This repo is https://developer.symbian.org/oss/FCL/interim/sftools/linux_build/. It is originally baselined on the MCL Symbian build tools package, https://developer.symbian.org/oss/MCL/sftools/dev/build/, at revision 0f5e3a7fb6af and on PDK 3.0.i. The sbsv2 component (Raptor) has been updated from v2.10 to v2.15

This package fixes the baseline so that:-

 *  All targets will build without errors or warnings on an Ubuntu 10.4 host using the GCC 4.4.x toolchain and corresponding Standard C++ Library, compiling to the c++0x standard.
 *  All targets will build without errors or warnings on a 32-bit Windows XP host using the Mingw GCC 3.4.x toolchain and corresponding Standard C++ Library, from a Symbian PDT 1.6 installation.

As implied by those objectives, the build for both Linux and Windows does not use the 3rd party STLPort implementation of the Standard C++ Library that is bundled in Symbian PDKs so that the build tools can be built. There is hence no need to download the '''binaries_epoc32_stlport''' component of the 3.0.i PDK to build the package.

The Windows/GCC 3.4 build is supported only to ensure that the Linux/GCC 4.4 build remains portable to the Windows Mingw GCC toolchain. You are expected to get Raptor from the PDT on Windows, rather than build it, because nothing is changed in the Raptor build.

There are numerous code changes to the upstream MCL package, but they are all superficial adaptations to the more restrictive portability goals, except in a few places where Linux-targeted implementations were TODO.      

The package is likely to build with little difficulty on other up-to-date 32bit GNU/Linux hosts. E.g. On Debian 5 with GCC 4.3, only the imgtools/romtools target fails, because the distribution's boost libraries are too old.

The package provides portable (Windows/Linux) perl tools for working with it. These perl tools reside in the '''cross-plat-dev-utils''' directory of the package and expect to be run from there. On both Windows and Linux, it is necessary to tweak the Raptor runtime configuration and apply minor patches to the epoc32 tree to achieve the objective. A perl tool is included to apply all these preparations.
== Install the host toolchain ==

{{{
$ sudo apt-get install build-essential
}}}

== For x86_64 hosts  ==
{{{
$ sudo apt-get install gcc-multilib
$ sudo apt-get install lib32stdc++6
$ sudo ln -s /usr/lib32/libstdc++.so.6 /usr/lib32/libstdc++.so
$ sudo ln -s /usr/lib32/libgcc_s.so.1 /usr/lib32/libgcc_s.so
}}}

On 64-bit hosts you will also later need to install 32-bit variants of some libraries using the '''getlibs''' tools. Download and install the '''getlibs-all.deb''' package from http://frozenfox.freehostia.com/cappy/

== Install the host prerequisites for building Raptor ==

{{{
$ sudo apt-get install bison
$ sudo apt-get install ncurses-dev
$ sudo apt-get install libbz2-dev
}}}

== Install 7z to unpack the PDK archives  ==
Although PDK archives have the extension .zip they are in fact 7z archives and the zip tool will not open
them.

{{{
$ sudo apt-get install p7zip-full
}}}

== Install the host prerequisites for building other targets ==

Install the boost libraries and their headers:

The package inherits from the MCL a bundled defective copy of the boost libraries v1.39 for building the imgtools/imglib
target. The headers of this copy are broken for Linux, so the Linux build is fixed to expect boost libraries
from the system. v1.40 is OK. (v1.35 is too old)

{{{
$ sudo apt-get install libboost1.40* # or whatever is the latest version for your distribution
}}}

== For x86_64 hosts  ==
You need to have the 32-bit variant of the boost threads library:

{{{
$ sudo getlibs -p libboost-thread1.40.0 # or whatever is the latest version for your distribution
$ ln -s /usr/lib32/libboost_thread.so.1.40.0 /usr/lib32/libboost_thread-mt.so
}}}



Install libxml2 and its headers:

{{{
$ sudo apt-get install libxml2
$ sudo apt-get install libxml2-dev
}}}

== For x86_64 hosts  ==
You need to have the 32-bit variant of libxml2:

{{{
$ sudo getlibs -p libxml2
}}}

libxml2 is also bundled in the package, as per MCL, for building the imgtools/imgcheck target, but there is no target that
exports the library so the linker fails to find it for the imgcheck build.
== Create an epocroot for building the tools ==

{{{
$ mkdir ~/epocroot-pdk-3.0.i
}}}

== Get the linux_build Package from the Symbian OSS repo ==

{{{
$ cd ~/epocroot-pdk-3.0.i
$ hg clone https://developer.symbian.org/oss/FCL/interim/sftools/linux_build/
}}}

== Build Raptor  ==

{{{
$ cd ~/epocroot-pdk-3.0.i/linux_build/cross-plat-dev-utils
$ ./build_raptor.pl
}}}

This build will take some minutes.
== Install the epoc32 build environment ==

To download the necessary PDK components, browse to http://developer.symbian.org/main/tools_and_kits/downloads/view.php?id=5

If PDK 3.0.i is current then its components will be listed under Downloads on this page. Otherwise follow the Previous Releases link and browse to the page for PDK 3.0.i

Download the following zip archives only:

 *  binaries_epoc.zip,
 *  binaries_epoc_sdk.zip
 *  tools_epoc.zip

Copy all these archives to ~/epocroot-pdk-3.0.i

Unzip them all with 7z to populate the epoc32 tree:

{{{
$ cd ~/epocroot-pdk-3.0.i
$ for file in *.zip; do 7z x $file; done
}}}

== Apply necessary fixes to the epoc32 tree and Raptor runtime config  ==

{{{
$ cd ~/epocroot-pdk-3.0.i/linux_build/cross-plat-dev-utils
$ ./prep_env.pl
}}}

'''prep_env.pl''' is a wrapper for the fix scripts appropriate to the Linux/Windows host.

On Linux, this script will:

 *  Apply a workaround for bug #1399
 *  Patch Raptor's gcc runtime config file so that:
  *  The GCC toolchain is configured to be the host GCC toolchain and not the Windows Mingw GCC toolchain
  *  The Standard C++ Library is configured to be the host GCC standard library and not the SLTPPort 5.1 implementation.
  *  GCC is configured to compile to the c++0x standard.
 *  Install a GCC pre-include header in epoc32/include/gcc that provides GCC 4.4 compatibility veneers.

On Windows, the script will:
 *  Patch Raptor's Mingw gcc runtime config file so that the Standard C++ Library is configured to be the Mingw GCC standard library and not the SLTPPort 5.1 implementation.
 *  Install a GCC pre-include header in epoc32/include/gcc that provides GCC 3.4 compatibility veneers.
== Read the READMEs ==
Read the README file in the package root directory, and README-LINUX the '''cross-plat-dev-utils''' directory (README-WINDOWS covers the same ground for Windows hosts.)
== Build All ==
{{{
$ cd ~/epocroot-pdk-3.0.i/linux_build/cross-plat-dev-utils
$ ./build_all.pl
}}}

This build will take some time. All being well, the built binaries will appear in '''~/epocroot-pdk3.0.i/epoc32/release/tools2/linux-????-libc2_??/{deb|rel}''', where '''linux-????-libc2_??''' is whatever Raptor designates as your '''HOSTPLATFORM_DIR'''. Exports that on Windows would appear in '''\plugins''' and '''\tools''' will appear respectively in '''~/epocroot-pdk3.0.i/plugins''' and '''~/epocroot-pdk3.0.o/tools'''.
== Tested? ==

 *  I have tested the built binaries as far (and no further) as having successfully used them to build Syborg/QEMU textshell and f32 test roms that boot and behave pretty well.
 *  I have made no attempt to test the portability of the perl, python and shell scripts that are exported by the build. (The .bat scripts that exported are obviously not portable.)

 

= Raptor 3 =


What Raptor 3 Should be

General purpose build system - more than Symbian. (prop: TimM)



== Notes for Study: The Open Build Service ==
 * http://www.youtube.com/watch?v=v3OMEAU_4HI&feature=related (REST vs SOAP - might be helpful)
 * http://www.youtube.com/watch?v=fa31g5A42Z4 (Open Build Service lecture - it's a bit dull but the beginning gives one an idea of how OBS works)
 * http://dspace.cc.tut.fi/dpub/bitstream/handle/123456789/20758/seppanen.pdf?sequence=3 OBS as used by meego - it's a pretty good paper and covers a lot of the questions I was asking myself e.g. the performance problem caused by building with virtual machines because, notionally, you have to create and configure a VM every time you rebuild a particular package. The Raptor team uses virtual machines to build it's utilities internally for different platforms for most of the same reasons that OBS does so it's of interest.
 * Open Build Service API: !https://api.opensuse.org/apidocs/

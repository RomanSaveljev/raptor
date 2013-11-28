# Howtos and In-depth Articles #

= How to build Raptor =

==  Obtaining the source code  ==

The Raptor source code is kept in a Mercurial repository here on `projects` at http://projects.developer.nokia.com/raptor/browser

You can simply clone this Mercurial repository using 
{{{
hg clone https://projects.developer.nokia.com/hg/raptor
}}}

This will create a `raptor` folder in your current directory, so move to the directory where you want this placed before running the command.

==  Repository layout and the branches of Raptor  ==

This section is out of date and mostly refers to the old Symbian Foundation repo.

Raptor is found in sbsv2/raptor inside the repository.  It is in the same place regardless of which branch of the repository you are viewing.

The build repository contains three branches:
 *  default
 *  'fix' - for defect fixes
 *  'wip' - feature work in progress

Our normal development practice is to make changes in the fix and wip branches as appropriate, and merge these into the default branch after doing sufficient release testing.  It's possible to create your own branches but given Mercurial will tend to create a new sub-branch whenever a new set of changes is made, this is rarely necessary.

==  Setting up the development environment  ==
Once the source repository has been cloned, a few further steps are required in order to get Raptor up and running. These differ between Linux and Windows.

In either case, you will have the directory `raptor` in the directory where you ran your `hg clone` command.
==  Linux Set up  ==
A Bash shell script called `sbs` is the command line interface to Raptor. This is located in `raptor/bin`. Ensure that this script and the `gethost.sh` script (in the same directory) have execute permissions.

Next, you need to add `raptor/bin` to your `PATH` environment variable:

{{{
export PATH=<somwhere>/raptor/bin:$PATH
}}}

Enter `sbs -v` and you should see an error message like this:

{{{
Error: sbs has not been installed with support for your platform: "linux unknown libc2_10".

The utilites for your platform should be in "/home/user/hg/build/sbsv2/raptor/linux-unknown-libc2_10" but sbs
cannot find them there.

sbs is supported on:
	win32
	linux i386 libc2_3 (Redhat 4)

sbs has been known to work (but is not supported) on:
	linux x86_64 libc2_5  (e.g. Centos/Redhat 5.3 64-bit)
	linux i386 libc2_8  (e.g. Fedora 9 32-bit)
	linux x86_64 libc2_10 (e.g. Fedora 11 64-bit)

Even with the appropriate utilities it may be necessary to install 32-bit
compatibility versions of some libraries (e.g. glibc) on these platforms,
particularly for 3rd party tools which are not built natively such as
compilers.

It may be possible to build and install the utilities for your platform by
entering /home/user/hg/build/sbsv2/raptor/util and running
	make -k
A full development environment is required however.
}}}

This example was taken from a Ubuntu 9.10 machine. To build the Raptor supporting tools, it is recommended that the following development packages are installed from your package manager (these are the Ubuntu/Debian names):
{{{
libncursesw5-dev
libreadline5-dev
libssl-dev
libgdbm-dev
libbz2-dev
libc6-dev
libsqlite3-dev
libgdbm-dev
libreadline5-dev
tcl8.4-dev
tk8.4-dev
}}}
Python is the main tool that depends on these development packages. Installing these ensures that almost all the Python modules are built.

Once you have installed these (as necessary), change directory to `raptor/util` and run `make -k`. This will build supporting utilities for Raptor. If you see any errors about packages not being found, you will have to install the development version of these for make to be able to succeed.
==  Windows Set up  ==

The setup for Windows is a little different and requires to set multiple additional env Variable.

You need to add sbs into the Path:
{{{
set PATH=C:\apps\raptor\bin;%PATH%
}}}

Raptor requires Cygwin (at least 1.5), Python (at least 2.6) and MinGW (at least 3.4.5) installed. They can be on the path, but must be pointed to by environment variables as described [wiki:Raptor_Environment_Variables here]. Cygwin 1.7 requires that `SBS_CYGWIN17` is set and points to the root of the Cygwin 1.7 installation.

At a DOS command shell, type `sbs -v` to see if it works. If you get an error, please follow the [wiki:Raptor_Environment_Variables#Troubleshooting troubleshooting] tips.

Notice: If you install your own MinGW on your Windows machine for use with Raptor, make sure to selcect the installation of the optional package Make and g++
==  Arm Tool Chain Set Up  ==
By tool chain, we mean the compilers and linkers and their supporting tools. Raptor supports the RVCT and GCCE tool chains.

By default, the RVCT tool chain requires certain environment variables to be available. For example, RVCT 2.2 uses at least these environment variables:

{{{
RVCT22BIN
RVCT22INC
RVCT22LIB
}}}

plus one to two for license settings. It is assumed that you have installed and configured RVCT appropriately for your network. At the time of writing, Raptor automatically detects the following versions of RVCT: 2.2, 3.1 and 4.0 from the environment variables set by the RVCT installers (or on Linux from certain shell scripts).

For GCCE, it is necessary for the user to set several environment variables to tell Raptor that versions of GCCE are installed. The reason for this is that the GCCE installers do not set any special environment variables other than optionally the PATH and it can convenient to switch between versions of GCCE in Raptor builds.

=== Releases pre-2.11.1 ===
Manually set the GCCEBIN environment variable to the bin directory inside your GCCE installation. 

=== Releases starting 2.11.1 onwards ===
Manually set the following environment variable to the bin directories inside your GCCE installations. 
{{{
SBS_GCCE432BIN
SBS_GCCE433BIN
SBS_GCCE441BIN
}}}
For example, on Linux, you might have have the following:
{{{
SBS_GCCE432BIN=/opt/symbian/GCCE432/arm-2008q3/bin
SBS_GCCE433BIN=/opt/symbian/GCCE433/arm-2009q1/bin
SBS_GCCE441BIN=/opt/symbian/GCCE441/arm-2009q3/bin
}}}
In this case, the directory names also indicate the corresponding CodeSourcery release of GCCE.

As a general convention in Raptor, any environment variable that Raptor is sensitive to, but that a user has to set themselves manually will have the prefix `SBS_` as in the example of the SBS_GCCExyzBIN environment variables. Conversely, the RVCT installers (or shell scripts) set the appropriate environment variables for the user, so they do not have the `SBS_` prefix.




= Tips for Big Builds with Raptor =


How to perform a large build efficiently with Raptor.
== Build from clean ==

Firstly, no make engine can cope with the number of dependencies that we produce for a build the size of Symbian OS. We will be working on ameliorating this problem, but for the moment building from clean is your only real option.
== Turn parallel parsing on ==

Use the `--pp=on` option to enable parallel parsing. For builds with many `BLD.INF`s to parse this can significantly reduce the time to parse them (for small numbers of `BLD.INF`s it can take longer).

However, note that you will need to perform the exports in a separate stage to the main build in order to avoid race conditions:

`sbs --export-only ...` (without `--pp=on`) then perform all other stages with `--pp=on --noexport` options.
== Perform target checking in a separate stage ==

Do not use the `--check` option, which is slow. Instead, run `sbs_filter --check` after the build to read the logs and check that all targets reported in the log are actually present on the file system.



= Building System Definition Layers in Order Using Raptor =


Raptor can build the layers of a system definition file in order. This can be useful in situations where one layer generates code or metadata that another layer might wish to use.

Here is an example system definition:
{{{
<SystemDefinition name="MCL" schema="2.0.0" >
 <systemModel>

  <layer name="GenerateSource">
  <!-- This layer creates source files and metadata -->
   <component name="metadata export">
    <unit bldFile="src/common/somecomponentA/gen" />
    <unit bldFile="src/common/somecomponentB/gen" />
    <unit bldFile="src/common/somecomponentC/gen" />
   </component>
  </layer>

  <layer name="All the ordinary components">
  <!-- This layer builds what was generated -->
   <component name="dependent">
    <unit bldFile="src/common/somecomponentA/group"/>
    <unit bldFile="src/common/somecomponentB/group"/>
    <unit bldFile="src/common/somecomponentC/group"/>
   </component>
  </layer>

 </systemModel>
</SystemDefinition>
}}}
To build the layers in order one uses the ordered layer option to sbs use {{{-o, --orderlayers}}}

like so:
{{{
sbs -s my_system_def.xml -o
}}}

to have the orders built in the order specified in <tt>my_system_def.xml</tt>.

Or use:
{{{
sbs -s my_system_def.xml -o -l layerA -l layerB
}}}

To build {{{layerA}}} first then {{{layerB}}}.




= Raptor Dependencies =

= Dependencies in Raptor =

Make relies on timestamps and therefore so does Raptor - so we don't know the difference between real and unreal change.

The basic dependency structure is
{{{
.c <- .o <- .sym <- .exe/.dll/.ldd/... <- ALL
}}}
I have attached a diagram which might be too complicated although it certainly misses out some things as well but it should give you an idea.
[wiki:File:Dependencies.png File:Dependencies.png]

The basic strategy is to generate accurate dependency information during the first build of each target for use when building incrementally later.

So at the first build there is no accurate information about exactly what C files need particular .h files and we have to use generalisations. e.g. we generalise to say "build all RESOURCES before building any object files" to ensure that .rsg files exist before any .cpp file can include them.

Incremental building doesn't always seem to work perfectly (it's a bit too eager to rebuild everything) but this is all partially because there isn't accurate dependency information at the start of the build. Trying to compute such information in advance is self-defeating since it involves a great deal of work - one might as well just get on with building using the generalisations.
= Order-Only Prerequisites and Dependency Generation =

We have worked around not having Order-Only Prerequisites in emake (prior to 4.4.0) by generating dependency files.

There are a couple of places where we still use them if they exist and this may help us with incremental builds when there are TEMS in the build. i.e. it might help us to not rebuild everything if a TEM rule is executed.

Order only prereqs are very useful and although we make less use of them than we used to, new FLMs might need them where we can't generate dependency information.
== How we used to use order-only prerequisites: ==


e.g. before building any source file we should make sure that all EXPORT RESOURCE BITMAP targets are generated. We don't want to trigger a complete rebuild of all source files if one resource is changed, however, so we use an order only prerequisite:

{{{
fred.o: fred.cpp | RESOURCE BITMAP EXPORT
}}}

armcc ...

== Using Generated Dependency Files to get around the lack of Order Only Prerequisites ==


We have found a complicated way to avoid using them. We do this:
{{{
DEPENDFILE:=$(wildcard fred.o.d)
fred.o: fred.cpp $(if $(DEPENDFILE),,RESOURCE EXPORT BITMAP)
armcc ...
generate dependencies.
-include $(DEPENDFILE)
}}}
Heuristic:
 * If we are building incrementally then we must have a dependency file from the last attempt to build fred.o so we know what the dependencies are precisely - we don't need to depend on \*all\* resources.
 * If this file hasn't been built before then we must make sure all resources are done before we try to build it.
This means that changing one resource won't trigger rebuilds everywhere, because by the time one is working incrementally, most source files are using the dependency files rather than the RESOURCE phony target.




= How to Use Raptor with RVCT 4.0 on RVCT2.2 Kits =

== The short answer ==

Download [wiki:File:Rvct4.xml File:Rvct4.xml] and put it into `%EPOCROOT%/epoc32/sbs_config` (creating this directory if necessary).

You can disable it and go back to RVCT 2.2 by (re)moving the file or changing its name to have a `.txt` extension.
== The long answer ==

All SDKs so far require RVCT2.2. It is possible, however, to use other compilers. This How-To uses RVCT4.0 as its example.

A simple way to invoke RVCT4.0 is:

{{{
sbs -c armv5.rvct4_0
}}}

RVCT4.0 requires the following environment variables to be set:

{{{
RVCT40BIN=C:\APPS\rvct40_400\bin
RVCT40INC=C:\APPS\rvct40_400\include
RVCT40LIB=C:\APPS\rvct40_400\lib
}}}

Obviously replacing `C:\APPS\rvct40_400` with the local RVCT4.0 installation directory.

However, due to a current technical difficulty with Raptor (which we are discussing how to resolve), supplying the `rvct4_0` variant does not remove the environmental requirements that `rvct2_2` imposes. `rvct2_2` is implied by the `armv5` alias.

Therefore, the following variables also need to be set for `sbs -c armv5.rvct4_0` to work:

{{{
RVCT22BIN
RVCT22INC
RVCT22LIB
}}}

If RVCT2.2 is installed, these variables will be set, so you need do no more. If it is not, you may set these variables to anything you like to remove the errors and allow the command to work.

An alternative is to avoid the `armv5`, `armv5_urel` and `armv5_udeb` aliases; this may be useful in scripts:

{{{
!Command that requires RVCT22... to be set
!Alternative that does not

sbs -c armv5_udeb.rvct4_0
sbs -c arm.v5.udeb.rvct4_0

sbs -c armv5_urel.rvct4_0
sbs -c arm.v5.urel.rvct4_0

sbs -c armv5.rvct4_0
sbs -c arm.v5.udeb.rvct4_0 -c arm.v5.urel.rvct4_0
}}}

Advanced users may like to set up their own aliases, as (not very fully) described [wiki:Raptor_Personal_Preferences here].




= Introduction to Developing Raptor (SBSv2) =


This page contains information that is useful for anyone wishing to develop Raptor, the build system for Symbian OS. "We" usually refers to the main Raptor development team from Nokia.


==  Technologies  ==

Raptor is written in Python and Gnu Make (with supporting Bash shell scripting) with XML configuration files. Also, there is a small number of supporting tools written in C (Talon and the Descrambler - see below).

Developers should have a good working knowledge of C, C++, Python and Make, and some knowledge of Bash shell scripting and XML.

The Python code is compatible with Python 2.5 and 2.6. We expect to move to using Python 3.x with Raptor at some point in the future, so the general advice is to use the newest Python available to you. At the time of writing, Python 2.6.4 is recommended.

Raptor's make files are only compatible with Gnu Make 3.81, and they rely on features only supported in this version of Gnu Make. This version is the latest one and has been around for a while, so obtaining it should be relatively simple.

The Raptor configuration files are all in XML.
==  Suggested development environment  ==

We recommend using the following development environment:

 *  [http://www.eclipse.org/cdt/ Eclipse with CDT] mainly for the syntax-highlighted makefile editor
 *  [http://pydev.org/ PyDev] - a Python IDE plug-in for Eclipse

While not absolutely essential, the PyDev/Eclipse combination has some very nice features, and the PyDev Python debugger is excellent.

Essential dependencies for development are
 *  [http://www.python.org/ Python] - preferably Python 2.6.4.
 *  Gnu Make 3.81 (Windows: Use [http://www.mingw.org/ MinGW],  Linux: part of build-essentials on .deb-based distros, or its own package on .rpm-based distros)
 *  Gnu Compiler Collection C/C++ (Windows: Use MinGW's version,  Linux: part of build-essentials on .deb-based distros, or its own package on .rpm-based distros). 
 *  Core utils/GNU Tools (Windows: Use [http://www.cygwin.com/ Cygwin] but be sure to not use Cygwin's make,  Linux: standard GNU tools)
 *  Appropriate compilers to build for the target platform(s) (e.g. ARM RVCT or GCCE)
  *  GCCE may be obtained from CodeSourcery's website http://www.codesourcery.com/sgpp/lite/arm/portal/subscription3058
 *  [http://mercurial.selenic.com/ Mercurial] (Windows: Download from the Mercurial website;  Linux: install from your package manager). You can also use [http://bitbucket.org/tortoisehg/stable/wiki/Home TortoiseHg] which is a cross-platform GUI front-end to Mercurial and provides good shell integration.

Binary versions of Python may also be obtained from [http://www.activestate.com/activepython/ ActiveState].

Some people like to use [http://www.vim.org/ Vim] for editing instead of Eclipse/PyDev, and it's possible to show correct syntax highlighting in that too. XML, Make and Python syntax highlighting is usually available and turned on.

For convenience, you can associate files with the .flm and .mk extensions with the same syntax-highlighting rules as Makefiles. This is a straightforward configuration option in Eclipse, and for Vim a simple addition to your .vimrc file enables this.

For Windows, Vim is available for download from the link above; for Linux, install it from your package manager if required - many distributions have it installed by default anyhow.

'''Note''' All Raptor's Python modules use tabs for indentation rather than space. You should set up your IDE/text editor to use tabs.
==  Version numbering scheme  ==

Raptor version numbers are generally of the form 2.X.Y, with X and Y being integers. If a release only contains bug fixes since the previous release, the "micro" version number, Y, is incremented by 1. If new features are included in a release, the "minor" version number X is incremented and the "micro" version number Y is set to 0. The following sequence illustrates this for the imaginary releases 2.15 and 2.16:

 * 2.15.0 New features, and possibly some bug fixes[[BR]]
 * 2.15.1 Bug fixes since 2.15.0[[BR]]
 * 2.15.2 Bug fixes since 2.15.1[[BR]]
 * 2.15.3 Bug fixes since 2.15.2[[BR]]
 * 2.16.0 New features, and possibly some bug fixes

Occasionally, a special beta-release is made for testing purposes and its version number (and version string) might contain some other text to indicate this.
==  Obtaining the source code  ==

The Raptor source code is kept in a Mercurial repository and is part of the Build Package. The URL is

http://developer.symbian.org/oss/FCL/sftools/dev/build/

You can simply clone this Mercurial repository using 

{{{
hg clone http://developer.symbian.org/oss/FCL/sftools/dev/build --pull
}}}

This will create a 'build' folder in your current directory, so move to the directory where you want this placed before running the command.
==  Repository layout and the branches of Raptor  ==
TODO - add comments about submitting changes/testing?

Raptor is found in sbsv2/raptor inside the repository.  It is in the same place regardless of which branch of the repository you are viewing.

The build repository contains three branches:
 *  default
 *  'fix' - for defect fixes
 *  'wip' - feature work in progress

Our normal development practice is to make changes in the fix and wip branches as appropriate, and merge these into the default branch after doing sufficient release testing.  It's possible to create your own branches but given Mercurial will tend to create a new sub-branch whenever a new set of changes is made, this is rarely necessary.
==  Setting up the development environment  ==

Please see our [wiki:How_to_build_Raptor How to get and build Raptor from source] page.
==  How Raptor Works  ==
Raptor consists of essentially four main parts: Shell script/batch file command-line interface, Python Code, FLMs (Function-Like Makefiles) and XML Configuration files.

The following diagram gives an overview of the interactions between the different parts of Raptor.
[wiki:File:RaptorOverview.png none]

The aim of this section is to provide an architectural overview of how each of the parts of Raptor work, not only in isolation, but together as the build system.
=  The `sbs` shell script and `sbs.bat` batch file  =
As already indicated, the `sbs` shell script (Linux) and the `sbs.bat` batch file (Windows) provide the command line interface to Raptor. The `sbs` shell script is also used on Windows when Raptor is used in a Cygwin shell, usually Bash.

For brevity, the term "shell script" will be applied to both the `sbs` shell script and the `sbs.bat` batch file, and  "shell scripts" will be used to refer to both of these.

Broadly, the purpose of the shell scripts is to set the correct environment for the build. 

The main environment settings required are `HOSTPLATFORM` and `HOSTPLATFORM_DIR`. These determine the locations of various host utilities. For Windows, this means Cygwin, MinGW and Python. For Linux, this means the bundled versions of Bash, Gnu Make, Python, Talon, PVM and PVMGMake.

On Linux, it should be noted that the supporting shell script `$SBS_HOME/bin/gethost.sh` is used to determine the values of `HOSTPLATFORM` and `HOSTPLATFORM_DIR`. 

Once all the environment variables have been set, the `$SBS_HOME/python/raptor_start.py` Python script is launched with the arguments given.

At the time of writing, there is some commonality between the `sbs` shell script and `sbs.bat` batch file and it is likely that it will be merged into the `sbs` shell script with the `sbs.bat` batch file invoking the `sbs` shell script via Cygwin's Bash.
=  Setting initialisation files  =
TODO
=  Python Code  =
The Python code in `$SBS_HOME/python` is referred to as the "front end" of Raptor. Its main roles are

 *  Metadata parsing: parse build information files (bld.inf's) and MMP files, including preprocessing etc
 *  Tool checking: check that specified tools are available and recent enough to work well with Raptor
 *  Perform exports: copies out all header files from bld.inf's.
 *  Writing out Raptor's makefiles
 *  Writing out XML log files
 *  Passing log files to filter modules to provide customisable output

The main entry point to Raptor is the Python module `$SBS_HOME/python/raptor_start.py`. This is a very simple wrapper that imports the "raptor" module (`$SBS_HOME/python/raptor.py`) and calls the Main function from that module. 

$SBS_HOME/python/raptor_start.py also enables developers to use the Python profiling module, cPython. To enable profiling, create an environment variable called SBS_PROFILE_BASENAME which should be the path to an output file for the profiling data. It is assumed that all directories exist, and the profile data file will be created as needed. For example, on Linux you might do this:

{{{
export SBS_PROFILE_BASENAME=~/profile_data_raptor_build.out
}}}

and on Windows something like

{{{
set SBS_PROFILE_BASENAME=%USERPROFILE%\Desktop\profile_data_raptor_build.out
}}}

$SBS_HOME/python/raptor_cli.py handles parsing of the command line options.

The Raptor module $SBS_HOME/python/raptor.py does all the setting up for the build: it parses the sbs_init.xml files if they exists, sets defaults, and acts on the command line options passed to it from $SBS_HOME/python/raptor_cli.py

== Plug-in Filters  ==
The output from Raptor comes from a number of sources such as the Python interpreter, the make process, child processes of make etc. Raptor's architecture is carefully constructed to ensure that output is valid XML, and the full XML output is always present.

However, the full XML output is not always needed. For example, for the terminal output the full XML is far too verbose. Thus, Raptor includes a plug-in filter feature. As the name suggests, these are dynamically loaded at runtime (hence "plug-in") and their purpose is to sieve (hence "filter") the XML output.

The filters are Python classes that implement a certain interface. Specifically, this interface is defined by the following class:
{{{
class Filter(object):
	
	def open(self, params):
		return False
	
	def write(self, text):
		return False

	def summary(self):
		return False
	
	def close(self):
		return False
	
	def formatError(self, message):
		return "sbs: error: " + message + "\n"
		
	def formatWarning(self, message):
		return "sbs: warning: " + message + "\n"	
}}}

which is defined in $SBS_HOME/python/filter_interface.py. Any class that implements this interface it referred to as a filter. You may have as many filters as you wish in any Python module, as long as their names are unique.

By default, Raptor uses two filters: filterterminal and filterlogfile. These are defined in the Python modules $SBS_HOME/python/plugins/filter_terminal.py and $SBS_HOME/python/plugins/filter_logfile.py. As you might expect, these filters are for terminal output and log file output. You may use any number of filters at a time specifying them with the --filters option - this option is case-insensitive so it will find FilterTerminal even if you specify filterterminal.

The mechanism works by passing output as it arrives in the Python interpreter's buffer to each filter and letting it do something with that output. For the log file filter, this is to simply write the data to the log file. In the case of terminal filter, the output is filtered and much is thrown away to produce informative build output like this example from 

{{{
> sbs -b  simple/bld.inf -c armv5
 compile    : simple/test1.c++       [armv5_urel]
 compile    : simple/test.cpp        [armv5_urel]
 compile    : simple/test2.cxx       [armv5_urel]
 compile    : simple/test3.Cpp       [armv5_urel]
 compile    : simple/test4.cc        [armv5_urel]
 compile    : simple/test5.CC        [armv5_urel]
 compile    : simple/test6.C++       [armv5_urel]
 compile    : simple/test.cpp        [armv5_udeb]
 compile    : simple/test1.c++       [armv5_udeb]
 compile    : simple/test2.cxx       [armv5_udeb]
 compile    : simple/test3.Cpp       [armv5_udeb]
 compile    : simple/test4.cc        [armv5_udeb]
 compile    : simple/test5.CC        [armv5_udeb]
 compile    : simple/test6.C++       [armv5_udeb]
 target     : epoc32/release/armv5/urel/test.exe        [armv5_urel]
 target     : epoc32/release/armv5/udeb/test.exe        [armv5_udeb]

no warnings or errors

Run time 20 seconds

sbs: build log in /home/user/sdk-01/epoc32/build/Makefile.2009-11-30-13-26-41.log
}}}

whereas the log file /home/user/sdk-01/epoc32/build/Makefile.2009-11-30-13-26-41.log is 54,260KB in size.

'''Note:''' the filters are called synchronously so they need to be efficient and return quickly.

Currently, filters are located in $SBS_HOME/python/plugins, but a mechanism will be added soon to allow them to be used from the SDK being built against, probably from a subdirectory of epoc32/sbs_config.
=  Make  =
As already mentioned, Raptor uses Gnu Make as its build engine. In fact, it's possible to use other make engines that are compatible with Gnu Make 3.81.

By default, Raptor generates one main makefile with name Makefile_all in $EPOCROOT/epoc32/build. This is usually a very short makefile that simply includes several others. Here is an example from a Windows build:

{{{
# GENERATED MAKEFILE : DO NOT EDIT

MAKEFILE_GROUP:=DEFAULT
# GROUPER MAKEFILE

ALL::

include Z:/epoc32/build/Makefile_all.export
include Z:/epoc32/build/Makefile_all.bitmap
include Z:/epoc32/build/Makefile_all.resource_deps
include Z:/epoc32/build/Makefile_all.resource
include Z:/epoc32/build/Makefile_all.default

# END OF GENERATED MAKEFILE : DO NOT EDIT
}}}

Separation into included makefiles like this allows Raptor to easily define the various targets such as BITMAP, RESOURCE, EXPORT etc. Each of these included makefiles contains the main machinery for doing builds: Function-Like Makefiles.
== Function-Like Makefiles (FLMs)  ==
As their name implies, function-like makefiles are used like functions: a list of variables is set for that makefile and then that FLM is included. This is similar to many other programming languages, where functions define their arguments and these are set before the function is run.

When Make parses the Makefile_all, as it parses the included makefiles it evaluates all the variables and then expands them for the included the FLM. To see this, here is a cut-down extract of Makefile_all.default from a Windows build:

{{{

# call C:/raptor/lib/flm/e32abiv2exe.flm
SBS_SPECIFICATION:=simple.mmp
SBS_CONFIGURATION:=armv5_urel

COMPONENT_META:=C:/raptor/test/smoke_suite/test_resources/simple/bld.inf
COMPONENT_NAME:=
COMPONENT_LAYER:=
PROJECT_META:=C:/raptor/test/smoke_suite/test_resources/simple/simple.mmp
DATE:=C:/raptor/win32/cygwin/bin/date.exe
DUMPBCINFO:=
GNUMAKE38:=C:/raptor/win32/mingw/bin/make.exe
GNUCP:=C:/raptor/win32/cygwin/bin/cp.exe
GNUCAT:=C:/raptor/win32/cygwin/bin/cat.exe
GNUMKDIR:=C:/raptor/win32/cygwin/bin/mkdir.exe
GNUMV:=C:/raptor/win32/cygwin/bin/mv.exe
GNURM:=C:/raptor/win32/cygwin/bin/rm.exe
GNULN:=C:/raptor/win32/cygwin/bin/ln.exe
.
.
.
MODULE:=simple
USER_LIBS_PATH_OPTION:=--userlibpath
VARIANTPLATFORM:=armv5
PLATFORM:=$(VARIANTPLATFORM)
VARIANTTYPE:=urel
VERSION:=10.0
VERSIONHEX:=000a0000
VFE_OPTION:=--no_vfe
EXPLICITVERSION:=
TARGETTYPE:=exe
UID1:=1000007a
include C:/raptor/lib/flm/e32abiv2exe.flm
MAKEFILE_LIST:= # work around potential gnu make stack overflow
}}}

In this case, the Raptor FLM in question is C:/raptor/lib/flm/e32abiv2exe.flm. In this build, 224 variables were set for this FLM. Internally, the FLM consists of a number of Make macros that are evaluated in the context of these variables. These produce the Make rules for a particular executable that is built from the MMP file C:/raptor/test/smoke_suite/test_resources/simple/simple.mmp

The make macros expand to rules to build the specified target. These are written in Bash shell script. For example, here is an extract from $SBS_HOME/lib/flm/e32abiv2.flm that deal with generating the ARTARGET:

{{{
## Link-type selection:
#	runtime static libraries link via AR
ifneq ($(ARTARGET),)
# Assuming that there are no libdeps in this case because this is probably one of the
# Runtime libraries which has no deps.

define artarget_func
$(ARTARGET): $(if $(MULTIFILE_ENABLED),$(MULTIFILEOBJECT),$(LINKOBJECTS)) $(STDCPPTAGFILE)
	$(if $(MULTIFILE_ENABLED),,@echo "$(STDCPPTAGFILE)" > $(VIAFILE);
	$(call groupin10,$(LINKOBJECTS)) ;)
	$(call startrule,ar,FORCESUCCESS) \
	$$(call dblquote,$(AR)) $(ARCHIVER_CREATE_OPTION) $$@ $(if $(MULTIFILE_ENABLED),$(MULTIFILEOBJECT),$(COMMANDFILE_OPTION)$(VIAFILE)) \
	$(if $(DUMPBCINFO),&& $(FROMELF) -v $$@  > $$@.elfdump,)  \
	$(call endrule,ar)
endef
$(eval $(artarget_func))

CLEANTARGETS:=$(CLEANTARGETS) $(VIAFILE) $(if $(DUMPBCINFO),$(ARTARGET).elfdump,)
endif
}}}

The 224 variables set for this FLM are defined by the XML interfaces discussed below.
=  XML configuration  =
Raptor has two main types of XML configuration files: those that contain "variants", "groups" and "aliases", and those containing "interfaces". These are defined in various XML files that are located in $SBS_HOME.

The "variants", "groups" and "aliases" are defined in the XML files stored in $SBS_HOME/lib/config whereas the "interfaces" are alongside their associated FLMs in $SBS_HOME/lib/flm.

Note that Raptor also reads XML files from $EPOCROOT/epoc32/sbs_config so that it is possible for some  "variants", "groups", "aliases" and "interfaces" to be defined there.
== XML configuration - Variants, Groups and Aliases  ==

"Variants", "groups" and "aliases" are, very roughly, the command line values passed to the -c option and tell Raptor which configurations to build for. For example, 

{{{
sbs -c armv5 -c armv5.test
}}}

builds armv5 production and armv5 test code. These dot-separated strings such as armv5 and test can be either a "group" combined with zero or more "variants", or an "alias" combined with zero or more "variants".

"Variants", "groups" and "aliases" are defined as XML tags in Raptor's XML files in $SBS_HOME/lib/config. For example, there is a "v5" variant element that defines characteristics of the AMRv5 architecture (see $SBS_HOME/lib/config/arm.xml):

{{{
	<var name="v5">
		<set name="TRADITIONAL_PLATFORM" value="ARMV5"/>
		<set name="VARIANTPLATFORM" value="armv5"/>
		<set name="DEBUG_FORMAT" value="$(CC.DWARF2)"/>
		<set name="TARGET_ARCH_OPTION" value="$(CC.ARMV5)"/>
		<set name="LINKER_ARCH_OPTION" value="$(LD.ARMV5)"/>
		<set name="COMPILER_FPU_DEFAULT" value="$(CC.SOFTVFP_MAYBE_VFPV2)"/>
		<set name="POSTLINKER_FPU_DEFAULT" value="$(PL.SOFTVFP_MAYBE_VFPV2)"/>
		<set name="GENERATE_ABIV1_IMPLIBS" value="$(SUPPORTS_ABIV1_IMPLIBS)"/>
	</var>
}}}

Here are two aliases:
{{{
	<alias name="armv5_urel" meaning="arm.v5.urel.rvct2_2"/>
	<alias name="armv5_udeb" meaning="arm.v5.udeb.rvct2_2"/>
}}}

Aliases provides shortened and simplified names for other complicated chains of variants. For example, we alias armv5_urel to the verbose arm.v5.urel.rvct2_2. The meaning attribute of an alias provides the "expansion" of that alias so wherever armv5_urel is used, Raptor will know that is really means arm.v5.urel.rvct2_2.

Groups provide a way to collect several convenient build configurations together. For example, the following XML tag defines the group called default:
{{{
	<group name="default">
		<groupRef ref="armv5"/>
		<groupRef ref="winscw"/>
	</group>
}}}

Using this group as the option to -c will build armv5 and winscw together.
== XML configuration - Interfaces  ==
TODO - I think this should live closer to the FLM documentation, but the document needs a little refactoring for that to happen.

"Interfaces" are a bit like function declarations in C/C++: they define the list of parameters that an FLM takes, i.e. which variables must be set for that FLM to obtain a meaningful result. If any variables in an interface are undefined, Raptor throws an error.

Interfaces are defined in XML "interface" tags. For example, the Symbian.lib interface defined in the following extract of the file $SBS_HOME/lib/flm/standard.xml:

{{{
	<interface name="Symbian.lib" extends="Symbian.e32abiv2" flm="e32abiv2lib.flm">
		<param name='AR'/>
		<param name='ARCHIVER_CREATE_OPTION'/>
		<param name='TARGETTYPE' default="lib"/>
	</interface>
}}}

Notice that the <tt>interface</tt> element has has two attributes: extends and flm.

The <tt>extends</tt> attribute gives the name of another <tt>interface</tt>, in this case <tt>Symbian.e32abiv2</tt>. This, as you would expect, indicates that <tt>Symbian.lib</tt> "extends" or inherits all the input parameters (<tt>param</tt> tags) from the interface <tt>Symbian.e32abiv2</tt>, and defines three extra ones of its own. The key parameter defined here is the <tt>TARGETTYPE</tt>: this is matched to the value of the MMP keyword <tt>TARGETTYPE</tt> (by the metadata parsing) and tells Raptor which interface to use for a given MMP. There is one interface for each MMP target type.

As implied, the <tt>interface</tt> elements form a tree via the <tt>extends</tt> attributes, each one gaining the parameters of the one it <tt>extends</tt> and possibly adding some of its own. The <tt>Symbian.pdl</tt> and <tt>Symbian.plugin</tt> interfaces (see  <tt>$SBS_HOME/lib/flm/standard.xml</tt>) are examples of interfaces that extend from others but do not require any further parameters.

The <tt>flm</tt> attribute tells Raptor which FLM to use for the given target type, and together with the parameters, generates the call to the FLM. Most of the variables in the interface get their values from the metadata (bld.inf and MMP files) and once Raptor has parsed all of these, it can write out the FLM call into a makefile.

As already noted, the above interface extends the <tt>Symbian.e32abiv2</tt> interface (see <tt>$SBS_HOME/lib/flm/standard.xml</tt>). This in turn <tt>extends</tt> yet another interface: <tt>Symbian.mmp</tt>. Following the <tt>extends</tt> tree upwards, we reach

{{{
	<interface name="base.flm" abstract="true">
		<param name='COMPONENT_META' default=''/>  <!-- bld.inf -->
		<param name='COMPONENT_NAME' default=''/>  <!-- MP4 Player -->
		<param name='COMPONENT_LAYER' default=''/> <!-- Multimedia -->
		<param name='PROJECT_META' default=''/>     <!-- my.mmp  -->
		.
		.
		.
		<param name='GNUMD5SUM'/>
		<param name='SAVESPACE' default=''/> <!-- remove intermediate files ASAP -->
		<param name='WHATLOG' default=''/>   <!-- emit formatted releasable info into the logs during the build -->
		<param name='USE_PROFILER_FEEDBACK' default=''/> <!-- use the profiler feedback file for the builds -->
		<param name='ARM_PROFILER_FILE' default=''/>
	</interface>
}}}

The <tt>base.flm</tt> interface is the "root" or "base" interface that other interfaces inherit from. The <tt>abstract</tt> attribute indicates that the interface cannot be used directly and should always be extended by another interface. Notice the <tt>name</tt> attribute has value "base.flm" - this is often a cause of confusion as it is suggestive of a file name. There is no file named base.flm; this is just a name. This interface defined in the file <tt>$SBS_HOME/lib/flm/base.xml</tt>.

The discussion so far has been focussed on the ARM target. There is an equivalent tree of interfaces for the WINSCW target defined in <tt>$SBS_HOME/lib/flm/emulator.xml</tt> and the discussion applies equally well to those.
=  Supporting tools and host utilities  =
== Talon ==
Talon is a shell wrapper sitting between make (GNU make or emake) and the bash shell where build commands are run.

As an illustration, a shell command issued by make to execute the compiler and build a particular file will be passed to the bash shell through Talon. Talon can then control bash output, enclosing it in descriptive XML tags and holding it until no other proceess are writing to the log. Talon can also timeout on long commands and retry failed commands.

Features such as retry on timeout add reliability to GNU make. Talon superceded "sbs_descramble" as the way of serialising output. Talon is designed in such a way as to use less memory than the prior descrambler based mechanism in Raptor.
=== Environment Variables  ===

Talon is controlled by environment variables but many parameters must be supplied that are specific to a particular recipe, such as the recipe name or the name of the MMP it's from. Talon needs these values to print correct xml tags.

Some variables can be set for the whole build while others are specific to each recipe. There is a mechanism to pass recipe-specific parameters via the commandline that make gives to Talon. Talon strips these parameters off and then passes the remainder of the command to bash.
=== Variables that are set for the whole build:  ===

    * TALON_BUILDID - a unique number generated by the build system that identifies this build. Used for naming the semaphore that controls access to the log.
    * TALON_SHELL - what shell to execute recipes in
    * TALON_RECIPEATTRIBUTES - specifies what attributes to set in the recipe output and what environment variables to use in those attributes. e.g. could be "name='$RECIPENAME' component='$COMPONENT_META'"
    * TALON_DESCRAMBLE - if set to '1' then obtain a semaphore before showing output from the recipe. prevents recipe output from being interleaved in the log. 
=== Variables that may be set per-recipe  ===

    * TALON_FLAGS - a space-separated list of words or "flags". Valid flags be "rawoutput" to allow descrambling without any XML. Also "forcesuccess" to ignore the success or failure of a command.
    * TALON_RETRIES - How many times to retry a failed recipe
    * TALON_TIMEOUT - how many milliseconds to wait before giving up on a build command.
    * TALON_DEBUG - if set, this causes talon to print out debugging information. Note that this generally messes up a build system so it's only useful in small tests. 
=== How Recipe Specific Parameters are Passed in  ===

Each command needing xml wrapping and descrambling must start with the following section:
{{{
          "|name1=value1;name2=value2;...;|<build commands here> "
}}}
For Example make runs the following:
{{{
         talon -c  "|name=compile;COMPONENT_META=fred/group/bld.inf;PROJECT_META=barney. mmp;| armcc -o betty.o betty.cpp"
}}}
The startrule/endrule FLM macros take care of adding the recipe-specific-variables in `||`.

Talon strips off the bit between pipe symbols and uses that to know what the recipe name is etc etc. If talon doesn't see the "||" section then that means that make is executing a "$(shell)" instruction in the makefile - it goes quiet and tries to transparently pass the commands through. It does buffer the output from the bash command but it doesn't use a semaphore to check when to output it. No XML is produced.




= How to use Raptor's log filter plug-ins =

As discussed here [http://developer.symbian.org/wiki/index.php/Raptor_Log_Format], Raptor's log file format is XML and the full XML log is always generated. However, in many cases this full log is simply too much information and not needed. Raptor deals with this via the plug-in filters ("filters" hereafter) mechanism (see [http://developer.symbian.org/wiki/index.php/Introduction_to_Developing_Raptor_%28SBSv2%29#Plug-in_Filters] for details on implementing these). The filters may be regarding as streams into which the full XML log is fed for further processing: examples of this further processing include counting just errors and warnings, producing build results summary reports, writing the full log to a file on disk, compressing the full log to an archive on disk.
= Available Filters =
As of Raptor 2.15.2, the following table lists the filters that are provided by default.

||= Filter Name =||= Command line usage =||= Description =||= Notes =||
|| FilterCarbide || \
|| sbs --filters=FilterCarbide [other options] || \
|| Cuts down the full XML log so that it's suitable for integration with Carbide's console. || \
|| This is a prototype filter intended to be used only by Carbide and is still at the experimental stage. ||
|| FilterTerminal || \
|| sbs --filters=FilterTerminal [other options] || \
|| Cuts down the XML log so that it's suitable for outputting to a terminal/command prompt || \
|| The terminal filter also provides the error/warning count that is printed at the end of any Raptor build. ||
|| Bz2log || \
|| sbs --filters=Bz2log [other options] || \
|| Compress the full XML log using the bzip2 method || \
|| Cannot be used with <tt>-f-</tt>; compressed log file name is the default log name with the .bz2 extension appended if not already present. The maximum bzip2 compression level is used so that a 500-600MB log files compresses to about 8-10 MB. ||
|| FilterSquashlog || \
|| sbs --filters=FilterSquashlog [other options] || \
|| Creates a version of the log file with all successful commands stripped out, i.e. only those recipes whose exit status is 'failed' have their commands and command output left in. || \
|| Approximate space savings range from 30 - 65%, depending on the size of the full log. Some examples include 321MB down to 116MB and 43KB down to 30KB. Don't use at the same time as FilterLogfile as both filters write to the same log file. ||
|| FilterTiming || \
|| sbs --filters=FilterTiming [other options] || \
|| The timing filter provides information about the duration of many tasks within Raptor by reading the start/end timers tags that are embedded in the raptor XML log. || \
|| Notes for FilterTiming ||
|| FilterWhat || \
|| sbs --filters=FilterWhat [other options] || \
|| Description for filter FilterWhat || \
|| Notes for FilterWhat ||
|| FilterLogfile || \
|| sbs --filters=FilterLogfile [other options] || \
|| Writes the full XML log file to a file on disk.  This is a default filter and the output file name can be set with the <tt>-f</tt> switch. Using <tt>-f-</tt> prints the full log to STDOUT. || \
|| - ||
|| FilterCopyFile || \
|| sbs --filters=FilterCopyFile [other options] || \
|| The CopyFile Filter is used internally by Raptor and is included by default.  Its job is to act on "finalcopy" tags in the Raptor log output.  It is not intended that users of Raptor should ever wish to specify it directly themselves. || \
|| These tags can be issued by Function-Like Makefiles in the build and the filter carries them out by copying a file from source to destination.  The filter is most useful in cluster builds where file copying on the cluster is inefficient.  If the copies are not needed by subsequent steps in the build then this feature allows them to be done more efficiently on the build host machine which is where they end up anyhow.  The filter acts at the end of each makefile stage (export,bitmap,resource,resource_deps,default). || \
|| - || 
|| FilterSplitlog || \
|| sbs --filters=FilterSplitlog [other options] || \
|| Description for filter FilterSplitlog || \
|| Notes for FilterSplitlog ||
|| FilterClean || \
|| sbs --filters=FilterClean [other options] || \
|| Description for filter FilterClean || \
|| Notes for FilterClean ||
|| FilterCheckComp || \
|| sbs --filters=FilterCheckComp [other options] || \
|| Description for filter FilterCheckComp || \
|| Notes for FilterCheckComp ||
|| HTML || \
|| sbs --filters=HTML [other options] || \
|| Generates a HTML summary of the build with detailed information about build problems. || \
|| A directory, whose name is the path to the log file with _html appended, is created. In this directory, the index.html file should be opened. This contains the main build summary overview with hyperlinks to more detailed information about build problems. Missing files are also recorded. ||
|| FilterBroken || \
|| sbs --filters=FilterBroken [other options] || \
|| Description for filter FilterBroken || \
|| Notes for FilterBroken ||
|| FilterTagCounter || \
|| sbs --filters=FilterTagCounter [other options] || \
|| Description for filter FilterTagCounter || \
|| Notes for FilterTagCounter || 
|| FilterCheck || \
|| sbs --filters=FilterCheck [other options] || \
|| Description for filter FilterCheck || \
|| Notes for FilterCheck ||
|| FilterComp || \
|| sbs --filters=FilterComp [other options] || \
|| Description for filter FilterComp || \
|| Notes for FilterComp ||
|| FilterWhatComp || \
|| sbs --filters=FilterWhatComp [other options] || \
|| Description for filter FilterWhatComp || \
|| Notes for FilterWhatComp ||

== Re-filtering a full log file after the build ==
It often happens that a build is done and the full log is available at the end for further analysis. However, for some reason not all the required filters were used, or some extra details are required from within the log.

Within the Raptor distribution in `raptor/bin`, there should be a Linux shell script named `sbs_filter` and a Windows batch file named `sbs_filter.bat`. These are the entry points for the re-filtering program. Usage is very straightforward and usage information is given with the `-h` option:

{{{
$ sbs_filter -h
usage: $SBS_HOME/bin/sbs_filter.py [sbs options]
  The log data is read from stdin.
  Type 'sbs -h' for a list of sbs options.
}}}

Of course $SBS_HOME will be expanded to the value on your machine.

Examples of use are:

Generate a HTML report using the HTML filter and a bzip2 archive of the log (Uses the Linux "cat" command; on Windows you can use the "type" command)
{{{
cat makefile.log | sbs_filter --filters=HTML,Bz2log
}}}

Generate a HTML report using the HTML filter and a bzip2 archive of the log. Alternative way of doing the previous example.
{{{
sbs_filter --filters=HTML,Bz2log < makefile.log
}}}




= Raptor Binary Variation =


Binary variation is a method of using the same source code to produce different binaries. This is achieved using binary variation macros ({{{#define}}}s) that are defined in the global HRH file (see Kit Set Up) and can be referenced (with {{{#ifdef}}}s) in source, header, {{{mmp}}} and {{{bld.inf}}} files.

== Overview ==

{{{#define}}}s for controlling binary variation are typically stored in the global preinclude HRH file that is implicitly included into each source and {{{.mmp}}} file. However, it would be very expensive for Raptor to try to determine automatically which components are dependent on the macros thus included, so instead the developer must mark {{{.mmp}}} files that produce binary-variant binaries by declaring {{{FEATUREVARIANT}}} in it.

Notice that if an exported header file uses a binary variation macro, any component including it will become binary variant (and must therefore be marked as such), so please avoid using binary variation macros in exported header files.

== Invoking Binary-Variant Builds ==

You can invoke your binary variant builds with a command line such as {{{sbs -c armv5.caribou}}} as long as you have placed an XML file such as the following in your {{{%EPOCROOT%/epoc32/sbs_config}}}:

{{{
<?xml version="1.0" encoding="ISO-8859-1" ?> 
<build xmlns="http://symbian.com/xml/build"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://symbian.com/xml/build build/2_0.xsd">
  <var name="caribou">
    <set name="FEATUREVARIANTNAME" value=".caribou" />
    <set name="FEATURELISTFILES" 
      value="$(EPOCROOT)/epoc32/include/config/caribou.txt" />
    <set name="VARIANT_HRH"
      value="$(EPOCROOT)/epoc32/include/config/caribou.hrh" /> 
  </var>
  <var name="ibex">
    <set name="FEATUREVARIANTNAME" value=".ibex" />
    <set name="FEATURELISTFILES" 
      value="$(EPOCROOT)/epoc32/include/config/ibex.txt" />
    <set name="VARIANT_HRH"
      value="$(EPOCROOT)/epoc32/include/config/ibex.hrh" /> 
  </var>
</build>
}}}

{{{FEATUREVARIANTNAME}}} sets a suffix for the output files: binary variant binaries will appear in {{{armv5.caribou}}}, rather than {{{armv5}}}. Non-binary-variant files will still appear in {{{armv5}}}. 

{{{FEATURELISTFILES}}} contains a list of macros that used to build the variants.  The file is not used directly in build, but by createvmap which is a tool to tell if the differences between the macros in two builds of the same file are significant as far as the variants are concerned.

Here the variants change what is built by changing the global HRH file and [optionally] the system include path.
== What Can Be Variated? ==

Feature macros can be used in bld.inf, .mmp and source files to change the compilation of '''binaries''' only. So the following is valid,

{{{
// bld.inf file

PRJ_MMPFILES
constant.mmp
#ifdef FEATURE_ONE
one.mmp
#endif
}}}

Meaning, only build one.mmp if FEATURE_ONE is defined for the product: there is a caveat here - if one.mmp contains resources, bitmaps and string-tables then this bld.inf is not valid, because all non-executable files cannot be variated (see What Can Not Be Variated? below). More subtle changes can be made in .mmp files,

{{{
// my.mmp file

SOURCEPATH .
SOURCE constant.cpp
#ifdef FEATURE_BONUS
SOURCE bonus.cpp
#endif
}}}

Meaning, only compile source file bonus.cpp if FEATURE_BONUS is defined. And, of course, the feature macros can be used in source code as well.
== What Can Not Be Variated? ==

You cannot use feature macros to control extension makefiles, bitmaps, resources or string-tables. This is because by design it is '''only binaries''' that are variated. Everything else should be constant and should build for the default target configuration (without BV).

So this is '''not valid''' in a bld.inf file,

{{{
START EXTENSION a.b.c
#ifdef FEATURE_A
OPTION A 1
#else
OPTION Z 26
#endif
END
}}}

And this is '''not valid''' in a .mmp file,

{{{
START RESOURCE 12345.rss
#ifdef FEATURE_Z
TARGETPATH secret/z
#endif
END
}}}

The result will always be that Raptor only builds extensions, bitmaps, resources and string tables once. So whatever the feature macro values are for the default target configuration is what you will get.
==  Controlling FEATUREVARIANT Output with FEATUREVARIANTSAFE  ==

'''Note: This support is available from Raptor 2.13.0'''

By default, .mmp files that include {{{FEATUREVARIANT}}} will generate binaries for both "normal", non-binary variant, build configurations ''and'' binary variant build configurations.  So, for example, if we consider two .mmps file containing the following:

'''.mmp One'''
{{{
TARGET invariant.dll
}}}

'''.mmp Two'''
{{{
TARGET variant.dll
FEATUREVARIANT
}}}

...when built with {{{sbs -c armv5 -c armv5.caribou}}} all of these files will be generated as output:

{{{
$(EPOCROOT)/epoc32/release/armv5/udeb/invariant.dll
$(EPOCROOT)/epoc32/release/armv5/urel/invariant.dll
$(EPOCROOT)/epoc32/release/armv5/udeb/variant.dll
$(EPOCROOT)/epoc32/release/armv5/urel/variant.dll
$(EPOCROOT)/epoc32/release/armv5.caribou/udeb/variant.dll
$(EPOCROOT)/epoc32/release/armv5.caribou/urel/variant.dll
}}}

In order to ensure that only invariant binaries are created for invariant build configurations, and variant binaries for variant build configurations, the optional setting  {{{FEATUREVARIANTSAFE}}} can be used.  {{{FEATUREVARIANTSAFE}}} can be set via an {{{os_properties.xml}}} file as follows:

{{{
<!-- Modify the root variant to turn on safe generation of Feature Variant binaries -->
<var name="root.changes">
    <set name='FEATUREVARIANTSAFE' value='1'/>
</var>
}}}

When set, variant binaries will no longer be created for invariant build configurations, giving the following output in response to {{{sbs -c armv5 -c armv5.caribou}}}:

{{{
$(EPOCROOT)/epoc32/release/armv5/udeb/invariant.dll
$(EPOCROOT)/epoc32/release/armv5/urel/invariant.dll
$(EPOCROOT)/epoc32/release/armv5.caribou/udeb/variant.dll
$(EPOCROOT)/epoc32/release/armv5.caribou/urel/variant.dll
}}}




= Raptor How Template Extension Makefiles are Dealt With =


Template (and normal) Extension Makefiles are a hangover from the past that don't fit well into a parallel build system.  This is a description of how Raptor (imperfectly) accommodates them until they can be rewritten as Function-Like Makefiles.
==  One Make Controls it All  ==
The main difference between Raptor and previous build systems is that in the past the make engine (e.g. gnumake) was invoked repeatedly - one component at a time.  This means that each invocation of the make engine could only "see" the dependencies that existed within a component.

It became important to execute components in a particular order to make them build correctly.

Raptor uses one make process builds all components - it is able to see the connections and dependencies between all parts of the build.  It is then able to schedule the build hardware with maximum efficiency.
==  Extensions  ==
The Symbian Metadata formats (bld.infs and mmps) are pretty descriptive and powerful but they can't describe everything.  There are always things that need to be built but which don't fit into any of the pre-existing patterns.

The BLD.INF format includes what is called an extension block e.g.:
{{{
 #Call extension for building the stlport library for the build host (used to create tools)
 START EXTENSION tools/stlport
    OPTION STLPORT_VERSION  5.1.0
    OPTION STL_REL_LIB_NAME  libstlport.5.1.a
    OPTION STL_DEB_LIB_NAME  libstlportg.5.1.a
    OPTION SOURCE_ARCHIVE ../source/STLport-5.1.0.zip
 END
 }}}

Extension blocks can be implemented either by:
   * Template Extension Makefiles (TEMs)
   * Function-Like Makefiles (FLMs)

FLMs are the modern solution, TEMs are supported by Raptor in an imperfect manner and should be replaced by FLMs at the earliest possible opportunity.
=  How TEMs work  =

A TEM is written using GNU Make syntax but their structure is completely at odds with the principles of Make.  TEMs are all expected to support a particular set of targets that correspond to "stages" in the build.  ABLD (SBSv1) builds by stages:

 *  MAKMAKE
 *  RESOURCE    
 *  LIB         
 *  BLD        
 *  RELEASABLES 
 *  FINAL
 
A TEM will have a rule corresponding to each of these.  e.g.
{{{
 GENERATED_FILES:=a.cpp b.cpp
 
 MAKMAKE : $(GENERATED_FILES)
 
 BLD : MAKMAKE
 
 SAVESPACE : MAKMAKE
 
 CLEAN : 
 	$(call remove,$(GENERATED_FILES))
 
 FREEZE : do_nothing
 
 LIB : do_nothing
 
 CLEANLIB : do_nothing
 
 RESOURCE : do_nothing
 
 FINAL : do_nothing
 
 RELEASABLES : do_nothing
 
 $(GENERATED_FILES): 
         #Do something here to create the files
}}}

The example is of a simplified TEM that generates code in it's MAKMAKE stage.

ABLD calls MAKMAKE for all extensions then RESOURCE for all, then LIB for all, then BLD for all and so on.  Inside abld's own makefiles there are also MAKMAKE, RESOURCE etc stages so that ABLD ensures that all resources, for example, are definitely created before all libraries.


=  Why is this so terrible even for ABLD?  =
Make is organised around the idea of dependencies.  i.e. the user tells make how objects are related and allows make to schedule their construction in whatever way is most efficient.  TEMS do not allow make to do it's job - ABLD is orchestrating make very rigidly and also in a very imprecise way.  e.g. in reality it is not necessary for all library stubs (.LIB/.DSO) files to be created before all executables and DLLS (the BLD target) - there are some dependencies but there is a lot more freedom in build order than TEMs allow.

This leads to problems:
 *  Must build components in a "special" order - stages are not a precise enough mechanism e.g. some resources depend on others. This cannot be represented in this system so one must build components in a special order to succeed.
 *  Reduced performance - since make is restricted by mostly artificial dependencies it cannot schedule as efficiently.
=  TEMs in Raptor  =
Raptor has it's single makefile which views everything.  It cannot see the dependencies inside TEMS because they run from sub-make processes so it has to just try to remember to run them at specific "stages" and hope that they will work.

Raptor has to create "proxy" targets in it's "target space" in memory that represent each of the rules in a TEM.

So every time there is a "start extension" block in a BLD.inf file, Raptor creates a new set of targets.   It makes a hash key using the bldinf name, and the number of the extension block (1,2,3...) in the BLD.inf and several other parameters and then declares a set of rules for the TEM roughly like this:
{{{
 RESOURCE_123a4fe3b:
       make -f stlport.mk RESOURCE
 
 BLD_123a4fe3b:
       make -f stlport.mk BLD
}}}
Raptor also has internal "global" targets like "RESOURCE" and the TEM rules are attached to them. e.g.
{{{
 RESOURCE:: RESOURCE_123a4fe3b
}}}

This ensures that the stages work.  e.g. in Raptor the equivalent of "BLD" is "TARGET".  TARGET depends on "RESOURCE" (indirectly through LIBRARY) so that means that the all the TEMs "resource" targets will be made before raptor tries to build any EXEs or DLLs.
== Why this is so Terrible for Raptor  ==
 *  Many TEMs produce something which only needs to be done once.  Raptor has to call the TEM for urel and udeb and for all the other platforms (e.g. winscw or whatever else you are building).  There is often no way to prevent these similar calls from happening at the same time and trying to write to the same file 
  *    emake detects it and reports "clashes" and slows down the build trying to rebuild all sorts of things.
  *    Other build systems don't detect it and generate corrupted output or report a locking failure.  These problems lie hidden for months and appear at random.  We have done things to try to avoid this but no solution is correct for everyone.   This is why we have to do the tools2 build separately from the main build - we can't put in all the dependency information.  It is inefficient and makes the build longer and more complicated.
 *  Again, like in ABLD, these generic categories are not really accurate enough but now there is no ordering.  e.g. some resources depend on each other but there is no way to represent that if TEMs produce resources.
 *  Raptor has become much more complicated and less efficient because of having to support TEMS.
 *  TEMS are always run using Raptor's "FORCESUCCESS" recipe mechanism. This means that all TEM failures are effectively ignored otherwise the whole build would halt! The problem is that anything (e.g. a DLL or EXE) that depends on one TEM has to depend on them all, so a single TEM failure would stop the build.  This is because of the way Raptor has to generate rules in the makefile for the "proxy" targets mentioned above. Therefore Raptor has to use FORCESUCCESS on every single TEM on every singe TEM stage.



= Guide to Writing Function-Like Makefiles for Raptor =

== Introduction and Scope ==

Raptor performs 2 main tasks:
 *  Reads build metadata such as system definitions, bld.inf files and MMP files and converts these into makefiles.
 *  Builds the makefiles using gnu make or emake.

These makefiles contain "calls" to "Function-Like Makefiles" (FLMs) which are a bit like function calls in an ordinary programming language but the language is GNU make.  An FLM produces some kind of object like a program or a library or a resource file.

This document describes how to write FLMs. It is useful for those who wish to:
 *  Maintain existing FLMs
 *  Create new build objects and implement them via FLMs
 *  Build Symbian software on new platforms

You will need to understand GNU Make syntax:
[http://www.gnu.org/software/make/manual/html_node/index.html]

== Function-Like Makefiles (FLMs) ==
Makefiles contain:
 *  targets - outputs of the build system e.g. an executable or a library 
 *  dependencies - the relations between targets and source files 
 *  recipes - which are lists of commands that will create a target from its dependencies.

Function-Like Makefiles (FLMs) are reusable makefiles.  They are "patterns" of targets, dependencies and recipes.  Every FLM describes a way to build some kind of object e.g. a Symbian DLL.

The syntax used in Raptor is the one implemented in GNU Make 3.81. GNU make is a freely available open source tool which comes with an excellent manual and it is important to read through the manual and understand it before continuing.

== When Would one Create a New FLM? ==

 *   To fix parallelism problems caused by nmakefiles, gnumakefiles and Template Extension Makefiles
 *   To build some new kind of software that cannot be done with an MMP
 *   To add support for a new platform (e.g. X86) or a new compiler (e.g. rvct 4.1).

== Examples: ==

 *  resource.flm is an FLM for producing resource files.
 *  mifconv.flm is used to create bitmaps.

== Towards an FLM in Steps ==

For this purpose we are going to look at the task of building executables and the primary example will be a program called agenda.exe.

We will start with a simple FLM to build agenda.exe and end with one that can build any executable.
== What are the Targets? ==

Targets are the outputs of the build system. Targets are usually files. A makefile might declare a target as follows: Clearly if we are building agenda.exe then this is the primary target but there are usually other products of a build process if it is not completely trivial e.g.:
{{{
agenda.exe:
agenda.exe.sym:
agenda.o:
note.o:
date.o:
}}} 
But how are these related?

== Define the Dependencies - how Targets are Related ==

Sometimes, one target is used in the construction of another. There are, in other words, dependencies that affect the order in which various targets should be constructed.

If target A depends on target B then: # B must be constructed before A # if B is altered then A must be updated too

To carry the example forward we would now have the following:

{{{
agenda.exe: agenda.sym
agenda.exe.sym: agenda.o note.o
agenda.o: agenda.cpp
note.o: note.cpp
}}}


In the example above, note.cpp and date.cpp must exist before a build starts as these are inputs. The files note.o and date.o are required by agenda.exe.sym and agenda.exe requires that ageneda.exe.sym exist before it can be constructed.
== Add the Recipes - how to Construct Targets from Inputs (and from Each Other) ==

We know how to state what will be built and when (in terms of order) but not how.

Recipes are the list of instructions that describe how a target is created.
{{{
agenda.exe: agenda.sym
    postlink -o $@ $^
agenda.exe.sym: agendaw.o note.o
    link -o $@ $^
    strip $@
agenda.o: agenda.cpp
   compile -o $@ $^
}}}
The tab-indented lines in a makefile are recipes (although the commands such as postlink and compile are simplified).
= Recipes MUST Begin with a TAB Character. =

This is worth repeating: when a recipe is written in an FLM or an ordinary Makefile, the first character on the line '''''MUST''''' be a TAB.

Each recipe describes how to produce its target ($@) by working on its prerequisites or dependencies ($^).
= Recipes are Written in BASH Shell Script =

When a target is to be made, the recipe is executed within a shell. In FLMs the Bourne Again Shell (BASH) version 3.2 or above, is used. This means that recipes are written in the BASH syntax.

The result of executing the recipe for agenda.o, for example, is the following BASH command:
{{{
compile --o agenda.o agenda.cpp
}}}
This invokes a fictional tool called "compile" whose input is agenda.cpp and whose output is agenda.o.
= Make a General Pattern from a Specific Example with $(eval) =

The example that has been use so far describes how to build "agenda.exe" but if one had to build tens, hundreds or tens of thousands of executables (e.g. when building an operating system) then it would become very laborious to type out the entire pattern repeatedly - not to mention being difficult to maintain. If, for example a general change was required to the way all executables were to be built then the same change would have to be made for every executable - perhaps thousands of changes.

The GNU makefile syntax allows one to create a pattern and then re-use it repeatedly. Here is a simple pattern for building an executable from a single source file:
{{{
define buildexe
$(TARGET).exe: $(TARGET).sym
    postlink --o $$@ $$^
$(TARGET).exe.sym: $(SOURCE).o
    link -o $$@ $$^
$(SOURCE).o: $(SOURCE).cpp
    compile --o $$@ $$^
endef
}}}
The pattern is now stored in a variable which may be referenced as $(buildexe). Note that the automatic variables @ and ^ now have two $ signs in front of them - this will be explained in a moment.

The next step is to use the pattern to create some specific targets, dependencies and recipes. This is done by setting the TARGET and SOURCE parameters and then using the $(eval) function to cause the pattern to be read into GNU Make.
{{{
# Create targets, dependencies and recipes
# for agenda.exe

TARGET:=agenda
SOURCE:=agenda
$(eval $(buildexe))
# Create targets, dependencies
# and recipes for "otherprogram.exe"
TARGET:=otherprogram
SOURCE:=main
$(eval $(buildexe))
}}}

In these two "evals" the variable defined as buildexe is parsed by GNU Make when the $(eval) function is called. Two sets of targets, dependencies and recipes are created.

The automatic variables @ and ^ have to be "protected" from being expanded "too early" by the $(eval) command. This is done by using two $ characters e.g. $$@.

The effect is identical to writing out the pattern twice and substituting the names "otherprogram" and "agenda":

It's important to note the use of immediate assignment with colon-equals (':=') - this is the way all assignments are made in FLMs with almost no exceptions.

Some more complex examples will be discussed in later sections that will describe how to create patterns with different inputs.
== Add the boilerplate ==

For sbs CLEAN and sbs --what to work properly (--what is important for packaging) you must add some special extra lines to the FLM. There are macros to make this easier:

{{{
# mark normal binaries as releasables
$(call raptor_release,$(TARGET)))
# Mark intermediate files for cleaning.
# Releasables (as specified above) do not need to be marked for cleaning as well.
$(call raptor_clean,$(OBJECT_FILES))
}}}

raptor_release does accept a second parameter, which can be one of EXPORT, RESOURCE, BITMAP, STRINGTABLE or ARCHIVE. This will affect how they are reported in the whatlog output. If you don't care about that, don't bother with it. 

= Define the Interface to the FLM =

When a makefile "calls" an FLM, the parameters that the FLM "requires" are known as its interface.  FLMs and Interfaces are concepts that equate to function definitions in the C/C++ languages: the "inteface specification" is akin to a function declaration or prototype, and the implementation is akin to the function definition.

The interfaces to FLMs in Raptor are defined in XML files that are stored in the same locations as the FLMs themselves. An interface lists all the parameters that are required by an FLM and also provides default parameters. The interface for our example would look like this:
{{{    
    <interface name="executable" flm="executable.flm">
        <param name='TARGET' />
        <param name='SOURCE' />
    </interface>
}}} 
In the Raptor "front end" there are parsers for the different build specifications e.g. MMP files and bld.inf files. When the front end reads an MMP file it will then generate a makefile that "calls" the associated FLMs to do the work that the MMP specifies (e.g. building a DLL). The parser reads the input file and uses the information in it to populate the fields that are specified by the FLM's interface. The front end "knows" what information it must provide to the FLM by reading the FLM's interface. An error condition will occur if the front end attempts to "call" an FLM without providing all the necessary information. Thus no FLM may be used by Raptor without an interface file.
= Where to Put Interface Files =

The interface is, in fact, the way in which the "front end" interacts with an FLM, and even where it discovers the name of the file that contains the FLM. The front-end finds all XML files under the lib/flm directory and treats them as interfaces.

FLMs may be created and be stored in-source, with a component.  In this case the FLM and it's interface file must be exported to a directory under
{{{
$EPOCROOT/tools/makefile_templates/
}}}
which should take the form: 
{{{
$EPOCROOT/tools/makefile_templates/<componentname>
}}}
See [wiki:How_to_use_in-source_FLMs_with_Raptor How to use in-source FLMs with Raptor] for more information.
== Default Parameters in Interfaces ==

It is sometimes desirable for an FLM parameter have a default value. This allows the FLM to provide "safe" settings for rarely used features so that the knowledge about what is "safe" is kept near the FLM and away from the front end (encapsulation).

It also allows the same FLM to offer two different interfaces and thus allows one to create two similar build objects using the same FLM but setting different default parameters.
{{{
<build>
    <interface name="executable" flm="executable.flm">
        <param name='TARGET' />
        <param name='SOURCE' />
        <param name='OPTIMISATION' default='-O0' />
    </interface>
</build>
}}} 
In the example above, the 'OPTIMISATION' parameter to the build of an executable is set to '-O0' which many compilers treat as "no optimisation". This is a "safe" default because programs that are compiled with this option cannot suffer from bugs in the compiler's optimisation mechanism. This interface offers the option to set optimisation to achieve higher performance or ignore it safely.
= Inheritance in Interfaces =

The example that has been used so far is relatively simple but FLMs can become large and complicated. When this happens their interfaces can also become long - full of parameter settings for the different tools that an FLM uses. There can be a lot of repetition in a set of interfaces that relate to FLMs if the FLMs are building similar objects.

The following example is somewhat trivial but it demonstrates inheritance in interfaces and also abstract interfaces (ones that exist only to be inherited by others but don't have an associated FLM):
{{{
<build>
    <interface name="project" abstract="true" extends='base.flm'>
        <param name='COMPONENT_NAME' default='' />
        <param name='NAME' />
        <param name='SOURCE' />
    </interface>

    <interface name='dll' extends='base' flm='armv5binary.flm'>
        <param name='TARGETTYPE' default='DLL' />
        <param name='OPTIMISATION' default='-O0' />
    </interface>

    <interface name='exe' extends='base' flm='armv5binary.flm'>
        <param name='TARGETTYPE' default='EXE' />
        <param name='OPTIMISATION' default='-O1' />
    </interface>
</build>
}}} 
The example above shows how two similar objects (ARMv5 binaries) can be made by the same FLM using different defaults and the interfaces can share common characteristics via inheritance (the objects that the interfaces describe are both made from a list of source files and they both have to have names).

Note: All Interfaces must eventually have the interface base.flm as an ancestor. This enables all sorts of features to work later on e.g. logging the component and project that an FLM is building.
= Recipes that Log their Output Correctly =

The simple FLM that has been used as an example so far is only an FLM in a loose sense. FLMs are expected to meet a number of other criteria and one of them is the way that they log the result of each recipe.
== FLMs Output XML ==

FLMs log their output in XML format. Here is a real example of the output from a recipe that postlinks an executable - note that the output of the recipe is dark and the rest of the text is information about the recipe such as what component it comes from and how long it took to execute:
{{{
<recipe name='postlink'
host='head.raptor.symbian.intra'
layer='HAL'
component='Integrator ARM1136 Core Module'
bldinf='/scratch/home/raptorbot/baseline_94_089_9.4/cedar/generic/base/integrator/core/cm1136/bld.inf
mmp='/scratch/home/raptorbot/baseline_94_089_9.4/cedar/generic/base/integrator/integratorap/datxap.mmp'
config='armv5_urel.techview'
platform='armv5'
phase='DEFAULT'>
<![CDATA[
+ /scratch/home/raptorbot/baseline_94_089_9.4/epoc32/tools/elf2e32
--sid=0x1000015b --version=10.0
--uid1=0x10000079 --uid2=0x100039d0 --uid3=0x1000015b
--vid=0x70000001 --capability=all --fpu=softvfp --targettype=PDD
--output=/scratch/home/raptorbot/baseline_94_089_9.4/epoc32/release/armv5/urel/_integrator_cm1136_euart.pdd
--elfinput=/scratch/home/raptorbot/baseline_94_089_9.4/epoc32/release/armv5/urel/_integrator_cm1136_euart.pdd.sym
'--defoutput=/scratch/home/raptorbot/baseline_94_089_9.4/epoc32/build/core/cm1136/_integrator_cm1136_euart_pdd/armv5/urel/_integrator_cm1136_euart{000a0000}.def'
'--dso=/scratch/home/raptorbot/baseline_94_089_9.4/epoc32/build/core/cm1136/_integrator_cm1136_euart_pdd/armv5/urel/_integrator_cm1136_euart{000a0000}.dso'
'--linkas=_integrator_cm1136_euart{000a0000}[1000015b].pdd'
--dlldata '--sysdef=_Z20CreatePhysicalDevicev,1;' --ignorenoncallable
'--libpath=/scratch/home/raptorbot/baseline_94_089_9.4/epoc32/release/armv5/lib/;/opt/symbian/a616/ARM/RVCT/Data/2.2/308/lib/armlib)'
]]>
<time start='1216035815.347488000' elapsed='4.543' />
<status exit='ok' />
</recipe>
}}} 
It might look like an intimidating amount of work to add this to our tiny example but Raptor includes utilities that help with these aspects of FLM writing.
== Using the startrule and endrule macros ==

Raptor provides many utilities to FLM writers including two macros called <tt>startrule</tt> and <tt>endrule</tt> which implement XML logging. When an FLM recipe uses these two macros the FLM gains many features:
 *  Logs are easy to parse.
 *  In parallel builds on an ordinary computer (not a cluster) the log output is not "scrambled" up.
 *  It is easily possible to know which BLD.INF or MMP a command belongs to even in parallel builds where this cannot be determined by "where" the output appears in a log file.

The sample FLM looks like this so far:
{{{
define buildexe
$(TARGET).exe: $(TARGET).exe.sym
   postlink -o $$@ $$^
$(TARGET).exe.sym: $(SOURCE).o
   link -o $$@ $$^
   strip $$@
$(SOURCE).o: $(SOURCE).cpp
   compile -o $$@ $$^
endef
}}}
With startrule and endrule it looks like this:

{{{
define buildexe
$(TARGET).exe: $(TARGET).exe.sym
     $(call startrule,postlink) \
     postlink -o $$@ $$^ \
     $(call endrule,postlink)

$(TARGET).exe.sym: $(SOURCE).o
    $(call startrule,link) \
    link -o $$@ $$^ && \
    strip $$@ \
    $(call endrule,link)

$(SOURCE).o: $(SOURCE).cpp
    $(call startrule,compile) \
    compile -o $$@ $$^ \
    $(call endrule,compile)
endef
}}}
== Why do Lines in Recipes End with "\" and Sometimes "&& \"? ==

Normal GNU make recipes consist of one or more lines, each containing a shell command. These commands are executed in sequence and the remainder of a recipe is abandoned if one fails. Each time a command is run, a new invocation of the shell is started for that command.

This poses problems for the <tt>startule</tt> and <tt>endrule</tt> macros, since they must be able to:
 *  Output a simple tag to the log so that it is easy to determine if a recipe failed 
 *  Close the XML tags 
 *  Gather the output of a recipe and ensure that it is displayed correctly in parallel builds (sometimes commands that execute simultaneously can have their output intermingled and the endrule macro implements a system for preventing this). 
 *  Time commands to determine how long they took.

If all commands are on separate lines then <tt>$(endrule)</tt> will not be invoked when a command fails and thus there can be no error reporting and the &lt;/recipe&gt; tag will not be printed.

So the answer is to put all commands on one line - then they can be processed by one shell invocation (improves performance slightly) and the endrule macro can catch errors and handle them correctly.

The GNU make syntax allows one to show that a recipe command is continued on the next line by the use of the backslash character "\". If this character is the last on the line then GNU make assumes that the recipe command is not finished and reads the remainder of it from the next line of the make file.

Thus the following two recipes are identical:
{{{
# copy a file
$(DESTFILE): $(SOURCEFILE)
   $(call startrule,cp) \
    cp $$^ $$@ \
    $(call endrule,cp)
</code> and 
<code python>
# copy a file
$(DESTFILE): $(SOURCEFILE)
    $(call startrule,cp) cp $$^ $$@ $(call endrule,cp)
}}}
== So what about the &&? ==

Some recipes have more than one command in them. e.g. the example has the following one:
{{{
$(TARGET).exe.sym: $(SOURCE).o
    $(call startrule,link) \
    link -o $$@ $$^ && \
    strip $$@ \
    $(call endrule,link)
}}}
In this recipe there are only \*two\* commands. They end up being on the same line when they are passed to the shell so they must be separated. If one wishes to simulate the same behaviour as make (stop after the first command fails) then the bash shell's "logical AND" separator should be used which is "&&".

The example above passes the following command to the bash shell:
{{{
   link -o $$@ $$^ && strip $$@ 
}}} 
... or in words "link the object file and if that succeeds then strip the symbol and debug information off it"

Note: Sometimes one wishes to perform two commands without stopping if the first command fails. In this case one would use the bash shell's ";" separator.
== Where Build Output Goes ==

So far, in the simple example, only two files are created and both are based on the variable $(TARGET).

This is somewhat unrealistic - it implies that the target files are created in the directory from which the build is started and this is not how Raptor arranges matters.

Symbian OS software is usually all built into a particular directory which may be anywhere on the filesystem with Raptor. Because its location is configurable, the directory is usually indicated by an environment variable named "EPOCROOT".

The interface of an FLM can request the location of this directory from the Raptor "front-end" and then use the variable $(EPOCROOT).

Intermediate files and other data that would not be stored on a ROM and run on a phone are created in $(EPOCROOT)/epoc32/build. Targets that \*would be included in a ROM - are generally stored under the $(EPOCROOT)/release tree (binaries) or $(EPOCROOT)/epoc32/data tree (resources, ini files etc).

An FLM needs to know where to put files and the "front-end" supplies three variables that help it:
 *  $(OUTPUTPATH) for intermediate files - This is a location underneath $(EPOCROOT)/epoc32/build which is unique for the component (bld.inf) and platform (e.g. winscw or armv5). Examples of files that could be placed here would be object files which are not useful outside the build process itself their own and are only retained to enable incremental builds. 
 *  $(TARGETPATH) - This is the location for files that would be released i.e. put on a phone or packaged for use later on. This is usually $EPCROOT/epoc32/release 
 *  $(FULLVARIANTPATH) - it's not enough to know $(TARGETPATH). Some FLMs are associated with a particular platform. e.g. an FLM called 'e32abiv2.flm" might produce armv5 libraries. The output from the armv5 FLM and the winscw version has to be separated. Even within armv5 there are two other variations - udeb and urel. This information is recorded in $(FULLVARIANTPATH) so that FLMs which produce objects that are affected by the platform can keep their output separate. This variable is combined as follows to produce output: $(TARGETPATH)/$(FULLVARIANTPATH)
= Applying OUTPUTPATH to the Example =

The first thing that should be done is to update the interface to obtain our four new variables:
{{{
<build>
   <interface name="project" abstract="true" extends='base.flm'>
      <param name='COMPONENT_NAME' default='' />
      <param name='NAME'/>
      <paramname='SOURCE'/>
      <param name='EPOCROOT' />
      <param name='OUTPUTPATH' />
      <param name='TARGETPATH' />
      <param name='FULLVARIANTPATH' />
   </interface>

   <interface name='dll' extends='project' flm='armv5binary.flm'>
      <param name='TARGETTYPE' default='DLL' />
      <param name='OPTIMISATION' default='-O0' />
   </interface>

   <interface name='exe' extends='project' flm='armv5binary.flm'>
      <param name='TARGETTYPE' default='EXE' />
      <param name='OPTIMISATION' default='-O1' />
   </interface>
</build>
}}} 
These are then made use of in the FLM as follows: 

{{{
RELEASEPATH:=$(TARGETPATH)/$(FULLVARIANTPATH)
define buildexe
$(RELEASEPATH)/$(TARGET).exe: $(TARGET).exe.sym
    $(call startrule,postlink) \
    postlink -o $$@ $$^ \
    $(call endrule,postlink)

$(OUTPUTPATH)/$(TARGET).exe.sym: $(SOURCE).o
    $(call startrule,link) \
    link -o $$@ $$^ && \
    strip $$@ \
    $(call endrule,link)

OBJFILE:=$(OUTPUTPATH)/$(notdir $(SOURCE)).o
$(OBJFILE): $(SOURCE).cpp
    $(call startrule,compile) \
    compile -o $$@ $$^ \
    $(call endrule,compile)
endef
}}} 
As can be seen the output of the compile and link recipes are both "intermediate files" so they go into the $(OUTPUTPATH). The executable is something that's useful outside the build so it goes under $(TARGETPATH)/$FULLVARIANTPATH).

As an example, if this were an FLM for building armv5 debug executables and one used it to build agenda.exe then the executable would be put into
{{{
$(EPOCROOT)/epoc32/release/armv5/udeb/agenda.exe
}}}

NOTE: There is clearly a change in this FLM regarding the way the object file's name is determined from the name of the source file. We are beginning to assume that the source file may not be in the users' current working directory which means that a directory path may have to be stripped off it before the name of the object file can be constructed under the $(OUTPUTPATH) directory. This is very important later on in large parallel builds where all the source files cannot possibly be in the same directory.
= Making Directories =

FLMs create targets but they must also create the directories in which those targets are stored before the target itself can be created.

Targets such as:
{{{
$(OUTPUTPATH)/$(SOURCE).o: $(SOURCE).cpp
}}} 
...and: 
{{{
$(RELEASEPATH)/$(TARGET).exe: $(TARGET).exe.sym
}}}
Will require that "$(OUTPUTPATH) and $(RELEASEPATH) are created.

There is a special way for this task to be done in FLMs and all FLMs must implement directory creation this way. The reasons are involved but they concern the way that some parallel build engines incorrectly infer dependencies between separate recipies that attempt to create the same directory.

The $(makepath) macro causes directories to be created while a makefile is being read in. Usage is as follows:

{{{
$(call makepath,path1 path2 path3)
}}}

The, perhaps unusual, result of this is that all directories for all output are created before any recipes are executed. This happens to be of importance to parallel builds with Electric Accelerator since two attempts to create the same directory can cause EA to assume a false "implicit ordering" between two recipes which impacts performance.
== Cleaning Up ==

'''This section is superseded by the section "Add the boilerplate" above, which recommends the use of the simpler macro raptor_clean.'''

At some point it will be necessary to remove the targets that were generated by a particular build. Sometimes this might involve cleaning away an entire EPOCROOT tree but often it is very useful to only clear away the targets that were generated by a single component or project.

A user of Raptor might do this by using the following command
{{{
sbs -b somecomponent/group/bld.inf -c armv5 CLEAN
}}} 
FLMs must keep a record of all the targets they can produce. They must use the "GenerateStandardCleanTarget" macro to cause this list to of files to be cleaned when the Raptor front-end attempts to build the "CLEAN" target. Once again, this macro is provided by metaflm.mk.

{{{
# Record all paths that are created
CREATABLEPATHS:=
. # The body of the FLM
.
.
$(call makepath,$(CREATABLEPATHS))
.
.
}}}
The two parameters, $(CLEANTARGETS) and $(CREATABLEPATHS) must contain a list, respectively, of all the targets that the FLM creates and all the directories that it has specified in the $(makepath) macro. The convention is to build up lists of targets and the directories as one defines the targets in an FLM that generate them. Here is the simple example, modified to demonstrate this strategy:
{{{
# Initialise (very important) - always initialise
CREATABLEPATHS:=
CLEANTARGETS:=

RELEASEPATH:=$(TARGETPATH)/$(FULLVARIANTPATH)

define buildexe
$(RELEASEPATH)/$(TARGET).exe: $(TARGET).exe.sym
    $(call startrule,postlink) \
    postlink -o $$@ $$^ \
    $(call endrule,postlink)

CREATABLEPATHS:=$(CREATABLEPATHS) $(RELEASEPATH)
CLEANTARGETS:=$(CLEANTARGETS) $(RELEASEPATH)/$(TARGET).exe

$(OUTPUTPATH)/$(TARGET).exe.sym: $(SOURCE).o
    $(call startrule,link) \
    link -o $$@ $$^ && \
    strip $$@ \
    $(call endrule,link)

CREATABLEPATHS:=$(CREATABLEPATHS) $(OUTPUTPATH)
CLEANTARGETS:=$(CLEANTARGETS) $(OUTPUTPATH)/$(TARGET).exe.sym

OBJFILE:=$(OUTPUTPATH)/$(notdir $(SOURCE)).o
$(OBJFILE): $(SOURCE).cpp
    $(call startrule,compile) \
    compile -o $$@ $$^ \
    $(call endrule,compile)

CLEANTARGETS:=$(CLEANTARGETS) $(OBJFILE)

$(call makepath,$(CREATABLEPATHS))
$(eval $(call GenerateStandardCleanTarget,$(CLEANTARGETS), $(CREATABLEPATHS)))
endef # buildexe
}}}
== Generating Many Targets from a List of Source Files. ==

So far in the simple example FLM, it is only possible to build executables from one source file. This is clearly rather simplistic.

In many circumstances an FLM is required to generate targets, dependencies and recipes from lists of input files.

This can be achieved with the GNU Make functions $(foreach) and $(eval) together with some simple macros. The approach is as follows: Create a macro that compiles one source file, make the source filename a variable For every source file:
# Set a variable to the name of the sourcefile 
# Evaluate the macro to create targets, dependencies and recipies. That are specific to that source file.
= Using $(foreach ..) and $(eval) =

{{{
define compile
OBJFILE:=$(OUTPUTPATH)/$(notdir $(SOURCE)).o
$(OBJFILE): $(SOURCE).cpp
    $(call startrule,compile) \
    compile -o $$@ $$^ \
    $(call endrule,compile)
endef
$(foreach SOURCE,$(SOURCEFILES),$(eval $(compile)))
}}}

In the example above, the compile macro is evaluated once for each sourcefile. This causes a target and recipe to be created to make an object file from each sourcefile. How would this fit into the overall simple flm? Well, the simple flm has one macro so far. One might embed the compile macro within it but this requires some complex "escaping" of '$' characters to ensure that they are not expanded before they can be properly evaluated.

The less confusing approach is to create the compile macro outside the simple FLM's macro and call it from within. Here is how this can be done:
{{{
# A "simple" flm

define link
RELEASEPATH:=$(TARGETPATH)/$(FULLVARIANTPATH)
$(RELEASEPATH)/$(TARGET).exe: $(TARGET).exe.sym
    $(call startrule,postlink) \
    postlink -o $$@ $$^ \
    $(call endrule,postlink)

CREATABLEPATHS:=$(CREATABLEPATHS) $(RELEASEPATH)
CLEANTARGETS:=$(CLEANTARGETS) $(RELEASEPATH)/$(TARGET).exe

$(OUTPUTPATH)/$(TARGET).exe.sym: $(SOURCE).o
    $(call startrule,link) \
    link -o $$@ $$^ && \
    strip $$@ \
    $(call endrule,link)

CREATABLEPATHS:=$(CREATABLEPATHS) $(OUTPUTPATH)
CLEANTARGETS:=$(CLEANTARGETS) $(OUTPUTPATH)/$(TARGET).exe.sym
endef

define compile
OBJFILE:=$(OUTPUTPATH)/$(notdir $(SOURCE)).o
$(OBJFILE): $(SOURCE).cpp
    $(call startrule,compile) \
    compile -o $$@ $$^ \
    $(call endrule,compile)

CLEANTARGETS:=$(CLEANTARGETS) $(OBJFILE)
endef
define buildexe
# Initialise (very important) - always initialise
CREATABLEPATHS:=
CLEANTARGETS:=

$(foreach SOURCE,$(SOURCEFILES),$(eval $(compile)))
$(eval link)

$(call makepath,$(CREATABLEPATHS))
$(eval $(call GenerateStandardCleanTarget,$(CLEANTARGETS), $(CREATABLEPATHS)))
endef
}}}
This example splits the buildexe macro into "compile" and "link" and then ties these two together in buildexe.

Note: there is an assumption in this addition to the example that there is a change to the FLM interface. The SOURCE variable is removed and a new variable, SOURCEFILES, replaces it.
== "Horizontal" or "Double-Colon" Targets ==

In a large build there are many targets that are independent. e.g. there might be 4000 executables in a particular build of Symbian OS. Sometimes it is necessary to create dependencies that relate to a general condition e.g. "target X requires that all import libraries have been built". Make provides a way to give a "name" to groups like "all import libraries" or "all releasable targets". This document chooses to use the word "horizontal target" to describe a target that is really a logical or abstract grouping of many other targets.. Targets and dependencies are usually drawn as a tree. "Horizontal targets" are used in FLMs to group targets that are at roughly the same level in the tree. If one were to draw them on the tree of all dependencies, they might look like horizontal boxes.

!raptor-horizontal-targets.png!

In the diagram, there is a horizontal target called "LIBRARY" which is needed by two targets "LinkedX" and "LinkedY". This might be generalised and represented in English as saying, "Linking cannot be performed until all import libraries have been built." Horizontal targets are, therefore, a way of being imprecise about a dependency relation. They are broad rather than specific. They are the "enemy" of high performance parallel builds because they force targets to be delayed unnecessarily by a large group of other targets of whom perhaps only a few are really required. One should avoid depending on them at all costs. Horizontal dependencies have a purpose however, in situations where the build system doesn't yet have enough information to create accurate dependencies. e.g. all compilation targets in a Symbian OS build initially depend on all "EXPORT" targets. This is because header files are placed into a known location by the "EXPORT" recipes. During the first build of a piece of software, there is no information about which source files need which specific header files so this generalisation is needed. The first build usually generates the precise dependency information so that in successive builds the compile recipes don't have to depend on the "EXPORT" target.
= The Standard Raptor "Horizontal Targets" =

The Symbian Build System Version 2 has some standard horizontal targets and all FLMs should attach their targets to the appropriate horizontal ones if there is one that corresponds:
{{{
EXPORT - Copies the exported files to their destinations)
FINAL - Allows extension makefiles to execute final commands)
FREEZE - Freezes exported functions in a .DEF file)
LIBRARY - Creates import libraries from the frozen .DEF files)
LISTING - Creates assembler listing file for corresponding source file)
MAKEFILE - Creates makefiles or IDE workspaces)
BITMAP - Creates bitmap files)
RESOURCE - Creates resource files and AIFs)
ROMFILE - generates an IBY file to include in a ROM)
TARGET - Creates the main executable and also the resources)
}}}
One might have an flm with a target like this: 
{{{
$(RELEASEPATH)/$(TARGET).exe: $(TARGET).exe.sym
}}}
... and one would add this target to the "TARGET" horizontal target.
{{{
TARGET:: $(RELEASEPATH)/$(TARGET).exe

$(RELEASEPATH)/$(TARGET).exe: $(TARGET).exe.sym
}}}
It should be noted that the horizontal target is postfixed with a "::" to indicate that it is not a normal target. This is the origin of the GNU make name for horizontal targets: "double colon targets."
== The ALLTARGET ==

FLMs should add their "toplevel" targets to the ALLTARGET. If an FLM was viewed as a tree, there would be one "root" in a simple tree. Some FLMs end up being more like a "wood" and have several "roots". "roots" are just the targets that one wants an flm to produce ultimately they are not depended on by anything else in the FLM itself.

During an overall build, nothing is built unless it is "needed" by something else. There is one overall "root" called the "ALLTARGET" and every other target in a build must have some direct or indirect dependency relationship with it in order to be built. This can be implemented in the same way as any other horizontal target. For the simple example FLM there is nothing more to do than:
{{{
$(ALLTARGET):: $(RELEASEPATH)/$(TARGET).exe
TARGET:: $(RELEASEPATH)/$(TARGET).exe

$(RELEASEPATH)/$(TARGET).exe: $(TARGET).exe.sym
}}}
The simple flm example doesn't produce any libraries or export anything so it is not necessary to show the whole FLM just for this change.
== Variables in OPTION values ==

How Raptor handles option values can seem unclear. EXTENSION_ROOT, often the source of such confusion is considered here although other OPTION values fall into this behaviour too.

The following interface and FLMs see 'X' defined either as an absolute path (bad.flm) or relative to EXTENSION_ROOT (good.flm)

Therefore we strongly recommend that you do not use variables in OPTION values. 

{{{
# interface
<?xml version="1.0" encoding="ISO-8859-1"?>
<build xmlns="http://symbian.com/xml/build" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://symbian.com/xml/build ../../schema/build/2_0.xsd">

    <!-- this FLM expects X to be an absolute path
    -->
    <interface name="my.bad.example" extends="Symbian.UserFLM" flm="bad.flm">
       <param name="X"/>
       <param name="Y"/>
    </interface>

    <!-- this FLM expects X to be relative to EXTENSION_ROOT
    -->
    <interface name="my.good.example" extends="Symbian.UserFLM" flm="good.flm">
       <param name="X"/>
       <param name="Y"/>
    </interface>

    <!-- both expect Y to be relative to the output folder -->

</build>
}}}

{{{
# bad.flm
# X is an absolute path. This *wont* work properly
# if X contains unexpanded variables...

TARGET:=$(PLATFORM_PATH)/$(CFG_PATH)/$(Y)
DEPENDS:=
COMMAND:=echo $(X)

$(call raptor_recipe,bad,$(TARGET),$(DEPENDS),$(COMMAND))

ALL:: $(TARGET)
}}}

{{{
# good.flm
# X is relative to EXTENSION_ROOT

TARGET:=$(PLATFORM_PATH)/$(CFG_PATH)/$(Y)
DEPENDS:=
COMMAND:=echo $(EXTENSION_ROOT)/$(X)

$(call raptor_recipe,good,$(TARGET),$(DEPENDS),$(COMMAND))

ALL:: $(TARGET)
}}}

{{{
# bad bld.inf
PRJ_EXTENSIONS

START EXTENSION my.bad.example
OPTION X $(EXTENSION_ROOT)/a.txt
OPTION Y a.bin
END

START EXTENSION my.good.example
OPTION X a.txt
OPTION Y a.run
END
}}}

{{{
# good bld.inf
PRJ_EXTENSIONS

START EXTENSION my.bad.example
OPTION X $(EXTENSION_ROOT)/b.txt
OPTION Y b.bin
END

START EXTENSION my.good.example
OPTION X b.txt
OPTION Y b.run
END
}}}

Escaping of make variables referenced in option values leads to an intentionaly delayed expansion by Raptor. This delay can make variables take seemingly unexpected values when used by the FLM.

OPTION X $(EXTENSION_ROOT)/a.txt in the example bld.infs when referenced by good.flm (X as a relative path) and bad.flm (X as a absolute path) illustrates the issue with the ECHO command output from each FLM: 

Output from good.flm
{{{
      ../example/a/a.txt (expected)
}}}      
and
{{{
      ../example/b/b.txt (expected)
}}}
Output from bad.flm
{{{
      ../example/a/a.txt (expected)
}}}      
and
{{{      
      ../example/a/b.txt (unexpected - still holding the initial expanded value of EXTENSION_ROOT)
}}}
Note the generated value of the EXTENSION_ROOT does not change in the bad output example, this is due to X containing an unexpanded variable.

It is possible to deal with escaping in a safer manner using the following command at the top of an FLM (continuing with the EXTENSION_ROOT example):

{{{
$(eval EXTENSION_ROOT:=$(EXTENSION_ROOT))
}}}

The files flmtools.mk and metaflm.mk are included into any Raptor build so that their macros are available to all FLMs. metaflm.mk contains raptor_clean and raptor_release, as well as all the macros used to make those. The macros in flmtools.mk are summarized below:

||||||= Literal Macros =||
||= Macro name =||= what it is =||= why =||
|| CHAR_COMMA || A literal comma || where typing , would be makefile syntax ||
|| CHAR_SEMIC || literal ; || ||
|| CHAR_COLON || literal : || ||
|| CHAR_SPACE || literal space || ||
|| CHAR_TAB || literal tab || ||
|| CHAR_DQUOTE || literal " || ||
|| CHAR_QUOTE || literal ' || ||
|| CHAR_LBRACKET || literal ( || ||
|| CHAR_RBRACKET || literal ) || ||

||||||= General Macros =||
||= Macro name =||= what it is =||= why =||
|| shEscapeBrackets || replaces ( and ) with \( and \) || useful for passing strings involving literal brackets to the shell ||
|| shEscapeQuotes || replaces ' and " with \' and \" || useful for passing to the shell ||
|| shEscape || escapes brackets and quotes || useful for passing to the shell ||
|| ruleEscape || precedes all spaces with \ || for rule targets or dependencies that may contain spaces ||
|| concat || concatenates a space-separated list of strings (second parameter) with a joining string (first parameter) || ||
|| lowercase || converts to lower case || ||
|| uppercase || converts to upper case || ||
|| uniq || removes duplicates from a (space-separated) list, retaining the original order || ||
|| enclose || encloses each item in a list (second parameter) with a pair of (first parameter) || for example, putting something in quotes ||
|| dblquote || encloses each item in a list in double quotes || ||
|| dblquoteitem || double-quotes a single item, but a null string remains unmolested || ||
|| addquotedprefix || puts each item in $(2) into "$(1)item" || ||
|| makemacrodef || puts each item in $(2) into $1'item' || making a command line; for example $(call makemacrodef,-D,LINUX TOOLS EXP=_declspec(export) NODEBUG) becomes -D'LINUX' -D'TOOLS' -D'EXP=_declspec(export)' -DNODEBUG ||
|| sanitise || turn forward slashes and colons into underscores || so that filenames can be used as variable names ||
|| groupin10infile || creates a command that pushes all the items in a list into a file; ten per line || to make command files ||

||||||= Debugging Macros =||
||= Macro name =||= what it is =||= why =||
|| flmdebug || causes all the variables named in $(FLMDEBUG) to be echoed as part of a rule || ||

||||||= Path Handling Macros =||
||= Macro name =||= what it is =||= why =||
|| slashprotect || don't know || ||
|| pathrep || don't know || ||
|| allsuffixsubst || replaces all the suffices in $(1) with the suffix in $(2) in the list of files in $(3) || for example $(call allsuffixsubst,.cpp .c++ .cxx .CPP,.o,$(FILES)) would convert C++ file names into their respective object file names ||
|| extractfilesoftype || returns all filenames in $(2) that match one of the suffixes specified in $(1) || for example $(call extractfilesoftype,.cpp .cxx .c++ .CPP,$(FILES)) would find all the C++ file names in $(FILES) ||
|| extractandmap || Effectively performs extractfilesoftype then allsuffixsubst, returning all files in $(3) that have one of the suffixes specified in $(1), but with the suffix replaced by $(2) || for example extracting C++ files and returning their respective object files ||
|| relocatefiles || returns the list of file names in $(2) but with their directory portions replaced with $(1) || ||

||||||= Simple Recipe-Writing Macros =||
||= Macro name =||= what it is =||= why =||
|| raptor_recipe || $(call raptor_recipe,myRuleName,target,prerequisites,command) builds a rule with target, prerequisites and command, wrapped with all the necessary boilerplate. The name gives the name that will be given to this recipe in the log || Ensures the recipe is correctly constructed with all the necessary boilerplate ||
|| raptor_phony_recipe || Creates a phony recipe || Don't use this ||

||||||= Simple Command-File Creating Macro =||
||= Macro name =||= what it is =||= why =||
|| createcommandfile || $(call createcommandfile,filename,contents) makes a rule to build the command file 'filename' with contents 'contents' (appropriately split over lines). This filename must, of course, be included as a dependency of whatever needs it. The command file depends on the MMP file, so will be rebuilt if the MMP file changes. || Useful for when command lines get too long and break shell command-line length limits ||

= When would you write a new FLM and how would you add it to Raptor? =

'''TODO: This section needs to be expanded'''

Replacing Template Extension Makefiles with FLMs

When Raptor comes across a reference to a template extension makefile in a bld.inf it looks for a similarly named FLM first in $SBS_HOME/lib/flm and uses this in preference. This means that new FLMs have to be added to Raptor which is not completely ideal. This should be rectified in future.
= Conclusion =

This document has shown how to bring an FLM to a high state of maturity.




= How to use in-source FLMs with Raptor =

To understand FLMs you should first have read the [wiki:Guide_to_Writing_Function-Like_Makefiles_for_Raptor Guide to Writing Function-Like Makefiles for Raptor].

Having created a Function-Like Makefile  you need to know how to get Raptor to use it.  There are two ways to do this:

1. '''Native FLMS:''' Add it into Raptor itself in the SBS_HOME/lib/flm directory.  This route is only open to people who are developing Raptor or who have an FLM that is of general utility to all users of the builds system.  It is not an appropriate place for FLMs that are only relevant to one component.
1. '''In-Source FLMS:''' Put the FLM in-source with the component that needs to use it.

This is a description of how to work with in-source FLMs
==  Keep your FLMs in you Component's "group" Directory  ==
To recap, an FLM consists of two parts:

1. The '''Interface specification''' XML files, can contain one or more interface per file
1. The '''Implementation''' a specially written makefile with the extension ".flm"

Custom FLMs are kept alongside your other source code, usually in the "group" directory of the component that they are associated with.
==  Export them to "makefile_templates" do Raptor can Find them  ==

Raptor doesn't know that flms are in the source for a component.  You have to export the "flm" and the interface file to a known location first where Raptor wil be able to find them.  That location is 
{{{
$EPOCROOT/epoc32/tools/makefile_templates
}}}
In general they should be put there in a subdirectory like this: 
{{{
$EPOCROOT/epoc32/tools/makefile_templates/<componentname>
}}}

You can perform this export using your bld.inf's PRJ_EXPORT section. 

The following example is for a "raptor_linux_dist" extension. It uses a Python script to package some directories.
= Example =

Assume that we are rewriting an extension makefile to convert it into an FLM to remove parallelism problems in the build:
{{{
## raptor_linux_dist.mk

MAKMAKE :
   cd "$(subst /,\,$(EXTENSION_ROOT)/..)"; python python/sbs_dist.py   $(RAPTOR_DIST) $(RAPTOR_DIST_INCLUDE_DIRS)

# Dummy target
DO_NOTHING :

RELEASABLES CLEAN BLD LIB SAVESPACE FREEZE CLEANLIB RESOURCE FINAL : DO_NOTHING
}}}

This runs the Python script "python/sbs_dist.py" from the directory`$(EXTENSION_ROOT)/..` in the MAKMAKE stage.

In this case, it is simple to write an FLM to do the same thing. Since Raptor does not really have a notion of stages as such (other than EXPORT),  we create a Make rule that specifies dependencies and a target file and attaches this to the `ALL` target but basically the commands are similar to those in the TEM.  We now have a  rule that will work properly when building incrementally.
{{{
## raptor_linux_dist.flm

## Parameters that are expected:
# RAPTOR_DIST
# RAPTOR_DIST_INCLUDE_DIRS


# We're now using dependencies which helps to make this parallel-safe.  Since
# sbs_dist generates many files we use a "marker file" to "represent" the other files and save
# ourselves from dealing with hundreds of files.

define sbs_dist

ALL:: $(RAPTOR_DIST)/completed

$(RAPTOR_DIST)/completed:  $(EXTENSION_ROOT)/../python/raptor_version.py
   $(call startrule,createsbsdist) \
   cd $(EXTENSION_ROOT)/.. && python python/sbs_dist.py $(RAPTOR_DIST) $(RAPTOR_DIST_INCLUDE_DIRS) && \
   $(GNUTOUCH) $(RAPTOR_DIST)/completed \
   $(call endrule,createsbsdist)

endef

$(eval $(sbs_dist))

# Clean up - we really should clean more thoroughly than just removing the marker file
# but that would be complicated.
$(eval $(call GenerateStandardCleanTarget,$(RAPTOR_DIST)/completed))

}}}

Define your interface (e.g: `tools.raptor_linux_dist`) and specify the parameters used in the FLM. The `interface` XML element has a `name` attribute whose value should be a ful-stop-separated string, in this case `tools.raptor_linux_dis`. The `flm` attribute is the filename of the FLM.

Raptor effectively joins these two attributes together to form the filename  `tools/raptor_linux_dist/raptor_linux_dist.flm`, which is relative to $EPOCROOT/epoc32/tools/makefile_templates/ - this is where the FLM  and its XML interface file should be exported to.

'''''N.B.:''' As your FLMs need to work on Linux case-sensitive file systems it is essential that the case of the letters of the filename on the file system matches exactly all references in the interface file as well as the bld.inf PRJ_EXPORTs section. 

Below is a complete Raptor XML file, that defines the interface for our `raptor_linux_dist.flm`. This tells Raptor to expect the parameters `RAPTOR_DIST`, `RAPTOR_DIST_INCLUDE_DIRS` and `EXTENSION_ROOT` to be set for this FLM invocation. 

{{{
  <?xml version="1.0" encoding="ISO-8859-1"?>
  <build xmlns="http://symbian.com/xml/build"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://symbian.com/xml/build http://symbian.com/xml/build/2_0.xsd">
    <!-- Extension interfaces : replacements for Template Extension Makefiles -->    
    <interface name="tools.raptor_linux_dist" flm="raptor_linux_dist.flm">
      <param name="RAPTOR_DIST" />
      <param name="RAPTOR_DIST_INCLUDE_DIRS" />
      <param name="EXTENSION_ROOT" />
    </interface>
  </build>
}}}

Below is an updated `bld.inf` file that exports the FLM and XML files, and invokes the FLM in the PRJ_EXTENSIONS section. Note that the EXTENSION_ROOT does not need to be set explicitly using the OPTION MMP keyword because it has a default value that Raptor provides.
{{{
PRJ_PLATFORMS
TOOLS TOOLS2

PRJ_EXPORTS
raptor_linux_dist.flm /epoc32/tools/makefile_templates/tools/raptor_linux_dist.flm
raptor_linux_dist.xml /epoc32/tools/makefile_templates/tools/raptor_linux_dist.xml

PRJ_EXTENSIONS
START EXTENSION tools/raptor_linux_dist

// Specifies distribution file name and location e.g. dist/sbsv2_linux_dist.tar.gz
OPTION RAPTOR_DIST dist/sbsv2_linux_dist.tar.gz

// Specifies the raptor subdirectories to be included in tar dist
OPTION RAPTOR_DIST_INCLUDE_DIRS bin lib python linux-i386 schema

// Set the EXTENSION_ROOT value
OPTION EXTENSION_ROOT directory/containing/bld_inf_file

END
}}}



= Detecting clashing exports =


There is a script in {{{SBS_HOME/bin}}} which you can use to check exports across a set of log files. It tells you about conflicts (multiple sources exported to the same destination), repeats (same source exported to the same destination by multiple components) and chains (file exported to a destination and then re-exported from there to somewhere else).
== Usage: ==
{{{
 sbs_check_exports.py < logfile.xml
}}}

or, to push all *.xml files (on Linux or on Windows where Cygwin binaries are on the path)

{{{
 cat log*.xml | sbs_check_exports.py
}}}

or, on Windows
{{{
 type log*.xml | sbs_check_exports.py
}}}



= How to use a System Definition file =

The Raptor command line interface implements the {{{-s|--sysdef}}} argument which can be used to pass in a version 1 or version 2 system definition file to build.  For example:

{{{
sbs -s sysdef.xml -c armv5_urel
}}}

Users can pass in multiple {{{-s}}} options, or even mix them with {{{-b|--bldinf}}} options specifying additional bld.infs to build.

By default, Raptor will build all the components (units, in sysdef terminology) in all the specified sysdefs (and additional specified bld.inf files).  Users can limit what components are built by specifying which [#Layers layers] should be built using the {{{-l|--layer}}} argument:

{{{
sbs -s sysdef.xml -l core
}}}

{{{
#!comment
I suspect that Raptor puts -b specified bld.infs into a layer called 'commandline' or similar, so -b foo/bld.inf -l layer won't build foo/bld.inf.  Might be worth adding if confirmed.
}}}

== Building version 3 package definitions ==

NOTE: This section needs updating.  Genxml is not a supported tool.

To build one or more v3 package definition, they must first be converted into a v2 system definition.  This uses the {{{genxml}}} tool.

For example:
{{{
\epoc32\tools\build\genxml.pl
    -s \
    -m y:\output\canonical_system_definition.xml
    -x E:\Build_E\common\dtd\sysdef_dtd_1_5_1.xml
    -x y:\src\sysdef\systemdefinition.xml
    -x y:\epoc32\tools\SystemBuild.xml
    -x y:\src\app\clock\layers.sysdef.xml
    -x y:\src\app\contacts\layers.sysdef.xml
}}}

In this example, y:\output\canonical_system_definiton.xml is the output for the merged system definition file.  The {{{-x}}} argument supplies the XML fragments to combine, with all the package definitions listed at the end.  The {{{-s}}} argument can be useful if all {{{-x}}} files are under a shared root, but in this example they aren't, so the value of backslash must be used.

{{{
#!comment
So, how can anyone get hold of these various header files?
}}}

== Ordered layers ==

The user can use the {{{-o|--orderlayers}}} argument to ensure that layers are built in the specified orders.  Normally Raptor will handle inter-component dependencies automatically, but components using extension makefiles may not properly announce their dependencies, so limiting the order in which they can be built may be useful.

Users can use the argument in one of two ways.  Firstly, as an option, combined with {{{-l}}}:

{{{
sbs -s sysdef.xml -l core -l ui -o
}}}

This would build all the components in the 'core' layer before starting to build any of the components in the 'ui' layer.

If -o is used without -l options, all layers are built in the order they occur in the system definiton file.

== How Raptor parses sysdefs ==

=== Unit elements ===
Unit elements contain the path to the bld.inf file.  The bld.inf file must be named 'bld.inf', and the bldinf attribute points to the folder containing the bld.inf file.

How these paths are handled differs between v2 and v3 system definition files, and whether they begin with a slash or not:

|| ||=v1/v2 =||=v3 =||
||=slash =||relative to source root ||relative to source root ||
||=no slash =||relative to the current working directory ||relative to sysdef/pkgdef file ||
[[BR]]
The source root is defined (for v2 and v3 sysdefs) as, in decreasing order of priority: # The value of the environment variable pointed to by the root attribute of the element (v3 only) # or, the value of the -a option # or, the value of the SRCROOT environment variable # or, the value of the SOURCEROOT environment variable # or, (somewhat bizarrely) the current working directory

For v1.3+ sysdefs it's just the value of the -a option.

Thus with v3 sysdefs it's possible to write modular pkgdefs - ones that live inside a component and work regardless of where the component is installed, by writing your bldinf paths so that they don't begin with a slash.  This is not possible with v1 or v2 sysdefs.  However note, [http://developer.symbian.org/bugs/show_bug.cgi?id=2735 Bug 2735] prevented this from working prior to v2.15.0 of Raptor.

=== Layers ===
Note that Raptor obtains the name of the layer from any component - not necessarily the one named 'Layer'.  Raptor creates a layer for every XML element providing its parent element doesn't specify a layer id.  The layer id is specified by the attribute 'id' in v3 sysdefs, and 'name' in v1/v2 sysdefs.  Normally the Layer element in v3 sysdefs ends up being the only element with an id that is inside an element without an id, though Raptor doesn't enforce this.

{{{
<SystemDefintion schema="3.0.0">

  <systemModel name="foo">
    <layer id="layerid"...>
      <package id="bar"...>
        <collection id="baz"...>
          <component id="bash"...>
            <unit .../>
          </component>
        </collection>
      </package>
    </layer>
  </systemModel>

</SystemDefinition>
}}}
Note also that internally, raptor records layers for the top level !SystemDefinition and !SystemModel elements, despite these not having the appropriate attribute.  This layer is recorded as being named the empty string, and contains no components, so is never reported in any error messages.   In this example the layers are 'layerid' and ' '.

{{{
#!comment
There shouldn't be a space between those last two quotes, but I'll be damned if I can figure out how to make this wiki display two quotes together.
}}}




= Overriding toolcheck =

=  Toolcheck in brief  =

Before Raptor runs a build, it checks the tools that will be invoked by the build. In this way, tools incompatibilities can be identified early, rather than causing confusing errors during the build itself.

Symbols defined in the XML configuration in `<env>` or `<set>` tags can have their `type` attribute set to `tool`. If so, it can also have `versionCommand` and`versionResult` attributes, which define the toolcheck.

`versionCommand` gives a command that is to be executed (in the `bash` shell) to retrieve the version information. The returned string is checked against a regular expression given by `versionResult` attribute. If it fails to match, a diagnostic is produced and the build is not run. Here's an example:

{{{
 <set name="GCCECC" value="$(GCCEBIN)/arm-none-symbianelf-g++$(DOTEXE)"
 type="tool"
 versionCommand="$(GCCECC) -dumpversion"
 versionResult="4\.3\.2"
 versionDescription="You are using an unsupported version of GCCE. Version 4.3.2 is required."/>
}}}

=  Overriding toolcheck  =

This is simply a case of overriding the appropriate symbol; i.e. reproducing the `<env>` or `<set>` tag for the tool that needs its version check modifying.

The easiest way to achieve this is to create a new variant with the modified `<env>` or `<set>` tag. For example, to modify the above to accept any GCCE 4.x.y, we could write:

{{{
 <var name="anygcce4">
   <set name="GCCECC" value="$(GCCEBIN)/arm-none-symbianelf-g++$(DOTEXE)"
   type="tool"
   versionCommand="$(GCCECC) -dumpversion"
   versionResult="4\.\d+\.\d+"/>
 </var>
}}}

Now all that remains is to ensure that this variant is called by default. We do this by overriding the default aliases as described in [wiki:Raptor_Kit_Configuration#Alias_redefinition Kit Configuration]:
{{{
 <alias name="armv5_urel" meaning="arm.v5.urel.gcce4_3_2.anygcce"/>
 <alias name="armv5_udeb" meaning="arm.v5.udeb.gcce4_3_2.anygcce"/>
}}}
This will allow a user to put any GCCE 4 in masquerading as 4.3.2 without having to disable toolcheck (with `--toolcheck=off`).




The trace compiler is (roughly) a tool for connecting tracepoints in code with user-readable messages without having to store those messages in the code that's being traced or transmit it over debugging connections.

With raptor one can switch tracing on or off at the SDK level so that older versions of Symbian that don't support tracing will turn it off whereas S^3 and newer SDKs will have it turned on at that level.

It is also necessary to switch it "on" for each particular MMP that one might wish to trace. In the past the way that this was effected was the use of userinclude:


{{{
userinclude ../traces
}}}

This indicated to raptor that it should run the Trace Compiler on the source code specified in the MMP.  From this code the Trace compiler could generate a list of trace "IDs", could store them in an id database and could generate header files that defined the ids so that the program, on compilation, would have the ids embedded at each corresponding trace point.  When a tracepoint is hit, the id can be transmitted to a debugger/trace viewer which can then search the trace database to find the string associated with that trace id.

The problem with this old method is that a component with several MMPs in it might look like this:

{{{
-group
     barney.mmp
     fred.mmp
     bld.inf
-source
    common.cpp
    barney.cpp
    fred.cpp
-traces
    commonTraces.h
    barneyTraces.h
    fredTraces.h
}}}


The problem is with "commonTraces.h" which stores trace IDs for a file that's common to two MMPs.  The problem with this is that it's wrong - whichever MMP is processed last will "win" and it's trace IDs will be recorded in commonTraces.h and the trace ID's of the previous MMP will be lost.  So if barney.mmp is processed first then it's version of "commonTrace.h" will be written then overwritten and all tracepoints in barney.cpp will actually appear to the user to be triggered by the executable specified in fred.mmp.

Hence Raptor 2.15.0 introduces a new method for keeping traces separated.  Instead of specifying "userinclude ../traces" one now uses the TRACES keyword:
{{{
TRACES
}}}

This creates a better directory structure:
{{{

-group
     barney.mmp
     fred.mmp
     bld.inf
-source
    common.cpp
    barney.cpp
    fred.cpp
-traces
    -barney_exe
          commonTraces.h
          barneyTraces.h
    -fred_dll
          commonTraces.h
          fredTraces.h
}}}

Now the two mmps don't get traces confused when there is a common file.


== Switching Tracing OFF ==

Files with tracepoints in them generally do this:

{{{
// Trace compile macro and header
#include "OstTraceDefinitions.h"
#ifdef OST_TRACE_COMPILER_IN_USE
#include "barneyTraces.h"
#endif

TInt E32Main()
{
        OstTrace0( TRACE_NORMAL, PLACE1, "Barney Tracepoint #1" );
        return 0;
}

}}}

The problem is that the Trace Compiler writes out the file "OstTraceDefinitions.h" and forces OST_TRACE_COMPILER_IN_USE to ON:

{{{
#define __OSTTRACEDEFINITIONS_H__
// OST_TRACE_COMPILER_IN_USE flag has been added by Trace Compiler
// REMOVE BEFORE CHECK-IN TO VERSION CONTROL
#define OST_TRACE_COMPILER_IN_USE
#include <opensystemtrace.h>
}}}


This essentially makes it impossible to switch tracing off for any MMP that has been configured to use it. The  OST_TRACE_COMPILER_IN_USE macro gets defined by this file which causes all tracepoints to be active - it basically tells opensystemtrace.h to define the trace macros as "real"

=== SOLUTION ===

So the way to avoid this annoying file that forces tracing on is to simply not include it!  The only thing it does is define  OST_TRACE_COMPILER_IN_USE

{{{
// Trace compile macro and header

#include <opensystemtrace.h>

#ifdef OST_TRACE_COMPILER_IN_USE
#include "barneyTraces.h"
#endif

TInt E32Main()
{
        OstTrace0( TRACE_NORMAL, PLACE1, "Barney Tracepoint #1" );
        return 0;
}

}}}

The idea here is to bypass the annoyance by not actually including "OstTraceDefinition.h" at all.  Raptor will define OST_TRACE_COMPILER_IN_USE when it sees the TRACES keyword in the MMP file so all that is needed to turn tracing on/off is to add/remove the TRACES keyword.






== Tools Platform ==
Raptor supports GCC from versions >4 and MINGW version 4.5 for building tools


== Symbian ARM Platform ==
GCCE versions >4 and <= 4.5 are supported.
The full list: https://sourcery.mentor.com/sgpp/lite/arm/portal/subscription3058

   * 4.5.1 -https://sourcery.mentor.com/sgpp/lite/arm/portal/release1589
   * 4.4.1 - https://sourcery.mentor.com/sgpp/lite/arm/portal/release1258

RVCT 2.2 (recommeded patch 686), 3.1 (not recommended), 4.0, 4.1
Patches avaliable at  https://silver.arm.com/browse/RVS22 (free login required).

== Symbian WINSCW Platform ==
Nokia Codewarrior Version  3.2 Runtime Built: Jun 29 2007 13:41:5






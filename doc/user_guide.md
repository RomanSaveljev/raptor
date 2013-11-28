# User guide #

= Raptor Quick Start =

==  How to Install Raptor  ==

If you have obtained Raptor as a {{{.exe}}} (Windows) or {{{.sh}}} (Linux) then you have an installer - run the file and follow the on-screen instructions.

If you have obtained Raptor as a {{{.zip}}} then you have an archived Windows distribution - unpack it somewhere accessible and add the {{{bin}}} directory of the unpacked tree to the system {{{PATH}}}.

If you have neither of the above, then follow the instructions below to use and configure a clone of our Mercurial repository.

=== Mercurial ===

This web-site hosts a Mercurial repository containing recent releases of Raptor - this repository can be cloned and used directly, on both Windows and Linux, but there are a few steps you'll need to go through to do this.

First of all, you'll need a valid install of Mercurial.

''Windows''

Grab the latest stable release (appropriate to your Windows version) of one of the following:

http://mercurial.selenic.com/downloads/

http://tortoisehg.bitbucket.org/download/index.html

TortoiseHg is more a useful set of GUI tools wrapped around Mercurial, although it does include the Mercurial command line tools as part of its distribution.  You don't need the GUI tools to install and use Raptor, but if you're going to use Mercurial in general they're very useful. TortoiseHg also works on Linux.

''Linux''

The Mercurial made available as part of your package management system is probably fine.  See the instructions in the right-hand pane here:

http://mercurial.selenic.com/downloads/

=== The Raptor Repository ===

==== Structure ====

As the Raptor Mercurial Repository is an on-going and updated entity, it houses both past and present Raptor versions.

The Trac Browser on this web-site provides a GUI means to navigate the current tree:

http://projects.developer.nokia.com/raptor/browser

If you click on the "Visit:" drop-down box in the browse it lists both the "branches" available in the repository and a set of "tags" that identify memorable instances of Raptor at particular points in time.  The {{{default}}} branch is where formal Raptor releases can be found.  Numerical tags identify a formal, tested, Raptor release (the bigger the number, the newer the release) and the {{{stable}}} tag value shows what we consider to be the last, ehh, stable, version ;-) .

==== Cloning ====

Typically you'll be interested in the latest {{{stable}}} release from the {{{default}}} branch.  To get this, from a command prompt navigate to where you wish to install Raptor and issue the following command:

{{{
    hg clone http://anonymous@projects.developer.nokia.com/hg/raptor -r stable
}}}

After a little while you should have a fully populated repository cloned at the {{{stable}}} changeset.  There's now some further configuration you need to do to get Raptor up and running

=== Configuration ===

==== General ====

The set-up now required varies depending on whether you're running on Windows or Linux, but one common step is that the {{{bin}}} directory within the root {{{raptor}}} directory needs to be on the system {{{PATH}}}. 
 
|| Environment Variable || Description || Windows || Linux ||
|| {{{PATH}}} || Permit easy {{{sbs}}} invocation || {{{set PATH=C:\my\install\raptor\bin;%PATH%}}} || {{{export PATH=/my/install/raptor/bin:$PATH}}} ||

==== Python ====

Raptor itself is a Python application, therefore you're going to need an appropriate version of Python installed and available; it is recommended that you run Raptor with Python 2.7 or later. Python3 support available from Raptor version 2.17.0 onwards.

|| Environment Variable || Description || Windows || Linux ||
|| {{{SBS_PYTHON}}} || Location of Python interpreter for Raptor to use || {{{set SBS_PYTHON=C:\Python27\python.exe}}} || {{{export SBS_PYTHON=/opt/python27/python}}} ||

''Windows''

Grab the latest 2.7.* release (appropriate to your Windows version) of one of the following:

http://www.python.org/download/

Install in the normal way.

''Linux''

If you have an appropriate version of Python on your system already, then you can just use that. Or download the appropriate version e.g. from above link.

''' NOTE! ''' In case of UCS2 stackless and UCS4 boost issues (e.g. Undefined Symbol: PyUnicodeUCS2_FromEncodedObject) ensure you're using same python version that raptor python extensions has been built with.

==== Support Tools and Utilities ====

Raptor makes uses of common shell tools as well as it's own custom tools.  Depending on whether you're running on Windows and Linux, what you need to install and configure differs

==== Cygwin (Windows Only) ====

Raptor runs under bash shell. Hence you need cygwin tools for Windows. Download and run Cygwin setup.exe:

http://cygwin.com/install.html

and follow the installation instructions. Further details what's really required can be found from [wiki:Raptor_Supporting_Tools Raptor_Supporting_Tools]

|| Environment Variable || Description || Windows || Linux ||
|| {{{SBS_CYGWIN}}} || Location of Cygwin for Raptor to use || {{{set SBS_CYGWIN=C:\cygwin}}} || {{{N/A}}} ||

'''NOTE! '''

For Cygwin17 you should use specific env variable''' SBS_CYGWIN17=C:\cygwin17''' due the differences between the mount options in 1.7.x and earlier versions.

==== MinGW (Windows Only) ====

Raptor uses the GNU tools and essentially the gnu make included in the set. Hence you need the minimalist GNU for Windows (MinGW). Download and run latest mingw-get-inst-*.exe:

http://www.mingw.org/wiki/Getting_Started

From the installer select following:

MinGW Compiler Suite
	- C Compiler
	- C++ Compiler

|| Environment Variable || Description || Windows || Linux ||
|| {{{SBS_MINGW}}} || Location of MinGW for Raptor to use || {{{set SBS_MINGW=C:\MinGW}}} || {{{N/A}}} ||


==== GNU tools (Linux only) ====

Raptor uses GNU tools which should be found by default in any linux setup you might have. Raptor defaults to the locations under /usr/bin for those. If you are missing
some, install them locally with the installation method supported on your system. 
You can also override the Raptor default location by setting the env variables like SBS_GNUCPP yourself to point on the version you wish to use. You can see all the GNU tool env variables from raptor/lib/config/locations.xml


=== Special Raptor utilities  ===

Raptor uses talon shell wrapper. '''Installation is required on linux side only'''. Windows binary exists in the repository already. 
To succesfully build the utilities like talon you need to set up SBS_HOME env variable:

|| Environment Variable || Description || Windows || Linux ||
|| {{{SBS_HOME}}} || Location of Raptor home dir || {{{Not required}}} || {{{set SBS_HOME=/my/install/raptor}}} ||

So on Linux you can install ''talon'' from raptor/util directory by running following commands:


{{{
make talon
make talonctl
}}}

For the full Utils build you'll  need additionally "libncurses5-dev" module plus following python modules:

dbm, gdbm, sqlite3, ssl, tkinter,  bz2, readline, zlib

Which can be obtained e.g. on Ubuntu like "sudo apt-get install <module>" or "sudo apt-get build-dep python"

=== Compiler ===

Download and run the latest CodeSourcery G++ Lite Installer for '''ARM SymbianOS'''
https://sourcery.mentor.com/sgpp/lite/arm/portal/release1258

You can use the 'typical' installation options.

|| Environment Variable || Description || Windows || Linux ||
|| {{{SBS_GCCE441BIN}}} || Location of GCCE for Raptor to use || {{{set SBS_GCCE441BIN=C:\Program Files (x86)\CodeSourcery\Sourcery G++ Lite\bin}}} || {{{export SBS_GCCE441BIN=/opt/CodeSourcery/Sourcery G++ Lite/bin}}} ||

=== Symbian tools ===

The Symbian tools, not part of the Raptor, but used by the Raptor build systems such as rcomp (resource compiler), elf2e32 and checklib etc. are supposed to be delivered within the SDKs. However there's only Windows executables at the moment included. How to deliver the Symbian tools linux executables to outside world is still TBD.


=== Perl ===


Symbian (S60) compilation requires also the Perl tool which is used by certain tools in the build process (e.g. DEF file creation and management) -> Obtain Perl e.g. from: 

http://www.activestate.com/activeperl/downloads

|| Environment Variable || Description || Windows || Linux ||
|| {{{SBS_PERL}}} || Location of PERL for Raptor to use || {{{set SBS_PERL=C:\actperl\perl.exe}}} || {{{export SBS_PERL=/opt/actperl/perl}}} ||

'''OR''' ensure perl is being found from PATH.

For most users that is all the configuration required. To confirm Raptor is correctly set up run the sbs ''version'' command and confirm you get output similar to that shown below: 

{{{
    >sbs -v
    sbs version 2.17.1 [<date> symbian build system xxx]
}}}

==  SDK Set Up  ==


=== EPOCROOT ===

Raptor is not associated with a particular SDK (unlike SBSv1). The  {{{EPOCROOT}}} environment variable is used to specify location of the (current) target SDK's {{{/epoc32}}} directory, expressed as an absolute path.

|| Environment Variable || Description || Windows || Linux ||
|| {{{EPOCROOT}}} || Path to {{{/epoc32}}} directory in target kit || set {{{EPOCROOT=c:\mybuildenv}}} || export {{{EPOCROOT=/usr/home/me/sdk101}}} ||

The target SDK must also have the [wiki:Raptor_Kit_Configuration#variant.cfg variant.cfg configuration file] installed at {{{EPOCROOT/epoc32/tools/variant/variant.cfg}}}, with the contents as shown below. Note that Symbian SDK's (examples) come with this file by default.

{{{
    epoc32\include\variant\Symbian_OS.hrh 
    ENABLE_ABIV2_MODE
}}}

The target SDK ''may'' also need a [wiki:Raptor_Kit_Configuration#Kit_Configuration_(sbs_config) Kit Configuration (sbs config)] file, for example if you want to use a different compiler, or define your own SDK specific build configuration. ''Note: You will need the configuration file if you want to use Raptor to build against an the Symbian!^1 (S60 5th Edition) SDK. See 
[wiki:Raptor_Kit_Configuration#root_changes_variant_(for_Symbian!^1/Symbian_OS_v9.4_kits) Kit Configuration (sbs config)] for more information. ''

==  SBS Commands   ==
A high level view on Raptor commands is given in the [wiki:Raptor_Quick_Reference Quick Reference], with more detail in the full [wiki:Raptor_Command_Line_Reference Command line reference].  The ''Quick Build'' section below shows some of the more common build commands using configuration ''aliases''.

==  Quick Build  ==

Install a SDK examples from projects.developer.nokia.com. Set the EPOCROOT to point to the SDK root: 
{{{
       set EPOCROOT=c:\my_build_env
}}}

With the  {{{EPOCROOT}}} set, Raptor knows that the current SDK is the target kit. There is no need to check for the {{{variant.cfg}}}, as this is present in all Symbian SDKs.

Example components that comes with the SDKs like {{{examples/symbian/gui/animation}}} for instance.

To build all default targets for a particular component, simply navigate to the folder in which its {{{bld.inf}}} file resides (usually "group"). Then do:
{{{sbs}}}

If you just want to build for winscw udeb do the following:
{{{sbs -c winscw_udeb}}}

If you want to build udeb and release binaries for arm5, and have RVCT 2.2. installed, do:
{{{sbs -c armv5}}}

If you're using non-commercial compiler GCCE for arm5 target, do:
{{{sbs -c arm.v5.urel.gcce4_4_1}}}

If you have any problems, follow the [wiki:#Troubleshooting troubleshooting checklist] below.

==  Troubleshooting  ==

 1. The {{{SBS_HOME}}} environment variable must be set to indicate the Raptor home directory. Done by Raptor automatically when invoked from PATH.
 1. The PATH variable must include {{{<SBS_HOME>/bin}}}.
 1. Check whether the {{{EPOCROOT}}} environment variable is set to an absolute path. Setting {{{EPOCROOT}}} to a relative path (for example, /) is supported to allow SBSv1 ("the old build system") and Raptor to coexist. Symbian recommends not to use a relative path unless both build systems must coexist.
 1. Check that the {{{EPOCROOT}}} directory contains the file {{{epoc32/tools/variant/variant.cfg}}} and that the file includes the following: {{{epoc32\include\variant\Symbian_OS.hrh ENABLE_ABIV2_MODE}}}
 1. Run the 'sbs' command with debug (-d) and output (-f-) options to check whether appropriate versions of the required tools are available. If the appropriate versions of the required tools are not available an error is reported. {{{ > sbs -d -f- }}}
 1. If you're using RVCT check that the {{{LM_LICENSE_FILE}}} or {{{ARMLMD_LICENSE_FILE}}} environment variable is set to a valid RVCT license file or a license server. 

==  Further Configuration  ==

No other configuration is required, or in general necessary. Note however that it is possible to further configure the way that Raptor will build for a particular kit, and to define your own aliases and build configurations. See the following documents for information:

 *  [wiki:Raptor_Personal_Preferences Personal Preferences] - How to configure Raptor for your own preferences on your own machine
 *  [wiki:Raptor_Kit_Configuration Kit Set up] - How to configure a kit (or any epoc32 tree) for Raptor

==  Related Info  ==

 *  [wiki:Raptor_Environment_Variables Environment Variables] - A listing of the Raptor environment variables
 *  [wiki:Raptor_Supporting_Tools Raptor_Supporting_Tools] - more details on the supporting tools

= Raptor Basic Concepts =

== Overview of Raptor Operation ==

Raptor builds in two distinct stages

=== Stage 1: Metadata Parsing ===

Metadata consists of {{{bld.inf}}} files and {{{.mmp}}} files. These are parsed and converted into a makefile that will drive the main part of the build.

The makefile produced depends also on the command-line options passed to Raptor, so you get a different makefile if you are building different configurations.

The makefile is in GNU make syntax.

=== Stage 2: The Build ===

The build is run with a standard make tool. Raptor can pass the makefile to one of the following make tools:
 * GNU make
 * PVMG make (a parallel version of GNU make -- the default)
 * Electric Make (a proprietary parallel make utility from Electric Cloud; must be installed separately)

=== Configurations, Variants and Aliases ===

What is built is specified on the command-line thus:

{{{
    sbs -c configuration_name
}}}

In reality, every configuration is composed from a number of ''variants'' from a single default configuration. Variants are composed with the {{{.}}} character, thus:

{{{
    sbs -c arm.v5.urel.rvct3_1
}}}

which specifies that the basic instruction set to be built is {{{arm}}}, that the architecture is {{{v5}}}, that the release version is to be built and that the compiler version to use is RVCT 3.1.

As such strings of variants are tiresome to type, ''aliases'' are provided:

{{{
    sbs -c armv5_urel
}}}

which does the same thing (assuming your kit defines RVCT 3.1 as the default compiler)

=== System Definition Files ===

By default, the {{{sbs}}} command will build everything specified by a {{{bld.inf}}} file in the current working directory. An explicit {{{bld.inf}}} file can be specified instead with the {{{-b}}} option. Alternatively, a System Definition file can be supplied, which is an XML file containing information about which {{{bld.inf}}} files are to be built, amongst other things. [reference needed]

=== Settings Files ===

There are three settings files:

|| {{{%SBS_HOME%\sbs_init.xml}}} or {{{%HOME%\.sbs_init.xml}}} || personal settings ||
|| {{{%EPOCROOT%\epoc32\sbs_config\os_properties.xml}}} || build settings ||
|| {{{%EPOCROOT%\tools\variant\variant.cfg}}} || pre-include file and other simple build settings ||

= Raptor Quick Reference =


This article provides a comparison of some common build commands in both ABLD and Raptor, along with some additional information about Raptor commands. More detailed information about Raptor commands is provided in the [wiki:Raptor_Command_Line_Reference Command Line Reference].

||= Abld =||= Raptor =||= Description =||
|| bldmake bldfiles || (Not needed) || Create build files ||
|| abld build || sbs, sbs -c default ||Builds the default platforms specified in your bld.inf, normally: armv5 winscw udeb urel ||
|| abld test build || sbs -c default.test || Builds test code for default platforms specified in your bld.inf ||
|| abld build armv5 || sbs -c armv5 || Build armv5 udeb and urel targets ||
|| abld build armv5smp || sbs -c armv5.smp || Build armv5 udeb and urel SMP targets ||
|| abld build armv5 udeb || sbs -c armv5_udeb || Build armv5 udeb target ||
|| abld build winscw || sbs -c winscw || Build winscw udeb and urel targets ||
|| abld test build winscw || sbs -c winscw.test || Build winscw test code ||
|| abld build armv5 urel -k || sbs -j 4 -c armv5_urel -k || Build arvm5 urel target, continuing if buildstep fails ||
|| abld clean || sbs -c default clean || Clean all default build targets ||
|| abld armv5 clean || sbs -c armv5 clean || Clean build of armv5 urel and udeb binaries ||
|| abld test build armv5 || sbs -c armv5.test || Build armv5 test binaries for urel and udeb targets ||
|| abld freeze armv5, abld test freeze armv5 || sbs -c armv5 freeze, sbs -c armv5.test freeze || Build armv5 target and freeze exports ||
|| ''none'' || sbs -v || Check the version of Raptor you have installed ||


Like bldmake, SBSv2 by default builds the file named {{{bld.inf}}} in the current directory (usually named {{{\group}}}.  You can also specify an explicitly named project file (which doesn't have to be called "bld.inf" using the {{{-b}}} flag:

{{{
    sbs -b d:\blah\bld.inf
}}}

You can chain multiple configurations together, the following:

{{{
    sbs -c winscw_udeb.test -c winscw_urel.test -c armv5_udeb.test -c armv5_urel.test -c winscw_udeb -c winscw_urel -c armv5_udeb -c armv5_urel
}}}

...is equivalent to:

{{{
    sbs -c default -c default.test
}}}

You can also specify a command file that can contain any valid SBSv2 commands. These can spread out across multiple lines, e.g. have multiple paths to bld.inf's one per line, for example:

{{{
    sbs --command=commands_file.txt
}}}

...where {{{command_file.txt}}} contains:

{{{
    -b F:\path\to\a\bld.inf
    -b F:\path\to\another\bld.inf
    -b F:\path\to\yet\another\bld.inf
    -b G:\path\to\g\drive\bld.inf
    -b K:\path\to\k\drive\a\bld.inf
    -b F:\path\to\build\information\file\with\a\different\name\not_a_bld_inf.inf
    -c armv5_urel
    -c winscw_udeb
    -c armv7
}}}

= Raptor Personal Preferences =

== Using your own Python, Cygwin or MinGW ==

Set {{{SBS_PYTHON}}}, {{{SBS_CYGWIN}}} (or {{{SBS_CYGWIN17}}} for using Cygwin 1.7) and {{{SBS_MINGW}}} environment variables to the installed locations of the Python executable, the location of the Cygwin bin directory and the location of the MinGW bin directory, respectively, you want to use. Any that are not set default to those bundled with Raptor.

== Your own command line options ==

Personal preferences can be defined for your own Raptor installation. These settings are placed in a file called either {{{%HOME%\.sbs_init.xml}}} or, if that does not exist, {{{%SBS_HOME%\sbs_init.xml}}}.

Within your Raptor installation, you will find a directory called {{{examples}}}. Please consult the {{{sbs_config.xml}}} file there for help in customizing your Raptor installation.

As an example, imagine that you wanted to be able to use RVCT4.0 in an SDK configured to use RVCT2.2 by default. The command lines you would need are {{{sbs -c arm.v5.udeb.rvct4_0}}} for debug, {{{sbs -c arm.v5.urel.rvct4_0}}} for release, or {{{sbs -c arm.v5.udeb.rvct4_0 -c arm.v5.urel.rvct4_0}}} for both. As this is tedious to write, you could add the following to your {{{sbs_init.xml}}}:

{{{
<alias name="armv5_urel_rvct4_0" meaning="arm.v5.urel.rvct4_0" />
<alias name="armv5_udeb_rvct4_0" meaning="arm.v5.udeb.rvct4_0" />
<group name="armv5_rvct4_0">
  <aliasRef ref="armv5_urel_rvct4_0" /> 
  <aliasRef ref="armv5_udeb_rvct4_0" /> 
</group>
}}}

so that{{{sbs -c armv5_udeb_rvct4_0}}}, {{{sbs -c armv5_urel_rvct4_0}}} and {{{sbs -c armv5_rvct4_0}}} become available on your installation.

Alternatively, you could override the existing {{{armv5_udeb}}} and {{{armv5_urel}}} definitions:

{{{
<alias name="armv5_urel" meaning="arm.v5.urel.rvct4_0" />
<alias name="armv5_udeb" meaning="arm.v5.udeb.rvct4_0" />
}}}

As {{{armv5}}} is defined as being composed of {{{armv5_udeb}}} and {{{armv5_urel}}} and you are changing the definition of both those aliases, you do not need to override {{{armv5}}} as well.

To add GCCE (with an {{{-fpermissive option}}}) you could similarly use:
{{{
<?xml version="1.0" encoding="ISO-8859-1"?>
<build xmlns="http://symbian.com/xml/build"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://symbian.com/xml/build ../../schema/build/2_0.xsd">
  <var name="permissive">
    <append name="CC_ERRORS_CONTROL_OPTION" value="-fpermissive"/>
  </var>
  <alias name="armv5_urel_gcce" meaning="arm.v5.urel.gcce4_4_1.permissive"/>
  <alias name="armv5_udeb_gcce" meaning="arm.v5.udeb.gcce4_4_1.permissive"/>
  <group name="armv5_gcce">
    <aliasRef ref="armv5_urel_gcce"/>
    <aliasRef ref="armv5_udeb_gcce"/>
  </group>
</build>
}}}

or to make GCCE the default:

{{{
<?xml version="1.0" encoding="ISO-8859-1"?>
<build xmlns="http://symbian.com/xml/build"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://symbian.com/xml/build ../../schema/build/2_0.xsd">
  <var name="permissive">
    <append name="CC_ERRORS_CONTROL_OPTION" value="-fpermissive"/>
  </var>
  <alias name="armv5_urel" meaning="arm.v5.urel.gcce4_4_1.permissive"/>
  <alias name="armv5_udeb" meaning="arm.v5.udeb.gcce4_4_1.permissive"/>
</build>
}}}
==  To make Raptor default to using 16 parallel jobs when building:  ==


{{{
<?xml version="1.0" encoding="ISO-8859-1"?>
<build xmlns="http://symbian.com/xml/build"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://symbian.com/xml/build ../../schema/build/2_0.xsd">

  <var name="defaults.init">
    <set name="jobs" value="16"/>
  </var>
</build>
}}}

= Common Raptor Build Problems =

This page contains a list of common Raptor build problems and some notes and comments about how to solve and work around them.

== Debugging tips for Linux ==

# strace: TODO  - quick over view of strace

# valgrind: TODO  - quick over view of valgrind

== Debugging tips for Windows ==

# Process Explorer from Microsoft's SysInternals Suite [http://technet.microsoft.com/en-us/sysinternals/bb842062.aspx] is highly recommended for debugging "stuck" processes. You can use it to see the process tree and examine processes that might be "stuck". Note that some of the other tools from that suite require administrator access to run.

== Debugging tips for all platforms ==

=== TALON_DEBUG ===

Raptor has a supporting tool named {{{talon}}} which is a C program. It is used a shell wrapper (i.e. wraps calls to Bash) and to ensure the log file from parallel jobs is not scrambled (using a semaphore). For those that remembered {{{sbs_descramble}}} (which served the function of unscrambling the log), {{{talon}}} has superseded it as well as having the additional functionality of wrapping the shell controlling the output from Bash, enclosing it in descriptive XML (recipe) tags and delaying the output until there are no other processes writing to the log. {{{talon}}} is also able to time out on long commands and to retry commands if they fail.

On occasion it is necessary to debug the commands that {{{talon}}} launches. In this case, the {{{TALON_DEBUG}}} environment may be set to any non-blank value.

On Windows:

{{{
    set TALON_DEBUG=true
}}}

On Linux/Unix (Bash shell):

{{{
   export TALON_DEBUG=true
}}}

When this is done, {{{talon}}} prints additional debugging information into the log file which can be used to isolate problems.

Removing the {{{TALON_DEBUG}}} environment variable will stop the debugging information being outputted.

=== A Raptor command hangs and does nothing ===

||= Problem =||= OS =||= Possible solution/comments =||
|| Windows problem || Windows || Sometimes if Windows hasn't been rebooted for a very long time (e.g. the "suspend" or "hibernate" option has been used or the machine has just been powered up for a long time), strange effects can manifest themselves. I'm not clear exactly what happens, but it is "well-known" that a reboot can solve many of these bizarre effects. So, give that a try first if your machine hasn't been restarted for a long time (say 5 or more working days). ||
|| Cygwin 1.5 problem || Windows || Raptor uses Cygwin to provide the "Core utils" (e.g. {{{cp}}}, {{{rm}}} etc) on Windows. In order that these function correctly, certain Cygwin mount points have to be set, in particular {{{/tmp}}}. Raptor tries to remount these every time it starts in order to ensure that all Cygwin programs function correctly. The {{{/tmp}}} mount point is required for certain Cygwin programs which won't run without it. Sometimes the {{{mount}}} or {{{umount}}} commands get stuck - you should be able to see that from Process Explorer.  If it's the case that {{{mount}}} or {{{umount}}} have hung, it is likely you have another Cygwin 1.5 installation and a program running from it. The recommended course of action is to stop that program and then from the Cygwin 1.5 installation that Raptor is using, run the command {{{umount -A}}}. This command removes *all* system mount points, and Raptor will put back the ones it needs next time you run it. You can also try this even if you have no other installations of Cygwin.  The main reason this problem occurs is that Cygwin 1.5 stores information about its mount points in the registry, thus making is very difficult to have more than one installation of Cygwin 1.5 on a single machine because all of the Cygwin installations read the mount points from the same location in the registry.  Cygwin 1.7 stores the mount points in a file inside its installation directory, which means that you can install several copies in parallel with no problems. Raptor can be used with Cygwin 1.7 - see [wiki:Raptor_Supporting_Tools] and [wiki:Raptor_Environment_Variables] for details on how to use Cygwin 1.7 with Raptor]. ||
|| Network license problems || All || Certain supporting tools might require a licence check every time they are run. In some situations, this licence must be stored on a licence server that is on the network. It can happen that the licence server is very slow to respond. In these cases, the build might appear to hang waiting for the licence request to complete.  In some cases with a network-based licence server, it has been observed that the driver for the ethernet card can crash or "get stuck" waiting for a licence request to complete. Adverse interaction with antivirus and anti-malware software has also been observed on occasion.  The resolution would be to investigate the ethernet driver and antivirus software - check for updates and apply them.  Note that it is possible for other software to also interfere with ethernet drivers. ||










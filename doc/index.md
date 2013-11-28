= The Raptor Build System =

The Raptor build system is used for building Symbian platform C++ applications, packages, or indeed the entire platform. Raptor can run on both Windows and Linux, and works with Symbian!^1/Symbian OS v9.4 and later (only). While it uses the same build metadata files (`bld.inf` and `.mmp`), Raptor builds are often significantly faster; when used with third-party parallel make programs, such as PVM Gmake and EMake, it can use multiple build machines to create a build farm.

----

==  User Guide ==
|| [wiki:Raptor_Quick_Start Raptor Quick Start] || Downloading, installation and set up ||
|| [wiki:Raptor_Basic_Concepts Basic Concepts] || An explanation of the basic terms used in the rest of this documentation ||
|| [wiki:Raptor_Quick_Reference Quick Reference] || command-line options and migrating from `abld` ||
|| [wiki:Raptor_Personal_Preferences Personal Preferences] || How to configure Raptor for your own preferences on your own machine ||
|| [wiki:Common_Raptor_Build_Problems Common Raptor Build Problems] || A list of common Raptor build problems and solutions/notes about them ||

----

== Reference Documentation ==
|| [wiki:Introduction_to_RAPTOR Architecture Overview] || An overview of Raptor architecture, usage, FLMs etc. ||
|| [wiki:Raptor_Command_Line_Reference Command-line reference] || Detailed command-line reference ||
|| [wiki:Raptor_Environment_Variables Environment Variables] || A listing of environment variables used by Raptor ||
|| [wiki:Raptor_Build_Extensions Build Extensions] || How to build non-standard components ||
|| [wiki:Raptor_Kit_Configuration Kit Configuration] || How to configure a kit (or any epoc32 tree) for Raptor ||
|| [wiki:Raptor_Log_Format Log file format] || What's in the logs, how to find out more ||
|| [wiki:Raptor_Symbian_Reference Reference] || What does the build system produce, what is Symbian made up of and how does it happen ||
|| [wiki:Raptor_Supporting_Tools Supporting Tools] || What supporting PC tools the build system uses ||
|| [wiki:Exports_and_Freezing_in_the_Build Exports and Freezing in the Build] || Short reference guide to exports and freezing in the build ||
|| [wiki:MMP_keywords MMP keywords] || Documentation for MMP keywords ||
|| [wiki:BLD.INF_keywords BLD.INF syntax] || Documentation for BLD.INF syntax and keywords ||

----

== Howtos and In-depth Articles ==
|| [wiki:How_to_build_Raptor How to Build Raptor] || How to get and build Raptor from source ||
|| [wiki:Tips_for_Big_Builds_with_Raptor Tips for Big Builds with Raptor] || Hints on performing a large build efficiently ||
|| [wiki:Building_System_Definition_Layers_in_Order_Using_Raptor Building System Definition Layers in Order Using Raptor] || Building System Definition Layers in Order ||
|| [wiki:Raptor_Dependencies Raptor Dependencies] || How Raptor Uses and Creates Dependencies ||
|| [wiki:How_to_Use_Raptor_with_RVCT_4.0_on_RVCT2.2_Kits How to Use Raptor with RVCT 4.0 on RVCT2.2 Kits] || Using RVCT4.0 in SDKs requiring RVCT2.2 ||
|| [wiki:Introduction_to_Developing_Raptor_(SBSv2) Introduction to Developing Raptor] || ||
|| [wiki:How_to_use_Raptor's_log_filter_plug-ins How to use Raptor's log filter plug-ins] || A guide on how to using Raptor's log filter plug-ins
|| [wiki:Raptor_Binary_Variation Raptor Binary Variation] || Binary Variation ||
|| [wiki:Raptor_How_Template_Extension_Makefiles_are_Dealt_With How Template Extension Makefiles are Dealt With] || How TEMS are catered for in Raptor. Note they should be rewritten as FLMS asap.  ||
|| [wiki:Guide_to_Writing_Function-Like_Makefiles_for_Raptor Guide to Writing Function-Like Makefiles for Raptor] || A guide to writing Function-Like Makefiles (FLM's) for Raptor
|| [wiki:How_to_use_in-source_FLMs_with_Raptor How to use in-source FLMs with Raptor] || A quick guide to using custom FLMs  ||
|| [wiki:Detecting_clashing_exports Detecting clashing exports] || How to tell if multiple projects are exporting files that overwrite each other ||
|| [wiki:How_to_use_a_System_Definition_file How to use a System Definition file] || How to a use System Definition file ||
|| [wiki:Overriding_toolcheck Overriding toolcheck] || Making an SDK insist on certain versions of tools ||
|| [wiki:Trace_Compiler_Switching] || How to make trace compilation ON/OFF switchable ||
|| [wiki:Raptor_Compilers] || Compilers that can be used with Raptor ||
|| [wiki:Caseless_Filesystem] || A filesystem for Linux that allows one to build code written on Windows without being forced to correct case inconsistencies first||
----

== Hobbies, side projects and work-in-progress ==
This section contains some information that's nothing to do with the team developing Raptor, and isn't supported or endorsed by them.  As such, you should use information from here at your own risk.

[wiki:Using_Raptor_in_pre-Symbian_Foundation_SDKs Using Raptor in pre-Symbian Foundation SDKs]

[wiki:Bootstrapping_the_Symbian_build_tools_on_Ubuntu_Linux Bootstrapping the Symbian build tools on Ubuntu Linux]

[wiki:Raptor_3 Raptor 3]

[wiki:OpenBuildServiceNotes]
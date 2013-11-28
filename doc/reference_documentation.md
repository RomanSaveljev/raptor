# Reference documentation #

= Introduction to RAPTOR =


{{For Technical Review|[[BR]]Aspects of this document might be '''out of date'''.  It's based on v2.0 of RAPTOR.  The current version (Oct 2009) is v2.9.2
[[BR]]If you wish to raise an issue or a query please visit our Tools forum: [[BR]]<nowiki>http://developer.symbian.org/forum/forumdisplay.php?f=42</nowiki>.}}

RAPTOR is the promotional name of the next-generation Symbian build system, also called Symbian Build System v2 (SBSv2)
= This document outlines: =

 * the fundamental technical concepts on which SBSv2 is built
 * the architecture of SBSv2
 * the platforms on which SBSv2 runs (Linux and Windows)
 * scalability of SBSv2
 * the short-term and long-term benefits
 * what needs to be done by customers to make use of SBSv2 in their build environment.
= Fundamental technical concepts =
This section describes the fundamental technical concepts that underpin RAPTOR.
= =Function Like Makefiles ==
The concept of Function Like Makefiles ([wiki:Glossary#FLM FLM]s) is at the core of RAPTOR and has been invented to solve some of the restrictions that exist in GNU Make today. Restrictions in GNU Make exist in the following areas:
 * modularity and code re-use
 * separation of interface and implementation
 * extensibility
 * testability.

FLMs solve these problems through a combination of meta-information describing an FLM and coding conventions. FLMs do this without requiring changes to the GNU Make language and thus changes to the make engines supporting these. Their key function is to reduce complexity and to make it possible to create a makefile-based build system that is maintainable, while also achieving good scalability in builds.

FLMs contain two parts:
 * an interface specification part (encoded in XML)
 * an implementation part (or body) which is encoded in GNU Make.

The specification part of the FLM exposes inputs, outputs, configurable parameters, and meta-information of the FLM. This makes an FLM an independent, re-usable, and testable component encoded in GNU Make. In essence the FLM becomes a black box with inputs, outputs, parameters and specified behaviours, which RAPTOR combines into a large makefile.

# Note that for historical reasons the name RAPTOR will be used instead of SBSv2 throughout this document.
# In fact similar restrictions exist for most make / build engines.
# Note that currently RAPTOR treats inputs, outputs, and meta-information like parameters.

[wiki:File:Raptor_FLM_Bitmap.png 500px]

Another way of trying to understand FLMs is to think about them in terms of C++ templates, with the key difference that they do not instantiate a class or function, but rather, a section of a dependency tree. As in a higher-level language, the templates are the building blocks to construct a larger system.

Coding conventions are used to achieve the make equivalent of re-entrancy (in other words, the same FLM can be included in the same hierarchy of makefiles several times). FLMs can make use of other FLMs, and therefore, complex FLMs can be created from simpler ones. All build processes in RAPTOR are implemented as FLMs, from core build processes used to build Symbian OS binaries, through to special functionality build processes such as kernel bootstraps. Therefore, extensibility is at the heart of RAPTOR.

In opposition to most languages where interfaces and implementation are separated, currently RAPTOR does not allow several FLM bodies to implement the same interface4. The reason for this is that this functionality was not needed in RAPTOR, and that the separation of interface and implementation was introduced to:
 * make it easy for the RAPTOR back-end to assemble larger makefiles from FLMs
 * ensure that RAPTOR needs to know as little as possible about makefiles
 * enable tooling that can be used to verify the FLM body against the FLM interface specification.

This means that it is possible to replace one FLM describing a build process with a different one, with little or no impact on the overall build system. Bugs in the build system can be detected easily, as each FLM can be tested individually. This means it is possible to isolate faults. Bugs can also be detected through tooling that supports formal verification of FLMs.
= ==Example of FLM interface specifications ===
The following section shows an example of FLM interface definitions and how these use derivation. Currently, all inputs and outputs in an FLM are treated equally.
<code xml>
<?xml version="1.0" encoding="ISO-8859-1"?>

<build xmlns="http://symbian.com/xml/build"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xsi:schemaLocation="http://symbian.com/xml/build ../../schema/build/2_0.xsd">

       <interface name="Symbian.flm" abstract="true">
              <param name='FLMHOME' />
       </interface>
       <interface name="buildprogram" extends="Symbian.flm" flm="buildprogram.flm">
              <param name='TARGET' />
              <param name='SOURCEFILE' />
              <param name='GCC' />
              <param name='DEBUG' />
       </interface>
       <interface name="strippedprogram" extends="buildprogram" flm="strippedprogram.flm">
              <param name='STRIP' />
       </interface>
</build>
</code>

The interface {{Icode|Symbian.flm}} is an abstract type, which is the root of all FLM interfaces that are used in RAPTOR. RAPTOR uses a hierarchy of abstract FLM interfaces for all FLMs to ensure consistency in core RAPTOR functionality. For example {{Icode|Symbian.MMP}} is the interface for all objects that are described in MMP files, {{Icode|Symbian.DLL}} is the FLM interface for all DLLs, {{Icode|Symbian.EXE}} is the FLM interface for all EXEs, etc. Inevitably there will be different implementations of FLMs for each interface, for example, a different DLL implementation for each toolchain.
= ==Corresponding BLD.INF file fragments ===
Declaring FLMs with interface XML files like the above allows the following syntax to be added to BLD.INF files, inside a <tt>PRJ_EXTENSIONS</tt> section:

 PRJ_EXTENSIONS
 
 START EXTENSION <b>buildprogram</b>
 <b>TARGET</b> my.o
 <b>SOURCEFILE</b> my.cpp
 END EXTENSION
 
 START EXTENSION <b>strippedprogram</b>
 <b>TARGET</b> my2.o
 <b>SOURCEFILE</b> my2.cpp
 END EXTENSION

The parameters <b>TARGET</b> and <b>SOURCEFILE</b> are declared with <tt>&lt;param&gt;</tt> tags in the interface XML, and these are supplied in the BLD.INF file. The remaining parameters, '''GCC''', '''DEBUG''', and '''STRIP''' must be defined in the configuration.

The extension block is called '''buildprogram''' because that is the name declared in the <tt>&lt;interface&gt;</tt> tag in the interface XML. The <tt>.flm</tt> file itself can have a completely unrelated name if you wish.
= ==Example of FLM body ===
The following section contains some simple examples of FLM bodies that match the interface specification above. The include files define global constants and some GNU Make macros for common operations. For example, constants for host specific characters, macros to create output in a consistent manner, macros to create standard boilerplate code for creation of paths or cleanup, etc.

 # buildprogram.flm
 #
 # Copyright (c) 2007 Symbian Ltd. All rights reserved.
 #
 # Function Like Makefile (FLM)
 # Builds a simple program using the GNU Toolchain
 
 <i>define</i> <b>buildprogram1</b>
 
 <b>$(TARGET): $(SOURCEFILE)</b><i> | $(CREATABLEPATHS)</i>
          <i>$$(call startrule,</i><b>buildprogram2</b><i>) \</i>
          <b>$(GCC) -o $$@ $(if $(DEBUG),-g,) $(SOURCEFILE)</b> \
          <i>$$(call endrule,</i><b>buildprogram2</b><i>)</i>
 <i>endef</i>
 
 # Evaluate - expand all variables so that a unique rule is created.
 <i>$(eval $(call</i> <b>buildprogram1</b><i>))</i>
 
 ## Create paths -- you may add to the paths to be created here
 <i>$(eval $(call GenerateCreatablePathTargets,$(CREATABLEPATHS)))</i>
 ## Clean up
 <i>$(eval $(call GenerateStandardCleanTarget,</i><b>$(TARGET)</b> <i>$(CREATABLEPATHS)))</i>
 ## What targets -- declare the files produced here
 <i>$(eval $(call whatmacro,</i><b>$(TARGET)</b><i>))</i>

In the examples above and below, all the text in italics is common boilerplate code that deals with output, creating directories, and cleaning up make targets. The code in bold is the actual build target, which uses macros in order to make the FLM look more consistent.

Notes:
 *  note the names of the parameters from the XML file above appearing in the FLM
  *  <b>TARGET</b> and <b>SOURCEFILE</b> come from the BLD.INF's <tt>START EXTENSION buildprogram</tt> block
  *  <b>GCC</b> and <b>DEBUG</b> come from the configuration
   *  There is no essential reason why GCC and DEBUG could not be set in the BLD.INF file instead, but this is clearly not the intention
  *  You are permitted to use these four variables because you declared them in <tt>&lt;param&gt;</tt> tags your interface XML
  *  If any of these variables are defined neither in the BLD.INF file nor the configuration, the build will fail with an appropriate error
 *  <b>buildprogram1</b> is a completely arbitrary name
 *  <b>buildprogram2</b> is what this rule will be called in the build log
 *  <tt>CREATABLEPATHS</tt> contains a list of directories that will need to be created; you do this with the 'Create paths' line
 *  the <tt>whatmacro</tt> function call sometimes takes a second parameter. This was mainly for historical reasons, and can now usually be left out.

The following example shows how an FLM calls another FLM. In this example, the {{Icode|strippedprogram}} FLM removes all symbolic information from a binary that is built by the {{Icode|buildprogram}} FLM.

 # strippedprogram.flm
 #
 # Copyright (c) 2007 Symbian Ltd. All rights reserved.
 #
 # Function Like Makefile (FLM)
 # Builds a simple program using the GNU Toolchain and strips any symbolic information
 # (including debug info)
 
 <b>STRIPPEDTARGET=$(TARGET).strip</b>
 
 <i>define</i> <b>strippedprogram</b>
 
 <b>$(STRIPPEDTARGET): $(TARGET)</b> <i>| $(CREATABLEPATHS)</i>
         <i>$$(call startrule,</i><b>strip</b><i>) \</i>
         <b>$(STRIP) -o $$@ $(TARGET)</b> \
         <i>$$(call endrule,</i><b>strip</b><i>)</i>
 <i>endef</i>
 
 # Evaluate - expand all variables so that a unique rule is created.
 $(eval $(call strippedprogram))
 
 # Call the buildprogram FLM to ensure that the program is built
 <b>include buildprogram.flm</b>
 
 ## Create paths
 <i>$(eval $(call GenerateCreatablePathTargets,$(CREATABLEPATHS)))</i>
 ## Clean up
 <i>$(eval $(call GenerateStandardCleanTarget,</i><b>$(STRIPPEDTARGET)</b> <i>$(CREATABLEPATHS)))</i>
 ## What targets -- declare the files produced here
 <i>$(eval $(call whatmacro,</i><b>$(STRIPPEDTARGET)</b><i>))</i>

Because FLMs separate interface and implementation, it is possible to develop test code against the interface specification. This is done by creating test vectors for inputs and parameters using the interface specification. The FLM is called with the test vectors as input. The test checks whether the correct outputs have been produced, and whether the FLM invokes command line tools in the right sequence with the right parameters.

In terms of granularity, RAPTOR uses FLMs for parts of the build which are independent of each other, and as large as possible. For example, RAPTOR uses FLMs for building bitmaps from sources, and for building Symbian platform binaries such as DLLs and EXEs from sources.
= =Build configurations ==
Another key generalization in RAPTOR over [wiki:Glossary#SBSv1 SBSv1] is the build configuration. Build configurations are in essence vectors of (parameter, value) pairs that control the build. These (parameter, value) pairs provide the values for the parameters that are exposed by all the FLMs that are needed to perform a build.

Build configurations which provide global default values for non-transient FLM parameters are stored in XML files and called build configuration files. These files normally describe build configurations that are linked to a specific toolchain or target type such as the GCC, ARM or the WINSCW toolchains.

Most parameters that influence the build directly originate in FLMs, in other words, they are parameters that are explicitly used in the FLM body, such as {{Icode|$(DEBUG}}) in the example above. Some are indirect, such as environment variables that are required by a tool that is called from an FLM, such as {{icode|$RVCT22LIB}}, which is needed by the Real View Compiler. For this reason, build configuration files allow specification of dependencies on environment variables, optionally with default values. This enables RAPTOR to verify whether the build environment is complete, and return a concrete error should this not be the case, or provide sensible default values where appropriate.
= ==Maintaining build configuration files ===
Managing lists of (parameter, value) pairs is made easier in RAPTOR by using the following concepts.
=  =Grouping======
More complex build configurations can be constructed by grouping simple build configurations into a hierarchy. To enable this, it must be possible to name build configurations and use them in different combinations.
=  =Extending======
For compactness of representation and ease of maintenance, it is possible for a build configuration to “extend” one named build configuration. This is similar to derivation as used in object-oriented languages such as C++. 

{{Note|Note that multiple derivation is not supported, however, RAPTOR allows the concept of abstract build configurations.}}
=  =Inclusion======
Besides extension, inclusion can be used to group named build configurations into a new build configuration. Inclusion is used in RAPTOR for build configurations that are static, and often at the root of a hierarchy of build configurations. In some sense, inclusion is used to implement a simple form of multiple derivation (not supported by extensions) that avoids the problems of multiple inheritance.
= ==Variants ===
The concept of variants is central to RAPTOR. For the end-user, a variant is a different version of a build. For example, PAGED could be a variant of the standard ARMv5 build with Demand Paging functions turned on.

In general a variant is something which modifies a build. As discussed earlier, build configurations control the behaviour of a build by providing the parameters to the tools that are executed as part of the build process. Therefore, a variant of a build can be seen as a set of functions which change these parameters, or in other words, a set of functions that change build configurations.

Derivation of build configurations already allows overriding of values in the parent build configuration. By allowing the following operations in build configurations, build configurations can be used to describe changes to other build configurations:
 * appending a value to the end of a variable
 * inserting a value at the beginning of a variable
 * deleting a variable
 * list operations.

This means that a variant becomes a special type of a build configuration. Build configurations that define default values for build processes are not considered variants, while build configurations that change the default are considered variants. In practice, there is no real difference between a build configuration and a variant.
= ==Example of build configurations ===
The following example shows small pieces of the build configuration which implements the ARMv5 Build Target in SBSv1. The example shows also how derivation is used to create the UREL and UDEB variants of the ARMv5 build.

[wiki:File:Code1.jpg none]

{{Note|Note that the ARMv5 build configuration is abstract and therefore cannot be used directly by the user. Also note that it is not necessary that extension happens in-lined within the same XML file.}}
= ==Transient build configurations and variants ===
Build configuration files only describe non-transient build parameters in FLMs. Transient parameters, such as input and output files, are specific to a component, and therefore cannot be separated from components. Transient build parameters are generated as needed, based on information in input files such as MMP and {{icode|bld.inf}} files. They are stored within RAPTOR in the same data format as build configurations, though only in RAPTOR’s internal data model.

Some MMP file keywords such as {{Icode|OPTION}} and {{Icode|OPTION_REPLACE}} allow changing the default behaviour of builds. Changing the default behaviour of builds is equivalent to changing default variables as expressed in build configuration files. The changes to the default are translated into transient variants, in other words, build configurations that exist only in RAPTOR’s internal data model and modify default parameters.

The key difference between transient and non-transient build configurations, is that non-transient configurations are typically applied to all components in the system and stored in XML files, whereas transient build configurations are only applied to a part of the system (usually only individual components), and are stored in RAPTOR’s internal data model. When we talk about build configurations, we normally refer to non-transient configurations.
= ==Combining ===
RAPTOR allows the combining of two different trees of build configurations, in a similar way to the concept of “cross products” in linear algebra. The intention of this is to make it easy to apply variants to other variants or build configurations.

[wiki:File:Hierarchies.jpg 300px]<center>Two hierarchies of build configurations</center>[[BR]][[BR]]

In this example, let us assume the configuration ABC describes “ARMv5 UDEB” and “ARMv5 UREL”, and the configuration DEF describes the different feature sets “Demand Paging ON” and “Demand Paging OFF”. Combining the two variants gives the following graph:

[wiki:File:Hierarchies2.jpg center]<center>Combination of two hierarchies of build configurations</center>[[BR]][[BR]]

This approach enables the easy application of the variants “Demand Paging ON” and “Demand Paging OFF” on top of “ARMv5 UDEB” and “ARMv5 UREL”.
= ==Build configuration properties summarized ===
Build configurations are a generalized way of describing parameters for FLMs. Build configurations have been designed such that they are:
 * extensible by anybody in the ecosystem, without the need to change Symbian OS source code
 * easy to use
 * easy to maintain.

The reason for this is so that key users in the ecosystem are likely to want to adapt build configurations to their needs. It is also planned that build configurations replace some of the file formats in SBSv1, for example, BSF files.
= =Build specifications ==
RAPTOR uses build specifications in its internal data model to pull together all non-default information that is needed for a build. It does this in a form that easily allows the creation of large makefiles. Build specifications expose a hierarchy of build steps at different levels of granularity: at the top level they expose the hierarchical structure of the system (as defined in {{Icode|System_definition.xml}}), the hierarchical structure within {{Icode|bld.inf}} files (i.e. MMP files contained within {{Icode|bld.inf}} files), and the implicit hierarchical structures that are contained in MMP files. In other words, a build specification describes the hierarchy of the entire system, from the system definition, down to individual FLMs. In addition to this, each node in the hierarchy contains information that is relevant to it, such as transient build parameters. Or put more simply: build specifications describe what to build and how build parameters deviate from the default.

{{Note|Note that nodes in the hierarchy are called build specification nodes.}}

Currently, build specifications only exist in RAPTOR’s internal data model. However, in future Symbian OS releases, build specifications may become the main interface into the build tools for some use-cases. For example, an IDE may interface with the build specification rather than an MMP file.
= ==Interfaces ===
An important property of a build specification node is a reference to the FLM interface which defines the build process to be used to build the node. Some nodes are used purely for grouping and have no interface. All other nodes contain exactly one active interface.
= ==Transient build configurations / variants ====
The build specification also describes how build parameters deviate from the default for a given node. This includes the following two cases:
# Transient parameters for which no default values are sensible, such as source files.
# Parameters which are overridden for a particular target or component. An example is the {{Icode|OPTION}} keyword in MMP files, which can be used to change arguments that are passed to the compiler or linker.
<code text>
OPTION CW –w off
</code>

This example switches off warnings for all invocations of the CodeWarrior compiler for the component described by an MMP file.
In both cases, the parameters are represented using transient build configurations (which are also variants). This means that all parameters that are passed to FLMs for the build are simply calculated by finding the build configuration that describes the default values and applying all relevant variants to it in the right order. It does not matter whether the variant is a named build configuration or embedded in a build specification.
= ==Filters ===
The build specification tree can contain conditional elements, in other words, the build specification tree contains nodes and variants which only become active when used in conjunction with certain build configurations or variants.

This conditional structure is represented using filters. A filter is a “wrapper” around a set of nodes, or a set of variants, or an interface which makes statements such as
 * this part of the tree is only valid for configuration X [and optionally derived configurations]
 * this part of the tree is only valid for configurations containing variant Y
 * this part of the tree is not valid for configuration X or configurations containing variant Y.
Filters will have an “else” part (or an inverse), so you can specify “use this if the filter is satisfied” otherwise “use this if the filter is not satisfied”.

Multiple filters can be applied. Conditional parts of a build specification are valid (and thus in existence) if all the filters “surrounding it” are satisfied. This means that one build specification can describe a family of software products that is created from the same code base.
As mentioned earlier, a build specification node can have at most one active interface. This means that several interfaces may be defined for a node, but when all conditions are resolved, only one active interface is instantiated. Violation of this rule results in errors.
= ==Example of a build specification ===
The following example shows sections of a build specification that has been generated while building an example component in Symbian OS. Note that the example does not show filters.

[wiki:File:Code2.jpg none]

The example shows the hierarchy of build specification nodes that have been generated from a component described by a {{Icode|bld.inf}} file, and how variants (which are a form of build configuration) are used to describe parameters that are specific to the component. The other set of parameters are encoded in a build configuration, which are more global, and in this case are applied to all build specification nodes.

{{Note|Note that generally, paths are absolute in build specifications, which is a prerequisite to enable parallel and incremental builds (see later).}}
= ==Build specification properties summarized ===
Currently, build specifications are only machine-generated, and not intended for manipulation by end-users of RAPTOR. For this reason, not much consideration has been given to usability of the build specification file format.
= RAPTOR architecture =
RAPTOR is designed to create, maintain, and extend a high-level model of multiple builds. It uses this model to generate a hierarchy of {{Icode|makefiles}}. The generated makefiles are based on the concept of Function Like Makefiles, which extends on the concept of Template Extension Makefiles ([wiki:Glossary#TEM TEMs]) in SBSv1.

RAPTOR automatically constructs a complex makefile (containing a complete dependency tree) by combining prefabricated FLMs using simple “glue code” to connect them.
= =Architecture ==
The diagram below shows a schematic of a generic build system. A build is basically a file transformation process. A number of source files are translated, often iteratively, into a number of target files, which are the build outputs. The build system uses toolchains to create different products for different target platforms.

{{Note| Note that GNU Make has been chosen as it is a commonly used build language. Architecturally there is no reason why RAPTOR could not use a different build language.}}

[wiki:File:Generic_Build_model.jpg center]<center>Generic build model</center>[[BR]][[BR]]

In the diagram, the generic model does not use the exact definitions as given earlier. Instead, a build specification is used to describe “what to build”, while the build system configuration is used to describe “how to build”.
= =Encapsulation ==
One of the key problems with SBSv1 is that the original design did not clearly encapsulate functionality. This makes SBSv1 hard to use and maintain, inefficient to run, and hard to extend.

RAPTOR uses encapsulation rigorously and consists of only a few logical parts. This means very few parts of RAPTOR are complex. The following table decribes the complexity in RAPTOR in more detail.

{| Border="1"
|- style="background:#FDC82F" 
|<b>Element</b> || <b>Description</b>
|- style="background:white"
| RAPTOR front-end||The purpose of the RAPTOR front-end is to parse the meta-data input files ({{Icode|System_Definition.xml, bld.inf}} and MMP files) in the context of one or more Symbian OS versions and translate their structures into generic RAPTOR data structures.
Today a significant proportion of the complexity of RAPTOR is in the front-end. The front-end handles all the special casing and the pre-processor directives in {{Icode|bld.inf}} and MMP files. All the complexity that has been built over time in SBSv1 is carried over into the RAPTOR front-end, and related processing is explicit in one place.
|-style="background:white"
| RAPTOR data model|| 
The RAPTOR data model represents the following generic concepts and their relationships:
 * Build configuration – defines the default arguments that are passed to individual elements of the FLM library.
 * Build specification – defines what to build, and deviations from the default.
 * FLM library – a library whose elements encapsulate how to translate input files into built artefacts up to the last level of detail.
The data model has been designed so that it is generic and independent of the front-end and can be represented in text form (XML).
If Symbian were to deprecate {{Icode|bld.inf}} and MMP files at some point in future, this would remove the need for complex processing in the front-end.
|-style="background:white"
|Function Like Makefiles (FLMs)||This is an individual element of the FLM library, which encapsulates how a set of input files is translated into a set of output files. FLMs are implemented in GNU Make notation in RAPTOR. However they could be implemented in any “language” that is used to build applications.
FLMs contain most of the complexity within the build system.
|-style="background:white"
|RAPTOR back-end||The RAPTOR back-end generates a hierarchy of makefiles from the data model. It does this by combining FLMs to a larger makefile and organizing information that is provided in build specifications and build configurations in the correct FLM.
Make engine
The make engine is the vehicle that is used to perform the actual build. RAPTOR supports all make engines that fully support the GNU Make file format, such as GNU Make, PVMgMake, and eMake (from Electric Cloud).
|}
= =Flowchart ==
The flowchart below illustrates the basic data-flows in RAPTOR. The key components (the front-end, the data model and the back-end) have been described above. RAPTOR constructs build specification from files that SBSv1 or other Symbian tools have introduced in the past. These files describe

 * the system via the {{Icode|System_definition.xml}} file
 * components via {{Icode|bld.inf}} files
 * executables via MMP files.

RAPTOR does this to be as compatible with SBSv1 as possible. However, in future releases, RAPTOR may be able to consume new file formats, should this be necessary. The RAPTOR architecture makes it possible to replace {{Icode|bld.inf}} and MMP files, enabling a gradual migration from SBSv1 file formats to new formats. 

{{Note|Note that in principle RAPTOR can support different descriptions of build files in parallel. Further note that some of the SBSv1 file formats that are used rarely, such as BSF files, will not be implemented by RAPTOR.}}
[wiki:File:Basic_data_flows_in_RAPTOR.jpg center]

{{Note|Note that RAPTOR itself does not perform the actual build, it produces makefiles and drives a make engine (such as GNU Make, PVM Gmake, or EMake from Electric Cloud) which runs the build. The top half of the figure shows the key elements of RAPTOR, while the bottom half of the figure illustrates the part of the process driven by the make engine.}}
= =Framework ==
RAPTOR itself is implemented as an extensible framework, as illustrated below. The framework and all but the make engine are implemented in Python8. There are three main ways to drive RAPTOR:
# Directly from the RAPTOR command-line.
# Indirectly from the ABLD command-line which provides compatibility with SBSv1.
# Directly from an IDE using the RAPTOR API. An IDE could also drive RAPTOR via the command-line, rather than using the API.
[[BR]][wiki:File:Raptor_framework.jpg center][[BR]]<center>RAPTOR framework</center>[[BR]][[BR]]

The RAPTOR Framework exposes a plug-in architecture that allows the loading of different plug-ins to support alternative command line interfaces, input file formats, and make engines. The framework is configured using an XML file – the {{Icode|init.xml}} or set-up file. File parser plug-ins are used to process Symbian OS specific file formats such as MMP files. Core RAPTOR functionality is exposed through the RAPTOR API which can be used to drive RAPTOR from an IDE.
= ==Set-up file ===
The root directory of RAPTOR ({{Icode|$RAPTOR_HOME}}) contains the RAPTOR initialization file ({{Icode|init.xml}}) which controls the default behaviour of RAPTOR. The file specifies locations of plug-ins, locations for configuration files such as build specifications and the FLM library, and other defaults, for example, the default build configuration and the default system definition.
The following example shows a RAPTOR initialization file.

[wiki:File:Code3.jpg none]
= ==Command-line ===
The primary way to drive RAPTOR is the command line. There are two scripts in the root directory of RAPTOR for launching the RAPTOR executable and passing it the correct arguments:
 * {{Icode|sbs}} for Linux
 * {{Icode|sbs.bat}} for Windows.
= ==Plug-ins ===
RAPTOR supports several types of plug-ins:
 * parsers for SBSv1 files
 * command-line interpreters
 * make engine drivers.
 * log file parsers

These plug-ins may require customization by licensees or replacement at a later date. For this reason, they have been isolated by clearly defining an interface between the plug-ins and the main RAPTOR code.
= ==APIs ===
RAPTOR is implemented in Python, which is an object-oriented scripting language. The framework, plug-ins and data model can all be accessed directly using the public APIs of the objects which represent them. Common functionality is hidden behind the RAPTOR API.
= =Parallelization and make engines ==
One of the key features of RAPTOR is its support of parallel building on appropriate hardware. As RAPTOR relies on a third party make engine for parallelization, its parallelization capabilities are “inherited” from the make engine. The GNU Make 3.81 standard was chosen because it provides the most options with regards to parallelization on different hardware platforms. The make engines that comply with the GNU Make 3.81 specification are listed below.

{| Border="1"
|- style="background:#FDC82F" 
|<b>Make engine</b> || <b>Main user</b> || <b>Linux</b> || <b>Windows</b>|| <b>Tested by Symbian</b>
|- style="background:white"
| GNU Make|| Developer || Yes|| Yes|| Windows and Linux
GNU Make is tested in single CPU and multi-CPU mode (using the –j option)
|-style="background:white"
| PVM GMake (open source) || Build Team||Yes|| No || Linux
|-style="background:white"
| Electric Accelerator || Build Team|| Yes|| yes || Windows and Linux
|}
= ==Electric Accelerator features ===
Electric Accelerator is the most comprehensive make engine in the table above, and provides the range of features listed below.
 * A caching file system.
 * The capability to fix dependency trees that are incomplete or otherwise broken. This feature will help in situations where a large amount of the build is performed from within extension’s makefiles, for example, third party Java code.
 * The capability to create a large dependency tree from smaller disjointed individual trees (representing individual makefiles). Again this feature will help with extensions.
 * Load balancing capabilities, which lead to increased performance by taking the time it took to build individual artefacts into account in subsequent build runs.
 * Additional analysis and build management tools.
 * Fail safety and redundancy, in other words, the build will complete even if hardware or software on the build cluster fails.
 * The capability to manage the software that is installed on nodes within the cluster using virtualization.
= =Properties of generated makefile hierarchy ==
To enable parallelization on all the make engines listed above, makefiles generated by RAPTOR must have the following key properties.
 * The makefiles must encode a complete and correct dependency tree. Without a complete and correct tree, parallel builds can fail randomly. Generally, RAPTOR achieves this without changes to source files, and deduces dependencies from various information sources in the build. However, in some rare cases it is necessary to augment MMP files with additional dependency information by using the {{Icode|DEPEND}} keyword (see section 6 for more detail). Also note that extensions to RAPTOR using the Template Extension Makefile mechanism may lead to incomplete or incorrect dependency trees if the extension is encoded incorrectly. As TEMs were originally developed by most of Symbian’s customers using SBSv1, where correct dependency trees were not required, dependency issues with TEMs written for SBSv1 are common. Due to RAPTOR’s design, missing dependencies in TEMs will not affect parallel builds, but can affect the correctness of incremental builds.
 * One large makefile must be generated, except in some situations, such as for SBSv1 template extension makefiles that are supported by RAPTOR.
 * All build artefacts must be unique and must use absolute paths.
Besides enabling parallel builds, these makefile properties are also sufficient to enable incremental builds.
= Platforms and setup =
The following section gives a brief overview of the test set-ups that Symbian is using.
= =Windows ==
Symbian uses a HP XW 4400 with the following specifications for individual team builds:
 * dual-core Pentium CPU, 3.4Ghz
 * 2GB RAM
 * 160 GB HDD.
Symbian uses a HP ProLiant DL 585 with the following specifications for system builds:
 * four dual-core AMD Opteron 875 CPUs, 2.2 GHz
 * 8GB RAM.

RAPTOR is tested for functional completeness on both machines using GNU Make without –j. However, only a few test runs with –j will be performed to assess performance.

The reason for not focussing performance testing on Windows is that file system performance on Windows is significantly worse than on Linux (based on earlier studies), but the Electric Accelerator caching file system addresses this.
= =Linux ==
Symbian uses an HP blade cluster with the following specifications:
 * As head node, a HP ProLiant DL380 G5 Server with 3GHz dual-core Xeon 5160 processors, with 2GB RAM, and 700GB storage.
 * An 8 dual-core HP ProLiant BL465c 2220 DC (1P) with 2.8 GHz AMD Opteron 2220 processors, with 4GB RAM, and 80GB storage.
 * An 8 quad-core HP Quad Core Intel 5355 Blade Server (1P) with 2.66GHz Intel Xeon 5355 processors, with 4GB RAM, and 80GB storage.
RAPTOR is tested for performance primarily with PVM and PVM GMake, and secondarily with GNU Make –j. The head node is not used for builds.

Symbian chose a mixed machine set-up, to be able to identify the optimal machine configuration, and determine whether dual-core processors are better than quad-core processors for RAPTOR, even though this introduces complexities for some performance measurements.
= =Electric Accelerator ==
Compliance and performance testing with Electric Accelerator will be performed in partnership with Electric Cloud. Data will only be made available on demand on a case-by-case basis. The reason for this is that Symbian platform licensees’ build environments are significantly more complex than Symbian’s internal build environment. For example, the number and size of build operations performed in extension makefiles is minimal within Symbian’s code base, but can be large for licensees, for example, Java code.
= =Pitfalls in machine setup ==
Symbian experienced various problems with parallel test runs at various points during the development cycle.
= ==Samba and PVM GMake ===
During early development, Samba was used to work around filename case issues on Linux. This approach had worked for test runs without PVM. Test runs using PVM GMake failed due to Samba “disappearing” when PVM GMake was run.
= ==License servers ===
When Symbian started testing RAPTOR, it had significant issues with FlexLM and RVCT, which limited performance testing on the Linux Blade clusters. Symbian has a policy of using floating licenses for most tools and it is difficult to get node locked licenses. The recommendation for RAPTOR is to use node locked RVCT licenses, or to run a license server on the cluster.

The issues appear in random build failures due to too many license requests to the license server in a short period of time, and as a result, RVCT cannot obtaining a license. Using re-try options helps but does not solve the problem, and the problem gets worse with the number of processors that are used during a build, which clearly indicates a bandwidth issue.
= Scalability and performance == =Amdahl’s and Gustafson's law ==
Two mathematical laws govern scalability in parallel computing
# Amdahl’s law, which deals with the relationship between the number of processors and the speedup that can achieved on a parallel system, while keeping the problem size constant.
# Gustafson’s law which looks at the speedup one can achieve on a parallel system, assuming that the problem size grows with the size of the parallel system.

Both laws are relevant for predicting and measuring the scalability of RAPTOR on parallel build clusters and for this reason, are stated in some detail in this document.
= ==Amdahl’s law ===
Amdahl’s law is used in parallel computing to predict the theoretical maximum speedup of a problem. The speedup S is defined as wall-clock time of best serial execution divided by the wall-clock time of parallel execution.

For parallel problems, Amdahl’s law states that if F is the percentage of a calculation that is sequential (also called the serial fraction, or the fraction of a computation that cannot benefit from parallelization), and (1 − F) is the fraction that can be parallelized (also called the parallel fraction), then the maximum speedup that can be achieved by using N processors is:

[wiki:File:Math.jpg center]

Where we have set a total time of F + (1 − F) = 1 for algebraic simplicity. For large systems, this is an extremely steep function near F = 0. At the limit, as N moves towards infinity, the maximum speedup moves towards 1/F. In fact the graph implies that very few problems will experience even a 100-fold speedup, as only very few problems will have a sufficiently small serial fraction.

[wiki:File:speedup_under_amdals_law.jpg center]

The law contains the implicit assumption that the serial fraction F of a problem is independent of the number of processors N, which is virtually never the case. One does not take a fixed-size problem and run it on various numbers of processors except when doing academic research. In practice, the problem size increases with the number of processors. Amdahl’s law is also problematic as it is difficult to estimate the serial fraction F of a problem.
= ==Gustafson’s law ===
Gustafson’s law governs the behavior of “sufficiently” large problems which are parallelized. It addresses the short-falls of Amdahl’s law. The key difference is that the serial fraction of a problem is not considered independent of the size N of the parallel computer on which the problem is solved. It is also a function of the problem size n.

[wiki:File:math2.jpg center]

The serial fraction F(n) is also called serial function. Assuming that the serial function diminishes with growing problem size, the speedups approaches the maximum speedup that can be achieved on a particular parallel computer. In practice this means that if we can show that the serial function of a problem decreases with the problem size n, we can prove that throwing more processing power at the problem will lead to increasing speedups.
= =I/O bottlenecks ==
I/O throughput is likely to be a key factor in limiting the scalability when parallelizing builds. Bottlenecks may be caused by the following factors:
 * the performance of the network for I/O operations that use NFS
 * the speed of reading from, and writing to disks.
Both of these factors can contribute to the serial fraction of the problem size and are parameters that can be changed (up to a degree) by choosing build hardware with faster disks, or a faster network.
= =Core fraction of the build ==
The time it takes RAPTOR to create makefiles from input files is called the core fraction of the build. The core fraction is executed serially on one CPU. The actual building (in other words, execution of make) can be performed in parallel. The overall build time is the sum of the two times.

Currently Symbian has no plans to parallelize the core fraction of the build, but may choose to do so in future.
= =Performance analysis ==
This section contains RAPTOR performance measurements.
= =Baseline: comparison on a single Windows processor ==
This section compares RAPTOR against SBSv1 on a single processor (not using hyper-threading). This comparison is only available on Windows and has been performed on a standard HP XW 4400 desktop machine with a 3.4 GHz processor. The table shows measurements for a single component, which in this case is {{Icode|multimedia_mmf}}.
{| Border="1"
|- style="background:#FDC82F" 
|<b> </b> || <b>SBSv1</b> || <b>RAPTOR</b>
|- style="background:white"
| Run 1|| 4.6 minutes || 4.0 minutes
|-style="background:white"
| Run 2 || 4.9 minutes|| 4.0 minutes
|- style="background:white"
| Run 3|| 4.8 minutes || 3.9 minutes
|- style="background:white"
| Average|| 4.8 minutes || 4.0 minutes
|}

Without exploiting parallelization, RAPTOR is approximately 20% faster than SBSv1. Other components show similar performance improvements.

We have not performed a wide range of performance tests on single processor machines, which may mean that the measurements are not valid for a growing problem size.
= ==Baseline: multiple processor build using SBSv1 ===
The complete Symbian OS v9.5 build time on a 4 dual-core 2.8Ghz AMD 64 processor, with 8GB RAM, using Windows, is 116 minutes. This time includes the following build configurations: ARMv5 UREL, ARMv5 UDEB and WINSCW UDEB. Note that these are slightly faster specifications than the ones defined in section 4.1, to allow direct comparison with builds performed on the Linux cluster. Note that due to its architecture SBSv1 does not scale beyond 8 CPUs.
= ==RAPTOR measurements on Linux ====  =Test series: constant code size with growing machine size======
The measurements covered in this section are for a complete Symbian OS v9.5 build (ARMv5 UREL, ARMv5 UDEB and WINSCW UDEB) using RAPTOR while increasing the number of CPUs on the Linux build cluster.

The tests shown below do not show the usage of hyper-threading on individual CPU cores during the build, as previous tests have not shown any benefits. Hyper-threading means that several artifacts are built on one core at the same time.

The tests have been performed by configuring the cluster with different hard-disk setups: standard (no [wiki:Glossary#RAID RAID]) and data striping (or [wiki:Glossary#RAID_0 RAID 0]). I/O performance for the latter is higher than in the standard setup, which allows us to see the impact of different disk performance on the build.

The following graph shows the SBSv1 baseline on eight CPUs, and two series of tests using different disk arrays. The tests exclude the core fraction of the build, which in this case is 8 minutes. 

[wiki:File:no_of_processors.jpg center]
<center> ARMv5 (UREL and UDEB) and WINSCW build time for Symbian OSv9.5 on a Linux blade cluster</center>[[BR]][[BR]]

As the problem size is fixed, we are seeing the effects of Amdahl’s law, and the diminishing returns for a larger number of CPUs, as expected. Analysis of the build times shows that in our hardware set-up, I/O performance (in this case the disk speed) is the bottleneck:
 * A faster disk increases the performance of the build by 18% (No RAID vs. RAID 0).
 * For I/O intensive build steps such as linkage, individual CPUs generally wait for disk operations.
 * Build configurations which require fewer disk accesses are faster than build configurations which require more disk accesses. It takes five minutes to perform an ARMv5 UREL build, 10 minutes to perform a WINSCW UDEB build, and 15 minutes to perform an ARMv5 UDEB build on 46 CPUs (no RAID). This agrees with an increased I/O wait proportion for more I/O intensive build configurations. The difference between the various build configurations is the amount of debug information that is generated by the compiler, and consequently has to be read by other tools such as the linker.

In the first release of RAPTOR, no optimization opportunities beyond the use of parallel make engines have been used. All disk operations in RAPTOR are performed via NFS. However, analysis has shown that there is plenty of room for future optimizations in hardware and software:
=  =Hardware======
 * higher performing disks and disk controllers
 * faster [wiki:Glossary#NIC NICs]
 * RAM disks.
=  =Software======
 * more node-local operations to reduce I/O traffic
 * specific optimizations for build acceleration tools such as Electric Accelerator. Symbian will work with Electric Cloud to explore and implement such optimisations in future.
=  =Test series: growing code size with constant machine size======
We ran a series of tests in which we increased the problem size while keeping the machine processing size constant. Using the Symbian OS source code as the basic unit of “code size”, five builds were performed, each one containing a multiple of the amount of code in Symbian OS (in other words, build 1 = 1 x Symbian OS, build 2 = 2 x Symbian OS, … , build 5 = 5 x Symbian OS). The size of the cluster and the number of allowed parallel tasks were constant throughout (28 CPUs and 28 tasks).

RAPTOR was used to create one makefile for a single build of the Symbian OS source code. Five copies of this makefile were created and the copies were adjusted so that the targets for each makefile would be created in different locations. A wrapper makefile was created that included these manually modified makefiles13. This approach ensured that all targets in the makefile were treated as if they were different. The following graph shows the increase in build time, which as expected, is nearly linear. 

[wiki:File:source_code_multiplayer.jpg center] <center>Build time vs. growing source base</center>[[BR]][[BR]]

This indicates that for five times the size of the Symbian OS source code, we are not exposed to any additional hardware bottlenecks.
= ==Conclusions ===
We have shown that it is possible to build Symbian platform in approximately 30 minutes (including the core fraction of the build), and customer builds are likely to experience similar performance increases, depending on the size of their code base. There is also significant potential for further optimization depending on the hardware and software used.
= =The performance impacts of extensions to RAPTOR ==
Extensions to RAPTOR enable Symbian’s customer to add build steps that are not supported by the standard version RAPTOR. RAPTOR supports two different extension mechanisms:
 * Template Extension Makefiles (also supported by SBSv1)
 * Function Like Makefiles.
Symbian cannot guarantee that build extensions to RAPTOR encode complete and correct dependency information.
= ==Template Extension Makefiles ===
TEMs are supported in RAPTOR to allow Symbian’s customers to smoothly migrate their code bases to RAPTOR. Customer code bases will have a significant number of TEMs in their code base. RAPTOR cannot parallelize extensions that use TEMs: they are executed using nested calls to the make engine on individual CPUs to guarantee the correctness of the build. If a large proportion of the build is encoded using TEMs, RAPTOR cannot realize its parallelization potential in extensions. If large components (for example, an implementation of Java) are integrated into a RAPTOR build using TEMs, the overall build time is limited by the time it takes to build these large components.

Make engines such as Electric Accelerator are designed to resolve such issues by correcting missing or incorrect dependencies in TEMs, and by overcoming the boundaries that are introduced by nested calls to make engines. The performance of RAPTOR will increase significantly in such situations.
= ==Function Like Makefiles ===
FLMs are designed to overcome the limitations of TEMs. However, they require the migration of build extensions to a new framework. For RAPTOR to work correctly in parallel and incremental build situations, FLMs also need to capture all dependencies correctly. Depending on the amount of extensions needed in a customer environment, migrating extensions to FLMs may require a significant amount of effort. In addition to this, in some situations it may not be practical to use FLMs instead of TEMs. Examples may be situations where a third party code base with incorrect dependency information is integrated into a Symbian platform build.
= Benefits == =Short-term benefits ==
The following benefits are available in initial releases of RAPTOR.
= =Incremental builds (speed) ==
Because RAPTOR generates complete and correct dependency trees, RAPTOR will be able to support incremental builds. Incremental builds lead to improved build performance because, only a subset of files in the system need to be re-built.

Both developers and system integrators will benefit from incremental builds. We do however expect that incremental builds will be used mainly by developers.
= ==Parallel builds (speed) ===
The key benefit of RAPTOR is in enabling fast parallel builds on different hardware platforms. The system is primarily designed to benefit system integrators (in other words, those using automated build systems), but will also benefit individual developers that can schedule builds on centrally-managed parallel build hardware through appropriate web interfaces, or interfaces in the IDE (neither are supplied by Symbian).
= ==More flexibility ===
A key benefit of RAPTOR over SBSv1 is the flexibility achieved through powerful abstractions that enable extensibility in the following areas:
 * The ability to modify properties of the build by extending build configurations (arguments that control the build) in different ways.
 * The ability to extend the core of the build system by extending the FLM library.
 * New ways to interact with the build system, such as the ability to address and build objects in the system model.
Both developers and system integrators will benefit from the extra flexibility that RAPTOR provides. Initial releases of RAPTOR provide significantly more flexibility than SBSv1. However, the need for backwards compatibility limits the flexibility a little, for example, it is not possible today to extend the build file formats, such as MMP files, or define your own formats. It should be noted however, RAPTOR’s architecture allows Symbian to implement such functionality in future should customers require such extensibility.
= =Mid-term benefits ==
In the future, Symbian can deliver additional benefits by building on top of the concepts that the initial release of RAPTOR introduces.
= ==Integration into IDEs ===
RAPTOR is designed to allow easier integration of build functionality into IDEs. It does this by using the following architectural concepts:
 * The RAPTOR API allows an Eclipse-based IDE to interact with RAPTOR. Large parts of RAPTOR are implemented in Python (and not in Java, as Eclipse is), which makes it possible to use Python implementations such as JPython or Jython, that seamlessly integrate with Java, and as a result, integrate with Eclipse1.
 * The concept of RAPTOR build configurations (arguments that control the build) conceptually maps directly onto the concept of describing build settings in IDEs.
 * Improved machine-readable logging formats that can be processed easily by IDEs.
= ==Product-line engineering in production environments ===
Product-line engineering is a method that creates an underlying architecture of an organization’s product platform. It provides an architecture that is based on commonality and similarity. Different product variants can be derived from the basic product family, which creates the opportunity to reuse and differentiate products in the family. Currently, during mobile phone production, software product-line engineering takes several forms:
 * The creation of software variants by compiling the same source code into different sets of variants.
 * A strong component model that allows the assembly of a product from different components.
 * The managment of software variants through different settings and other run-time configuration mechanisms. Note that most run-time configuration mechanisms can be seen as a generalized form of settings.

Symbian OS has supported functionality that enables variant creation in various forms for some time, particularly through strong feature and configuration management. The RAPTOR concepts of build configurations, variants, and filters in build specifications map to, and interact directly with existing concepts in Symbian OS. This means, with RAPTOR builds, it is possible to create and integrate systems that describe and manage software configurations centrally. Such systems would generate RAPTOR build configurations or variants automatically, which can then be applied to RAPTOR builds.

Managing settings is an area which is less established in Symbian OS, but is conceptually similar to build configurations. In a general sense, settings are no different to vectors of (parameter, value) pairs that are encoded in different data formats. This means that systems that manage settings for phone configurations are conceptually similar to systems that manage software configurations, which again are conceptually similar to build configurations. Settings management systems could generate settings files or repositories in different binary formats automatically, which in turn could be fed into RAPTOR through generated build configurations or build specifications. The latter can be achieved by using the RAPTOR API, which could be used to inject build artefacts into RAPTOR builds.

All file formats that RAPTOR has introduced are XML, in order to allow easy machine generation of data files such as build configurations.
= ==Integrating other phone software production use-cases ===
The generic concepts of FLMs, FLM libraries, build specifications, and variants introduced by RAPTOR allow other tools that are part of the software production process to be migrated into the RAPTOR front-end. This allows the use of the hardware, and as a result, the use of parallelization capabilities that RAPTOR introduces for non-build use-cases that are important during phone software production. It also enables Symbian customers who use Electric Accelerator to make use of Electric Accelerator for these use-cases.

Examples of such integrations are as follows.
 * Static analysis tools can be integrated by extending FLMs (or adding additional FLMs) and build configurations.
 * Tools for checking properties of the code base, such as CDB and AURA, can be integrated by adding additional FLMs and build configurations to RAPTOR.
 * ROM building can be supported by adding additional FLMs and build configurations to RAPTOR.
 * Delivery tools, such as the CBR tools (in particular, the generation of CBR archives after a build), can be integrated into RAPTOR by adding additional FLMs and build configurations.
This requires that these tools are available on the host platform on which RAPTOR is run.

{{Note|Note that initial release versions of RAPTOR will not provide these capabilities. However, the RAPTOR architecture enables Symbian to support such use-cases in future.}}
= Migration to RAPTOR == =Steps taken to ease migration ==
The following steps have been taken to make migration to RAPTOR as easy as possible.
= ==Backwards compatibility ===
RAPTOR is compatible with the interfaces of SBSv1, {{Icode|bld.inf}} files and MMP files are retained, as are the {{Icode|bldmake}} and abld commands. These commands become proxies which pass the appropriate arguments to RAPTOR. It is expected that SBSv1 will be used alongside RAPTOR for approximately 12-18 months, with users gradually migrating to RAPTOR as they require increased performance and new features. Once RAPTOR is released, no new features will be added to SBSv1, although it will be maintained for up to 2 years.
= ==Binary equivalence ===
We have also implemented binary equivalence in RAPTOR, meaning that building source code with SBSv1 and RAPTOR on any platform will result in the same end-product.
= =What needs to be done to migrate to RAPTOR ==
The following differences between RAPTOR and SBSv1 are likely to affect many of Symbian’s customers, and will need to be addressed before RAPTOR can be used.
= ==Migrations for all customers ====  =Build scripts======
This section is applicable if you have build scripts that wrap SBSv1. This migration only applies for system builds, not for component builds.
To make use of the full parallel build capability of RAPTOR it is necessary to use the {{Icode|system_definition.xml}} file which describes the components that are used in a build. Without this file, RAPTOR does not know which components constitute your system and thus cannot generate a makefile that contains a complete dependency tree. Note that RAPTOR only needs the {{Icode|<systemModel>}} section of the file. RAPTOR ignores the {{Icode|<build>}} part of the system definition which is used by a wrapper script available with SBSv1.

In order to migrate, modify the build scripts so that they use RAPTOR with the {{Icode|system_definition.xml}} file. 

{{Note|Note that using the ABLD compatibility layer does not give you full parallel build capability.}}
=  =BR.1968 RAPTOR produces a different logging output======
This section is applicable if you use tools which parse the output that SBSv1 produces.
RAPTOR produces a different logging output from the current build system. The output has been designed to be easily parseable by tools such as an IDE, and to avoid corruptions of logs, as is often seen in distributed execution environments. The following example shows a small part of a RAPTOR log.

[wiki:File:code4.jpg none]

The logging output is supported by the Symbian log summary tools, meaning that tools based on these, using the summary output, will not be affected.

Any tools that rely on the log output that have been developed outside of Symbian may need to be modified to support the new log format.
=  =Missing dependencies======
This section is applicable if your build breaks because of missing dependencies that RAPTOR cannot deduce.
In some rare circumstances RAPTOR cannot automatically deduce dependencies between individual files, for example header files that are generated during resource creation and used by source files.

In Symbian’s code base there have been approximately 50 instances of this problem, where one generated resource header file is used in 50 source files.

In order to migrate, dependencies in MMP files will need to be specified using the DEPEND keyword. This keyword has also been added to SBSv1. For convenience, a global list of dependencies has been introduced to avoid having to change individual MMP files.
= ==Migrations that apply to customers that use legacy SBSv1 functionality ====  =Extension makefiles======
This section is applicable if you are using GNU or NMake extension makefiles.

RAPTOR does not support GNU or NMake extension makefiles. These have to be ported to TEMs or FLMs The reason for not supporting these extension types is that TEMs have been introduced to promote more re-use of build patterns in build system extensions, which is something that GNU and NMake extension makefiles do not provide. GNU and NMake extension makefiles encourage the user to copy and paste (resulting in long-term maintenance issues), while TEMs encourage code re-use in build extensions.

For information on migration, run a search on “Symbian OS v9.3 new build system features” in the Symbian Developer Library, and see the RAPTOR documentation.
=  =ABIv2======
This section is applicable if you are building your code base in ABIv1 mode.
RAPTOR does not support compiling code in ABIv1 mode. Further note that future compiler versions, RVCT v3.x for example, do not support compilation in ABIv1 mode.

To switch to ABIv2 mode, edit the {{Icode|variant.cfg}} located at {{Icode|epoc32\tools\variant}} and add the macro {{Icode|ENABLE_ABIV2_MODE}}. For more information, run a search on “How to switch to ABIv2 mode” in the Symbian Developer Library.

{{Note|Note that RVCT is stricter when using the ABIv2 mode and consequently some source changes need to be made. The changes typically fall into the following problem categories:
 * mismatches between exports and imports
 * fixing of incorrect DEF files which are a consequence of erroneous mismatches, which compilers accepted in ABIv1 mode.}}
=  =Old build platforms======
This section is applicable if you depend on legacy build platforms and want to use RAPTOR.

RAPTOR does not support some target platforms that SBSv1 supported. Symbian has no plans to support the following legacy target platforms:
 * ARMv4, ARMv4T, VS6, VS2003, WINS, X86, Thumb, ARMvI.
 * Note that the first released version of RAPTOR does not support ARMv5 ABIv1 builds, but support will be added in the future.
External code using these target platforms will not build without creating additional build configurations, or in some cases additional FLMs for RAPTOR.

Licensees will be able to create their own target platform configurations and FLMs using documentation provided with RAPTOR.
=  =BR.1967 RAPTOR does not use BSF files======
This section applies if you are using BSF files in SBSv1.

The current build system allows BSF files to be placed in {{Icode|/epoc32/tools}} to create new target platforms, by extending other target platforms. The new build system will not support this mechanism, so third-party tools requiring extra platforms in BSF files will break.
In order to help with migration, a tool will be provided to translate existing BSF files into a build specification that is required by RAPTOR. However, until a tool is provided it is possible to define build specifications manually. The following example shows a build specification for an ARMv6 build.



= Raptor Command Line Reference =

== Command-line reference ==

Raptor command-line usage is as follows:

{{{
    sbs [target] [-c configuration] [other options]
}}}

Help is available by typing {{{sbs --help}}}.

== Targets ==

The table below lists the available targets; If no target is specified, {{{export}}}, {{{library}}}, {{{resource}}}, {{{target}}} and {{{final}}} are all applied.

Multiple targets can be defined, for example {{{sbs export resource target}}}. However, combining {{{clean}}}, {{{cleanexport}}} or {{{reallyclean}}} with another target may produce unpredictable results, and so is not recommended.

||= Target =||= Meaning =||
|| {{{export}}} || Copies exported files to destinations ||
|| {{{library}}} || Creates import libraries from frozen {{{.def}}} files ||
|| {{{resource}}} || Creates resource files and AIFs ||
|| {{{target}}} || Creates main executables ||
|| {{{final}}} || Allows legacy extension makefiles to execute final commands ||
|| {{{bitmap}}} || Creates bitmap files [TODO more explanation need] ||
|| {{{cleanexport}}} || Removes exported files ||
|| {{{clean}}} || Removes built files and intermediates, but not exported files ||
|| {{{reallyclean}}} || Same as {{{clean}}} but also removes exported files ||
|| {{{freeze}}} || Freezes exported functions into the {{{.def}}} files. See also the {{{remove_freeze}}} variant ||
|| {{{listing}}} || Creates assembler listing {{{.lst}}} files alongside all the source files specified. Each file is named {{{<source-file-name>.<build-paltform>.<build-variant>.<project>.<targettype>.lst}}}. Remove these files with {{{sbs clean listing}}}. ||
|| {{{preprocess}}} || Creates preprocessor output {{{.pre}}} files alongside all the source files specified. Each file is named {{{<source-file-name>.<build-paltform>.<build-variant>.<project>.<targettype>.pre}}}. Remove these files with {{{sbs clean preprocess}}}. Note that dependencies are not resolved in a {{{preprocess}}} build, so you may have to do a normal build first. ||
|| {{{romfile}}} || Creates an {{{.iby}}} file to be included in a ROM ||
|| {{{--what}}} || List files created by the build ||


==  Configurations (Variants and Aliases)  ==

A configuration is composed of a number of dot-separated list of ''variants'' applied, one after another, to the default configuration. If two variants alter the same setting, the latest variant in the list overrides any earlier attempt to set that setting.

For example, the following configuration specifies that the basic instruction set to be built is {{{arm}}}, that the architecture is {{{v5}}}, that the release version is to be built and that the compiler version to use is RVCT 2.2:

{{{
    sbs -c arm.v5.urel.rvct2_2
}}}

A configuration can also be specified by an [wiki:#Useful_Aliases alias]; this is a short, friendly name for a list of variants. For example, the {{{armv5_urel}}} alias is the same as the above configuration (RVCT 2.2 is the default compiler unless you specify otherwise in your kit.)

{{{
    sbs -c armv5_urel
}}}


Cleaning does not require a configuration [TODO does supplying a configuration have an effect?]

Multiple configurations can be supplied and all configurations will be built simultaneously, for example:

{{{
    sbs -c armv5 -c armv5.test
}}}

If multiple configurations and multiple targets are provided on the same command, all combinations of target and configuration will be built, regardless of the order of options given. For example:

{{{
    sbs resource -c armv5 target -c armv5.test
}}}

is equivalent to:

{{{
    sbs resource target -c armv5 -c armv5.test
}}}

Both perform the {{{resource}}} and {{{target}}} steps for {{{armv5}}} test and release code.

== Useful Variants ==

||= Variant =||= Meaning =||
|| {{{trace}}} || Turns on Trace Compiler (if you have it installed) ||
|| {{{test}}} || Builds test code, disables building of production code ||
|| {{{savespace}}} || Removes all intermediate files [TODO such as?] ||
|| {{{bfc}}} || Skips dependency inclusion; only correct if building from clean; may be necessary to make a large build complete in available memory[TODO how is this different from --no-depend-include?] ||
|| {{{smp}}} || Builds SMP (meaningful for Kernel-side code only) [TODO ?] ||
|| {{{rvct2_2}}} || Forces use of RVCT 2.2 compiler ||
|| {{{rvct3_1}}} || Forces use of RVCT 3.1 compiler ||
|| {{{rvct4_0}}} || Forces use of RVCT 4.0 compiler ||
|| {{{gcce4_3_2}}} || Forces use of GCCE 4.3.2 compiler. Note that this builds binaries to the same location as RVCT ||
|| {{{remove_freeze}}} || Allows {{{freeze}}} target to mark removed exports as {{{ABSENT}}} in the {{{.def}}} file. '''WARNING''' This breaks binary compatibility with any user of the function ||
|| {{{armv5_udeb}}}, {{{armv5_udeb}}}, {{{armv5}}} || Build for {{{armv5}}}; debug, release or both ||
|| {{{winscw_udeb}}}, {{{winscw_urel}}}, {{{winscw}}} || Build for {{{winscw}}}; debug, release or both ||
|| {{{default}}} || Normally this is {{{armv5}}} and {{{winscw}}} together, but an SDK can define it to mean whichever configurations are the standard ones to build for that SDK. ||
|| {{{release_gcce}}} || For use with gcce_armv5/armv5 variants, ensure armv5 output of GCCE builds goes into epoc32/release/gcce ||
|| {{{release_gccev6}}} || For use with armv6 variants, ensure armv6 output of GCCE builds goes into epoc32/release/gccev6 ||
|| {{{release_gccev7}}} ||  For use with armv7 variants, ensure armv7 output of GCCE builds goes into epoc32/release/gccev7 ||
|| {{{win32}}} || For use exclusively on Linux with the "tools2" variant (e.g. {{{sbs -c tools2_urel.win32}}}). Uses the MinGW cross compiler to build Win32 programs on Linux. Certain distributions like Fedora, Ubuntu and Debian provide a pre-packaged version of MinGW for cross-compiling Windows programs and this variant relies on those. Ensure the environment variable {{{SBS_MINGW_LINUX_PREFIX}}} is set correctly. See [wiki:Raptor_Environment_Variables Raptor Environment Variables] ||

'''Note:''' By default, output from Raptor's GCCE builds goes into the epoc32/release/armv5, epoc32/release/armv6, epoc32/release/armv7.

== Useful Aliases ==

||= Alias =||= Expands to =||= Effect =||
|| {{{armv5_urel}}} || {{{arm.v5.urel.rvct2_2}}} || ARMv5 release binaries compiled with RVCT 2.2 ||
|| {{{armv5_udeb}}} || {{{arm.v5.udeb.rvct2_2}}} || ARMv5 debug binaries compiled with RVCT 2.2 ||
|| {{{armv5_urel.smp (no short alias currently)}}} || {{{arm.v5.urel.rvct2_2.smp}}} || ARMv5 release SMP binaries compiled with RVCT 2.2 ||
|| {{{armv5_udeb.smp (no short alias currently)}}} || {{{arm.v5.udeb.rvct2_2.smp}}} || ARMv5 debug SMP binaries compiled with RVCT 2.2 ||
|| {{{armv5_urel_gcce4_3_2}}} || {{{arm.v5.urel.gcce4_3_2}}} || ARMv5 release binaries compiled with GCCE 4.3.2 ||
|| {{{armv5_udeb_gcce4_3_2}}} || {{{arm.v5.udeb.gcce4_3_2}}} || ARMv5 debug binaries compiled with GCCE 4.3.2 ||
|| {{{armv5_urel_gcce4_3_3}}} || {{{arm.v5.urel.gcce4_3_3}}} || ARMv5 release binaries compiled with GCCE 4.3.3 ||
|| {{{armv5_udeb_gcce4_3_3}}} || {{{arm.v5.udeb.gcce4_3_3}}} || ARMv5 debug binaries compiled with GCCE 4.3.2 ||
|| {{{armv6_urel}}} || {{{arm.v6.urel.rvct2_2}}} || ARMv6 release binaries compiled with RVCT 2.2 ||
|| {{{armv6_udeb}}} || {{{arm.v6.udeb.rvct2_2}}} || ARMv6 debug binaries compiled with RVCT 2.2 ||
|| {{{armv7_urel}}} || {{{arm.v7.urel.rvct3_1}}} || ARMv7 release binaries compiled with RVCT 3.1 ||
|| {{{armv7_udeb}}} || {{{arm.v7.udeb.rvct3_1}}} || ARMv7 debug binaries compiled with RVCT 3.1 ||
|| {{{arm9e_urel}}} || {{{arm.9e.urel.rvct2_2}}} || ARM 9 release binaries compiled with RVCT 2.2 ||
|| {{{arm9e_udeb}}} || {{{arm.9e.udeb.rvct2_2}}} || ARM 9 debug binaries compiled with RVCT 2.2 ||
|| {{{arm.v5.udeb.gcce4_4_1 (no short alias currently)}}} || {{{arm.v5.udeb.gcce4_4_1}}} || ARMv5 debug binaries compiled with GCCE 4.4.1 with output going in epoc32/release/armv5/udeb ||
|| {{{arm.v5.udeb.gcce4_4_1.release_gcce (no short alias currently)}}} || {{{arm.v5.udeb.gcce4_4_1.release_gcce}}} || ARMv5 debug binaries compiled with GCCE 4.4.1 with output going in epoc32/release/gcce/udeb ||
|| {{{arm.v7.udeb.gcce4_4_1.release_gccev7 (no short alias currently)}}} || {{{arm.v7.udeb.gcce4_4_1.release_gccev7}}} || ARMv5 debug binaries compiled with GCCE 4.4.1 with output going in epoc32/release/gccev7/udeb ||


== Options ==

||= Option =||= Effect =||
|| {{{-h}}}, {{{--help}}} || show this help message and exit ||
|| {{{-a}}} ''SYS_DEF_BASE'', {{{--sysdefbase=}}}''SYS_DEF_BASE'' || Root directory for relative paths in the System Definition XML file. ||
|| {{{-b}}} ''BLD_INF_FILE'', {{{--bldinf=}}}''BLD_INF_FILE'' || Build information filename. Multiple -b options can be given. ||
|| {{{-c}}} ''CONFIG_NAME'', {{{--config=}}}''CONFIG_NAME'' || Configuration name to build. Multiple {{{-c}}} options can be given. The standard configs are all, armv5, armv7, default, tools, tools2 and winscw. ||
|| {{{--configpath=}}}''CONFIG_LIST'' || Append a list of paths to the default list of XML configuration folders. Use ';' as the separator on Windows, and ':' on Linux. Multiple {{{--configpath}}} options can be given. ||
|| {{{--check}}} || Test for the existence of files created by the build, printing the ones which are missing. Do not build anything. ||
|| {{{--command=}}}''COMMAND_FILE'' || Provide a set of command-line options in a file. ||
|| {{{-d}}}, {{{--debug}}} || Display information useful for debugging. ||
|| {{{-e}}} ''MAKE_ENGINE'', {{{--engine=}}}''MAKE_ENGINE'' || Name of the make engine which runs the build. E.g. {{{sbs -e make}}}, {{{sbs -e pvmgmake}}} ||
|| {{{--export-only}}} || Generate exports only and do not create any make files. Use {{{sbs --export-only}}} instead of {{{sbs export}}} if you need to do exports only. ||
|| {{{--noexport}}} || Don't export any files - useful in some builds when you know exports have already been done. ||
|| {{{-f}}} ''LOGFILE'', {{{--logfile=}}}''LOGFILE'' || Name of the log file, or '-' for stdout. ||
|| {{{--filters=}}}''FILTER_LIST'' || Comma-separated list of names of the filters to use (case sensitive). Providing the name of a non-existent filter returns the list of available filters. See [wiki:Filter_examples filter examples] ||
|| {{{-i}}}, {{{--ignore-os-detection}}} || Disables automatic application of OS variant based upon the OS version detected from each epoc32 tree. '''Note:''' this option is looking like a candidate for deprecation. Please do not use it. For customising SDKs, please use the epoc32/sbs_config/os_properties.xml mechanism. ||
|| {{{-j}}} ''NUMBER_OF_JOBS'', {{{--jobs=}}}''NUMBER_OF_JOBS'' || The maximum number of jobs that make should try and run in parallel (on a single machine). ||
|| {{{-k}}}, {{{--keepgoing}}} || Continue building, even if some build commands fail. ||
|| {{{-l}}} ''SYS_DEF_LAYER'', {{{--layer=}}}''SYS_DEF_LAYER'' || Build a specific layer in the System Definition XML File. Multiple -l options can be given. ||
|| {{{-m}}} ''MAKEFILE'', {{{--makefile=}}}''MAKEFILE'' || Top-level makefile to be created. Use this if you would like to control the base of the file name of your makefiles. This is useful if you want the makefiles somewhere other than epoc32/build/, or if you just want a different filename. The default makefile basename is "$EPOCROOT/epoc32/build/Makefile_all". ||
|| {{{--mo=}}}''MAKE_OPTION'' || Option that must be passed through to the make engine. Multiple {{{--mo}}} options can be given. ||
|| {{{-n}}}, {{{--nobuild}}} || Just create makefiles, do not build anything. ||
|| {{{--no-depend-include}}} || Do not include generated dependency files. This is only useful for extremely large non-incremental builds. [TODO what is the difference between this and the bfc variant?] ||
|| {{{--no-depend-generate}}} || Do not generate dependency files. This is only useful for extremely large non-incremental builds.  Implies --no-depend-include. ||
|| {{{--no-metadata-depend}}} || Do not consider a project's outputs out-of-date if the MMP file has been changed. This is useful if you use a tool such as {{{qmake}}} to generate the MMP file. An incremental build will be performed. The user is responsible for ensuring that complete rebuilds are performed when the information in the MMP file really has materially changed. ||
|| {{{-o}}}, {{{--orderlayers}}} || Build layers in the System Definition XML file in the order listed or, if given, in the order of {{{-l}}} options. ||
|| {{{-p}}} ''PROJECT_NAME'', {{{--project=}}}''PROJECT_NAME'' || Build a specific project (mmp or extension) in the given bld.inf file. Multiple -p options can be given. ||
|| {{{-q}}}, {{{--quiet}}} || Run quietly, not generating output messages. ||
|| {{{--query=''QUERY''}}} || Access various build settings and options using a basic API.  See [wiki:Raptor_Query_Reference Raptor Query Reference] for more details on the available options and output.  Multiple {{{--query}}} options can be given. ||
|| {{{-s}}} ''SYS_DEF_FILE'', {{{--sysdef=}}}''SYS_DEF_FILE'' || System Definition XML filename. This effectively provides a list of {{{bld.inf}}} files to be processed. See [wiki:System_Definition System Definition] for more details on the System Definition format. ||
|| {{{--source-target=}}}''SOURCE_TARGET'' || Build the listed source or resource file in isolation - do not perform any dependent processing. Multiple --source-target options can be given. ||
|| {{{-t}}} ''TRIES'', {{{--tries=}}}''TRIES'' || How many times to run a command before recording an error. The default is 1. This is useful for builds where transient failures can occur. ||
|| {{{--toolcheck=}}}''TOOLCHECK'' || Possible values are:[[BR]] "on"     -  Check the versions of tools that will be used in the build. Use cached results from previous builds to save time. This is the default.[[BR]] "off"    -  Do not check tool versions whatsoever.[[BR]] "forced" -  Check all tool versions. Don't use cached results. ||
|| {{{--timing}}} || Show extra timing information for various processes in the build. ||
|| {{{--pp=}}}''PARALLEL_PARSING'' || Controls how metadata (e.g. bld.infs) are parsed in Parallel. Possible values are:[[BR]] "on"  - Parse bld.infs in parallel (should be faster on clusters/multicore machines) [[BR]] "slave" - used internally by Raptor [[BR]] "off" - Parse bld.infs serially ||
|| {{{-v}}}, {{{--version}}} || Print the version number and exit. ||
|| {{{--what}}} || Print out the names of the files created by the build. Do not build anything. ||


== System Definition Files ==

By default, the {{{sbs}}} command will build everything specified by a {{{bld.inf}}} file in the current working directory. An explicit {{{bld.inf}}} file can be specified instead with the {{{-b}}} option. 

Alternatively, a [wiki:System_Definition System Definition] file can be supplied, which is an XML file containing information about which {{{bld.inf}}} files are to be built, amongst other things. 

== Settings Files ==

It is possible to configure some of the behaviour of SBSv2 using global, personal and kit-specific configuration files. These can change what and how SBSv2 builds by default, and add new variants. Information on how the settings files work discussed here:
 *  [wiki:Raptor_Personal_Preferences Personal Preferences]
 *  [wiki:Raptor_Kit_Configuration Kit Set up] - How to configure a kit (or any epoc32 tree) for SBSv2


= Raptor Environment Variables =

==  SBSv2 Environment Variables  ==

SBSv2 can be configured by a number of environment variables, as listed in the following table. The only one of these that ''must'' be set is {{{SBS_HOME}}} SBSv2 is usually installed with its own versions of Python, Mingw and Cygwin which it will use by default if the environment variables are not set.

Please note that the values assigned to these environment variables should not be surrounded by quotes, even if there are spaces in them. This will result in confusing errors. Linux environment variables should not contain spaces.

||= Environment variable =||= Meaning =||= Optional or Mandatory =||= Example =||
|| {{{SBS_HOME}}} || The base directory of the Raptor installation that you to use; must not have spaces. Be warned that if {{{SBS_HOME}}} is set and a different {{{sbs.bat}}} is on the path, odd effects may result. || Optional from 2.10 || {{{C:\Apps\Raptor}}} ||
|| {{{SBS_PYTHON}}} || The python executable that you want Raptor to use; should be at least Python 2.5; must not have spaces. See notes on python usage below. || Optional || {{{C:\Python26\python.exe}}} ||
|| {{{SBS_PYTHONPATH}}} || The {{{PYTHONPATH}}} to use in Raptor runs. See notes on python usage below. || Optional || {{{C:\Python26}}} ||
|| {{{SBS_CYGWIN}}} [[BR]] {{{SBS_CYGWIN17}}} || The base directory of the Cygwin installation that you want Raptor to use; must not have spaces. {{{SBS_CYGWIN17}}} must be used if pointing to Cygwin 1.7 || Optional || {{{C:\Apps\Cygwin}}} ||
|| {{{SBS_MINGW}}} || The base directory of the MinGW installation that you want Raptor to use; must not have spaces || Optional || {{{C:\Apps\mingw}}} ||
|| {{{SBS_BVCPP}}} || C pre-processor capable of supporting our Binary Variation implementation. Raptor comes with a fork of CPP that will do, and {{{SBS_BVCPP}}} defaults to this version. Otherwise it can point to any CPP from GCC 4.4 or later || Optional || {{{C:\Apps\gcc4.4\bin\cpp.exe}}} ||
|| {{{SBS_GCCE432BIN}}} [[BR]] {{{SBS_GCCE433BIN}}} [[BR]] {{{SBS_GCCE441BIN}}} || The base directory of the GCCE 4.3.2/4.3.3/4.4.1 compiler, if used || Only required if the corresponding GCCE compiler is to be used || {{{C:\Apps\gcc4.3.2\bin}}} ||
|| {{{SBS_MINGW_LINUX_PREFIX}}} || Linux only: the prefix string of the MinGW GCC compiler and associated tools. For example, if the {{{gcc}}} executable's name is {{{i586-mingw32msvc-gcc}}}, then the prefix is {{{i586-mingw32msvc}}}. That is, you must not have {{{-}}} at the end of this prefix; Raptor adds it for you. || Optional: Only required to build Windows TOOLS2 binaries on Linux. || Ubuntu {{{i586-mingw32msvc}}} [[BR]] Fedora {{{i586-redhat-linux}}} ||
|| {{{SBS_GNUMAKE38}}} || On Windows, this variable must be set to the full path of the the MinGW Make executable {{{mingw32-make.exe}}} (or {{{make.exe}}} if it has been renamed). Please do not use the MSys nor the Cygwin Make as neither of these handles correctly the Windows paths that Raptor's makefiles present. || Optional: Only if Make is not to be found in the expected place within the MinGW installation || {{{C:\Apps\MinGW\bin\mingw32-make.exe}}} ||

==  Python Usage  ==

From 2.12.4, the following policy will be employed to determine both the Python interpreter Raptor will use, and how the {{{PYTHONPATH}}} environment variable will be set.

In general, {{{SBS_PYTHON}}} and/or {{{SBS_PYTHONPATH}}} environment variables will take precedence.  If these are set, then the Python interpreter used will be that pointed to by {{{SBS_PYTHON}}} with the {{{PYTHONPATH}}} environment variable set to the value of {{{SBS_PYTHONPATH}}}.

If {{{SBS_PYTHON}}} isn't set, then Raptor will check to see if a supported version of Python is sitting locally within its installed directory structure; for example, with 2.12.4, Raptor will check to see if {{{%SBS_HOME%\win32\python264\python.exe}}} exists.  If a suitable Python ''does'' exist locally, then Raptor will make use of it; in order that the local interpreter's default settings are used, the {{{PYTHONPATH}}} or {{{PYTHONHOME}}} environment variable will be set to empty, unless specifically overridden with {{{SBS_PYTHONPATH}}}.

If {{{SBS_PYTHON}}} isn't set, and a suitable supported Python doesn't exist locally, then Raptor will attempt to use a Python interpreter located from the system {{{PATH}}}.  In this case, {{{PYTHONPATH}}} will remain unchanged versus the environment, unless explicitly overridden with {{{SBS_PYTHONPATH}}}.

==  Troubleshooting  ==

The following tips explain some common environment variable configuration issues.

 *  If you set {{{SBS_CYGWIN}}} wrong, toolcheck may fail with a traceback, leaving no indication of what the problem is!
 *  If you set one of the others wrong, it's a little better, but could still do with some usability enhancements:

||= Report =||= What's wrong =||
|| {{{C:\badname\pythin.exe' is not recognized as an internal command, operatable program or batch file}}} || {{{SBS_PYTHON}}} ||
|| {{{sbs: error: <error>tool 'GNUCPP' from config 'none' did not return version 'cpp(.exe)? .* [345]\..*' as required.[[BR]] sbs: error: <error>tool 'GNUMAKE38' from config 'none' did not return version 'GNU Make 3.8[1-9]' as required.[[BR]] sbs: error: no CHECK information found}}} || {{{SBS_MINGW}}} [[BR]] as well go to the folder {{{%SBS_MINGW%\bin}}}. [[BR]] Find file {{{mingw32-make.exe}}} and copy it to the file {{{make.exe}}} into the same folder. ||
|| {{{python.exe: can't open file '...\raptor_start.py': [Errno 2] No such file or directory}}} || {{{SBS_HOME}}} ||
|| {{{sbs: error: A critical tool could not be found.[[BR]] Please check that 'C:\Appz\cygwin\bin\bash.exe' is in the path. ([Error 3] The system cannot find the path specified)}}} || {{{SBS_CYGWIN}}} ||
|| {{{cygwin warning:}}} || Perhaps you have {{{SBS_CYGWIN}}} pointing to a Cygwin 1.7 installation. Use {{{SBS_CYGWIN17}}} instead. ||
|| {{{Files\CSL was unexpected at this time}}} [[BR]] or [[BR]] {{{... contains spaces that cannot be neutralized ...}}} || An environment variable containing spaces is surrounded by quotes. SBS environment variables on Windows may contain spaces but may not be surrounded by quotes. ||
|| {{{sbs: error: tool 'GNUMAKE38' from config 'none' did not return version 'GNU Make 3.8[1-9]' as required. [[BR]] Command 'c:/Apps/MinGW/bin/make.exe -v' returned: /usr/bin/bash: c:/Apps/MinGW/bin/make.exe: No such file or directory}}} || {{{SBS_GNUMAKE38}}} ||
|| {{{C:\Python26\python.exe: can't find '__main__.py' in 'C:\\source\\hg\\build\\sbsv2\\raptor'}}} || Perhaps {{{SBS_HOME}}} ends with a space ||



= Raptor Build Extensions =

*Not sure what this is supposed to be but it shouldn't be a dupe of personal prefs*



= Raptor Kit Configuration =

This article describes SBSv2 configuration files that can be used modify the build targets, compilers, and configuration "aliases" on a per-kit basis. The settings in the kit-specific configuration files are used in preference to the default SBSv2 settings, or any [wiki:Raptor_Personal_Preferences#Your_own_command_line_options personal preferences (sbs init.xml)].  ''Note: SBSv2 is default configured to work with Symbian!^2/SymTB9.2 kits, so you will need to use the configuration files if you want to use Raptor with the Symbian!^1 SDK, or if you wan to use a different compiler.''

==  Kit Configuration (sbs_config)  ==

Kit configuration settings are stored in one or more XML files within the kit {{{%EPOCROOT%\epoc32\sbs_config\}}} directory (by convention a single file named {{{os_properties.xml}}} is used, but there is nothing to stop you spreading the settings across several files in the directory, or using any name you choose).

The framework for each settings file is shown below: individual variant and alias settings are inserted between the {{{<build>}}} tags (see the following sections):
{{{
<?xml version="1.0" encoding="ISO-8859-1"?>
<build xmlns="http://symbian.com/xml/build" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://symbian.com/xml/build ../../schema/build/2_0.xsd">

<!-- variants and alias go here -->

</build>
}}}

=  root changes variant (for Symbian!^1/Symbian OS v9.4 kits)  =

The ''root.changes'' variant must be declared for Symbian!^1/Symbian OSv9.4 kits. Note that all SBSv2 ''root.changes'' settings (personal and default) are replaced with this variant setting.  
{{{
    <var name="root.changes">
        <set name='POSTLINKER_SUPPORTS_WDP' value=''/>
        <set name='SUPPORTS_STDCPP_NEWLIB' value=''/>
        <set name='RVCT_PRE_INCLUDE' value='$(EPOCINCLUDE)/rvct2_2/rvct2_2.h'/>
        <set name='VARIANT_HRH' value='$(EPOCINCLUDE)/variant/Symbian_OS.hrh'/>
    </var>
}}}

''Note: If you don't change this setting then you need to add '''.v94''' to your build configuration, or you'll get errors about a missing target '''scppnwdl.lib''' ''

=  meta variant (How project file metadata is interpreted)  =

The ''meta'' variant is used to define how the metadata in the ''bld.inf'' and ''.mmp'' files is interpreted, including the default platforms that will be built.

The variant below redefines the meaning of DEFAULT, BASE_DEFAULT and BASE_USER_DEFAULT in the PLATFORMS declaration of the .mmp file by extending the ''default.locations''. Using {{{<append/>}}} as shown means that the new values are added to the existing variable values; use {{{<set/>}}} to overwrite the existing variables completely. Note also that this setting overwrites the SBSv2 default and personal settings.
{{{
    <var name="meta" extends="default.locations">
        <append name='DEFAULT_PLATFORMS' value='ARMV6'/>
        <append name='BASE_DEFAULT_PLATFORMS' value='ARMV6'/>
        <append name='BASE_USER_DEFAULT_PLATFORMS' value='ARMV6'/>
    </var>
}}}

=  Alias redefinition  =

You can specify an aliases and groups for your own build configurations; these can be used as proxies for your build configurations in the same way as the default aliases (like winscw_udeb). You can also change the way the default aliases are interpreted. For example the following alias definitions will make ''armv5_urel'' and ''armv5_udeb'' build with RVCT 4.0. In fact this will also change how the configuration ''arm5'' is interpreted, as this is defined in terms of the other aliases.
{{{
    <alias name="armv5_urel" meaning="arm.v5.urel.rvct4_0"/>
    <alias name="armv5_udeb" meaning="arm.v5.udeb.rvct4_0"/>
}}}

== variant.cfg ==

As of sbs version 2.15.2 kits no longer require a variant configuration file {{{%EPOCROOT%\epoc32\tools\variant\variant.cfg}}}. Instead, the variant configuration can be done using the "root.changes" variant as described above. The pre-included header file location is defined by the following property,
{{{
    <set name='VARIANT_HRH' value='$(EPOCINCLUDE)/variant/Symbian_OS.hrh'/>
}}}

If this property is not set then a {{{variant.cfg}}} file is expected to exist instead. In other words, the default behaviour is the same as before.

A {{{variant.cfg}}} file should look as shown below:
{{{
# Comments begin with a hash
# the first (noncomment) line is the pre-include file
epoc32\include\variant\Symbian_OS.hrh
# any other lines are something else. I don't know what the set of acceptable words are.
# This is redundant because Raptor does not support ABIv1
ENABLE_ABIV2_MODE
}}}

== devices.xml ==

SBSv2 is not aware of the {{{devices.xml}}} kit management tool used by Carbide.c++ and legacy Symbian kits. The current active kit is instead managed through the directory specified in the {{{EPOCROOT}}} environment variable.
== Overriding toolcheck ==

You can make toolcheck stricter or laxer, for example if you have found that, for a particular kit, certain compilers produce erroneous output. See [wiki:Overriding_toolcheck Overriding toolcheck].



= Raptor Log Format =

Raptor Creates a log in an XML Format.  The log comprises a single {{{<build>}}} tag that contains everything else.

=  Metadata Parsing  =

The build process starts with parsing the bld.infs, mmps and system definitions that define what the user wishes to build.
This part of the build process is called "Metadata Parsing".

Raptor produces {{{<error>}}}, {{{<warning>}}} and {{{<info>}}} tags during this time. If the {{{-d}}} option is specified then {{{<debug>}}} tags will also be encountered.

== Info tags  ==

"Info" tags contain data intended to be human readable that is helpful or informative when looking at the log.

The logs start, for example, with {{{<info>}}} statements that contain the version of Raptor used and the commandline parameters that it was given.  They also list the entire list of the user's environment variables.  These items are terrifically useful when dealing with any problem that a user may have had.

{{{
 <info>sbs: version 2.12.1 [2010-01-29 symbian build system CHANGESET]</info>
 <info>SBS_HOME /home/tnmurphy/x/build/sbsv2/raptor</info>
 <info>Set-up /home/tnmurphy/x/build/sbsv2/raptor/sbs_init.xml</info>
 <info>Command-line-arguments -b smoke_suite/test_resources/simple_gui/Bld.inf -c armv5 -c winscw -m /home/tnmurphy/x/test/epocroot/epoc32/build/smoketestlogs/exe_armv5_winscw_single_file_baseline_build.mk -f /home/tnmurphy/x/test-epocroot/epoc32/build/smoketestlogs/exe_armv5_winscw_single_file_baseline_build.log</info>
 <info>Current working directory /home/tnmurphy/x/build/sbsv2/raptor/test</info>
 <info>Environment ARMLMD_LICENSE_FILE=8784@log.europe.nokia.com:8824@falc.europe.nokia.com:2998@samg1.np.nokia.com</info>
 <info>Environment PATH=/home/tnmurphy/x/build/sbsv2/raptor/linux-unknown-libc2_10/python262/bin:/home/tnmurphy/x/build/sbsv2/raptor/linux-unknown-ibc2_10/bin:/opt/symbian/make-pvm-381:/bin:/opt/symbian/bin:/usr/bin:/home/tnmurphy/bin:/home/tnmurphy/bin:/usr/local/bin:/home/tnmurphy/x/build/sbsv2/raptor:/home/tnmurphy/x/build/sbsv2/raptor/bin:/home/tnmurphy/x/test-epocroot/epoc32/tools:/home/tnmurphy/x/test-epocroot/epoc32/release/winc/urel:/opt/symbian/a616/ARM/RVCT/Programs/2.2/308/linux-pentium:/opt/symbian/pvm3/bin/LINUX:/opt/symbian/pvm3/lib/LINUX:/opt/symbian/bin:/home/tnmurphy/x/build/sbsv2/raptor/linux-unknown-libc2_10/cw_build470msl19/release/Symbian_Tools/Command_Line_Tools</info>
}}}

== Error tags  ==

Error tags indicate that the build will fail.  If {{{-k}}} is specified then Raptor will continue despite errors but one should expect to see further failures.

{{{
 <error>/data/scarab/wse/simple/caseaware/mekehrju/wk02/ncp_sw/
 corecom/aasw/hwdevices/hwdevicebase/group/errorconcealmentintfcci.mmp (37) : 
 Unrecognised Keyword ['SYMBIAN_MW_LAYER_PUBLIC_EXPORT_PATH']</error>
}}}

== Warning tags  ==

Indicate build issues that deserve attention but probably won't cause a failure.

== Debug Tags  ==

... are very very useful when trying to determine the cause of a build problem.  Enable them with {{{-d}}}.  They show, for example, how the state of bld.inf and mmp files after preprocessing so that one can see how they were affected by the system's HRH macros.

=  Makefile Parsing and Building  =

When a makefile executes a rule, e.g. a compilation, it is enclosed in a {{{<recipe>}}} tag.  In parallel builds (e.g. with {{{-j 4}}}) Raptor's shell wrapper, Talon, ensures that the output from recipes is not intermingled. So each set of {{{<recipe>}}} tags will come out correctly even when many recipes are being executed at once.

{{{
 <recipe name='postlink' target='/home/tmurphy/pf/short/tmurphy/build/fix/raptor/test/epocroot/epoc32/release/armv5/udeb/createstaticdll.dll' 
    host='head.raptor.symbian.intra' layer='' component='' bldinf='/home/tmurphy/pf/short/tmurphy/build/fix/raptor/test/smoke_suite/test_resources/simple_dll/bld.inf' 
    mmp='/home/tmurphy/pf/short/tmurphy/build/fix/raptor/test/smoke_suite/test_resources/simple_dll/CreateStaticDLL.mmp' config='armv5_udeb' 
    platform='armv5'       
    phase='ALL' source=''>
 <![CDATA[
 BUILD OUTPUT FOR THIS RULE GOES HERE
 ]]>
 </recipe>
}}}

The type of build command (complation linking etc) may be inferred from the "name" attribute. Other parameters are available such as the location of the {{{bld.inf}}} with which this command is associated.

Within {{{<recipe>}}} tags the success or failure of the recipe is recorded in a {{{<status>}}} tag: 

{{{
 <status exit='ok' attempt='1'>
}}}

Failed build commands are indicated by {{{"exit='failed'"}}}.

=  A Complete Recipe  =

{{{
 <recipe name='postlink' target='/home/tmurphy/pf/short/tmurphy/build/fix/raptor/test/epocroot/epoc32/release/armv5/u
 deb/createstaticdll.dll' host='head.raptor.symbian.intra' layer='' component='' bldinf='/home/tmurphy/pf/short/tmurp
 hy/build/fix/raptor/test/smoke_suite/test_resources/simple_dll/bld.inf' mmp='/home/tmurphy/pf/short/tmurphy/build/fi
 x/raptor/test/smoke_suite/test_resources/simple_dll/CreateStaticDLL.mmp' config='armv5_udeb' platform='armv5' phase=
 'ALL' source=''>
 <![CDATA[
 + /home/tmurphy/pf/short/tmurphy/build/fix/raptor/test/epocroot/epoc32/tools/elf2e32 --sid=0x0 --version=10.0 --uid1
 =0x10000079 --uid2=0xe800004c --vid=0x70000001 --capability=All-TCB --fpu=softvfp --targettype=DLL --output=/home/tm
 urphy/pf/short/tmurphy/build/fix/raptor/test/epocroot/epoc32/release/armv5/udeb/createstaticdll.dll --elfinput=/home
 /tmurphy/pf/short/tmurphy/build/fix/raptor/test/epocroot/epoc32/release/armv5/udeb/createstaticdll.dll.sym '--defout
 put=/home/tmurphy/pf/short/tmurphy/build/fix/raptor/test/epocroot/epoc32/build/simple_dll/c_1aa4d81710db40d3/creates
 taticdll_dll/armv5/udeb/createstaticdll{000a0000}.def' '--dso=/home/tmurphy/pf/short/tmurphy/build/fix/raptor/test/e
 pocroot/epoc32/build/simple_dll/c_1aa4d81710db40d3/createstaticdll_dll/armv5/udeb/createstaticdll{000a0000}.dso' '--
 linkas=createstaticdll{000a0000}.dll' --paged --definput=/home/tmurphy/pf/short/tmurphy/build/fix/raptor/test/smoke_
 suite/test_resources/simple_dll/CREATESTATICDLLARM.def '--libpath=/home/tmurphy/pf/short/tmurphy/build/fix/raptor/te
 st/epocroot/epoc32/release/armv5/lib/;/opt/symbian/a616/ARM/RVCT/Data/2.2/308/lib/armlib)'
 ]]><time start='1233765446.971932000' elapsed='0.018' />
 + RV=0
 + set +x
 <status exit='ok' attempt='1' />
 </recipe>
}}}

=  Metadata Generation Recipes  =

When Parallel Parsing is turned on ({{{--pp=on}}}) Raptor uses the make engine (gnumake, emake or whatever) to parse the metadata in parallel.  Thus at the start of the log one may see unusual recipes with the name "metadata_generation".

These contain sub-invocations of Raptor and thus might seem unusual as Raptor logging will thus appear withing the CDATA section of a recipe.

{{{
 <recipe name='makefile_generation' target='y:/output/logs/makefile/92_7952_201004_wk04_05_dfs_build_ncp_dfs_variants_pp_1' host='' layer='' component='' bldinf='' mmp='' config='armv5_udeb.gekko79' platform='' phase='ALL' source=''>
 <![CDATA[
 + E:/build_e/sbs-2.12_tc_speed/bin/sbs.bat --noexport --toolcheck=off -n -k -b y:/ncp_sw/corecom/dgsw_s60display/tv_out/group/bld.inf -b y:/ext/os/netdo_config/group/bld.inf
}}}

=  Make messages  =

Messages may appear between recipe nodes - these are from the make tool. e.g. 

{{{
 </recipe> *** Error: could not create fred.exe <recipe .... >
}}}

A schema is attached to this page. 

=  Whatlog tags  =

Raptor also prints messages into the output that  show what releasable targets have been created in a build:

{{{
 <whatlog bldinf='/home/tnmurphy/x/build/sbsv2/raptor/test/smoke_suite/test_resources/simple_gui/Bld.inf' mmp='/home/tnmurphy/x/build/sbsv2/raptor/test/smoke_suite/test_resources/simple_gui/HelloWorld.mmp' config='winscw_urel'>
 <build>/home/tnmurphy/x/test-epocroot/epoc32/release/winscw/urel/helloworld.exe</build>
 <build>/home/tnmurphy/x/test-epocroot/epoc32/release/winscw/urel/helloworld.exe.map</build>
 </whatlog>
}}}

=  Clean tags  =

Clean tags indicate the names of all the intermediate files that are produced by the build.

They are put into the log by make while it is reading the generated makefiles.  These tags are read by Raptor and used to implement the "clean" operation:

{{{
 <clean bldinf='/home/tnmurphy/x/build/sbsv2/raptor/test/smoke_suite/test_resources/simple_gui/Bld.inf' mmp='/home/tnmurphy/x/build/sbsv2/raptor/test/smoke_suite/test_resources/simple_gui/HelloWorld.mmp' config='winscw_udeb'>
 <file>/home/tnmurphy/x/test-epocroot/epoc32/build/simple_gui/c_82c4dfdddc84fd2d/helloworld_exe/winscw/udeb/helloworld.UID.CPP</file>
 <file>/home/tnmurphy/x/test-epocroot/epoc32/build/simple_gui/c_82c4dfdddc84fd2d/helloworld_exe/winscw/udeb/HelloWorld_Main.o</file>
 <file>/home/tnmurphy/x/test-epocroot/epoc32/build/simple_gui/c_82c4dfdddc84fd2d/helloworld_exe/winscw/udeb/HelloWorld_Application.o</file>
 <file>/home/tnmurphy/x/test-epocroot/epoc32/build/simple_gui/c_82c4dfdddc84fd2d/helloworld_exe/winscw/udeb/HelloWorld_Document.o</file>
 <file>/home/tnmurphy/x/test-epocroot/epoc32/build/simple_gui/c_82c4dfdddc84fd2d/helloworld_exe/winscw/udeb/HelloWorld_AppUi.o</file>
 </clean>
}}}



= Raptor Symbian Reference =


This page is for information about how Symbian OS based code is built - regardless of build system.

This is pretty thin, so far...

||[wiki:Raptor_Resource_Files_Reference Resource files and localization] || Resource files and localization ||



= Tools Required by Raptor =

Raptor relies on a number of supporting tools. This page lists third-party tools and utilities and provides some notes on usage and versions etc.

=  MinGW GCC and Make - Linux and Windows  =

For tools2 builds, Raptor requires at least MinGW's GCC 3.4.5 and Gnu Make 3.81.

MinGW's GCC 4.4, GCC 4.5 and Gnu Make 3.82 also work, but further testing is required.

MinGW's Gnu Make is essential because it correctly handles paths with a drive-letter and colon in (e.g. D:\src\my\component\code.cpp) and Cygwin's version of Gnu Make does not handle the Windows-style paths correctly.

Notes: Starting with 2.13.0, using the Linux ports of MinGW (e.g. on Fedora, Ubuntu, Debian etc), Raptor also supports the cross-compilation of tools2 components for Windows on Linux.

=  Cygwin - Windows only  =

As Raptor uses the GNU tool command line interface, it is necessary to use a system such as Cygwin that provides these on Windows. Raptor supports Cygwin 1.5 and, as of Raptor 2.13.0, also Cygwin 1.7. Some work was necessary to add support for Cygwin 1.7 due to a change in command line interface of some of the Cygwin tools. As a result, the way Raptor interfaces with Cygwin 1.7 is different.

Raptor is made aware of the location of Cygwin via the {{{SBS_CYGWIN}}} (for Cygwin 1.5) and {{{SBS_CYGWIN17}}} (for Cygwin 1.7) environment variables. The following bullet points indicate the order of precedence of the {{{SBS_CYGWIN}}} and {{{SBS_CYGWIN17}}} environment variables:

 *  {{{SBS_CYGWIN}}} set, {{{SBS_CYGWIN17}}} '''not''' set: Raptor will assume Cygwin 1.5 is being used
 *  {{{SBS_CYGWIN}}} set, {{{SBS_CYGWIN17}}} set: Raptor will assume Cygwin 1.7 is being used
 *  {{{SBS_CYGWIN}}} '''not''' set, {{{SBS_CYGWIN17}}} set: Raptor will assume Cygwin 1.7 is being used

''You will get errors if you set SBS_CYGWIN to be the root of a Cygwin 1.7 installation directory and if SBS_CYGWIN17 is not defined correctly.''

Cygwin 1.7 uses a different mechanism for mounts points, and can be used safely alongside Cygwin 1.5, and indeed other installations of Cygwin 1.7.

== Notes ==
 *  Cygwin's Perl, Python and Make are not suitable for use with Raptor, and it is recommended to avoid them. Please use native Windows versions of these tools.
 *  Raptor ensures certain mount points are present before the start of the build, so if you have an installation of Cygwin 1.5 already, it might cause problems with your mount points.

== Obtaining Cygwin ==
 *  Download the Cygwin installer (setup.exe) from http://www.cygwin.com/. A full installation guide is available on Cygwin's website [http://www.cygwin.com/cygwin-ug-net/setup-net.html].
 *  Run the installer, allowing for proxy server etc. Select an appropriate installation directory, preferably without spaces in the directory name if possible. Accept the default package list; for simplicity you can ensure that neither Perl nor Python is selected. Make sure zip and unzip are selected.
 *  Once installation is complete, set the {{{SBS_CYGWIN}}} or {{{SBS_CYGWIN17}}} environment variables as indicated above.

''The Cygwin project considers Cygwin 1.5 as a legacy option, and their recommendation is to use the latest release of Cygwin 1.7 unless absolutely necessary.''

=  Perl  =
Certain tools used in a build rely on Perl. On Windows, ActiveState's Perl is recommended. [http://strawberryperl.com/ Strawberry Perl] might also be an option.


TODO: Add other tools.



= Exports and Freezing in the Build =

== TARGETTYPEs and Exported Interfaces ==

This is a short guide outlining the support in Raptor and gives details on exported functions etc and freezing. 

||= TARGETTYPE =||= Group =||= DEFFILE required? =||= Import Library Generated? =||= Exported Interface Handling? =||
|| EXE || A || No || No || Not explicitly required nor applicable ||
|| KLIB || A || No || No || Not explicitly required nor applicable ||
|| LIB || A || No || No || Not explicitly required nor applicable ||
|| NONE || A || No || No || Not explicitly required nor applicable ||
|| STDEXE || A || No || No || Not explicitly required nor applicable ||
|| STDLIB || A || No || No || Not explicitly required nor applicable ||
|| ANI || B || No || No || Automatically handled by the build system ||
|| FSY || B || No || No || Automatically handled by the build system ||
|| LDD || B || No || No || Automatically handled by the build system ||
|| KEXT || B || No || No || Automatically handled by the build system ||
|| PLUGIN || B || No || No || Automatically handled by the build system ||
|| TEXTNOTIFIER2 || B || No || No || Automatically handled by the build system ||
|| PDD || B || No || No || Automatically handled by the build system ||
|| PDL || B || No || No || Automatically handled by the build system ||
|| VAR || B || No || No || Automatically handled by the build system ||
|| VAR2 || B || No || No || Automatically handled by the build system ||
|| DLL || C || Yes || Yes, assuming that a frozen .def file exists.  || Handled by def file maintained alongside source code ||
|| EXEXP || C || Yes || Yes, assuming that a frozen .def file exists.  || Handled by def file maintained alongside source code ||
|| IMPLIB || C || Yes || Yes, assuming that a frozen .def file exists.  || Handled by def file maintained alongside source code ||
|| KDLL || C || Yes || Yes, assuming that a frozen .def file exists.  || Handled by def file maintained alongside source code ||
|| STDDLL || C || Yes || Yes, assuming that a frozen .def file exists.  || Handled by def file maintained alongside source code ||

== TARGETTYPEs and Exported Interfaces in more detail ==

The vast majority of components built for the Symbian OS are built from .mmp files and, as a result, build in the context of a defined TARGETTYPE. TARGETTYPEs dictate specific traits of the component to be built - the UIDs required/used by default, libraries given priority in linking etc. One such trait relates to how the component's exported interface, if applicable, is defined and controlled by the build system. Broadly speaking, TARGETTYPEs that support an exported interface either have their exports (a) statically defined by the build system or (b) frozen in a .def file that is created and managed by the build system. In the latter case, these TARGETTYPEs support the generation of an import library for other components to link against.

In terms of interface, we therefore have three broad categories of TARGETTYPE that have the following default behaviour with regard to their exported interface and import library generation: 

=== Group A: The management of an exported interface isn't explicitly required or is not applicable ===
EXE [[BR]]
KLIB[[BR]]
LIB[[BR]]
NONE[[BR]]
STDEXE[[BR]]
STDLIB[[BR]]

No import library is generated. 

=== Group B: One or more exports forming the interface are hard-coded by the build system ===
ANI[[BR]]
FSY[[BR]]
LDD[[BR]]
KEXT[[BR]]
PLUGIN[[BR]]
TEXTNOTIFIER2[[BR]]
PDD[[BR]]
PDL[[BR]]
VAR[[BR]]
VAR2[[BR]]

No import library is generated. 

=== Group C: The exported interface is variable and must be maintained in a .def file ===

DLL[[BR]]
EXEXP[[BR]]
IMPLIB *[[BR]]
KDLL[[BR]]
STDDLL[[BR]]

An import library can be generated assuming that a frozen .def file exists.


IMPLIB is a bit of a special case - its purpose is solely to support the generation of an import library from a pre-existing .def file; it does not support the compile and link of source.

== .def File Names and Locations ==

For components using a TARGETTYPE from group C, the build system implicitly determines .def file name and location using the following logic:

Emulator:
{{{
    .mmp file location/../bwins/targetu.def
}}}

Target:
{{{
   .mmp file location/../eabi/targetu.def
}}}

There are two keywords that can be used to modify this behaviour, and they can be used in combination: 

'''DEFFILE'''

If the value listed by DEFFILE:

 *  solely specifies a path (ends in a slash) then the implicit targetu.def file is assumed to be at this location, relative to the .mmp file.
 *  just specifies a filename (contains no slashes) then the listed filename is assumed to be at the implicit location.
 *  specifies both a path and filename then the listed filename is assumed to be at the path specified, relative to the .mmp file.
 *  contains '~', then '~' will be replaced, according to the build, by 'bwins' or 'eabi'. 

An additional use of DEFFILE is to coerce TARGETTYPEs from group B, where any exports are statically defined by the build system and a .def file is not normally required, into requiring a .def file, supporting additional exports and generating an import library. This overriding behaviour also applies to EXE and STDEXE TARGETTYPEs from group A, but I can't see any overly good reason to shout about that much ;-). 

'''NOSTRICTDEF'''

By default, the build system will assume that any implicit or explicit .def file must physically exist with the letter "u" directly before the extension (a throw-back to the days of narrow/wide non-unicode/unicode builds and their differing exports). With NOSTRICTDEF listed in the .mmp file, this assumption is removed.

Example:

{{{
    /src/mycomponent/mycomponent.mmp

    DEFFILE deffiles/~/mydeffile.def
    NOSTRICTDEF

    /src/mycomponent/deffiles/bwins/mydeffile.def
    /src/mycomponent/deffiles/eabi/mydeffile.def
}}}
    
== Freezing Exports ==

Freezing a component's interface naturally only applies to components that support .def files - so, that amounts to all those using TARGETTYPES from group C above, and those from group B where an explicit DEFFILE statement is present; the build system only generates a FREEZE target for components that match these criteria. The act of freezing involves the build system having knowledge of a component's current exports and, as such, it can only occur in the context of a up-to-date build.

=== Analysis of Current Exports ===

The actual means by which the current exports of a component are determined varies depending on the build being performed.

In the emulator build a temporary import library is generated as a side-effect of a "stage one" link where no pre-existing .def file is listed. The import library generated represents the current exports of the component, as it was just built, and this is passed through the linker to generate a .inf file - essentially a text description of the import library's contents. The .inf file is presented to Symbian's MAKEDEF script along with any pre-existing frozen .def file (if one exists) and any static export expectations dervied from the TARGETTYPE (if a group B TARGETTYPE is being built).

In the target build the function of the standalone MAKEDEF is performed by ELF2E32 and, as part of post-linking, ELF2E32 determines the state of the current exports versus any pre-existing frozen .def file (if one exists).

In both of the above cases a temporary .def file is generated reflecting the current export state and the build system generates errors and warnings depending on how the current situation matches with its expectations.

Exports that are identified as missing generate an error - this indicates a break in BC for components already in existence.
Exports that are present in addition to those that are expected generate a warning - typically this indicates a component using a group C TARGETTYPE where development has lead to new exports that have not yet been frozen. This does not indicate a BC break for components already in existence, but unfrozen exports will need to frozen in order that (a) they can be managed and validated by the build system and (b) the build system will permit the generation of an import library that includes them.

=== Generating Frozen .def Files ===

In all builds the Symbian EFREEZE script is used to create and update .def files. In Raptor builds, this is invoked in the background in response to the FREEZE target:

{{{
    sbs freeze
}}}

EFREEZE does its work by analysing the frozen exports in any pre-existing .def file (if present) together with those present in the temporary .def file generated during the build (see above). It then generates a new .def file that reflects the current, validated, exported interface state.

There's a further level of validation that also gets applied here...

As Symbian interfaces are based on ordinal position rather than name, EFREEZE analyses the temporary .def file reflecting the current exports to conclude whether it includes the same exports, in the same order, as any pre-existing frozen .def file; any difference in the sequence of ordinals versus a frozen .def file is considered an error, and it is not possible to generate a new .def file if this is the case. At least, it's not possible to generate a .def file in what would be considered a normal, default, freeze...

EFREEZE also takes on optional "-r" argument. This permits the creation of frozen .def files where missing expected exported functions can be formally flagged as ABSENT (see below), and hence accepted as "absent with leave" in future builds and freezing sessions.

=== {{{EXPORTUNFROZEN}}} ===

By default, the build system will only generate an import library for components using a group C TARGETTYPE, or a group B TARGETTYPE with a DEFFILE statement, if the current exports are frozen within a .def file. In essence this is an attempt to maintain BC by not allowing anything to link to a component that isn't flagging its exports as being managed by the build system. However, this default behaviour can be circumvented if EXPORTUNFROZEN is listed in the .mmp file - regardless of unfrozen exports, EXPORTUNFROZEN will see an import library created, albeit with an appropriate warning. The use of this keyword is really to ease development when the interface of a component is in a state of flux, and it isn't the intention that it is present in production source.

It's worth noting here that EXPORTUNFROZEN does not generate an import library without reference to a frozen .def file (if it exists). Rather it generate an import library where any unfrozen exports are reflected after those already represented in any pre-existing .def file.

=== ABSENT Exports and Freezing  ===

ABSENT is used within .def files to plug holes where an exported function may no longer be present but, for the purpose of maintaining binary compatibility, the ordinal sequence must be maintained. Below are a couple examples of ABSENT in place in emulator and target .def files (respectively):

{{{
    ?FallBack@CImapSettings@@QBEHXZ @ 39 NONAME ABSENT
    _ZTIN4Meta11TMetaVarLenI5RBuf8EE @ 5 NONAME ABSENT
}}}

The second example above is actually pretty representative of most cases of ABSENT that can be found in the core Symbian OS sourcebase. A past change in ARM build behaviour lead to multiple type information and v-table exports no longer being part of the interface of built binaries. However, as these exports had become part of the frozen interface of components, and other "real" function exports had typically been frozen following them, in order to maintain ordinal sequence they were flagged as ABSENT in the relevant .def files.

By default, freezing exports using Raptor will not see missing exports automatically ABSENT-ed.  In fact, by default, it is considered a fundamental error in the build if exports that were once frozen are found to be missing - usually this has quite serious implications for existing "clients" of DLLs etc, and will result in MAKEDEF and ELF2E32 errors, depending on the build configuration.  However, assuming that the impact is known, the process to ABSENT missing exports is as follows:

{{{
    sbs -k
    sbs -c default.remove_freeze freeze
}}}

The first step above basically amounts to "Build my component(s) and keep-going - I expect errors due to missing exports, but I need a build of them so that the build system can create a temporary .def file showing the current exports".  The second step ensures that, when freezing, the EFREEZE script will be launched with its "-r" option, permitting the ABSENT-ing of exports found the be missing when the current exports are compared to the frozen ones.

The sort of errors you will see from the first step will depend on the build configurations processed.  For the emulator you should expect to see MAKEDEF errors:

{{{
    MAKEDEF ERROR: 1 Frozen Export(s) missing from object files (POSSIBLE COMPATIBILITY BREAK):
     M:/src/examples/Basics/bwins/createstaticdllu.def(2) : ?ShowMessage@CMessenger@@QAEXXZ @1
}}}

...and for ARM builds, errors from ELF2E32:

{{{
    elf2e32 : Error: E1036: Symbol _ZN10CMessenger11ShowMessageEv Missing from ELF File : M:/builds/tb101sf/epoc32/release/armv5/udeb/createstaticdll.dll.sym
}}}

Attempting the second step will show additional EFREEZE output listing the ABSENT-ing of the missing exports:

{{{
    EFREEZE: Marking 1 Export(s) as ABSENT in M:/src/examples/Basics/bwins/createstaticdllu.def :
     ?ShowMessage@CMessenger@@QAEXXZ @ 1 NONAME ; void CMessenger::ShowMessage(void)
    EFREEZE: Marking 1 Export(s) as ABSENT in M:/src/examples/Basics/eabi/createstaticdllu.def :
     _ZN10CMessenger11ShowMessageEv @ 1 NONAME
}}}

In the above example, both emulator and ARM .def files have been updated to mark the missing ShowMessage(void) export as ABSENT; ordinal 1 will now remain allocated, but ABSENT, and any following exports in the .def files will respect this.

== TBD ==

After discussing a related issue, it's clear that there's a PREPDEF shaped hole in this story that needs to be filled.



= MMP keywords =

==  One Line Keywords  ==

The following single-line MMP keywords are recognised by Raptor.

=== AIF ===

=== ALWAYS_BUILD_AS_ARM  ===

=== APPLY ===

Sets a variant as though it had been added to the {{{-c}}} option, but only for this MMP file. For example, suppose an MMP file describes an executable with so much debugging information that the linker cannot link the debug version. Then its MMP file could contain the following line:
{{{
 APPLY nodebug
}}}

This would cause that executable (only; no other MMPs are affected) to be built as though the {{{-c}}} option had included {{{.nodebug}}}. This would suppress the creation of debugging information for this executable.

Any variant can be applied, but beware of applying variants that are not compatible with all configurations for which the MMP file might be invoked.

=== ARMFPU ===

Valid options are: 

 *  {{{softvfp}}}[[BR]]
 *  {{{vfpv2}}}[[BR]]
 *  {{{softvfp+vfpv2}}}[[BR]]
 *  {{{softvfp+vfpv3}}} (from the version *after* SBS v2.15.3 - no version number yet, but likely to be 2.15.4)

=== ASSPABI ===

=== ASSPEXPORTS ===

=== ASSPLIBRARY ===

=== BYTEPAIRCOMPRESSTARGET ===

=== CAPABILITY ===

=== COMPRESSTARGET ===

=== DEBUGGABLE ===

=== DEBUGGABLE_UDEBONLY ===

=== DEBUGLIBRARY ===

Libraries listed after this keyword will only be linked into debug versions of an executable (e.g an armv5 udeb exe)

=== DEFFILE ===

=== DOCUMENT ===

=== EPOCALLOWDLLDATA ===

=== EPOCCALLDLLENTRYPOINTS ===

=== EPOCFIXEDPROCESS ===

=== EPOCHEAPSIZE ===

=== EPOCNESTEDEXCEPTIONS ===

This keyword allows an executable to have up to three concurrently active C++ exceptions. This will be used for Qt applications from Symbian^4 onwards and may be useful when porting applications from other systems, but should never be needed for native Symbian applications. The cost of EPOCNESTEDEXCEPTIONS is at least 320 bytes worth of heap space per thread.

The keyword only has an effect when building for the ARM target (for other targets it is ignored). It is only applicable to MMP files with TARGETTYPE  set to ''EXE'' or ''STDEXE''.

=== EPOCPROCESSPRIORITY ===

=== EPOCSTACKSIZE ===

=== EXPORTLIBRARY ===

=== EXPORTUNFROZEN ===

=== FEATUREVARIANT ===

An executable (EXE or DLL for example) marked as {{{FEATUREVARIANT}}} in its .mmp file is considered "feature variant".

Feature variant binaries are not usually built in a normal build (using, for example {{{sbs -c armv5_urel}}}, but will be built to {{{epoc32/release/armv5.<productname>}}} using {{{sbs -c armv5_urel.<productname>}}}. {{{<productname>}}} could be, for example, {{{vasco}}} or {{{gecko79T}}}.

To find the possible values for {{{<productname>}}}, use:
{{{
 sbs --query=products
}}}

For more information on controlling whether a {{{FEATUREVARIANT}}} executable is built in a normal build or not, please see [wiki:Raptor_Binary_Variation#Controlling_FEATUREVARIANT_Output_with_FEATUREVARIANTSAFE SDK FEATURESAFE option]

=== FIRSTLIB ===

=== INFLATECOMPRESSTARGET ===

=== LANG ===

=== LIBRARY ===

=== LINKAS ===

=== LINKEROPTION ===

=== MACRO ===

=== NEWLIB ===

=== NOCOMPRESSTARGET ===

=== NOEXPORTLIBRARY ===

=== NOLINKTIMECODEGENERATION ===

=== NOMULTIFILECOMPILATION ===

=== NOSTDCPP ===

=== NOSTRICTDEF ===

=== OPTION_REPLACE ===

=== OPTION ===

valid tools are 'ARMCC', 'CW', 'GCC', 'MSVC', 'GCCXML', 'ARMASM', 'GCCE'

=== PAGED ===

{{{PAGED}}}

In old kits which '''do not set''' POSTLINKER_SUPPORTS_WDP to ''true'' this keyword specifies that the code of this executable '''can''' be demand paged.

This keyword implies the BYTEPAIRCOMPRESSTARGET keyword. The executable is compressed using byte pair compression scheme, which has a compression ratio of 68% and decompression is faster when compared to the other compression schemes.

In newer kits which '''do set''' POSTLINKER_SUPPORTS_WDP to ''true'' this keyword is equivalent to PAGEDCODE.

In versions of sbs '''before 2.13.0''' this keyword was equivalent to PAGEDCODE plus PAGEDDATA, but this was considered unsafe in a semi-WDP environment.

This keyword will eventually be deprecated, so use PAGEDCODE instead for new projects.

=== PAGEDCODE ===

{{{PAGEDCODE}}}

Specifies that the '''code''' of this executable '''can''' be demand paged.

This keyword implies the BYTEPAIRCOMPRESSTARGET keyword. The executable is compressed using byte pair compression scheme, which has a compression ratio of 68% and decompression is faster when compared to the other compression schemes.

Available in kits which set POSTLINKER_SUPPORTS_WDP to ''true''.

=== PAGEDDATA ===

{{{PAGEDDATA}}}

Specifies that the '''data''' of this executable '''can''' be demand paged.

This keyword implies the BYTEPAIRCOMPRESSTARGET keyword. The executable is compressed using byte pair compression scheme, which has a compression ratio of 68% and decompression is faster when compared to the other compression schemes.

Available in kits which set POSTLINKER_SUPPORTS_WDP to ''true''.

=== RAMTARGET ===

=== RESOURCE ===

=== ROMTARGET ===

=== SECUREID ===

=== SMPSAFE ===

=== SOURCEPATH ===

{{{
 SOURCEPATH ../source
 SOURCE foo.cpp
 SOURCEPATH ../source/nested
 SOURCE bar.cpp
}}}

Sets the directory (relative to the directory in which this MMP file resides) in which to look for source files (given by any following {{{SOURCE}}} directive). In this example, {{{foo.cpp}}} is found in {{{../source}}} and {{{bar.cpp}}} is found in {{{../source/nested}}}.

Each {{{SOURCEPATH}}} directive overrides the last one. That is, a {{{SOURCEPATH}}} directive is in force only until the next {{{SOURCEPATH}}} directive is encountered in the same file.

{{{SOURCEPATH}}} directives do not contain multiple directories, so {{{SOURCEPATH ../source;../inc}}} is illegal.

=== SOURCE ===

{{{
 SOURCE foo.cpp bar.cpp
 SOURCE baz.cpp
}}}

Sets source files to be compiled. In this case, {{{foo.cpp}}}, {{{bar.cpp}}} and {{{baz.cpp}}}. It does not matter how many source files are listed for each {{{SOURCE}}} directive, or how many {{{SOURCE}}} directives there are.

The path to each source file is given by the last mentioned  {{{SOURCEPATH}}} directive.

Files listed in a {{{SOURCE}}} directive may use relative paths from their {{{SOURCEPATH}}}.

=== SRCDBG ===

=== STATICLIBRARY ===

=== STDCPP ===

=== STRICTDEPEND ===

=== SYSTEMINCLUDE ===

=== SYSTEMRESOURCE ===

=== TARGETPATH ===

=== TARGET ===

=== TARGETTYPE ===

=== TRACES ===

From version 2.15.1 TRACES indicates that your code contains tracepoints.  If the trace compiler is enabled in the build this will ensure it is run for your project.  It is no longer necessary to add a SYSTEMINCLUDE or USERINCLUDE to locate the trace header files as the TRACES feature does that for you.  It also causes the   OST_TRACE_IN_USE macro to be defined such that your code can protect access to trace headers and only include them if tracing is enabled in the build.

TRACES causes a directory to be created for trace header files.  For the sake of uniqueness the name includes the name of the binary (e.g. traces_hello_exe for hello.exe) as there are many components out there where similarly named source files would otherwise produce clashing trace header files.

You may also specify a relative path ("TRACES <path>") if the structure of your project makes the default location unsuitable.  The default is "../" which assumes that your mmp file is in a "/group" folder and therefore attempts to create the trace header file directory at the same level as /group.  Some components that do not follow the normal layout might need to use the parameter to ensure that the trace headers are created in a suitable location.

(Tracing is enabled when the .tracecompile variant is used and in some kits/SDKs it is enabled by default).

=== UNPAGED ===

{{{UNPAGED}}}

In old kits which '''do not set''' POSTLINKER_SUPPORTS_WDP to ''true'' this keyword specifies that the code and data of this executable '''cannot''' be demand paged.

In newer kits which '''do set''' POSTLINKER_SUPPORTS_WDP to ''true'' this keyword is equivalent to UNPAGEDCODE plus UNPAGEDDATA.

This keyword will eventually be deprecated, so use UNPAGEDCODE and UNPAGEDDATA instead for new projects.

=== UNPAGEDCODE ===

{{{UNPAGEDCODE}}}

Specifies that the '''code''' of this executable '''cannot''' be demand paged.

Available in kits which set POSTLINKER_SUPPORTS_WDP to ''true''.

=== UNPAGEDDATA ===

{{{UNPAGEDDATA}}}

Specifies that the '''data''' of this executable '''cannot''' be demand paged.

Available in kits which set POSTLINKER_SUPPORTS_WDP to ''true''.

=== USERINCLUDE ===

=== VENDORID ===

=== VERSION ===

=== WCHARENTRYPOINT ===

==  Keyword Blocks  ==

The following MMP keyword blocks are recognised by Raptor.

===  START ARMCC ===

ARMRT [[BR]]
ARMINC [[BR]]
ARMLIBS

=== START BITMAP ===

SOURCE [[BR]]
SOURCEPATH [[BR]]
TARGETPATH [[BR]]
HEADER

=== START RESOURCE ===

TARGET [[BR]]
TARGETPATH [[BR]]
UID [[BR]]
DEPENDS [[BR]]
LANG [[BR]]
HEADER [[BR]]
HEADERONLY

=== START STRINGTABLE ===

EXPORTPATH [[BR]]
HEADERONLY

=== START TOOLS ===

WIN32_LIBRARY [[BR]]

=== START WINS ===

BASEADDRESS [[BR]]
WIN32_LIBRARY [[BR]]
WIN32_RESOURCE [[BR]]
WIN32_HEADERS [[BR]]
COPY_FOR_STATIC_HEADERS



= BLD.INF keywords =

== BLD.INF syntax ==

=== Overview ===

The {{{bld.inf}}} contains four different types of information: Platforms to be built for, project (MMP) files, extensions (non-standard build steps) and exports to be copied before the build starts in earnest.

Each of these pieces of data is contained in a section headed by one of the section identifiers {{{PRJ_PLATFORMS}}}, {{{PRJ_MMPFILES}}}, {{{PRJ_EXTENSIONS}}}, {{{PRJ_EXPORTS}}}, {{{PRJ_TESTMMPFILES}}}, {{{PRJ_TESTEXTENSIONS}}}, {{{PRJ_TESTEXPORTS}}} (case is not significant here; lowercase will do just as well).

Each type of section can be present any number of times (including none); this means the same as having all the contents of each section of the same type concatenated together.

'''warning:''' this means that you cannot make one {{{PRJ_PLATFORMS}}} list apply to one {{{PRJ_MMPFILES}}} and another {{{PRJ_PLATFORMS}}} apply to another {{{PRJ_MMPFILES}}}. All the platforms apply to all the MMP files unless pre-processor tricks are used; see below.

The C pre-processor is invoked before parsing the {{{bld.inf}}} file with the system-wide {{{.hrh}}} file preincluded and platform macros defined. This means that pre-processor tricks can be used to select different projects with different features or even platforms. C and C++ style comments may also be used.

'''warning:''' Although {{{bld.inf}}}s can be included into each other, this may not have the desired effect because the {{{PRJ_PLATFORMS}}} sections will be combined as described above.

=== PRJ_PLATFORMS ===

Declare the platforms to be built for in the {{{PRJ_PLATFORMS}}} section. For example:

{{{
 PRJ_PLATFORMS
 WINSCW ARMV5
}}}

'''warning:''' Any text on the same line as PRJ_PLATFORMS is treated as a comment and ignored!

=== PRJ_EXPORTS ===

Declare files that must be copied before the main part of the build starts in the {{{PRJ_EXPORTS}}} section. A source file name on its own will be copied to {{{%EPOCROOT%epoc32/include}}}. Relative destination paths will be considered to be relative to {{{%EPOCROOT%epoc32/include}}}. Absolute paths with drive letters will be copied to {{{%EPOCROOT%epoc32/data/&lt;drive-letter&gt;/&lt;path&gt;/{{{.

A destination ending in a slash will be considered a directory, and the file name of the copy will match the file name of the source.

A destination not ending in a slash will be considered a file name, and the copy will have this name.

{{{
 PRJ_EXPORT
 foo.h                       // copied to epoc32/include/foo.h
 bar2.h    myfolder/bar.h    // copied to epoc32/include/myfolder/bar.h
 baz.h     e:/               // copied to epoc32/data/e/
                             // and also epoc32/release/winscw/urel|udeb/e/
                             // if WINSCW is a platform
}}}

{{{PRJ_TESTEXPORTS}}} is the same, but will be run only in a test build.

==== :zip  ====

A line of the form "{{{:zip <i>source</i> <i>destination</i>}}}" will unzip the source file to the path indicated by "''destination''", but note that, for some reason, if the destination path is missing it will default to the {{{bld.inf}}}'s directory. Also, the destination will always be considered a path, even if it does not end in a slash.

==== :xexports ====

This feature is available from version '''2.16.8'''.

A line of the form "{{{xexport[options] source destination}}}" will copy the files in the directory ''source'' to the directory ''destination''.

''options'' is a space-separated list of options, each one is a name and value separated by {{{=}}}.

Available options are:

||= option =||= description =||= default =||
|| {{{match=pattern}}} || Limits copies to source files matching ''pattern'' ({{{?}}} matches a single character and {{{*}}} matches multiple characters) || {{{*}}} ||
|| {{{recursive=true/false}}} || If {{{true}}} applies operations to subdirectories. The directory tree with be copied; i.e. the subfolders that contain matching files will be generated in the destination directory and each file copied will have the same relative path to the destination directory as its source had to the source directory || {{{false}}} ||

Example:

File System - Source

{{{
 /component/bld.inf
 /component/dir1/file1dir1.txt
 /component/dir1/file2dir1.txt
 /component/dir1/dir2/file1dir2.txt
 /component/dir1/dir2/file2dir2.txt
 /component/dir1/dir2/dir3/file1dir3.txt
 /component/dir1/dir2/dir3/file2dir3.txt
}}}

/component/bld.inf

{{{
 PRJ_EXPORTS
 
 dir1/file1dir1.txt                           destdir1
 :xexport dir1/dir2                           destdir2
 :xexport[recursive=true] dir1/dir2           destdir3
 :xexport[match="*1dir?.txt"] dir1/dir2       destdir4
 :xexport[match="*1dir?.txt" recursive=true]  dir1/dir2  destdir5/subdir
}}}

File System - Destination

{{{
 $EPOCROOT/epoc32/include/destdir1/file1dir1.txt
 
 $EPOCROOT/epoc32/include/destdir2/file1dir2.txt
 $EPOCROOT/epoc32/include/destdir2/file2dir2.txt
 
 $EPOCROOT/epoc32/include/destdir3/file1dir2.txt
 $EPOCROOT/epoc32/include/destdir3/file2dir2.txt
 $EPOCROOT/epoc32/include/destdir3/dir3/file1dir3.txt
 $EPOCROOT/epoc32/include/destdir3/dir3/file2dir3.txt
 
 $EPOCROOT/epoc32/include/destdir4/file1dir2.txt
 
 $EPOCROOT/epoc32/include/destdir5/subdir/file1dir2.txt
 $EPOCROOT/epoc32/include/destdir5/subdir/dir3/file1dir3.txt
}}}

===  PRJ_MMPFILES ===

A list of MMP files. {{{PRJ_TESTMMPFILES}}} is the same, but for test builds.

===  PRJ_EXTENSIONS ===

TODO.

{{{PRJ_TESTEXTENSIONS }}} is the same, but for test builds.




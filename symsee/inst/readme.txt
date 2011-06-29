Installing Raptor from the zip provided

Unzip the zip and set the path to point to the bin directory.

If you want to unbundle Python, Cygwin or MinGW, or if you want to set up
integration with RVCT or GCCE compilers, please follow the instructions on the
SF Wiki at:

http://alfonse.europe.nokia.com/mediawiki/index.php/Raptor_Environment_Variables

This will tell you how to set up the various environment variables to point to
the unbundled tools which you will have to have installed separately.

A more complete set of environment variables for even more tool locations can
be found in the notes/tools_env_vars.txt file.  This file is also reproduced
alonside this readme file.

***PLEASE NOTE*** Please do not set SBS_HOME, it can now only cause trouble.

***PLEASE NOTE*** Do not set SBS_PYTHON or any other variable to point to
bundled tools within the Raptor distribution, as this will break if we change
their locations. Please leave such variables unset.

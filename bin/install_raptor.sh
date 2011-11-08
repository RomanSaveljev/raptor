#!/bin/bash
# raptor script

# install sbsv2

# parse command line options
# -s indicates silent (non-interactive operation); the dialog utility is not used in this mode and
#    the -i option is required; if the -i is missing, the script exits
# -i specifies the installation directory; this is ignored in non-silent mode

# SILENT is the empty string
export SILENT=""
export SYMBIANHOME=/opt/symbian

while getopts si: VARNAME; do

	case $VARNAME in
		s)
			export SILENT=1
			echo "install_raptor.sh: operating in silent mode"
		;;
		i)
			export INSTALL_DIR=$OPTARG
			echo "install_raptor.sh: given installation directory is $INSTALL_DIR"
		;;
	esac
done

# exit if no installation directory is given in silent mode
if [[ $SILENT ]]; then
	if [[ -z $INSTALL_DIR ]]; then
		echo "install_raptor.sh: error: no installation directory specified. Unable to continue. Exiting."
		exit 1
	else
		echo "install_raptor.sh: using installation directory $INSTALL_DIR"
	fi
else
	if [[ ! -z $INSTALL_DIR ]]; then
		echo "install_raptor.sh: remark: installation directory, $INSTALL_DIR, specified in interactive mode. Ignoring."
	fi
fi

chmod a+x "${PWD}/bin/gethost.sh"
export HOSTPLATFORM=$("$PWD/bin/gethost.sh")
export HOSTPLATFORM_DIR=$("$PWD/bin/gethost.sh" -d)

export build_utils=no
if [[ ! -d "$PWD/$HOSTPLATFORM_DIR" ]]; then
cat << MSG

The Raptor installer has determined that this computer is running:
	$HOSTPLATFORM_DIR
This platform is not directly supported by the installer.

If you proceed then the installation will attempt to build the Raptor tools for your platform.

Your system must have some tools installed:
MSG

if [ "$(which gcc)" ]; then
   echo "You appear to have gcc"
else
   echo "You DON'T appear to have gcc - please install it"
fi

if [ "$(which g++)" ]; then
   echo "You appear to have gcc-c++"
else
   echo "You DON'T appear to have gcc-c++ (also called g++) - please install it"
fi

if [ "$(which make)" ]; then
   echo "You appear to have GNU make"
else
   echo "You DON'T appear to have GNU make - please install it (version 3.81)"
fi

if [ "$(which bison)" ]; then
   echo "You appear to have GNU bison"
else
   echo "You DON'T appear to have GNU bison - please install it "
fi

if [ -f "/usr/include/ncurses.h" ]; then
   echo "You appear to have the ncurses dev libraries"
else
   echo "You DON'T appear to have the ncurses dev libraries - please install them (ncurses-dev or ncurses-devel)"
fi

if [ -f "/usr/include/bzlib.h" ]; then
   echo "You appear to have the bzip2 dev libraries"
else
   echo "You DON'T appear to have the bzip2 dev libraries - please install them (bzip2-dev or bzip2-devel)"
fi

echo "Do you wish to continue (Y or y for 'yes' anything else for no)?"

read X
if [[  "$X" != "y" && "$X" != "Y" ]]; then
	exit 1
else
	build_utils=yes
fi


# Build the dialog utility so that we can get started
if [[ ! $SILENT ]]; then
(export SBS_HOME=$PWD;cd "$SBS_HOME/util" && echo "Building dialog utility..." && (make -k -j2 dialog> dialog_util_build.log 2>&1 && echo -e "\nBuild Complete") || (echo "Dialog utility build failed, see $PWD/dialog_util_build.log for more details"; read X; exit 1)) || exit 1
fi

fi

export DIALOG="$PWD/$HOSTPLATFORM_DIR/bin/dialog"
chmod a+x "$DIALOG"

test -w "$SYMBIANHOME"
if [[ $? -ne 0 ]]; then
	SYMBIANHOME=$(echo ~)
fi

export TMPSBSDIR="$PWD"

errorexit() {
        echo -e "\nRaptor installation aborted: $1" 1>&2
	echo -e "\nInstall tmp dir is $TMPSBSDIR" 1>&2
	exit 1
	}
	

# get FULLVERSION and VERSION from .version file
export FULLVERSION=""
export VERSION=""
eval $(cat .version)


if [[ "$FULLVERSION" == "" || "$VERSION" == "" ]]; then
	errorexit "Bad install package - no version found." 
fi


export RESPONSEFILE=$PWD/.installdir
export MANIFEST=$PWD/.manifest
export SBS_HOME=$SYMBIANHOME/raptor-$(echo "$VERSION" | sed 's#\.##g')

if [[ ! $SILENT ]]; then
	DIALOGVER=$($DIALOG --version)

	if  ! expr match "$DIALOGVER" "Version:" 2>&1 >/dev/null; then
		errorexit "Could not run the installation user interface on this version of Linux.\nPlease install the compat-glibc and compat-ncurses packages (RedHat) or the equivalent for your distribution and then try again.\n\nYou may also simply 'untar' raptor using the ' --target NewDirectory --noexec' options to this installer.\n"
	fi

	export DIALOGSBS=$DIALOG "--backtitle 'Installing $FULLVERSION'"
	$DIALOGSBS --msgbox "Symbian Build System Installer\n\n$FULLVERSION" 0 0
	
	# check what SBS_HOME
	$DIALOGSBS --title "Select Symbian Home Directory" --fselect  "$SBS_HOME"  10 50   2> "$RESPONSEFILE"
	SBS_HOME=$(cat "$RESPONSEFILE")
else
	SBS_HOME=$INSTALL_DIR
fi

if [[ ! -d "$SBS_HOME" ]]; then
	if [[ ! $SILENT ]]; then
		$DIALOGSBS --yesno  "$SBS_HOME does not exist - should it be created?" 0 0; YESNO=$?
	else
		# always make the directory in silent mode
		YESNO=0
	fi
	if [[ "$YESNO" -eq 0 ]]; then
		mkdir -p "$SBS_HOME" || 
		(
			errorexit "Could not create directory $SBS_HOME"
		)
	else
		errorexit "SBSv2 Installation aborted: User chose not to create installation directory $SBS_HOME" 
	fi
else
	# check if there's a previous install and give an option to stop in interactive mode
	if [[ ! $SILENT ]]; then
		$DIALOGSBS --defaultno --yesno  "$SBS_HOME already exists - should the installation be overwritten?" 0 0; YESNO=$?
	else
		# always abort in silent mode
		YESNO=1
	fi
	
	if [[ "$YESNO" -eq 1 ]]; then
		errorexit "Not replacing existing installation." 
	fi
fi

# Install the software
if [[ ! $SILENT ]]; then
	echo "" >"$MANIFEST"
	(tar -cf - *) | (cd $SBS_HOME && tar -xvf - > "$MANIFEST" && echo -e "\nCopying complete - press RETURN" >> "$MANIFEST") &
	(
	$DIALOGSBS --title "Copying SBS files" --tailbox "$MANIFEST" 20 60 
	)
else
	(tar -cf - *) | (cd $SBS_HOME && tar -xvf - && echo -e "\nCopying complete") 
fi


dobuildutils() {
cd "$SBS_HOME/util" && echo "Building utilities ..." && make -k -j2  
if [[ $? -eq 0 ]]; then
	echo -e "\nBuild Complete" 
else
	echo -e "\nUtility build failed, see $BUILDLOG for more details"
	exit 1
fi
}

# Build the utilities if needed 
if [[ "$build_utils" == "yes" ]]; then
	BUILDLOG=$SBS_HOME/util/util_build.log
	if [[ ! $SILENT ]]; then
		( dobuildutils ) > "$BUILDLOG" 2>&1  & (
		$DIALOGSBS --title "Building utilities for $HOSTPLATFORM_DIR" --tailbox "$BUILDLOG" 20 60 
		)
	else
		( dobuildutils 2&>1 ) | tee "$BUILDLOG"
	fi
fi

# Force sbs to be executable:
chmod a+x "${SBS_HOME}/bin/sbs"
chmod a+x "${SBS_HOME}/bin/gethost.sh"
chmod a+x "${SBS_HOME}/bin/setup_user.sh"
chmod -R a+r "${SBS_HOME}"
chmod a+x "${SBS_HOME}/$HOSTPLATFORM_DIR/bin/"*
chmod a+x "${SBS_HOME}/$HOSTPLATFORM_DIR/bv/bin/"* 
chmod a+x "${SBS_HOME}/$HOSTPLATFORM_DIR/bv/libexec/"*/*/*


# Prepare user scripts for bashrc and bash_profile
INSTALLER="${SBS_HOME}/util/install-linux"
sed "s#__SBS_HOME__#${SBS_HOME}#" < "${INSTALLER}/linux_bash_profile" > "${SBS_HOME}/bin/user.bash_profile"
sed "s#__SBS_HOME__#${SBS_HOME}#" < "${INSTALLER}/linux_bashrc" > "${SBS_HOME}/bin/user.bashrc"

# Set symbolic link
if [[ -L "$SYMBIANHOME/raptor" ]]; then
	rm "$SYMBIANHOME/raptor"
fi

if [[ ! -e "$SYMBIANHOME/raptor" ]]; then
	ln -s  "$SBS_HOME" "$SYMBIANHOME/raptor"
fi

if [[ ! $SILENT ]]; then
	$DIALOGSBS --msgbox "Raptor $VERSION\ninstallation complete" 0 0
else
	echo "Raptor $VERSION installation complete" 
fi



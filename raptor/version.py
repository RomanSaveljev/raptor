#
# Copyright (c) 2006-2014 Microsoft Mobile and/or its subsidiary(-ies).
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
# raptor version information module

# replace ISODATE with the creation date of the release
# replace CHANGESET with the Hg changeset of the release
#
# both of these are done automatically by the installer builder.

name = 'sbs' # Raptor's name
version=(2,17,5,"ISODATE","symbian build system","CHANGESET")

def numericversion():
	"""Raptor version string"""
	return "{0}.{1}.{2}".format(*version[:3])

def fullversion():
	"""Raptor version string"""
	return "{0}.{1}.{2} [{3} {4} {5}]".format(*version)

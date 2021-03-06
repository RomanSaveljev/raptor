/*
* Copyright (c) 2009-2014 Microsoft Mobile and/or its subsidiary(-ies).
* All rights reserved.
* This component and the accompanying materials are made available
* under the terms of the License "Eclipse Public License v1.0"
* which accompanies this distribution, and is available
* at the URL "http://www.eclipse.org/legal/epl-v10.html".
*
* Initial Contributors:
* Nokia Corporation - initial contribution.
*
* Contributors:
*
* Description: 
*
*/




#include "log.h"
#include <stdarg.h>
#include <stdio.h>

int loglevel=LOGNORMAL;
int debug(const char *format, ...)
{
	int rt=0;
	
	if (loglevel >= LOGDEBUG)
	{
		va_list ap;
		va_start(ap, format);
		rt = vfprintf(stderr, format,  ap);
		va_end(ap);

	}

	return rt;
}


int error(const char *format, ...)
{
	int rt=0;
	
	if (loglevel >= LOGNORMAL)
	{
		va_list ap;
		va_start(ap, format);
		rt = vfprintf(stderr, format,  ap);
		va_end(ap);

	}

	return rt;
}

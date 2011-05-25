/*
* Copyright (c) 2011 Nokia Corporation and/or its subsidiary(-ies).
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
* Description: functions for manipulating environment variables.
*
*/

#include "../config.h"

#ifdef HAS_WINSOCK2
#include <winsock2.h>
#include <ws2tcpip.h>
#define WIN32_LEAN_AND_MEAN
#endif


#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <stdio.h>
#include <fcntl.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <stdarg.h>

#include "env.h"
#include "log.h"

void talon_setenv(char name[], char val[])
{
#if defined(HAS_GETENVIRONMENTVARIABLE)
	SetEnvironmentVariableA(name,val); 
#elif defined(HAS_GETENV)
	setenv(name,val, 1);
#else
#	error "Need a function for setting environment variables"
#endif
}

char * talon_getenv(char name[])
{
#if defined(HAS_SETENV)
	char *val = getenv(name);
	char *dest = NULL;
	
	if (val)
	{
		dest = malloc(strlen(val) + 1);
		if (dest)
		{
			strcpy(dest,val);
		}
	}
	return dest;
#elif defined(HAS_SETENVIRONMENTVARIABLE)
	char *val = malloc(TALON_MAXENV);
	if (0 != GetEnvironmentVariableA(name,val,TALON_MAXENV-1))
		return val;
	else
		return NULL;
#else
#	error "Need a function for setting environment variables"
#endif
}

int talon_pathprepend(char value[])
{
	int extra_length = strlen(value);
	int path_length;
	char *path = talon_getenv("PATH");
	char *new_path;

	if(path != NULL)
	{
		path_length = strlen(path);
		new_path = malloc(sizeof(char) * (1 + 1 + path_length + extra_length));

		if(new_path != NULL)
		{
			new_path[0] = '\0';
			new_path = strcat(new_path, value);
			new_path = strcat(new_path, ";");
			new_path = strcat(new_path, path);
			talon_setenv("PATH", new_path);
			DEBUG(("talon_pathprepend: PATH set to %s\n", new_path));

			free(new_path);
			free(path);

			return 0;
		}
		else
		{
			return -1;
		}
	}
	else
	{
		return -1;
	}

}

int talon_pathappend(char name[])
{
	return 0;
}

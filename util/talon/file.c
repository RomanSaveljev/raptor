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
* Description: 
*
*/

#include "../config.h"
#include "file.h"
#include "log.h"

#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#ifdef HAS_MSVCRT
#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#endif

/*
 * is_file - tests if the given string is an existing file
 * value: C string of a filename to check for existence. Note, that
 * no manipulation or "tidying up" is done, e.g. no double \'s are fixed, nor
 * is any conversion of / to \ done.
 * Returns -1 on error; 0 if the file does not exist; 1 if the file exists
 */

int is_file(char name[])
{
	int ret_val = 1;
#ifdef HAS_MSVCRT
	/*
	 * This can be changed to use fstat as this is available on Windows.
	 */
	WIN32_FIND_DATA find_file_data;
	HANDLE handle;
	LPVOID msg_buff;

	handle = FindFirstFile(name, &find_file_data);

	if (handle == INVALID_HANDLE_VALUE)
	{
		DWORD last_error = GetLastError();
		FormatMessage(
		        FORMAT_MESSAGE_ALLOCATE_BUFFER |
		        FORMAT_MESSAGE_FROM_SYSTEM |
		        FORMAT_MESSAGE_IGNORE_INSERTS,
		        NULL,
		        last_error,
		        MAKELANGID(LANG_NEUTRAL, SUBLANG_DEFAULT),
		        (LPTSTR) &msg_buff,
		        0, NULL );

		if(last_error == ERROR_FILE_NOT_FOUND || last_error == ERROR_PATH_NOT_FOUND)
		{
			DEBUG(("File \"%s\" does not exist (error code: %d):\n%s\n",
					name, last_error, msg_buff));
			ret_val = 0;
		}
		else
		{
			DEBUG(("FindFirstFile failed (error code: %d)\n"
					"Unable to determine existence of \"%s\":\n%s\n",
					last_error, name, msg_buff));
			ret_val = -1;
		}
		LocalFree(msg_buff);
		return ret_val;
	}
	else
	{
		DEBUG(("The first file found is %s\n", find_file_data.cFileName));
		FindClose(handle);
		return 1;
	}
#else
	return 0;
#endif
}

char *get_cwd(void)
{
#if defined(HAS_GETCURRENTDIRECTORY)
	int limit = 32000;
	char * cwd = malloc(limit * sizeof(char));
	if(cwd)
	{
		GetCurrentDirectory(limit, cwd);
		DEBUG(("get_cwd: current working directory calculated as: %s\n", cwd));
		return cwd;
	}
	else
		return NULL;
#else
#	error "Need a function for getting the current working directory"
#endif
}

char *get_exe_location(void)
{
#if defined(HAS_MSVCRT)

	char *full_path_to_exe = malloc(32000*sizeof(char *));
	DWORD last_error;
	LPVOID msg_buff;

	if(full_path_to_exe)
	{
		// GetModuleFileName: giving NULL as the first argument retrieves the
		// path of the executable file of the current process.
		DWORD dw = GetModuleFileName(NULL, full_path_to_exe, 32000);
		if(dw != 0)
		{
			DEBUG(("Full path to this exe is: %s\n", full_path_to_exe));
			return full_path_to_exe;
		}
		else
		{
			last_error = GetLastError();
			FormatMessage(
				FORMAT_MESSAGE_ALLOCATE_BUFFER |
				FORMAT_MESSAGE_FROM_SYSTEM |
				FORMAT_MESSAGE_IGNORE_INSERTS,
				NULL,
				last_error,
				MAKELANGID(LANG_NEUTRAL, SUBLANG_DEFAULT),
				(LPTSTR) &msg_buff,
				0, NULL );
			DEBUG(("Failed to determine the full path to this exe: %s\n", msg_buff));
			LocalFree(msg_buff);
			return NULL;
		}
	}
	else
		return NULL;
#else
#	error "Need a function for getting the full path of the currently execting process"
#endif
}

char *get_parent_dir(char dir[])
{
	if(dir == NULL)
		return NULL;

	int len = strlen(dir);
	int start = len - 1;

	/* If dir ends with /, skip it in the searching */
	if(dir[start] == SEP)
		start--;

	while(dir[start] != SEP)
		start--;

	char *parent_dir = malloc(len * sizeof(char));
	if(parent_dir)
	{
		strncpy(parent_dir, dir, start);
		parent_dir[start] = '\0';
		return parent_dir;
	}
	return NULL;
}

char *path_join(char component1[], char component2[])
{
	if(component1 == NULL)
		return component2;

	if(component2 == NULL)
			return component1;

	// Enough space for strings and extra SEP characters
	int full_length = strlen(component1) + strlen(component2) + 5;
	char *joined_path = malloc(full_length);

	if(joined_path != NULL)
	{
		DEBUG(("Joining paths %s and %s\n", component1, component2));
		snprintf(joined_path, full_length, "%s%sc%s", component1, SEP, component2);
		DEBUG(("Joined path is: s\n", joined_path));
		return joined_path;
	}
	else
	{
		DEBUG(("Joining paths %s and %s failed.\n", component1, component2));
		return NULL;
	}
}

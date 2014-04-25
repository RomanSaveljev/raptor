/*
* Copyright (c) 2011-2014 Microsoft Mobile and/or its subsidiary(-ies).
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

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <fcntl.h>

#include "env.h"
#include "log.h"
#include "buffer.h"
#include "talon_process.h"
#include "file.h"

#ifdef HAS_MSVCRT
  /* Make all output handling binary */
  unsigned int _CRT_fmode = _O_BINARY;
#endif


#define OUTPUT_UNWANTED 0
#define OUTPUT_WANTED 1
#define OUTPUT_UNBUFFERED 2
#define OUTPUT_BUFFERED 3

typedef struct env_vars
{
	char name[1000];
	char value[1000];
} env_var;

env_var sbs_env[] =
{
	{"HOSTPLATFORM", "win 32"},
	{"HOSTPLATFORM_DIR", "win32"},
	{"HOSTPLATFORM32_DIR", "win32"},
	{"SBS_HOME", "C:\\build_c\\hg\\raptor"},
	{"__PYTHON__", "C:\\build_c\\Apps\\Python270\\python.exe"},
	{"PYTHONPATH", "C:\\build_c\\hg\\raptor\\raptor"},
	{"__MINGW__", "C:\\build_c\\hg\\win32-support\\mingw"},
	{"__MOUNTOPTIONS__", "-u"},
	{"__UMOUNTOPTIONS__", "-u"},
	{"CYGWIN", "nontsec nosmbntsec"},
	{"__CYGWIN__", "C:\\build_c\\hg\\win32-support\\cygwin"},
};


typedef struct command_struct
{
	char *name;
	char *commandline;
} command;

command commands[] =
{
		{"umount.exe", "-u /tmp"},
		{"mount.exe",  "-u \"C:\\build_c\\hg\\win32-support\\cygwin\\tmp\" /tmp"},
		{"umount.exe", "-u /"},
		{"mount.exe",  "-u \"C:\\build_c\\hg\\win32-support\\cygwin\" /"},
		{"mount.exe", ""},
		{(char *)0, (char *)0}
};

int do_process(char executable[], char *args[], int timeout, int want_output)
{
	proc *p;
	p = process_run(executable, args, timeout);
	int retval = 0;

	if (p)
	{
		unsigned int iterator = 0;
		byteblock *bb;
		while ((bb = buffer_getbytes(p->output, &iterator)))
		{
			if(want_output)
				write(STDOUT_FILENO, &bb->byte0, bb->fill);
		}
		retval = p->returncode;
		process_free(&p);
		return retval;
	} else {
		fprintf(stderr, "error: %s", "failed to run process\n");
		return 1;
	}
}

char *get_sbs_home(void)
{
	char *sbs_home = talon_getenv("SBS_HOME");
	if(sbs_home != NULL)
		DEBUG(("SBS_HOME found in environment: %s\n", sbs_home));
	else
	{
		sbs_home = get_parent_dir(get_parent_dir(get_exe_location()));
		DEBUG(("SBS_HOME calculated as: %s\n", sbs_home));
	}

	return sbs_home;
}

char *set_python(char *sbs_home)
{
	char *sbs_python = talon_getenv("SBS_PYTHON");
	if(sbs_python != NULL)
	{
		DEBUG(("SBS_PYTHON = %s\n", sbs_python));
		return sbs_python;
	}

	char local_python[] = "win32\\python27\\python.exe";
	int size = strlen(sbs_home) + strlen(local_python) + 2;
	char *__local_python__ = malloc(size);

	snprintf(__local_python__, size, "%s\\%s", sbs_home, local_python);

	int exists = is_file(__local_python__);

	if(exists == 1) // Check that local python exists
	{
		DEBUG(("Found local Python %s\n", __local_python__));
		talon_setenv("SBS_PYTHON", __local_python__);
		talon_setenv("PYTHONPATH", "");
		talon_setenv("PYTHONHOME", "");
	}
	else
	{
		DEBUG(("Using python.exe from PATH as no local Python exists.\n"));
		// __local_python__ is already at least the length of
		// the string "python.exe" due to the malloc above, so
		// it can be reused to return "python.exe"
		snprintf(__local_python__, 11, "python.exe");
	}
	return __local_python__;
}

int main(int argc, char *argv[])
{
	int i;
	int retval = 0;
	char * talon_debug = talon_getenv("TALON_DEBUG");
	if(talon_debug != NULL)
	{
		loglevel = 1;
		free(talon_debug);
	}

	char *sbs_home = get_sbs_home();
	if(sbs_home == NULL)
	{
		printf("Error determining SBS_HOME. Cannot continue.");
		retval = -1;
	}

	char *python = set_python(sbs_home);
	DEBUG(("Using python = %s\n", python));

	/* sizeof(sbs_env)/sizeof(env_var) is the size of the sbs_env array */
	for(i = 0; i < sizeof(sbs_env)/sizeof(env_var); i++)
	{
		talon_setenv(sbs_env[i].name, sbs_env[i].value);
	}

	int path_prepend_ok = talon_pathprepend("C:\\build_c\\hg\\win32-support\\mingw\\bin;"
					"C:\\build_c\\hg\\win32-support\\cygwin\\bin;"
					"C:\\build_c\\hg\\raptor\\win32\\bin");
	if(path_prepend_ok != 0)
	{
		printf("Failed to prepend to PATH. Exiting.\n");
		return -1;
	}

	i = 0;
	char **args = malloc((argc+10)*sizeof(char *));
	while((commands[i].name != (char *)0) && (commands[i].commandline != (char *)0))
	{
		DEBUG(("command:\n%s\ncommandline:\n%s\n", commands[i].name, commands[i].commandline));
		args[0] = NULL;
		args[1] = commands[i].commandline;
		args[2] = NULL;
		retval = do_process(commands[i].name, args, 4000, OUTPUT_WANTED);
		i++;
	};

	args[0] = NULL;
	args[1] = "C:\\build_c\\hg\\raptor\\python\\raptor_start.py";

	for(i = 1; i < argc; i++)
	{
		args[i+1] = argv[i];
	}
	args[argc+1] = NULL;

	retval = do_process(python, args, 3600000, OUTPUT_WANTED);

	free(python);
	free(args);
	free(sbs_home);
	return retval;
}

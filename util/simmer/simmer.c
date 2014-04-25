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
* This program attempts to simulate the activity of a compiler.  It can
* then be used to test the scalability of the build system and measure
* the contribution of various factors to scaling.
*/


#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <stdio.h>

#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <stdarg.h>

#include "../config.h"

#include "log.h"

#ifdef HAS_MSVCRT
/* Make all output handling binary */
unsigned int _CRT_fmode = _O_BINARY;
#endif


double getseconds(void)
{
	struct timeval tp;
	gettimeofday(&tp, NULL);

	return (double)tp.tv_sec + ((double)tp.tv_usec)/1000000.0L;
}

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


#define TALON_MAXENV 4096
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

extern int sim_mallocs(int totalallocs, long allocbeforefree);

typedef struct {
	long filedata; /* roughly 800k */
	int copylen; /* length of string copies */
	int copycount; 
	int totalallocs; 
    long allocsbeforefree; /*  how many mallocs before free */
} params;

params p = {850000L,256,7966,10000,1000};

char help[]="\nsimmer: a compiler simulator for performance testing\n\
--filedata=<n>  (default 850000L)\n\
--copylen=<n>   (default 256)\n\
--copycount=<n> (default 7966)\n\
--totalallocs=<n>    (default 10000) \n\
--allocsbeforefree<n> (default 1000)\n\n";

int opt_process(params *p, int argc, char *argv[])
/* 
	Windows doesn't have getopt() and trying to copy open source implementations is tricky so
	this function will have to simulate what's "right" for the moment.
 */
{
	int i;

	for (i=1; i < argc; i++)
	{
		if (0 == strncmp(argv[i], "--filedata=", sizeof("--filedata=")-1))
		{
			p->filedata = atol(argv[i] + sizeof("--filedata="));
		} else if (0 == strncmp(argv[i], "--copylen=", sizeof("--copylen=")-1)) {
			p->copylen = atoi(argv[i] + sizeof("--copylen="));

		} else if (0 == strncmp(argv[i], "--copycount=", sizeof("--copycount=")-1)) {
			p->copycount = atoi(argv[i] + sizeof("--copycount="));

		} else if (0 == strncmp(argv[i], "--totalallocs=", sizeof("--totalallocs=")-1)) {
			p->totalallocs = atoi(argv[i] + sizeof("--totalallocs="));

		} else if (0 == strncmp(argv[i], "--allocsbeforefree=", sizeof("--allocsbeforefree=")-1)) {
			p->allocsbeforefree = atol(argv[i] + sizeof("--allocsbeforefree="));

		} else if (0 == strncmp(argv[i], "-h", sizeof("-h")-1)) {
			fprintf(stderr,"%s", help);

		} else {
			fprintf(stderr,"%s", help);
		exit(0);
		}
	}
}

int main(int argc, char *argv[])
{

	char *recipe = NULL;
	int returncode = 0;
	long j;

	opt_process(&p, argc, argv);


	sim_mallocs(p.totalallocs,p.allocsbeforefree);

	/*******************************/
	FILE *f;
	/* 	Real example:
		fwrite count: 19110
		fwrite totalbytes: 202876
		avgbytes = 11
	*/

	f = tmpfile();

	for (j=0; j < p.filedata/11 + 1; j++)
	{
		fwrite("AAAAAAAAAA\n",1,11, f);
	}

	fflush(f);



	/* Something CPU-ish */

	long X;

	/* The size of of each string copy cannot be easily determined for the 
	   program that's being simulated so this is just a guess: */

	char *buf1 = malloc(p.copylen);
	char *gap = malloc(p.copylen);
	char *buf2 = malloc(p.copylen);

	/* one measured instance of the compiler did this number of string copies
	   whilst compiling a trivial-sized program : */
	int c,i,d;

	for (i = 0; i < p.copylen - 1; i++)
		buf2[i] = 'A';

	buf2[p.copylen-1] = '\0';

	for (c = 0; c < p.copycount; c++)
	{
		strcpy(buf1, buf2);
		buf1[0]='B';  /* try to spoil the cache */
		for (d = 0; buf2[d] != '\0'; d++)
		{
			buf1[d]=toupper(tolower(buf1));
		}
	}
		
	free(buf2);
	free(gap);
	free(buf1);
	buf2 = buf1 = gap = NULL;


	/*******************************/
	/* read in the data we wrote out */

	rewind(f);

	while (!feof(f))
	{
		fgetc(f);
	}

	fclose(f);
	
		
	return returncode;
}

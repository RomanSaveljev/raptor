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
* Simulate the malloc behavior of a certain compiler. The rather
* simplistic approach is to replay a set of mallocs recorded 
* from a trivial build using said compiler.
*/

#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <stdio.h>

#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <stdarg.h>


typedef struct {
	int size;
	int count;
} analloc;

/*
   Typical malloc sizes during compilation, each followed by a count
   of how many of allocations of that size.  This is data from which
   to roughly simulate how the compiler works.
   List is in random order to try to avoid any systematic behavior and
   be as "average" as possible.

   This is an imperfect simulation but so are all simulations and
   it can be improved.
*/
analloc allocs[]={
{31, 242},
{101, 1},
{1024, 1},
{2880, 1},
{58, 5},
{100, 18966},
{52, 17},
{5, 10},
{85, 1},
{141, 1},
{17, 129},
{0, 1},
{92, 20},
{68, 9},
{18, 182},
{78, 5},
{19, 130},
{34, 175},
{80, 7},
{83, 1},
{89, 2},
{29, 203},
{3001, 1},
{97, 1},
{4096, 1},
{9, 55},
{65, 8},
{48, 21},
{46, 62},
{53, 43},
{2048, 2},
{36, 163},
{38, 158},
{79, 12},
{202, 1},
{102, 1},
{70, 1},
{1048576, 1},
{42, 76},
{124, 1},
{33, 227},
{72, 4},
{360, 1},
{81, 11},
{77, 5},
{26, 205},
{57, 2},
{86, 4},
{2000, 5},
{4001, 1},
{82, 2},
{74, 5},
{64, 7},
{12, 57},
{88, 1},
{60, 9},
{95, 5},
{40, 132},
{106, 2},
{43, 53},
{35, 140},
{824, 1},
{4000, 1},
{61, 9},
{50, 15},
{41, 82},
{84, 4},
{2, 4763},
{253, 1},
{22, 130},
{59, 3},
{67, 4},
{183, 1},
{1321, 1},
{21, 154},
{24, 232},
{137, 1},
{71, 14},
{51, 15},
{94, 4},
{25, 314},
{133, 1},
{62, 7},
{99, 1},
{193, 1},
{37, 128},
{20, 368},
{44, 32},
{90, 2},
{401, 2},
{39, 110},
{1600, 1},
{93, 3},
{7, 35},
{75, 8},
{47, 34},
{10, 35},
{55, 5},
{96, 1},
{49, 14},
{13, 50},
{15, 87},
{73, 14},
{30, 226},
{139, 2},
{8, 78},
{256, 1},
{28, 155},
{800, 38},
{1464, 1},
{14, 60},
{1, 8471},
{69, 6},
{1800, 1},
{11, 37},
{23, 149},
{372, 1},
{16, 111},
{9120, 1},
{45, 27},
{6, 19},
{56, 3},
{104, 2},
{65536, 22},
{76, 5},
{63, 9},
{66, 9},
{98, 2},
{3, 45},
{27, 196},
{54, 7},
{32, 211},
{4, 224},
{-1, -1}
};

int sim_mallocs(int totalallocs, long allocsbeforefree)
/*  totalallocs - how many allocations to do - basically runs a distance
	through the preprogrammed allocations will be enacted.
	alloccount - Allocations to build up before we free again */
{
	char **memlist = NULL;
	long i, j,k;
	long nallocs = 0L;
	long count = 0L;


	memlist = (char **)calloc(allocsbeforefree, sizeof(char *));

	for (i=0; allocs[i].size >= 0 && nallocs >= totalallocs; i++)
	{
		for (j=0; j < allocs[i].count && nallocs >= totalallocs; j++)
		{
			memlist[nallocs] = malloc(allocs[i].size);
			*memlist[nallocs] = '\0';
			nallocs++;


			if (nallocs % allocsbeforefree == 0)
			{
				for (k=0; k < allocsbeforefree; k++)
				{
					free(memlist[k]);
					memlist[k] = NULL;
				}
			}
		}
	}

	/* final cleanup check */	
	for (k=0; k < allocsbeforefree; k++)
	{
		if (memlist[k] != NULL) free(memlist[k]);
		memlist[k] = NULL;
	}

	free(memlist);
}

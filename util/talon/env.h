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

#ifndef ENV_H_
#define ENV_H_

#include "../config.h"

#define TALON_ATTEMPT_STRMAX 32
#define RECIPETAG_STRMAX 2048
#define STATUS_STRMAX 120

#define TALONDELIMITER '|'
#define VARNAMEMAX 100
#define VARVALMAX 1024

#define HOSTNAME_MAX 100

#define TALON_MAXENV 4096

void talon_setenv(char name[], char val[]);
char * talon_getenv(char name[]);
int talon_pathprepend(char value[]);
int talon_pathappend(char value[]);

#endif /* ENV_H_ */

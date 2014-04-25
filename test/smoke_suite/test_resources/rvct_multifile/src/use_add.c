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

#include <e32def.h>
#include "add.h"

typedef unsigned char bool; // Just there to trap compiler error if --cpp was used

void use_add()
{
	TInt z = add(5,6);
}




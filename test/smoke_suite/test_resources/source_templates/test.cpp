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

#include "e32def.h" // intentional  include

char test[]="Long includes test.";

// Use a selection of the available testXX functions
TInt test01();
TInt test22();
TInt test39();
TInt test45();
TInt test57();
TInt test63();

TInt E32Main()
{
	test01();
	test22();
	test39();
	test45();
	test57();
	test63();
	return 0;
}

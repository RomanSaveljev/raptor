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
#include <e32def.h> // intentional  include

void fake_assembler_function1(void);
void fake_assembler_function2(void);
void fake_assembler_function3(void);
void fake_assembler_function4(void);

TInt asmtest()
{
	fake_assembler_function1();
	fake_assembler_function2();
	fake_assembler_function3();
	fake_assembler_function4();
	return 0;
}

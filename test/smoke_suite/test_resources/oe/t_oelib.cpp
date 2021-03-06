/*
* Copyright (c) 2008-2014 Microsoft Mobile and/or its subsidiary(-ies).
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

#ifndef __SYMBIAN_STDCPP_SUPPORT__
#error __SYMBIAN_STDCPP_SUPPORT__ should be defined for all STD* TARGETTYPE builds
#endif

#ifndef __SYMBIAN32__
#define EXPORT __declspec(export) 
#else
#define EXPORT  
#endif

EXPORT int test_oe_function_A(int arg)
{
	return (arg + 1);
}

int test_oe_function_B(int arg)
{
	return (arg + 2);
}

int test_oe_function_C(int arg)
{
	return (arg + 3);
}


int test_oe_allocator(int arg)
{
	int *p = new int;
	delete p;

	return 0;
}

// end


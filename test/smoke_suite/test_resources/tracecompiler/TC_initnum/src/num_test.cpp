/*
Copyright (c) 2011-2014 Microsoft Mobile and/or its subsidiary(-ies).
All rights reserved.
This component and the accompanying materials are made available
under the terms of the License "Eclipse Public License v1.0"
which accompanies this distribution, and is available
at the URL "http://www.eclipse.org/legal/epl-v10.html".

Initial Contributors:
Nokia Corporation - initial contribution.

Contributors:

Description: 

*/

#include <e32uid.h>

#include <num_test.h>

#include "OstTraceDefinitions.h"
#ifdef OST_TRACE_COMPILER_IN_USE
#include "num_testTraces.h"
#endif

EXPORT_C CTestCode* CTestCode::NewLC(CConsoleBase& aConsole)
	{
	CTestCode* self=new (ELeave) CTestCode(aConsole);
	return self;
	}

CTestCode::CTestCode(CConsoleBase& aConsole)
	: iConsole(aConsole)
	{
	}

EXPORT_C void CTestCode::HelloWorld()
	{
    	OstTrace0( TRACE_NORMAL, _HELLOWORLD, "CTestCode::HelloWorld()");
	iConsole.Printf(_L("Hello world!\n"));
	}

/*
* Copyright (c) 2000-2014 Microsoft Mobile and/or its subsidiary(-ies).
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
* This program creates an exe.
*
*/


#include "CreateEXE_variant3.h"
#include <e32uid.h>

// construct/destruct

EXPORT_C CMessenger* CMessenger::NewLC(CConsoleBase& aConsole, const TDesC& aString)
	{
	CMessenger* self=new (ELeave) CMessenger(aConsole);
	CleanupStack::PushL(self);
	self->ConstructL(aString);
	return self;
	}

CMessenger::~CMessenger() // destruct - virtual, so no export
	{
	delete iString;
	}

TInt E32Main()
{
	return 0;
}

EXPORT_C void CMessenger::ShowMessage()
	{
#ifdef B_100
	_LIT(KFormat1,"B_100 %S\n");
#else
	_LIT(KFormat1,"%S\n");
#endif
	iConsole.Printf(KFormat1, iString); // notify completion
	}

// constructor support
// don't export these, because used only by functions in this EXE, eg our NewLC()

CMessenger::CMessenger(CConsoleBase& aConsole) // first-phase C++ constructor
	: iConsole(aConsole)
	{
	}

void CMessenger::ConstructL(const TDesC& aString) // second-phase constructor
	{
	iString=aString.AllocL(); // copy given string into own descriptor
    }

# 
# Copyright (c) 2010 Nokia Corporation and/or its subsidiary(-ies).
# All rights reserved.
# This component and the accompanying materials are made available
# under the terms of the License "Eclipse Public License v1.0"
# which accompanies this distribution, and is available
# at the URL "http://www.eclipse.org/legal/epl-v10.html".
# 
# Initial Contributors:
# Nokia Corporation - initial contribution.
# 
# Contributors:
# 
# Description: 
# 
# 


TEMPLATE = app
TARGET = helloworldqt
DEPENDPATH += .

TEMPLATE = app

INCLUDEPATH += /epoc32/include/stdapis/stlportv5
INCLUDEPATH += /epoc32/tools/qt/mkspecs/common/symbian/stl-off
INCLUDEPATH += /epoc32/tools/qt/mkspecs/common/symbian
INCLUDEPATH += $$APP_LAYER_SYSTEMINCLUDE


symbian {    
	TARGET.UID3 = 0x20029F39
	TARGET.CAPABILITY = CAP_APPLICATION AllFiles TrustedUI
	TARGET.EPOCHEAPSIZE = 0x20000 0x1600000 // 128kB - 23MB
	MMP_RULES += "STDCPP"
}


# Input
SOURCES += helloworld.cpp

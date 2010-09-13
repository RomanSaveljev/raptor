
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

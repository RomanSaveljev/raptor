# -------------------------------------------------
# Project created by QtCreator 2010-08-31T09:43:31
# -------------------------------------------------
TARGET = lottonumberpicker
INCLUDEPATH += /epoc32/include/stdapis/stlportv5
INCLUDEPATH += /epoc32/include/qt/mkspecs/common/symbian/stl-off
INCLUDEPATH += /epoc32/include/qt/mkspecs/common/symbian
INCLUDEPATH += $$APP_LAYER_SYSTEMINCLUDE


symbian {    
        TARGET.UID3 = 0x20029F39
        TARGET.CAPABILITY = CAP_APPLICATION AllFiles TrustedUI
        TARGET.EPOCHEAPSIZE = 0x20000 0x1600000 // 128kB - 23MB
        MMP_RULES += "STDCPP"
}


TEMPLATE = app
SOURCES += main.cpp \
    lottonumberpicker.cpp \
    integerpair.cpp
HEADERS += lottonumberpicker.h \
    integerpair.h
FORMS += lottonumberpicker.ui

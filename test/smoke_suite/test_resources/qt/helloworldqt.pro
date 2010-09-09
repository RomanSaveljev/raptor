
TEMPLATE = app
TARGET = 
DEPENDPATH += .
symbian {

INCLUDEPATH += /epoc32/tools/qt/mkspecs/common/symbian/stl-off
INCLUDEPATH += /epoc32/tools/qt/mkspecs/common/symbian
INCLUDEPATH += /epoc32/include/stdapis/stlport
INCLUDEPATH += $$APP_LAYER_SYSTEMINCLUDE
}

# Input
SOURCES += helloworld.cpp

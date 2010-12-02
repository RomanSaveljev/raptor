#include <QtGui/QApplication>
#include "lottonumberpicker.h"

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    LottoNumberPicker w;
    w.show();
    return a.exec();
}

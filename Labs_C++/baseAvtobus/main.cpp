#include "MainWin.h"
#include <QtWidgets/QApplication>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    //QApplication::setStyle("QFusionStyle");
    MainWin w;
    w.show();
    return a.exec();
}

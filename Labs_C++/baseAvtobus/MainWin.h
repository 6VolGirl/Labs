#pragma once

#include <QtWidgets/QMainWindow>
//#include "ui_baseAvtobus.h"
//#include <QMenu>
#include <QtWidgets/QLayout>
#include <QtWidgets/qtablewidget.h>

#include "Buses.h"
#include "DialogAdd.h"
#include "DialogDeleteBus.h"
#include "DialogGetNum.h"
#include <QVBoxLayout>
#include <qsplitter.h>
#include <QTextEdit>
#include <qplaintextedit.h>
#include "DialogGetNumBas.h"
#include "DialogStop.h"

class MainWin : public QMainWindow
{
    Q_OBJECT

public:
    MainWin(QWidget* parent = nullptr);
    ~MainWin();

private:
    Buses baseBus;
private:
    //Ui::baseAvtobusClass ui;
    QMenu* fileMn;
    QMenu* baseMn;
    QAction* openBaseAct;
    QAction* saveBaseAct;
    QAction* createBaseAct;
    QAction* exitProgAct;
    QAction* addAvtobAct;
    QAction* deleteAvtobAct;

    QWidget* workWidget;
    QTableWidget* workTable;
    QVBoxLayout* mainLayout;
    QSplitter* split;
    //QTextEdit* outText;
    QPlainTextEdit* outText;
    DialogAdd* dialogAdd;
    DialogDeleteBus* dialogDelete;
    DialogGetNum* dialogGetNum;
    DialogGetNumBas* dialogGetNumBas;
    DialogStop* dialogStop;

    void createUI();
    void createMenu();
    void fillTable();
    void wstrToOutText(wstring wstr);

private slots:
    void openBase();
    void saveBase();
    void createBase();
    void exitProg();
    void addAvtob();
    void deleteAvtob();
    void findRoute();
    void identicalStops();
    void routeOfBase();

    //void clearMap();


};

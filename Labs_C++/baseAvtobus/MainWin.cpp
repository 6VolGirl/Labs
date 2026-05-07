#include "MainWin.h"
#include <QString>
#include <string>
#include <QMenu>
#include <qmenubar.h>
#include <QFileDialog>
#include <QStyleFactory>


MainWin::MainWin(QWidget* parent)
    : QMainWindow(parent)
{
    //baseBus.addBus({ 1, L"газ. Звезды", L"Петровщина", L"class", 78 });
    //baseBus.addBus({ 64, L"Брест", L"Курган", L"class", 23 });

    createUI();
}

MainWin::~MainWin()
{}

void MainWin::createUI()
{
    createMenu();
    workTable = new QTableWidget(10, 5, this);
    QStringList ls;
    ls << QString::fromStdWString(L"Номер автобуса ") 
        << QString::fromStdWString(L"Начало маршрута") 
        << QString::fromStdWString(L"Конец маршрута") 
        << QString::fromStdWString(L"Тип автобуса") 
        << QString::fromStdWString(L"Номер автобазы");

    workTable->setHorizontalHeaderLabels(ls);
    fillTable();

    split = new QSplitter(this);
    outText = new QPlainTextEdit(this);
    outText->setReadOnly(true);

    mainLayout = new QVBoxLayout(this);
    mainLayout->addWidget(workTable);
    mainLayout->addWidget(split);
    mainLayout->addWidget(outText);
    workWidget = new QWidget(this);
    workWidget->setLayout(mainLayout);
    setCentralWidget(workWidget);

    dialogAdd = new DialogAdd(this);
    //dialogAdd->setStyle(QStyleFactory::create("QFusionStyle"));
    dialogAdd->leNumBus->setValidator(new QRegExpValidator(QRegExp("[0-9]*"), this));   //Ввод только цифр
    dialogAdd->leBase->setValidator(new QRegExpValidator(QRegExp("[0-9]*"), this));

    dialogDelete = new DialogDeleteBus(this);
    dialogDelete->leNumBus->setValidator(new QRegExpValidator(QRegExp("[0-9]*"), this));   //Ввод только цифр

    dialogGetNum = new DialogGetNum(this);
    dialogGetNum->leNumBus->setValidator(new QRegExpValidator(QRegExp("[0-9]*"), this));

    dialogGetNumBas = new DialogGetNumBas(this);
    dialogGetNumBas->leNumBas->setValidator(new QRegExpValidator(QRegExp("[0-9]*"), this));

    dialogStop = new DialogStop(this);
    dialogStop->leStop;                      ///?????????

    resize(1200, 500);
}

void MainWin::createMenu()
{
    fileMn = new QMenu(tr("&File"));

    openBaseAct = new QAction(tr("&Open..."), this);
    connect(openBaseAct, &QAction::triggered, this, &MainWin::openBase);
    fileMn->addAction(openBaseAct);

    saveBaseAct = new QAction(tr("&Save"), this);
    connect(saveBaseAct, &QAction::triggered, this, &MainWin::saveBase);
    fileMn->addAction(saveBaseAct);

    createBaseAct = new QAction(tr("&Create..."), this);
    connect(createBaseAct, &QAction::triggered, this, &MainWin::createBase);
    fileMn->addAction(createBaseAct);

    fileMn->addSeparator();

    exitProgAct = new QAction(tr("&Exit"), this);
    connect(exitProgAct, SIGNAL(triggered()), SLOT(exitProg()));
    fileMn->addAction(exitProgAct);

    menuBar()->addMenu(fileMn);

    baseMn = new QMenu(tr("&Base"), this);

    addAvtobAct = new QAction(tr("&Add avtobus..."), this);
    connect(addAvtobAct, SIGNAL(triggered()), SLOT(addAvtob()));
    baseMn->addAction(addAvtobAct);

    deleteAvtobAct = new QAction(tr("&Delete avtobus..."), this);
    connect(deleteAvtobAct, SIGNAL(triggered()), SLOT(deleteAvtob()));
    baseMn->addAction(deleteAvtobAct);

    menuBar()->addMenu(baseMn);

    QMenu * functionMn = new QMenu(tr("&Function"), this);

    QAction* findRoute = new QAction(tr("&Determine the route by number"), this);
    connect(findRoute, SIGNAL(triggered()), SLOT(findRoute()));
    functionMn->addAction(findRoute);

    QAction* sameSpops = new QAction(tr("&List of buses with a specific stop"), this);
    connect(sameSpops, SIGNAL(triggered()), SLOT(identicalStops()));
    functionMn->addAction(sameSpops);

    QAction* routeBase = new QAction(tr("&Give a list of carpool routes"), this);
    connect(routeBase, SIGNAL(triggered()), SLOT(routeOfBase()));
    functionMn->addAction(routeBase);

    menuBar()->addMenu(functionMn);
}

void MainWin::fillTable()
{
    auto resStr = baseBus.outStrings();
    int numStr = resStr.size();
    workTable->setRowCount(numStr);
    QTableWidgetItem* qtwi;
    for (int i = 0; i < numStr; i++)
    {
        for (int j = 0; j < 5; j++)
        {
            qtwi = new QTableWidgetItem(QString::fromStdWString(resStr[i][j]));
            workTable->setItem(i, j, qtwi);
        }
    }

}

void MainWin::wstrToOutText(wstring wstr)
{
    QString qstr = QString::fromStdWString(wstr);
    outText->appendPlainText(qstr);
}

void MainWin::openBase()
{
    baseBus.clearMap();
    QString qs = QFileDialog::getOpenFileName(0, "Open base of bus", "", "*.txt");
    if (!qs.isEmpty()) 
    {
        wstring fName = qs.toStdWString();
        baseBus.openFile(fName);
        fillTable();
    }
}

void MainWin::saveBase()
{
    QString qs = QFileDialog::getSaveFileName(0, "Save base of bus", "", "*.txt");
    if (!qs.isEmpty())
    {
        wstring fName = qs.toStdWString();
        baseBus.saveFile(fName);
    }
}

void MainWin::createBase()
{
    baseBus.newBase();
    fillTable();
}

void MainWin::exitProg()
{
    this->close();
}

void MainWin::addAvtob()
{
    if (dialogAdd->exec() == QDialog::Accepted) {
        if (!dialogAdd->leNumBus->text().isEmpty() 
            && !dialogAdd->leBegin->text().isEmpty() 
            && !dialogAdd->leEnd->text().isEmpty() 
            && !dialogAdd->leType->text().isEmpty() 
            && !dialogAdd->leBase->text().isEmpty())
        {
            Bus elem;
            elem.number = dialogAdd->leNumBus->text().toInt();
            elem.beggining = dialogAdd->leBegin->text().toStdWString();
            elem.finishing = dialogAdd->leEnd->text().toStdWString();
            elem.type = dialogAdd->leType->text().toStdWString();
            elem.base = dialogAdd->leBase->text().toInt();
            baseBus.addBus(elem);
            fillTable();
        }
    }
}

void MainWin::deleteAvtob()
{
    if (dialogDelete->exec() == QDialog::Accepted)
    {
        if (!dialogDelete->leNumBus->text().isEmpty())
        {
            int elem = dialogDelete->leNumBus->text().toInt();
            auto num = baseBus.findRoute(elem);
            if (!num[0].empty())
            {
                outText->clear();
                baseBus.deleteBus(elem);
                fillTable();
            }
            else
            {
                wstrToOutText(L"Нет такого автобуса");
            }
        }
    }
}

void MainWin::findRoute()
{
    if (dialogGetNum->exec() == QDialog::Accepted)
    {
        if (!dialogGetNum->leNumBus->text().isEmpty())
        {
            int elem = dialogGetNum->leNumBus->text().toInt();
            auto rout = baseBus.findRoute(elem);
            if (!rout[0].empty()) 
            {
                outText->clear();
                wstrToOutText(L"Маршрут для автобуса - " + to_wstring(elem));
                wstrToOutText(rout[0] + L" -> " + rout[1]);
                //outText->appendPlainText()
            }
            else
            {
                wstrToOutText(L"Нет такого автобуса");
            }
        }
    }
}

void MainWin::identicalStops()
{
    if (dialogStop->exec() == QDialog::Accepted)
    {
        if (!dialogStop->leStop->text().isEmpty())
        {
            outText->clear();
            wstring stop = dialogStop->leStop->text().toStdWString();
            vector<wstring> vec_num = baseBus.identicalStops(stop);
            if (!vec_num.empty())
            {
                wstrToOutText(L"Номера автобусов проезжающих через остановку - " + stop);
                for (int i =0;  i < vec_num.size(); i++)
                {
                    wstrToOutText(vec_num[i]);
                }
            }
            else
            {
                wstrToOutText(L"Нет такой остановки");
            }
        }
    }
}

void MainWin::routeOfBase()
{
    if (dialogGetNumBas->exec() == QDialog::Accepted)
    {
        if (!dialogGetNumBas->leNumBas->text().isEmpty())
        {
            outText->clear();
            int base = dialogGetNumBas->leNumBas->text().toInt();
            vector<pair<wstring, wstring>> stops = baseBus.routeOfBase(base);
            if (!stops.empty())
            {
                wstrToOutText(L"Маршруты относящиеся к базе - " + to_wstring(base));
                for (auto iter = stops.begin(); iter < stops.end(); iter++)
                {
                    wstrToOutText(iter->first + L" -> " + iter->second);
                }
            }
            else
            {
                wstrToOutText(L"Нет такой базы");
            }
        }
    }
}



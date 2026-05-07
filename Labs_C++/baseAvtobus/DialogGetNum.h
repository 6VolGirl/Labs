#pragma once
#include "ui_DialogGetNumBus.h"
#include <qdialog.h>
class DialogGetNum :
    public QDialog, public  Ui::DialogGetNumAvtobus
{
    Q_OBJECT
public: 
    DialogGetNum(QWidget* parent =0);
};


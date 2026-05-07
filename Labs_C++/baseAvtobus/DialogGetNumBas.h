#pragma once
#include "ui_DialogGetNumBase.h"
#include <qdialog.h>
class DialogGetNumBas :
    public QDialog, public Ui::DialogGetNumBase
{
    Q_OBJECT
public: 
    DialogGetNumBas(QWidget* parent);
};


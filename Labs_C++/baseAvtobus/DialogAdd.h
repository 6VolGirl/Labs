#pragma once
#include "ui_DialogButtonBottom.h"
#include <qdialog.h>
class DialogAdd :
    public QDialog, public Ui::DialogAddAvtobus
{
    Q_OBJECT
public:
    DialogAdd(QWidget* parent = 0);
};


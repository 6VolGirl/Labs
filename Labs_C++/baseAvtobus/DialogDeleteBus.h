#pragma once
#include "ui_DialogDelete.h"
#include <qdialog.h>
class DialogDeleteBus :
    public QDialog, public Ui::DialogDeleteAvtobus
{
    Q_OBJECT
public :
    DialogDeleteBus(QWidget* parent = 0);
};


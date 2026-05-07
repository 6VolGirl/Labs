#pragma once
#include "ui_DialogGetStop.h"
#include <qdialog.h>
class DialogStop :
    public QDialog, public Ui::DialogGetStop
{
    Q_OBJECT
public:
    DialogStop(QWidget* parent = 0);
};


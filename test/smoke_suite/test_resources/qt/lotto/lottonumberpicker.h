#ifndef LOTTONUMBERPICKER_H
#define LOTTONUMBERPICKER_H

#include <QDialog>

namespace Ui {
    class LottoNumberPicker;
}

class LottoNumberPicker : public QDialog {
    Q_OBJECT
public:
    LottoNumberPicker(QWidget *parent = 0);
    ~LottoNumberPicker();

public slots:
    void on_chooseButton_clicked(void);

protected:
    void changeEvent(QEvent *e);

private:
    Ui::LottoNumberPicker *ui;
    int randomSeedModifier;
};

#endif // LOTTONUMBERPICKER_H

#include "lottonumberpicker.h"
#include "ui_lottonumberpicker.h"

#include "integerpair.h"

#include <QTime>
#include <QtGlobal>
#include <QList>
#include <iostream>

LottoNumberPicker::LottoNumberPicker(QWidget *parent) :
    QDialog(parent),
    ui(new Ui::LottoNumberPicker),
    randomSeedModifier(0)
{
    ui->setupUi(this);
    on_chooseButton_clicked();
}

LottoNumberPicker::~LottoNumberPicker()
{
    delete ui;
}

void LottoNumberPicker::changeEvent(QEvent *e)
{
    QDialog::changeEvent(e);
    switch (e->type()) {
    case QEvent::LanguageChange:
        ui->retranslateUi(this);
        break;
    default:
        break;
    }
}

void LottoNumberPicker::on_chooseButton_clicked(void)
{
    QTime midnight(0, 0, 0);
    qsrand(randomSeedModifier + midnight.secsTo(QTime::currentTime()));

    QList <IntegerPair> numbers;

    for(int i = 1; i < 50; i++)
    {
        numbers << IntegerPair(i, qrand());
    }

    qSort(numbers);

    randomSeedModifier = numbers[0].getSortBy();

    QList <int> generatedNumbers;
    generatedNumbers << numbers[0].getNumber() << numbers[1].getNumber() << numbers[2].getNumber() <<
             numbers[3].getNumber() << numbers[4].getNumber() << numbers[5].getNumber();
    qSort(generatedNumbers);

    ui->firstNum->setText(QString::number(generatedNumbers[0]));
    ui->secondNum->setText(QString::number(generatedNumbers[1]));
    ui->thirdNum->setText(QString::number(generatedNumbers[2]));
    ui->fourthNum->setText(QString::number(generatedNumbers[3]));
    ui->fifthNum->setText(QString::number(generatedNumbers[4]));
    ui->sixthNum->setText(QString::number(generatedNumbers[5]));
}


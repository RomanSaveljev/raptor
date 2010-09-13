/********************************************************************************
** Form generated from reading UI file 'lottonumberpicker.ui'
**
** Created: Mon Sep 13 23:06:42 2010
**      by: Qt User Interface Compiler version 4.6.4
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_LOTTONUMBERPICKER_H
#define UI_LOTTONUMBERPICKER_H

#include <QtCore/QVariant>
#include <QtGui/QAction>
#include <QtGui/QApplication>
#include <QtGui/QButtonGroup>
#include <QtGui/QDialog>
#include <QtGui/QGroupBox>
#include <QtGui/QHBoxLayout>
#include <QtGui/QHeaderView>
#include <QtGui/QLabel>
#include <QtGui/QPushButton>
#include <QtGui/QVBoxLayout>

QT_BEGIN_NAMESPACE

class Ui_LottoNumberPicker
{
public:
    QVBoxLayout *verticalLayout_2;
    QVBoxLayout *verticalLayout;
    QGroupBox *groupBox;
    QHBoxLayout *horizontalLayout_5;
    QVBoxLayout *verticalLayout_3;
    QHBoxLayout *horizontalLayout;
    QLabel *firstNum;
    QLabel *secondNum;
    QLabel *thirdNum;
    QLabel *fourthNum;
    QLabel *fifthNum;
    QLabel *sixthNum;
    QVBoxLayout *verticalLayout_4;
    QPushButton *chooseButton;

    void setupUi(QDialog *LottoNumberPicker)
    {
        if (LottoNumberPicker->objectName().isEmpty())
            LottoNumberPicker->setObjectName(QString::fromUtf8("LottoNumberPicker"));
        LottoNumberPicker->resize(141, 270);
        verticalLayout_2 = new QVBoxLayout(LottoNumberPicker);
        verticalLayout_2->setSpacing(6);
        verticalLayout_2->setContentsMargins(11, 11, 11, 11);
        verticalLayout_2->setObjectName(QString::fromUtf8("verticalLayout_2"));
        verticalLayout = new QVBoxLayout();
        verticalLayout->setSpacing(6);
        verticalLayout->setObjectName(QString::fromUtf8("verticalLayout"));
        groupBox = new QGroupBox(LottoNumberPicker);
        groupBox->setObjectName(QString::fromUtf8("groupBox"));
        horizontalLayout_5 = new QHBoxLayout(groupBox);
        horizontalLayout_5->setSpacing(6);
        horizontalLayout_5->setContentsMargins(11, 11, 11, 11);
        horizontalLayout_5->setObjectName(QString::fromUtf8("horizontalLayout_5"));
        verticalLayout_3 = new QVBoxLayout();
        verticalLayout_3->setSpacing(6);
        verticalLayout_3->setObjectName(QString::fromUtf8("verticalLayout_3"));
        horizontalLayout = new QHBoxLayout();
        horizontalLayout->setSpacing(6);
        horizontalLayout->setObjectName(QString::fromUtf8("horizontalLayout"));
        firstNum = new QLabel(groupBox);
        firstNum->setObjectName(QString::fromUtf8("firstNum"));

        horizontalLayout->addWidget(firstNum);

        secondNum = new QLabel(groupBox);
        secondNum->setObjectName(QString::fromUtf8("secondNum"));

        horizontalLayout->addWidget(secondNum);

        thirdNum = new QLabel(groupBox);
        thirdNum->setObjectName(QString::fromUtf8("thirdNum"));

        horizontalLayout->addWidget(thirdNum);

        fourthNum = new QLabel(groupBox);
        fourthNum->setObjectName(QString::fromUtf8("fourthNum"));

        horizontalLayout->addWidget(fourthNum);

        fifthNum = new QLabel(groupBox);
        fifthNum->setObjectName(QString::fromUtf8("fifthNum"));

        horizontalLayout->addWidget(fifthNum);

        sixthNum = new QLabel(groupBox);
        sixthNum->setObjectName(QString::fromUtf8("sixthNum"));

        horizontalLayout->addWidget(sixthNum);


        verticalLayout_3->addLayout(horizontalLayout);

        verticalLayout_4 = new QVBoxLayout();
        verticalLayout_4->setSpacing(6);
        verticalLayout_4->setObjectName(QString::fromUtf8("verticalLayout_4"));
        chooseButton = new QPushButton(groupBox);
        chooseButton->setObjectName(QString::fromUtf8("chooseButton"));
        QSizePolicy sizePolicy(QSizePolicy::Minimum, QSizePolicy::Minimum);
        sizePolicy.setHorizontalStretch(0);
        sizePolicy.setVerticalStretch(0);
        sizePolicy.setHeightForWidth(chooseButton->sizePolicy().hasHeightForWidth());
        chooseButton->setSizePolicy(sizePolicy);
        chooseButton->setAutoFillBackground(false);
        chooseButton->setDefault(true);

        verticalLayout_4->addWidget(chooseButton);


        verticalLayout_3->addLayout(verticalLayout_4);


        horizontalLayout_5->addLayout(verticalLayout_3);


        verticalLayout->addWidget(groupBox);


        verticalLayout_2->addLayout(verticalLayout);


        retranslateUi(LottoNumberPicker);

        QMetaObject::connectSlotsByName(LottoNumberPicker);
    } // setupUi

    void retranslateUi(QDialog *LottoNumberPicker)
    {
        LottoNumberPicker->setWindowTitle(QApplication::translate("LottoNumberPicker", "LottoNumberPicker", 0, QApplication::UnicodeUTF8));
        groupBox->setTitle(QApplication::translate("LottoNumberPicker", "Lotto Numbers", 0, QApplication::UnicodeUTF8));
        firstNum->setText(QApplication::translate("LottoNumberPicker", "0", 0, QApplication::UnicodeUTF8));
        secondNum->setText(QApplication::translate("LottoNumberPicker", "0", 0, QApplication::UnicodeUTF8));
        thirdNum->setText(QApplication::translate("LottoNumberPicker", "0", 0, QApplication::UnicodeUTF8));
        fourthNum->setText(QApplication::translate("LottoNumberPicker", "0", 0, QApplication::UnicodeUTF8));
        fifthNum->setText(QApplication::translate("LottoNumberPicker", "0", 0, QApplication::UnicodeUTF8));
        sixthNum->setText(QApplication::translate("LottoNumberPicker", "0", 0, QApplication::UnicodeUTF8));
        chooseButton->setText(QApplication::translate("LottoNumberPicker", "&Choose", 0, QApplication::UnicodeUTF8));
    } // retranslateUi

};

namespace Ui {
    class LottoNumberPicker: public Ui_LottoNumberPicker {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_LOTTONUMBERPICKER_H

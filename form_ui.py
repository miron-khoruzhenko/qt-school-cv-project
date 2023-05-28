# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.4.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QMetaObject, QSize, Qt)
from PySide6.QtGui import (QBrush, QColor, QCursor)
from PySide6.QtWidgets import (QAbstractScrollArea, QFrame, QGraphicsView,
    QHBoxLayout, QLabel, QPushButton, QSizePolicy,
    QSlider, QVBoxLayout)

class Ui_Widget(object):
    def setupUi(self, Widget):
        if not Widget.objectName():
            Widget.setObjectName(u"Widget")
        Widget.resize(550, 520)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Widget.sizePolicy().hasHeightForWidth())
        Widget.setSizePolicy(sizePolicy)
        Widget.setMinimumSize(QSize(550, 520))
        Widget.setMaximumSize(QSize(99999, 99999))
        Widget.setCursor(QCursor(Qt.ArrowCursor))
        Widget.setAutoFillBackground(False)
        Widget.setStyleSheet(u"background: \"#333333\";")
        self.horizontalLayout_5 = QHBoxLayout(Widget)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.vertical_slider = QSlider(Widget)
        self.vertical_slider.setObjectName(u"vertical_slider")
        self.vertical_slider.setStyleSheet(u"")
        self.vertical_slider.setMinimum(1)
        self.vertical_slider.setMaximum(200)
        self.vertical_slider.setSingleStep(0)
        self.vertical_slider.setPageStep(100)
        self.vertical_slider.setOrientation(Qt.Vertical)

        self.horizontalLayout_5.addWidget(self.vertical_slider)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.frame = QFrame(Widget)
        self.frame.setObjectName(u"frame")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy1)
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.frame)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.loaded_img = QGraphicsView(self.frame)
        self.loaded_img.setObjectName(u"loaded_img")
        self.loaded_img.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.loaded_img.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.horizontalLayout_4.addWidget(self.loaded_img)


        self.horizontalLayout_3.addWidget(self.frame)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.load_img_btn = QPushButton(Widget)
        self.load_img_btn.setObjectName(u"load_img_btn")
        sizePolicy.setHeightForWidth(self.load_img_btn.sizePolicy().hasHeightForWidth())
        self.load_img_btn.setSizePolicy(sizePolicy)
        self.load_img_btn.setMinimumSize(QSize(150, 50))
        self.load_img_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.load_img_btn.setStyleSheet(u"background: qlineargradient(spread:pad, x1:0.5, y1:0, x2:0.5, y2:1, stop:0 rgba(74, 74, 74, 255), stop:1 rgba(64, 64, 64, 255));\n"
"border: 1px solid #6a6a6a;\n"
"color: white;")

        self.verticalLayout_3.addWidget(self.load_img_btn)

        self.process_img_btn = QPushButton(Widget)
        self.process_img_btn.setObjectName(u"process_img_btn")
        sizePolicy.setHeightForWidth(self.process_img_btn.sizePolicy().hasHeightForWidth())
        self.process_img_btn.setSizePolicy(sizePolicy)
        self.process_img_btn.setMinimumSize(QSize(150, 50))
        self.process_img_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.process_img_btn.setStyleSheet(u"background: qlineargradient(spread:pad, x1:0.5, y1:0, x2:0.5, y2:1, stop:0 rgba(74, 74, 74, 255), stop:1 rgba(64, 64, 64, 255));\n"
"border: 1px solid #6a6a6a;\n"
"color: white;")

        self.verticalLayout_3.addWidget(self.process_img_btn)


        self.horizontalLayout_3.addLayout(self.verticalLayout_3)


        self.verticalLayout_2.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.frame_2 = QFrame(Widget)
        self.frame_2.setObjectName(u"frame_2")
        sizePolicy1.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy1)
        self.frame_2.setMinimumSize(QSize(0, 0))
        self.frame_2.setSizeIncrement(QSize(0, 0))
        self.frame_2.setBaseSize(QSize(0, 0))
        self.frame_2.setLayoutDirection(Qt.LeftToRight)
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.frame_2)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.processed_img = QGraphicsView(self.frame_2)
        self.processed_img.setObjectName(u"processed_img")
        self.processed_img.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.processed_img.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.processed_img.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        brush = QBrush(QColor(0, 0, 0, 255))
        brush.setStyle(Qt.Dense5Pattern)
        self.processed_img.setBackgroundBrush(brush)

        self.horizontalLayout.addWidget(self.processed_img)


        self.horizontalLayout_2.addWidget(self.frame_2)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.save_btn = QPushButton(Widget)
        self.save_btn.setObjectName(u"save_btn")
        sizePolicy.setHeightForWidth(self.save_btn.sizePolicy().hasHeightForWidth())
        self.save_btn.setSizePolicy(sizePolicy)
        self.save_btn.setMinimumSize(QSize(150, 50))
        self.save_btn.setStyleSheet(u"background: qlineargradient(spread:pad, x1:0.5, y1:0, x2:0.5, y2:1, stop:0 rgba(74, 74, 74, 255), stop:1 rgba(64, 64, 64, 255));\n"
"border: 1px solid #6a6a6a;\n"
"color: white;")

        self.verticalLayout_4.addWidget(self.save_btn)

        self.length_label = QLabel(Widget)
        self.length_label.setObjectName(u"length_label")
        sizePolicy.setHeightForWidth(self.length_label.sizePolicy().hasHeightForWidth())
        self.length_label.setSizePolicy(sizePolicy)
        self.length_label.setMinimumSize(QSize(150, 50))
        self.length_label.setStyleSheet(u"background: #222222;\n"
"border: 1px solid #2d2d2d;")
        self.length_label.setFrameShape(QFrame.NoFrame)
        self.length_label.setAlignment(Qt.AlignCenter)

        self.verticalLayout_4.addWidget(self.length_label)


        self.horizontalLayout_2.addLayout(self.verticalLayout_4)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.verticalLayout_2.setStretch(0, 1)
        self.verticalLayout_2.setStretch(1, 1)

        self.horizontalLayout_5.addLayout(self.verticalLayout_2)


        self.retranslateUi(Widget)

        QMetaObject.connectSlotsByName(Widget)
    # setupUi

    def retranslateUi(self, Widget):
        Widget.setWindowTitle(QCoreApplication.translate("Widget", u"Widget", None))
        self.load_img_btn.setText(QCoreApplication.translate("Widget", u"Load Image", None))
        self.process_img_btn.setText(QCoreApplication.translate("Widget", u"Process", None))
        self.save_btn.setText(QCoreApplication.translate("Widget", u"Save", None))
        self.length_label.setText("")
    # retranslateUi


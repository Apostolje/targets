# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ui/raw/application_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ApplicationWindow(object):
    def setupUi(self, ApplicationWindow):
        ApplicationWindow.setObjectName("ApplicationWindow")
        ApplicationWindow.resize(945, 909)
        self.centralwidget = QtWidgets.QWidget(ApplicationWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.tab)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.graphWidget = HypergraphWidget(self.tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.graphWidget.sizePolicy().hasHeightForWidth())
        self.graphWidget.setSizePolicy(sizePolicy)
        self.graphWidget.setMinimumSize(QtCore.QSize(300, 100))
        self.graphWidget.setObjectName("graphWidget")
        self.horizontalLayout.addWidget(self.graphWidget)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.verticalLayout_4.setContentsMargins(-1, 0, -1, -1)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.tabWidget_2 = QtWidgets.QTabWidget(self.tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget_2.sizePolicy().hasHeightForWidth())
        self.tabWidget_2.setSizePolicy(sizePolicy)
        self.tabWidget_2.setObjectName("tabWidget_2")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.tab_3)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.label_4 = QtWidgets.QLabel(self.tab_3)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.label_5 = QtWidgets.QLabel(self.tab_3)
        self.label_5.setObjectName("label_5")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_5)
        self.label_6 = QtWidgets.QLabel(self.tab_3)
        self.label_6.setObjectName("label_6")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_6)
        self.immuneNp = QtWidgets.QLineEdit(self.tab_3)
        self.immuneNp.setObjectName("immuneNp")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.immuneNp)
        self.immuneCi = QtWidgets.QLineEdit(self.tab_3)
        self.immuneCi.setObjectName("immuneCi")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.immuneCi)
        self.immuneNi = QtWidgets.QLineEdit(self.tab_3)
        self.immuneNi.setObjectName("immuneNi")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.immuneNi)
        self.immuneButton = QtWidgets.QPushButton(self.tab_3)
        self.immuneButton.setObjectName("immuneButton")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.SpanningRole, self.immuneButton)
        spacerItem = QtWidgets.QSpacerItem(20, 63, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.formLayout.setItem(3, QtWidgets.QFormLayout.SpanningRole, spacerItem)
        self.horizontalLayout_5.addLayout(self.formLayout)
        self.tabWidget_2.addTab(self.tab_3, "")
        self.tab_5 = QtWidgets.QWidget()
        self.tab_5.setObjectName("tab_5")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.tab_5)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.formLayout_2 = QtWidgets.QFormLayout()
        self.formLayout_2.setObjectName("formLayout_2")
        self.label_7 = QtWidgets.QLabel(self.tab_5)
        self.label_7.setObjectName("label_7")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_7)
        self.gaNp = QtWidgets.QLineEdit(self.tab_5)
        self.gaNp.setObjectName("gaNp")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.gaNp)
        self.label_8 = QtWidgets.QLabel(self.tab_5)
        self.label_8.setObjectName("label_8")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_8)
        self.gaMp = QtWidgets.QLineEdit(self.tab_5)
        self.gaMp.setObjectName("gaMp")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.gaMp)
        self.gaNi = QtWidgets.QLineEdit(self.tab_5)
        self.gaNi.setObjectName("gaNi")
        self.formLayout_2.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.gaNi)
        self.gaButton = QtWidgets.QPushButton(self.tab_5)
        self.gaButton.setObjectName("gaButton")
        self.formLayout_2.setWidget(5, QtWidgets.QFormLayout.SpanningRole, self.gaButton)
        spacerItem1 = QtWidgets.QSpacerItem(20, 30, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.formLayout_2.setItem(4, QtWidgets.QFormLayout.SpanningRole, spacerItem1)
        self.evolutionBox = QtWidgets.QComboBox(self.tab_5)
        self.evolutionBox.setObjectName("evolutionBox")
        self.evolutionBox.addItem("")
        self.evolutionBox.addItem("")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.SpanningRole, self.evolutionBox)
        self.label_9 = QtWidgets.QLabel(self.tab_5)
        self.label_9.setObjectName("label_9")
        self.formLayout_2.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_9)
        self.horizontalLayout_6.addLayout(self.formLayout_2)
        self.tabWidget_2.addTab(self.tab_5, "")
        self.verticalLayout_4.addWidget(self.tabWidget_2)
        self.groupBox = QtWidgets.QGroupBox(self.tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setMinimumSize(QtCore.QSize(240, 0))
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setStyleStrategy(QtGui.QFont.PreferDefault)
        self.groupBox.setFont(font)
        self.groupBox.setFlat(False)
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.result = QtWidgets.QTextEdit(self.groupBox)
        self.result.setMinimumSize(QtCore.QSize(0, 256))
        self.result.setStyleSheet("border: 0px solid gray;")
        self.result.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.result.setFrameShadow(QtWidgets.QFrame.Plain)
        self.result.setReadOnly(True)
        self.result.setObjectName("result")
        self.horizontalLayout_7.addWidget(self.result)
        self.verticalLayout_4.addWidget(self.groupBox)
        self.horizontalLayout.addLayout(self.verticalLayout_4)
        self.verticalLayout_5.addLayout(self.horizontalLayout)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.verticalLayout_16 = QtWidgets.QVBoxLayout(self.tab_2)
        self.verticalLayout_16.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_16.setObjectName("verticalLayout_16")
        self.scrollArea = QtWidgets.QScrollArea(self.tab_2)
        self.scrollArea.setStyleSheet("background: white;")
        self.scrollArea.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scrollArea.setLineWidth(0)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 925, 853))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_15 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_15.setObjectName("verticalLayout_15")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_3 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.targetsTable = QtWidgets.QTableWidget(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.targetsTable.sizePolicy().hasHeightForWidth())
        self.targetsTable.setSizePolicy(sizePolicy)
        self.targetsTable.setObjectName("targetsTable")
        self.targetsTable.setColumnCount(0)
        self.targetsTable.setRowCount(0)
        self.verticalLayout.addWidget(self.targetsTable)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.addTargetButton = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.addTargetButton.setObjectName("addTargetButton")
        self.horizontalLayout_3.addWidget(self.addTargetButton)
        self.deleteTargetButton = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.deleteTargetButton.setObjectName("deleteTargetButton")
        self.horizontalLayout_3.addWidget(self.deleteTargetButton)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        spacerItem3 = QtWidgets.QSpacerItem(20, 25, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem3)
        self.verticalLayout_7.addLayout(self.verticalLayout)
        self.label_2 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_7.addWidget(self.label_2)
        self.verticalLayout_14 = QtWidgets.QVBoxLayout()
        self.verticalLayout_14.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.verticalLayout_14.setObjectName("verticalLayout_14")
        self.weaponsTable = QtWidgets.QTableWidget(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.weaponsTable.sizePolicy().hasHeightForWidth())
        self.weaponsTable.setSizePolicy(sizePolicy)
        self.weaponsTable.setObjectName("weaponsTable")
        self.weaponsTable.setColumnCount(0)
        self.weaponsTable.setRowCount(0)
        self.verticalLayout_14.addWidget(self.weaponsTable)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.addWeaponButton = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.addWeaponButton.setObjectName("addWeaponButton")
        self.horizontalLayout_4.addWidget(self.addWeaponButton)
        self.deleteWeaponButton = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.deleteWeaponButton.setObjectName("deleteWeaponButton")
        self.horizontalLayout_4.addWidget(self.deleteWeaponButton)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem4)
        self.verticalLayout_14.addLayout(self.horizontalLayout_4)
        self.verticalLayout_7.addLayout(self.verticalLayout_14)
        spacerItem5 = QtWidgets.QSpacerItem(20, 25, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_7.addItem(spacerItem5)
        self.label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.verticalLayout_7.addWidget(self.label)
        self.possibilitiesTable = QtWidgets.QTableWidget(self.scrollAreaWidgetContents)
        self.possibilitiesTable.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.possibilitiesTable.setObjectName("possibilitiesTable")
        self.possibilitiesTable.setColumnCount(0)
        self.possibilitiesTable.setRowCount(0)
        self.verticalLayout_7.addWidget(self.possibilitiesTable)
        spacerItem6 = QtWidgets.QSpacerItem(20, 25, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_7.addItem(spacerItem6)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.saveIntoFileButton = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.saveIntoFileButton.setObjectName("saveIntoFileButton")
        self.horizontalLayout_2.addWidget(self.saveIntoFileButton)
        self.loadFromFileButton = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.loadFromFileButton.setObjectName("loadFromFileButton")
        self.horizontalLayout_2.addWidget(self.loadFromFileButton)
        self.generateButton = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.generateButton.setObjectName("generateButton")
        self.horizontalLayout_2.addWidget(self.generateButton)
        spacerItem7 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem7)
        self.verticalLayout_7.addLayout(self.horizontalLayout_2)
        spacerItem8 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_7.addItem(spacerItem8)
        self.verticalLayout_15.addLayout(self.verticalLayout_7)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout_16.addWidget(self.scrollArea)
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.tab_4)
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_8.setSpacing(0)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.solutionTable = QtWidgets.QTableWidget(self.tab_4)
        self.solutionTable.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.solutionTable.setObjectName("solutionTable")
        self.solutionTable.setColumnCount(0)
        self.solutionTable.setRowCount(0)
        self.verticalLayout_8.addWidget(self.solutionTable)
        self.tabWidget.addTab(self.tab_4, "")
        self.verticalLayout_2.addWidget(self.tabWidget)
        ApplicationWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(ApplicationWindow)
        self.tabWidget.setCurrentIndex(0)
        self.tabWidget_2.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(ApplicationWindow)

    def retranslateUi(self, ApplicationWindow):
        _translate = QtCore.QCoreApplication.translate
        ApplicationWindow.setWindowTitle(_translate("ApplicationWindow", "Назначение целей"))
        self.label_4.setText(_translate("ApplicationWindow", "Размер популяции:"))
        self.label_5.setText(_translate("ApplicationWindow", "Коэффициент Ci:"))
        self.label_6.setText(_translate("ApplicationWindow", "Итераций:"))
        self.immuneNp.setText(_translate("ApplicationWindow", "10"))
        self.immuneCi.setText(_translate("ApplicationWindow", "2.8"))
        self.immuneNi.setText(_translate("ApplicationWindow", "300"))
        self.immuneButton.setText(_translate("ApplicationWindow", "Выполнить"))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_3), _translate("ApplicationWindow", "Иммунный"))
        self.label_7.setText(_translate("ApplicationWindow", "Размер популяции:"))
        self.gaNp.setText(_translate("ApplicationWindow", "10"))
        self.label_8.setText(_translate("ApplicationWindow", "Вероятность мутации:"))
        self.gaMp.setText(_translate("ApplicationWindow", "0.19"))
        self.gaNi.setText(_translate("ApplicationWindow", "300"))
        self.gaButton.setText(_translate("ApplicationWindow", "Выполнить"))
        self.evolutionBox.setItemText(0, _translate("ApplicationWindow", "Эволюция Дарвина"))
        self.evolutionBox.setItemText(1, _translate("ApplicationWindow", "Эволюция Де Фриза"))
        self.label_9.setText(_translate("ApplicationWindow", "Итераций:"))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_5), _translate("ApplicationWindow", "Генетический"))
        self.groupBox.setTitle(_translate("ApplicationWindow", "Результат поиска"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("ApplicationWindow", "Основное"))
        self.label_3.setText(_translate("ApplicationWindow", "Цели и их значимость"))
        self.addTargetButton.setText(_translate("ApplicationWindow", "Добавить"))
        self.deleteTargetButton.setText(_translate("ApplicationWindow", "Удалить"))
        self.label_2.setText(_translate("ApplicationWindow", "Типы исполнителей и их количество"))
        self.addWeaponButton.setText(_translate("ApplicationWindow", "Добавить"))
        self.deleteWeaponButton.setText(_translate("ApplicationWindow", "Удалить"))
        self.label.setText(_translate("ApplicationWindow", "Вероятности"))
        self.saveIntoFileButton.setText(_translate("ApplicationWindow", "Сохранить условия в файл..."))
        self.loadFromFileButton.setText(_translate("ApplicationWindow", "Загрузить условия из файла..."))
        self.generateButton.setText(_translate("ApplicationWindow", "Сгенерировать..."))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("ApplicationWindow", "Условия задачи"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), _translate("ApplicationWindow", "Матрица назначений"))
from ui.src.hypergraph_widget import HypergraphWidget

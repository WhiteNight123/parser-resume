# Form implementation generated from reading ui file 'resume_visiual_dialog.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Dialog2(object):
    def setupUi(self, Dialog2):
        Dialog2.setObjectName("Dialog2")
        Dialog2.resize(512, 416)
        Dialog2.setMinimumSize(QtCore.QSize(512, 416))
        Dialog2.setMaximumSize(QtCore.QSize(512, 416))
        self.tabWidget = QtWidgets.QTabWidget(parent=Dialog2)
        self.tabWidget.setGeometry(QtCore.QRect(20, 50, 471, 301))
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.verticalLayoutWidget_4 = QtWidgets.QWidget(parent=self.tab)
        self.verticalLayoutWidget_4.setGeometry(QtCore.QRect(0, 0, 451, 271))
        self.verticalLayoutWidget_4.setObjectName("verticalLayoutWidget_4")
        self.verticalLayout_1 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_4)
        self.verticalLayout_1.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_1.setObjectName("verticalLayout_1")
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.verticalLayoutWidget_3 = QtWidgets.QWidget(parent=self.tab_2)
        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(0, 0, 451, 271))
        self.verticalLayoutWidget_3.setObjectName("verticalLayoutWidget_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(parent=self.tab_3)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(0, 0, 451, 271))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.tabWidget.addTab(self.tab_3, "")
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.verticalLayoutWidget = QtWidgets.QWidget(parent=self.tab_4)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 451, 271))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.tabWidget.addTab(self.tab_4, "")
        self.ok_button = QtWidgets.QPushButton(parent=Dialog2)
        self.ok_button.setGeometry(QtCore.QRect(220, 360, 75, 24))
        self.ok_button.setObjectName("ok_button")
        self.title_text = QtWidgets.QLabel(parent=Dialog2)
        self.title_text.setGeometry(QtCore.QRect(190, 10, 141, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.title_text.setFont(font)
        self.title_text.setObjectName("title_text")

        self.retranslateUi(Dialog2)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Dialog2)

    def retranslateUi(self, Dialog2):
        _translate = QtCore.QCoreApplication.translate
        Dialog2.setWindowTitle(_translate("Dialog2", "简历统计可视化"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Dialog2", "学历统计"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Dialog2", "年龄统计"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("Dialog2", "毕业院校统计"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), _translate("Dialog2", "工作年限统计"))
        self.ok_button.setText(_translate("Dialog2", "确定"))
        self.title_text.setText(_translate("Dialog2", "简历统计可视化"))

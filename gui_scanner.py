import os
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from Scanner import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_11 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.verticalLayout_11.addWidget(self.label)
        self.verticalLayout_1 = QtWidgets.QVBoxLayout()
        self.verticalLayout_1.setObjectName("verticalLayout_1")
        self.horizontalLayout_1 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_1.setObjectName("horizontalLayout_1")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setObjectName("textEdit")
        self.horizontalLayout_1.addWidget(self.textEdit)
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.tableView = QtWidgets.QTableView(self.centralwidget)
        self.tableView.setAutoFillBackground(False)
        self.tableView.setObjectName("tableView")
        self.tableView.horizontalHeader().setCascadingSectionResizes(True)
        self.tableView.horizontalHeader().setStretchLastSection(True)
        #
        model = QtGui.QStandardItemModel()
        model.setHorizontalHeaderLabels(['Input', 'Type'])
        self.tableView.setModel(model)

        header = self.tableView.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        #
        self.verticalLayout_6.addWidget(self.tableView, 0, QtCore.Qt.AlignRight)
        self.verticalLayout_9 = QtWidgets.QVBoxLayout()
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.verticalLayout_6.addLayout(self.verticalLayout_9)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setToolTip('Start scan')
        self.pushButton.setObjectName("pushButton")
        #
        self.pushButton.clicked.connect(self.start_scanning)
        #
        self.verticalLayout_6.addWidget(self.pushButton, 0, QtCore.Qt.AlignBottom)
        self.horizontalLayout_1.addLayout(self.verticalLayout_6)
        self.verticalLayout_1.addLayout(self.horizontalLayout_1)
        self.verticalLayout_11.addLayout(self.verticalLayout_1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuQUIT = QtWidgets.QMenu(self.menubar)
        self.menuQUIT.setObjectName("menuQUIT")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionNew = QtWidgets.QAction(MainWindow)
        self.actionNew.setObjectName("actionNew")
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionQuit = QtWidgets.QAction(MainWindow)
        self.actionQuit.setObjectName("actionQuit")
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSave)
        self.menuQUIT.addAction(self.actionQuit)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuQUIT.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Write your code here:"))
        self.pushButton.setText(_translate("MainWindow", "Run Scanner"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuQUIT.setTitle(_translate("MainWindow", "Other"))
        self.actionNew.setText(_translate("MainWindow", "New"))
        self.actionNew.setShortcut(_translate("MainWindow", "Ctrl+N"))
        #
        self.actionNew.triggered.connect(self.clear_text)
        #
        self.actionOpen.setText(_translate("MainWindow", "Open"))
        self.actionOpen.setShortcut(_translate("MainWindow", "Ctrl+O"))
        #
        self.actionOpen.triggered.connect(self.open_file)
        #
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionSave.setShortcut(_translate("MainWindow", "Ctrl+S"))
        #
        self.actionSave.triggered.connect(self.save_file)
        #
        self.actionQuit.setText(_translate("MainWindow", "Quit"))
        self.actionQuit.setShortcut(_translate("MainWindow", "Ctrl+Q"))
        #
        self.actionQuit.triggered.connect(self.close_program)
        #

    #
    def saveText(self):
        with open('input.txt', 'w') as f:
            mytext = self.textEdit.toPlainText()
            f.write(mytext)

    def readData(self):
        with open("output.txt", "r") as f:
            lines = f.readlines()

        table_model = self.tableView.model()

        table_model.setRowCount(0)

        for line in lines:
            token = json.loads(line)

            rowPosition = table_model.rowCount()
            table_model.insertRow(rowPosition)

            table_model.setItem(rowPosition, 0, QStandardItem(list(token.items())[0][0]))
            table_model.setItem(rowPosition, 1, QStandardItem(list(token.items())[0][1]))

    def start_scanning(self):
        self.saveText()
        success = scanner("input.txt", "output.txt")
        if not success:
            self.msg = QtWidgets.QMessageBox()
            self.msg.setWindowTitle("Error scanning")
            self.msg.setText("Error occurred")
            self.msg.setIcon(QMessageBox.Warning)
            self.msg.setStandardButtons(QMessageBox.Ok)
            self.msg.show()

        self.readData()

    def save_file(self):
        filename = QFileDialog.getSaveFileName(None, 'Save File', os.getenv('HOME'))
        if filename[0]:
            with open(filename[0], 'w') as f:
                my_text = self.textEdit.toPlainText()
                f.write(my_text)

    def open_file(self):
        filename = QFileDialog.getOpenFileName(None, 'Open File', os.getenv('HOME'))
        if filename[0]:
            with open(filename[0], 'r') as f:
                file_text = f.read()
                self.textEdit.setText(file_text)

    def clear_text(self):
        self.textEdit.clear()

    def close_program(self):
        sys.exit()
    #


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

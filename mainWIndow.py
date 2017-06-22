from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDesktopWidget,QMainWindow
import sys
import os
import sqlite3
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(1280, 720)
        MainWindow.setWindowTitle('招聘信息提取分析器')
        MainWindow.setWindowIcon(QtGui.QIcon(os.getcwd() + '/resource/myico.png'))      

        #set mainwindow to center of desktop
        qr = MainWindow.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        MainWindow.move(qr.topLeft())

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)

        qss_file = open(os.getcwd() + '/resource/QSS/Mainwindow.qss').read()
        self.setStyleSheet(qss_file)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        

        self.TypeBox = QtWidgets.QComboBox(self.centralwidget)
        self.TypeBox.setGeometry(QtCore.QRect(20, 40, 100, 30))

        self.positionEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.positionEdit.setGeometry(QtCore.QRect(170, 40, 150, 30))
        self.positionEdit.setObjectName("postionEdit")
    
        self.keywordEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.keywordEdit.setGeometry(QtCore.QRect(370, 40, 330, 30))
        self.keywordEdit.setObjectName("keywordEdit")

        self.serchBtn = QtWidgets.QPushButton(self.centralwidget)
        self.serchBtn.setGeometry(QtCore.QRect(970, 40, 300, 30))
        self.serchBtn.setObjectName("serchBtn")
        self.serchBtn.clicked.connect(self.work)

        self.SalaryImage = QtWidgets.QLabel(self.centralwidget)
        self.SalaryImage.setGeometry(QtCore.QRect(520, 80, 440, 600))
        self.SalaryImage.setAlignment(QtCore.Qt.AlignCenter)
        self.SalaryImage.setObjectName("SalaryImage")
        
        self.PositionImage = QtWidgets.QLabel(self.centralwidget)
        self.PositionImage.setGeometry(QtCore.QRect(20, 80, 500, 600))
        self.PositionImage.setAlignment(QtCore.Qt.AlignCenter)
        self.PositionImage.setObjectName("PositionImage")

        #从数据库里得到最后一次搜索的网站类型，便于恢复数据显示
        self.db = sqlite3.connect('jobs.db')
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM latestType")
        self.type = cursor.fetchall()[0][1]
        cursor.close()
        self.db.commit()

        PixMapSalary = QtGui.QPixmap(os.getcwd() + '/resource/%s/images/1.png' % self.type).scaled(400,600)
        self.SalaryImage.setPixmap(PixMapSalary)
        PixMapPosition = QtGui.QPixmap(os.getcwd() + '/resource/%s/images/2.png' % self.type).scaled(500,500)
        self.PositionImage.setPixmap(PixMapPosition)

        self.TypeLabel = QtWidgets.QLabel(self.centralwidget)
        self.TypeLabel.setGeometry(QtCore.QRect(20,5,100,30))
        self.TypeLabel.setObjectName("TypeLabel")
      
        self.PositionLabel = QtWidgets.QLabel(self.centralwidget)
        self.PositionLabel.setGeometry(QtCore.QRect(170, 5, 150, 30))
        self.PositionLabel.setObjectName("PostionLabel")

        self.KeywordLabel = QtWidgets.QLabel(self.centralwidget)
        self.KeywordLabel.setGeometry(QtCore.QRect(370, 5, 330, 30))
        self.KeywordLabel.setObjectName("KeywordLabel")

        self.Crawl_label = QtWidgets.QLabel(self.centralwidget)
        self.Crawl_label.setGeometry(QtCore.QRect(750, 5, 170, 30))
        self.Crawl_label.setObjectName("label")

        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(970, 80, 300, 600))
        self.listWidget.setObjectName("listWidget")
        self.listWidget.doubleClicked.connect(self.showItem)
        self.showStaff()


        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(970, 10, 300, 20))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")

        self.spinBox = QtWidgets.QSpinBox(self.centralwidget)
        self.spinBox.setGeometry(QtCore.QRect(750, 40, 170, 30))
        self.spinBox.setObjectName("spinBox")
        self.spinBox.setValue(20)
        self.spinBox.setMinimum(1)
        self.spinBox.setMaximum(100)

        #设置菜单栏
        exitAction = QtWidgets.QAction(QtGui.QIcon(os.getcwd() + '/resource/myico.png'),'退出',self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.triggered.connect(QtWidgets.qApp.quit)

        aboutAction = QtWidgets.QAction(QtGui.QIcon(os.getcwd() + '/resource/myico.png'),'关于 Qt',self)
        aboutAction.triggered.connect(QtWidgets.qApp.aboutQt)


        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1280, 28))
        self.menubar.setObjectName("menubar")

        fileMenu = self.menubar.addMenu('&文件')
        fileMenu.addAction(exitAction)

        aboutMent = self.menubar.addMenu('&关于')
        aboutMent.addAction(aboutAction)

        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")

        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        #界面初始化时，读取一次文件并存入内存中，方便提取
        

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "招聘信息抓取分析器"))
        self.serchBtn.setText(_translate("MainWindow", "搜索"))
        self.PositionLabel.setText(_translate("MainWindow", "位置 （例如 北京）:"))
        self.KeywordLabel.setText(_translate("MainWindow", "关键字（例如 C++）:"))
        self.Crawl_label.setText(_translate("MainWindow", "爬取的网页数: "))
        self.TypeLabel.setText(_translate("MainWindow", "选择爬取的网站: "))
        self.TypeBox.addItem("拉勾网")
        self.TypeBox.addItem("智联招聘")




        

















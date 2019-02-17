import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QCompleter
from PyQt5 import QtGui, QtCore
import socket

HOST = 'localhost'
PORT = 9009


class MyWindow(QMainWindow):
    filename = ""
    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        self.setGeometry(800, 400, 300, 150)

        # Label
        label = QLabel("IP", self)
        label.move(15, 20)

        '''
        self.progressBar = QProgressBar(self)
        self.progressBar.move(180, 80)
        self.progressBar.setRange(0, 10)
        '''

        btn1 = QPushButton("Click me", self)
        btn1.move(180, 20)
        # btn1.clicked.connect(self.btn1_clicked)
        btn1.clicked.connect(self.getFileFromServer)

        # LineEdit
        self.lineEdit = QLineEdit("", self)
        self.lineEdit.move(50, 20)
        self.lineEdit.returnPressed.connect(self.btn1_clicked)

        # StatusBar
        self.statusBar = QStatusBar(self)
        self.setStatusBar(self.statusBar)

    def lineEditChanged(self):
        self.statusBar.showMessage(self.lineEdit.text())


    def btn1_clicked(self):
        self.filename = self.lineEdit.text()
        self.getFileFromServer()
        #self.btn1.clicked.connect(self.btn1_clicked)4


    def getFileFromServer(self):
        QMessageBox.about(self, "Okay", "시작")

        data_transferred = 0

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((HOST, PORT))
            sock.sendall(self.filename.encode())

            data = sock.recv(1024)
            if not data:
                print('파일[%s]: 서버에 존재하지 않거나 전송중 오류발생' % self.filename)
                return

            with open('download/' + self.filename, 'wb') as f:
                try:
                    while data:
                        f.write(data)
                        data_transferred += len(data)
                        data = sock.recv(1024)
                        QMessageBox.about(self, "성공", '파일[%s] 전송종료. 전송량 [%d]' % (self.filename, data_transferred))
                except Exception as e:
                    QMessageBox.about(self, "실패", '오류가 발생했습니다')

        print('파일[%s] 전송종료. 전송량 [%d]' % (self.filename, data_transferred))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QCompleter
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import *
import socket


class MyWindow(QMainWindow):
    HOST = ''
    PORT = 9009
    filename = ""

    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        self.setGeometry(800, 400, 300, 180)
        self.setWindowTitle("파일 전송")
        self.setWindowIcon(QIcon("images.png"))

        # Label
        label = QLabel("파일 이름", self)
        label.move(20, 70)

        # IPAddress
        self.ip_addr_label = QLabel("IP 주소", self)
        self.ip_addr_label.move(20, 30)
        self.ip_addr_line_edit = QLineEdit("127.0.0.1", self)
        self.ip_addr_line_edit.resize(150, 30)
        self.ip_addr_line_edit.move(130, 30)

        # File name
        self.line_edit = QLineEdit("파일 이름입력", self)
        self.line_edit.resize(150, 30)
        self.line_edit.move(130, 70)
        self.line_edit.returnPressed.connect(self.btn1_clicked)

        btn1 = QPushButton("전송 시작", self)
        btn1.move(180, 120)
        # btn1.clicked.connect(self.btn1_clicked)
        btn1.clicked.connect(self.btn1_clicked)

        ip_addr_btn = QPushButton("IP 설정", self)
        ip_addr_btn.move(20, 120)
        ip_addr_btn.clicked.connect(self.get_ip_addr)

    def get_ip_addr(self):
        self.HOST = self.ip_addr_line_edit.text()
        QMessageBox.about(self, "Okay", 'IP 주소 설정 완료')

    def line_edit_changed(self):
        self.statusBar.showMessage(self.lineEdit.text())

    def btn1_clicked(self):
        line_edit_empty_checker = "파일 이름입력"
        self.filename = self.line_edit.text()

        # 아이피 주소가 잘못 성절되었을 경우
        # 파일 이름이 입력되지 않았을 경우
        # 두가지 경우 모두
        # 세가지 상황에 모두 대처 할것
        if self.filename == line_edit_empty_checker:
            QMessageBox.about(self, "실패", '파일 이름을 입력해주세요')
        else:
            self.get_file_from_server()

    def get_file_from_server(self):
        # QMessageBox.about(self, "Okay", "시작")

        data_transferred = 0

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            try:
                # 연결이 없을 경우 자동으로 끊어버리는 기능 추가 할것
                sock.connect((self.HOST, self.PORT))
                sock.sendall(self.filename.encode())
                data = sock.recv(1024)
            except Exception as e:
                QMessageBox.about(self, "실패", 'IP 주소를 설정하고 다시 시도해 주세요')
                return None

            if not data:
                QMessageBox.about(self, "실패", '파일[%s]: 서버에 존재하지 않거나 전송중 오류발생' % self.filename)
                return None

            with open('download/' + self.filename, 'wb') as f:
                try:
                    while data:
                        f.write(data)
                        data_transferred += len(data)
                        data = sock.recv(1024)
                except Exception as e:
                    QMessageBox.about(self, "실패", '파일[%s]: 서버에 존재하지 않거나 전송중 오류발생' % self.filename)
            f.close()
            sock.close()

            QMessageBox.about(self, "성공", '파일[%s] 전송종료. 전송량 [%d]' % (self.filename, data_transferred))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()
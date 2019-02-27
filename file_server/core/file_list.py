import os

from PyQt5.QtGui import *
from PyQt5.QtCore import *

import sys

from PyQt5.QtWidgets import QListWidget, QMessageBox, QApplication


class FileListSearch:
    def __init__(self, dirname):
        self.dirname = dirname

    def search(self):
        filenames = os.listdir(self.dirname)
        return filenames


class myListWidget(QListWidget):

    def Clicked(self, item):
        QMessageBox.information(self, "ListWidget", "You clicked: " + item.text())


def main():
    app = QApplication(sys.argv)

    FileList = FileListSearch("C:/")
    file_list = FileList.search()


    listWidget = myListWidget()

    # Resize width and height
    listWidget.resize(300, 120)

    listWidget.setWindowTitle('PyQT QListwidget Demo')
    listWidget.itemClicked.connect(listWidget.Clicked)

    listWidget.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
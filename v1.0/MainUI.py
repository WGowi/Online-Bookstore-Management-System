import sys
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal


class MainUI(QWidget):
    switch_window1 = pyqtSignal()
    switch_window2 = pyqtSignal()
    switch_window3 = pyqtSignal()

    def __init__(self):
        super(MainUI, self).__init__()
        self.initUI()

    def initUI(self):
        # 字体
        font = QFont("Arial", 40, QFont.Black)

        # 标签
        title = QLabel(self)
        title.setFont(font)
        title.setText('欢迎来到网上书店管理系统')
        img = QPixmap('/Users/wugaowei/学习/编程练习/Pycharm/Python 3.7/pure python/数据库课设/img/login01.png')
        img_lable = QLabel(self)
        img_lable.setPixmap(img)

        # 按钮
        B_ifo_btn = QPushButton("管理图书信息")
        M_ifo_btn = QPushButton('查看会员信息')
        O_ifo_btn = QPushButton("查看购买记录")
        B_ifo_btn.clicked.connect(self.find_b_ifo)
        M_ifo_btn.clicked.connect(self.find_m_ifo)
        O_ifo_btn.clicked.connect(self.find_o_ifo)

        # 布局
        self.resize(868, 600)
        self.center()
        self.setWindowTitle('欢迎来到网上书店管理系统')
        grid = QGridLayout()
        grid.setSpacing(10)
        grid.addWidget(title, 0, 0, 1, 2)
        grid.addWidget(img_lable, 1, 0, 1, 2)
        grid.addWidget(B_ifo_btn, 2, 0)
        grid.addWidget(M_ifo_btn, 2, 1)
        grid.addWidget(O_ifo_btn, 3, 0, 1, 2)
        self.setLayout(grid)
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def find_b_ifo(self):
        self.switch_window1.emit()

    def find_m_ifo(self):
        self.switch_window2.emit()

    def find_o_ifo(self):
        self.switch_window3.emit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainUI()
    sys.exit(app.exec_())

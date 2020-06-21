import sys

import qdarkstyle
# from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import *


# from hello import MainUI


class LoginUI(QWidget):
    switch_window = pyqtSignal()

    def __init__(self):
        super(LoginUI, self).__init__()
        self.initUI()

    def initUI(self):
        # 标签
        self.username_label = QLabel("用户名:")
        self.pwd_label = QLabel("密    码:")

        # 输入框
        self.username_edit = QLineEdit()
        self.pwd_edit = QLineEdit()
        self.pwd_edit.setEchoMode(QLineEdit.Password)  # 密码不可见

        # 按钮
        self.OK_btn = QPushButton("登陆")
        self.Cancel_btn = QPushButton("退出")
        self.Cancel_btn.clicked.connect(self.close)
        self.OK_btn.clicked.connect(self.login)

        # 布局
        flo = QFormLayout()
        # flo.addRow()
        flo.addRow(self.username_label, self.username_edit)
        flo.addRow(self.pwd_label, self.pwd_edit)
        flo.addRow(self.OK_btn, self.Cancel_btn)
        self.setLayout(flo)

        self.setWindowTitle('Login')
        self.center()
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def login(self):
        if self.username_edit.text() == 'admin' and self.pwd_edit.text() == 'admin':
            self.switch_window.emit()

        else:
            QMessageBox.critical(self, "登陆失败", "用户名或密码错误")
            # 保留用户名删除密码，光标停留在密码处
            self.pwd_edit.clear()
            self.pwd_edit.setFocus()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    LoginUI = LoginUI()
    LoginUI.show()
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    sys.exit(app.exec_())

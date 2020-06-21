import sys
import pymssql
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import *

server = 'localhost'
user = 'SA'
password = ''
database = 'Course_Design'


class Member_informationUI(QWidget):
    switch_window = pyqtSignal()

    def __init__(self):
        super(Member_informationUI, self).__init__()
        self.initUI()

    def initUI(self):
        # 从数据库中获取数据
        self.connect = pymssql.connect(server, user, password, database)  # 服务器名,账户,密码,数据库名
        self.cursor = self.connect.cursor()
        self.sql = 'select Member_name,Member_sex,Member_address,Member_phone from Member_Information'
        self.cursor.execute(self.sql)
        self.results = self.cursor.fetchall()

        # 标签
        self.f_label = QLabel("查询会员姓名:")

        # 输入框
        self.e1 = QLineEdit()
        # 表格
        self.up = 0
        self.down = 10
        self.page = 10
        self.table = QTableWidget(self.page, len(self.results[0]))
        self.row_name = [
            '会员姓名',
            '性别',
            '住址',
            '电话号码',
        ]
        self.table.setHorizontalHeaderLabels(self.row_name)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.show_all_member()

        self.table.setAlternatingRowColors(True)  # 相邻的行不同的色

        # 按钮
        self.find_btn = QPushButton("查询")
        self.up_dtn = QPushButton('上一页')
        self.down_dtn = QPushButton('下一页')
        self.back_btn = QPushButton('返回主页')
        self.find_btn.clicked.connect(self.find_Member)
        self.down_dtn.clicked.connect(self.down_page)
        self.up_dtn.clicked.connect(self.up_page)
        self.back_btn.clicked.connect(self.back_home)

        # 布局
        self.resize(540, 420)
        self.setWindowTitle('会员信息')
        grid = QGridLayout()
        grid.setSpacing(10)
        grid.addWidget(self.f_label, 0, 0, 1, 1)
        grid.addWidget(self.e1, 0, 1, 1, 4)
        grid.addWidget(self.find_btn, 0, 5, 1, 1)
        grid.addWidget(self.table, 1, 0, 2, 6)
        grid.addWidget(self.up_dtn, 4, 0, 1, 3)
        grid.addWidget(self.down_dtn, 4, 3, 1, 3)
        grid.addWidget(self.back_btn, 5, 0, 1, 6)
        self.setLayout(grid)
        self.show()

    def down_page(self):
        print('后一页')
        print('self.up', self.up)
        print('self.down', self.down)
        if self.down + self.page < len(self.results):
            self.up += self.page
            self.down += self.page
            self.table.clearContents()
            # self.Table_show()
            self.table.setHorizontalHeaderLabels(self.row_name)
            self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
            for i in range(0, 10):
                for j in range(len(self.results[0])):
                    self.table.setItem(i, j, QTableWidgetItem(str(self.results[i + self.down][j])))
                    self.table.item(i, j).setTextAlignment(Qt.AlignCenter)

        else:
            QMessageBox.critical(self, "操作失败", "已经到达最后一页")

    def up_page(self):
        print('前一页')
        print('self.up', self.up)
        print('self.down', self.down)
        # print('len(self.results)', len(self.results))
        if self.up - self.page >= 0:
            self.up -= self.page
            self.down -= self.page
            self.table.clearContents()
            # self.Table_show()
            self.table.setHorizontalHeaderLabels(self.row_name)
            self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
            self.show_member()

        else:
            QMessageBox.critical(self, "操作失败", "已经到达最前一页")

    def back_home(self):
        self.switch_window.emit()

    def find_Member(self):
        Member_name = self.e1.text()
        sql1 = "select Member_name,Member_sex,Member_address,Member_phone from Member_Information where Member_name like N" + "\'" + Member_name + "%\'"
        self.cursor.execute(sql1)
        self.results = self.cursor.fetchall()

        for i in range(len(self.results)):
            print(self.results[i])

        if len(self.results) == 0:
            self.show_all_member()
            QMessageBox.critical(self, "失败", "未查询到此会员信息")
        else:
            self.show_member()

    def show_member(self):
        self.table.clearContents()
        if len(self.results) >= 10:
            x = 10
        else:
            x = len(self.results)
        for i in range(0, x):
            for j in range(len(self.results[0])):
                self.table.setItem(i, j, QTableWidgetItem(str(self.results[self.up + i][j])))
                self.table.item(i, j).setTextAlignment(Qt.AlignCenter)

    def show_all_member(self):
        self.sql = 'select Member_name,Member_sex,Member_address,Member_phone from Member_Information'
        self.cursor.execute(self.sql)
        self.results = self.cursor.fetchall()
        self.show_member()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    Member_informationUI = Member_informationUI()
    sys.exit(app.exec_())

import sys
import pymssql
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import *

server = 'localhost'
user = 'SA'
password = ''
database = 'Course_Design'


class Book_informationUI(QWidget):
    switch_window1 = pyqtSignal()
    switch_window2 = pyqtSignal()
    switch_window3 = pyqtSignal()
    switch_window4 = pyqtSignal()

    def __init__(self):
        super(Book_informationUI, self).__init__()
        self.initUI()

    def initUI(self):
        # 从数据库中获取数据
        self.connect = pymssql.connect(server, user, password, database)  # 服务器名,账户,密码,数据库名
        self.cursor = self.connect.cursor()
        self.sql = 'select Book_name, Book_author, Book_Publishing_house, Book_kind, Book_price, Book_stock from Book_Information inner join Book_storage on Book_Information.Book_no = Book_storage.Book_no'
        self.cursor.execute(self.sql)
        self.results = self.cursor.fetchall()

        # 标签
        self.f_label = QLabel("查询书名:")

        # 输入框
        self.e1 = QLineEdit()

        # 表格
        self.up = 0
        self.down = 10
        self.page = 10
        self.table = QTableWidget(self.page, len(self.results[0]))
        self.row_name = [
            '书名',
            '作者',
            '出版社',
            '种类',
            '价格',
            '库存',
        ]
        self.show_all_book()
        self.table.setHorizontalHeaderLabels(self.row_name)
        # self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.table.setAlternatingRowColors(True)  # 相邻行不同的色

        # 按钮
        self.buy_btn = QPushButton("进货")
        self.sell_btn = QPushButton("出货")
        self.change_btn = QPushButton("修改图书信息")
        self.find_btn = QPushButton("查询")
        self.up_dtn = QPushButton('上一页')
        self.down_dtn = QPushButton('下一页')
        self.back_btn = QPushButton('返回主页')
        self.buy_btn.clicked.connect(self.show_addUI)
        self.sell_btn.clicked.connect(self.show_sellUI)
        self.change_btn.clicked.connect(self.show_changeUI)
        self.find_btn.clicked.connect(self.find_book)
        self.down_dtn.clicked.connect(self.down_page)
        self.up_dtn.clicked.connect(self.up_page)
        self.back_btn.clicked.connect(self.back_home)

        # 布局
        self.resize(600, 420)
        self.setWindowTitle('图书信息')
        grid = QGridLayout()
        grid.setSpacing(10)
        grid.addWidget(self.f_label, 0, 0, 1, 1)
        grid.addWidget(self.e1, 0, 1, 1, 5)
        grid.addWidget(self.find_btn, 0, 6, 1, 1)
        grid.addWidget(self.table, 1, 1, 8, 6)
        grid.addWidget(self.up_dtn, 9, 1, 1, 3)
        grid.addWidget(self.down_dtn, 9, 4, 1, 3)
        grid.addWidget(self.buy_btn, 2, 0, 1, 1)
        grid.addWidget(self.sell_btn, 4, 0, 1, 1)
        grid.addWidget(self.change_btn, 6, 0, 1, 1)
        grid.addWidget(self.back_btn, 8, 0, 1, 1)
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
            # self.show_book()
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
            # self.show_book()
            self.table.setHorizontalHeaderLabels(self.row_name)
            self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
            self.show_book()

        else:
            QMessageBox.critical(self, "操作失败", "已经到达最前一页")

    def back_home(self):
        self.switch_window1.emit()

    def show_sellUI(self):
        self.switch_window2.emit()

    def show_addUI(self):
        self.switch_window3.emit()

    def show_changeUI(self):
        self.switch_window4.emit()

    def find_book(self):
        book_name = self.e1.text()
        sql1 = "select Book_name, Book_author, Book_Publishing_house, Book_kind, Book_price, Book_stock from Book_Information inner join Book_storage on Book_Information.Book_no = Book_storage.Book_no where Book_name like N" + "\'" + book_name + "%\'"
        self.cursor.execute(sql1)
        self.results = self.cursor.fetchall()

        for i in range(len(self.results)):
            print(self.results[i])

        if len(self.results) == 0:
            self.show_all_book()
            QMessageBox.critical(self, "失败", "未查询到此书")
        else:
            self.show_book()

    def show_book(self):
        self.table.clearContents()
        if len(self.results) >= 10:
            x = 10
        else:
            x = len(self.results)
        for i in range(0, x):
            for j in range(len(self.results[0])):
                self.table.setItem(i, j, QTableWidgetItem(str(self.results[self.up + i][j])))
                self.table.item(i, j).setTextAlignment(Qt.AlignCenter)

    def show_all_book(self):
        self.sql = 'select Book_name, Book_author, Book_Publishing_house, Book_kind, Book_price, Book_stock from Book_Information inner join Book_storage on Book_Information.Book_no = Book_storage.Book_no'
        self.cursor.execute(self.sql)
        self.results = self.cursor.fetchall()
        self.show_book()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    Book_informationUI = Book_informationUI()
    sys.exit(app.exec_())

import sys
import pymssql
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import *

server = 'localhost'
user = 'SA'
password = ''
database = 'Course_Design'


class Change_bookUI(QWidget):
    switch_window = pyqtSignal()

    def __init__(self):
        super(Change_bookUI, self).__init__()
        self.initUI()

    def initUI(self):
        # 从数据库中获取数据
        self.connect = pymssql.connect(server, user, password, database)  # 服务器名,账户,密码,数据库名
        self.cursor = self.connect.cursor()
        self.sql = 'select Book_Information.Book_no, Book_name, Book_author, Book_Publishing_house, Book_kind, Book_price, Book_stock from Book_Information inner join Book_storage on Book_Information.Book_no = Book_storage.Book_no'
        self.cursor.execute(self.sql)
        self.results = self.cursor.fetchall()

        # 标签
        self.f_label = QLabel("查询书名:")

        # 输入框
        self.e1 = QLineEdit()

        # 按钮
        self.find_btn = QPushButton("查询")
        self.up_dtn = QPushButton('上一页')
        self.down_dtn = QPushButton('下一页')
        self.back_btn = QPushButton('返回上一级')
        self.find_btn.clicked.connect(self.find_book)
        self.down_dtn.clicked.connect(self.down_page)
        self.up_dtn.clicked.connect(self.up_page)
        self.back_btn.clicked.connect(self.back_home)

        # 表格
        self.up = 0
        self.down = 10
        self.page = 10
        self.table = QTableWidget(self.page, len(self.results[0]) + 2)
        self.row_name = [
            '图书编号',
            '书名',
            '作者',
            '出版社',
            '种类',
            '价格',
            '库存',
            '修改按钮',
            '修改完成按钮',
        ]
        self.table.setHorizontalHeaderLabels(self.row_name)
        # self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # self.table.setEnabled(False)

        self.show_all_book()
        self.table.setAlternatingRowColors(True)  # 相邻行不同的色

        # 布局
        self.resize(540, 420)
        self.setWindowTitle('图书信息')
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
        self.btn1s = []
        self.btn2s = []
        btn01 = QPushButton("修改")
        btn02 = QPushButton("完成")
        btn11 = QPushButton("修改")
        btn12 = QPushButton("完成")
        btn21 = QPushButton("修改")
        btn22 = QPushButton("完成")
        btn31 = QPushButton("修改")
        btn32 = QPushButton("完成")
        btn41 = QPushButton("修改")
        btn42 = QPushButton("完成")
        btn51 = QPushButton("修改")
        btn52 = QPushButton("完成")
        btn61 = QPushButton("修改")
        btn62 = QPushButton("完成")
        btn71 = QPushButton("修改")
        btn72 = QPushButton("完成")
        btn81 = QPushButton("修改")
        btn82 = QPushButton("完成")
        btn91 = QPushButton("修改")
        btn92 = QPushButton("完成")

        btn01.clicked.connect(lambda: self.edit_row(0, 7, btn01))
        btn11.clicked.connect(lambda: self.edit_row(1, 7, btn11))
        btn21.clicked.connect(lambda: self.edit_row(2, 7, btn21))
        btn31.clicked.connect(lambda: self.edit_row(3, 7, btn31))
        btn41.clicked.connect(lambda: self.edit_row(4, 7, btn41))
        btn51.clicked.connect(lambda: self.edit_row(5, 7, btn51))
        btn61.clicked.connect(lambda: self.edit_row(6, 7, btn61))
        btn71.clicked.connect(lambda: self.edit_row(7, 7, btn71))
        btn81.clicked.connect(lambda: self.edit_row(8, 7, btn81))
        btn91.clicked.connect(lambda: self.edit_row(9, 7, btn91))

        btn02.clicked.connect(lambda: self.edit_ok(0, 7, btn01))
        btn12.clicked.connect(lambda: self.edit_ok(1, 7, btn11))
        btn22.clicked.connect(lambda: self.edit_ok(2, 7, btn21))
        btn32.clicked.connect(lambda: self.edit_ok(3, 7, btn31))
        btn42.clicked.connect(lambda: self.edit_ok(4, 7, btn41))
        btn52.clicked.connect(lambda: self.edit_ok(5, 7, btn51))
        btn62.clicked.connect(lambda: self.edit_ok(6, 7, btn61))
        btn72.clicked.connect(lambda: self.edit_ok(7, 7, btn71))
        btn82.clicked.connect(lambda: self.edit_ok(8, 7, btn81))
        btn92.clicked.connect(lambda: self.edit_ok(9, 7, btn91))

        self.btn1s.append(btn01)
        self.btn1s.append(btn11)
        self.btn1s.append(btn21)
        self.btn1s.append(btn31)
        self.btn1s.append(btn41)
        self.btn1s.append(btn51)
        self.btn1s.append(btn61)
        self.btn1s.append(btn71)
        self.btn1s.append(btn81)
        self.btn1s.append(btn91)

        self.btn2s.append(btn02)
        self.btn2s.append(btn12)
        self.btn2s.append(btn22)
        self.btn2s.append(btn32)
        self.btn2s.append(btn42)
        self.btn2s.append(btn52)
        self.btn2s.append(btn62)
        self.btn2s.append(btn72)
        self.btn2s.append(btn82)
        self.btn2s.append(btn92)

        print('后一页')
        print('self.up', self.up)
        print('self.down', self.down)
        if self.down + self.page < len(self.results):
            self.up += self.page
            self.down += self.page
            self.table.clearContents()
            # self.show_book()
            self.row_name = [
                '图书编号',
                '书名',
                '作者',
                '出版社',
                '种类',
                '价格',
                '库存',
            ]
            self.table.setHorizontalHeaderLabels(self.row_name)
            self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
            # self.table.setEnabled(False)
            for i in range(0, 10):
                if self.down + i > len(self.results) - 1:
                    break
                for j in range(len(self.results[0])):
                    if i + self.down >= len(self.results):
                        break
                    self.table.setItem(i, j, QTableWidgetItem(str(self.results[i + self.down][j])))
                    self.table.item(i, j).setTextAlignment(Qt.AlignCenter)
                    if j == len(self.results[0]) - 1:
                        self.table.setCellWidget(i, len(self.results[0]), self.btn1s[i])
                        self.table.setCellWidget(i, len(self.results[0]) + 1, self.btn2s[i])


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
            self.row_name = [
                '图书编号',
                '书名',
                '作者',
                '出版社',
                '种类',
                '价格',
                '库存',
                '修改按钮',
                '修改完成按钮',
            ]
            self.table.setHorizontalHeaderLabels(self.row_name)
            self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
            # self.table.setEnabled(False)
            self.show_book()

        else:
            QMessageBox.critical(self, "操作失败", "已经到达最前一页")

    def back_home(self):
        self.switch_window.emit()

    def find_book(self):
        book_name = self.e1.text()
        sql1 = "select Book_Information.Book_no, Book_name, Book_author, Book_Publishing_house, Book_kind, Book_price, Book_stock from Book_Information inner join Book_storage on Book_Information.Book_no = Book_storage.Book_no where Book_name like N" + "\'" + book_name + "%\'"
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
        self.btn1s = []
        self.btn2s = []
        btn01 = QPushButton("修改")
        btn02 = QPushButton("完成")
        btn11 = QPushButton("修改")
        btn12 = QPushButton("完成")
        btn21 = QPushButton("修改")
        btn22 = QPushButton("完成")
        btn31 = QPushButton("修改")
        btn32 = QPushButton("完成")
        btn41 = QPushButton("修改")
        btn42 = QPushButton("完成")
        btn51 = QPushButton("修改")
        btn52 = QPushButton("完成")
        btn61 = QPushButton("修改")
        btn62 = QPushButton("完成")
        btn71 = QPushButton("修改")
        btn72 = QPushButton("完成")
        btn81 = QPushButton("修改")
        btn82 = QPushButton("完成")
        btn91 = QPushButton("修改")
        btn92 = QPushButton("完成")

        btn01.clicked.connect(lambda: self.edit_row(0, 7, btn01))
        btn11.clicked.connect(lambda: self.edit_row(1, 7, btn11))
        btn21.clicked.connect(lambda: self.edit_row(2, 7, btn21))
        btn31.clicked.connect(lambda: self.edit_row(3, 7, btn31))
        btn41.clicked.connect(lambda: self.edit_row(4, 7, btn41))
        btn51.clicked.connect(lambda: self.edit_row(5, 7, btn51))
        btn61.clicked.connect(lambda: self.edit_row(6, 7, btn61))
        btn71.clicked.connect(lambda: self.edit_row(7, 7, btn71))
        btn81.clicked.connect(lambda: self.edit_row(8, 7, btn81))
        btn91.clicked.connect(lambda: self.edit_row(9, 7, btn91))

        btn02.clicked.connect(lambda: self.edit_ok(0, 7, btn01))
        btn12.clicked.connect(lambda: self.edit_ok(1, 7, btn11))
        btn22.clicked.connect(lambda: self.edit_ok(2, 7, btn21))
        btn32.clicked.connect(lambda: self.edit_ok(3, 7, btn31))
        btn42.clicked.connect(lambda: self.edit_ok(4, 7, btn41))
        btn52.clicked.connect(lambda: self.edit_ok(5, 7, btn51))
        btn62.clicked.connect(lambda: self.edit_ok(6, 7, btn61))
        btn72.clicked.connect(lambda: self.edit_ok(7, 7, btn71))
        btn82.clicked.connect(lambda: self.edit_ok(8, 7, btn81))
        btn92.clicked.connect(lambda: self.edit_ok(9, 7, btn91))

        self.btn1s.append(btn01)
        self.btn1s.append(btn11)
        self.btn1s.append(btn21)
        self.btn1s.append(btn31)
        self.btn1s.append(btn41)
        self.btn1s.append(btn51)
        self.btn1s.append(btn61)
        self.btn1s.append(btn71)
        self.btn1s.append(btn81)
        self.btn1s.append(btn91)

        self.btn2s.append(btn02)
        self.btn2s.append(btn12)
        self.btn2s.append(btn22)
        self.btn2s.append(btn32)
        self.btn2s.append(btn42)
        self.btn2s.append(btn52)
        self.btn2s.append(btn62)
        self.btn2s.append(btn72)
        self.btn2s.append(btn82)
        self.btn2s.append(btn92)

        self.table.clearContents()
        if len(self.results) >= 10:
            x = 10
        else:
            x = len(self.results)
        for i in range(0, x):
            for j in range(len(self.results[0])):
                self.table.setItem(i, j, QTableWidgetItem(str(self.results[self.up + i][j])))
                self.table.item(i, j).setTextAlignment(Qt.AlignCenter)
            self.table.setCellWidget(i, len(self.results[0]), self.btn1s[i])
            self.table.setCellWidget(i, len(self.results[0]) + 1, self.btn2s[i])
            # if j == len(self.results[0]) - 1:
            # btn1 = QPushButton('修改')
            # btn2 = QPushButton('完成')
            # self.btn1s.append(btn1)
            # self.btn2s.append(btn2)

    # for i in range(len(self.btn1s)):
    #     self.btn1s[i].clicked.connect(lambda: self.edit_row(i, len(self.results[0]), self.btn1s[i]))
    #     self.btn2s[i].clicked.connect(lambda: self.edit_row(i, len(self.results[0]) + 1, self.btn2s[i]))

    def show_all_book(self):
        self.sql = 'select Book_Information.Book_no ,Book_name, Book_author, Book_Publishing_house, Book_kind, Book_price, Book_stock from Book_Information inner join Book_storage on Book_Information.Book_no = Book_storage.Book_no'
        self.cursor.execute(self.sql)
        self.results = self.cursor.fetchall()
        self.show_book()

    def edit_row(self, row, col, btn):
        print('row', row)
        print('col', col)
        print('btn.index', btn)
        if len(self.results) < len(self.btn1s):
            x = len(self.results)
        else:
            x = len(self.btn1s)
        for i in range(x):
            if i != row:
                self.btn1s[i].setEnabled(False)
                self.btn2s[i].setEnabled(False)
                for j in range(len(self.results[0])):
                    self.table.item(i, j).setFlags(Qt.ItemIsEditable)
        self.table.item(row, 0).setFlags(Qt.ItemIsEditable)
        for i in range(1, len(self.results[0])):
            # self.table.item(row, i).setFlags(QAbstractItemView.)
            # self.table.item(row, i).setFlags(Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            self.table.setEditTriggers(QAbstractItemView.AllEditTriggers)

    def edit_ok(self, row, col, btn):
        Book_no = self.table.item(row, 0).text().rstrip()
        Book_name = self.table.item(row, 1).text().rstrip()
        Book_author = self.table.item(row, 2).text().rstrip()
        Book_Publishing_house = self.table.item(row, 3).text().rstrip()
        Book_kind = self.table.item(row, 4).text().rstrip()
        Book_price = self.table.item(row, 5).text().rstrip()
        Book_stock = self.table.item(row, 6).text().rstrip()

        sql = "update Book_Information set Book_name=N'" + Book_name + "',Book_author=N'" + Book_author + "',Book_Publishing_house=N'" + Book_Publishing_house + "',Book_kind=N'" + Book_kind + "'"+ " where Book_no='" + str(Book_no) + "'"
        print(sql)
        self.cursor.execute(sql)
        self.connect.commit()
        sql0 = "update Book_storage  set Book_price=" + str(Book_price) + ",Book_stock=" + str(
            Book_stock) + " where Book_no='" + str(Book_no) + "'"
        print(sql0)
        self.cursor.execute(sql0)
        self.connect.commit()
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        if len(self.results) < len(self.btn1s):
            x = len(self.results)
        else:
            x = len(self.btn1s)
        for i in range(x):
            if i != row:
                self.btn1s[i].setEnabled(True)
                self.btn2s[i].setEnabled(True)
                for j in range(len(self.results[0])):
                    self.table.item(i, j).setFlags(Qt.ItemIsEnabled)
        self.table.item(row, 0).setFlags(Qt.ItemIsEnabled)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    Book_informationUI = Change_bookUI()
    sys.exit(app.exec_())

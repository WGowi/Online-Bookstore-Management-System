import sys
import pymssql
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import *

server = 'localhost'
user = 'SA'
password = ''
database = 'Course_Design'


class Add_bookUI(QWidget):
    switch_window = pyqtSignal()

    def __init__(self):
        super(Add_bookUI, self).__init__()
        self.initUI()

    def initUI(self):
        # 从数据库中获取数据
        self.connect = pymssql.connect(server, user, password, database)  # 服务器名,账户,密码,数据库名
        self.cursor = self.connect.cursor()

        # 标签
        self.book_name_label = QLabel("图书名称:")
        self.author_name_label = QLabel("作者:")
        self.pub_house_label = QLabel("出版社:")
        self.book_kind_label = QLabel("图书种类:")
        self.price_label = QLabel("销售价格:")
        self.num_label = QLabel("购入数目:")

        # 输入框
        self.book_name_e = QLineEdit()
        self.author_name_e = QLineEdit()
        self.pub_house_e = QLineEdit()
        self.book_kind_e = QLineEdit()
        self.price_e = QLineEdit()
        self.num_e = QLineEdit()
        self.book_name_e.editingFinished.connect(self.kind_is_ok)
        self.book_name_e.editingFinished.connect(self.price_is_ok)
        self.pub_house_e.editingFinished.connect(self.kind_is_ok)
        self.pub_house_e.editingFinished.connect(self.price_is_ok)
        self.author_name_e.editingFinished.connect(self.kind_is_ok)
        self.author_name_e.editingFinished.connect(self.kind_is_ok)

        # 按钮
        self.ok_btn = QPushButton("确认")
        self.cancel_btn = QPushButton("取消")
        self.ok_btn.clicked.connect(self.order_is_ok)
        self.cancel_btn.clicked.connect(self.cancel_order)

        # 布局
        self.setWindowTitle("购入图书")
        self.resize(300, 400)
        self.center()
        grid = QGridLayout()
        grid.setSpacing(10)
        grid.addWidget(self.book_name_label, 0, 0)
        grid.addWidget(self.book_name_e, 0, 1)
        grid.addWidget(self.author_name_label, 1, 0)
        grid.addWidget(self.author_name_e, 1, 1)
        grid.addWidget(self.pub_house_label, 2, 0)
        grid.addWidget(self.pub_house_e, 2, 1)
        grid.addWidget(self.book_kind_label, 3, 0)
        grid.addWidget(self.book_kind_e, 3, 1)
        grid.addWidget(self.price_label, 4, 0)
        grid.addWidget(self.price_e, 4, 1)
        grid.addWidget(self.num_label, 5, 0)
        grid.addWidget(self.num_e, 5, 1)
        grid.addWidget(self.cancel_btn, 6, 0)
        grid.addWidget(self.ok_btn, 6, 1)
        self.setLayout(grid)
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def kind_is_ok(self):
        book_name = self.book_name_e.text()
        author_name = self.author_name_e.text()
        pub_house = self.pub_house_e.text()
        sql = 'select Book_kind from Book_information where Book_name = N' + "\'" + book_name + "\' and Book_author=N\'" + author_name + "\' and Book_Publishing_house=N\'" + pub_house + "\'"
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        if len(results) > 0:
            self.book_kind_e.setText(results[0][0])
            self.book_name_e.setReadOnly(True)

    def price_is_ok(self):
        book_name = self.book_name_e.text()
        author_name = self.author_name_e.text()
        pub_house = self.pub_house_e.text()
        sql = 'select Book_price from Book_Information inner join Book_storage on Book_Information.Book_no = Book_storage.Book_no  where Book_name = N' + "\'" + book_name + "\' and Book_author=N\'" + author_name + "\' and Book_Publishing_house=N\'" + pub_house + "\'"
        print(sql)
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        if len(results) > 0:
            self.price_e.setText(str(results[0][0]))

    def order_is_ok(self):
        book_name = self.book_name_e.text()
        author_name = self.author_name_e.text()
        pub_house = self.pub_house_e.text()
        book_kind = self.book_kind_e.text()
        book_price = self.price_e.text()
        num = self.num_e.text()
        if book_name == "":
            QMessageBox.critical(self, "操作失败", "请输入图书名称")
        elif author_name == "":
            QMessageBox.critical(self, "操作失败", "请输入作者名字")
        elif pub_house == "":
            QMessageBox.critical(self, "操作失败", "请输入出版社信息")
        elif book_price == "":
            QMessageBox.critical(self, "操作失败", "请输入图书售价")
        elif book_kind == "":
            QMessageBox.critical(self, "操作失败", "请输入图书种类")
        else:
            QMessageBox.question(self, "提醒", "确定完成进货操作确定后无法更改，确定操作？", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if QMessageBox.Yes:
                sql1 = 'select Book_no from Book_information where Book_name = N' + "\'" + book_name + "\' and Book_author=N\'" + author_name + "\' and Book_Publishing_house=N\'" + pub_house + "\'"
                self.cursor.execute(sql1)
                results = self.cursor.fetchall()
                if len(results) > 0:
                    sql1 = 'select Book_no from Book_information where Book_name = N' + "\'" + book_name + "\' and Book_author=N\'" + author_name + "\' and Book_Publishing_house=N\'" + pub_house + "\'"
                    self.cursor.execute(sql1)
                    results = self.cursor.fetchall()
                    Bno = results[0][0]
                    sql2 = 'update Book_storage set Book_stock=Book_stock+' + num + ' where Book_no = ' + "\'" + Bno + "\'"
                    print(sql2)
                    self.cursor.execute(sql2)
                    self.connect.commit()
                else:
                    sql3 = 'select top 1 Book_no from Book_Information order by Book_no desc'
                    self.cursor.execute(sql3)
                    results = self.cursor.fetchall()
                    print(results[0][0].split('B'))
                    no = int(results[0][0].split('B')[1]) + 1
                    Bno = "B" + str(no)
                    sql4 = "insert into Book_Information values (\'" + Bno + '\',N\'' + book_name + '\',N\'' + author_name + '\',N\'' + pub_house + '\',N\'' + book_kind + '\'' + ')'
                    sql5 = "insert into Book_storage values (" + "\'" + Bno + "\'," + str(book_price) + "," + str(
                        num) + ")"
                    print(sql4)
                    self.cursor.execute(sql4)
                    self.connect.commit()
                    print(sql5)
                    self.cursor.execute(sql5)
                    self.connect.commit()
                    # results = self.cursor.fetchall()
                    # print(results)
                self.switch_window.emit()

    def cancel_order(self):
        QMessageBox.question(self, "确定取消进货", "取消操作后返回上一级", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if QMessageBox.Yes:
            self.switch_window.emit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Add_bookUI()
    sys.exit(app.exec_())

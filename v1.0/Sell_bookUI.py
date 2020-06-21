import sys

import pymssql
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import *

server = 'localhost'
user = 'SA'
password = ''
database = 'Course_Design'


class Sell_bookUI(QWidget):
    switch_window1 = pyqtSignal()
    switch_window2 = pyqtSignal()

    def __init__(self):
        super(Sell_bookUI, self).__init__()
        self.initUI()

    def initUI(self):
        # 从数据库中获取数据
        self.connect = pymssql.connect(server, user, password, database)  # 服务器名,账户,密码,数据库名
        self.cursor = self.connect.cursor()

        # 标签
        self.book_name_label = QLabel("出售书名:")
        self.author_name_label = QLabel("作者名字:")
        self.publishing_house_label = QLabel("出版社:")
        self.sell_num_label = QLabel("销售量:")
        self.buy_iph_label = QLabel("购入买方手机号码:")
        self.buy_adr_label = QLabel("买方地址(配送必填):")
        self.send = QLabel("是否配送:")

        # 输入框
        self.book_name_edit = QLineEdit()
        self.sell_num_edit = QLineEdit()
        self.buy_iph_edit = QLineEdit()
        self.buy_adr_edit = QLineEdit()
        self.book_name_edit.editingFinished.connect(self.book_is_exist)
        self.book_name_edit.editingFinished.connect(self.show_aut_ifo)
        self.sell_num_edit.textChanged.connect(self.sell_num_is_ok)
        # print(self.buy_iph_edit.maxLength())
        self.buy_iph_edit.setMaxLength(11)
        # self.buy_iph_edit.setValidator(QIntValidator(0, 2147483647))
        self.buy_iph_edit.editingFinished.connect(self.check_iph)
        self.buy_iph_edit.editingFinished.connect(self.find_adr)

        # 下拉框
        self.author_name_ifo = QComboBox()
        self.publishing_house_ifo = QComboBox()
        self.send_ifo = QComboBox()
        self.send_ifo.addItem("是")
        self.send_ifo.addItem("否")
        self.author_name_ifo.currentIndexChanged.connect(self.show_pub_ifo)

        # 按钮
        self.ok_btn = QPushButton("确定订单")
        self.cancel_btn = QPushButton("取消订单")
        self.ok_btn.clicked.connect(self.ok_order)
        self.cancel_btn.clicked.connect(self.cancel_order)

        # 布局
        self.setWindowTitle("填写出货订单")
        self.resize(300, 400)
        self.center()
        grid = QGridLayout()
        grid.setSpacing(10)
        grid.addWidget(self.book_name_label, 0, 0)
        grid.addWidget(self.book_name_edit, 0, 1)
        grid.addWidget(self.author_name_label, 1, 0)
        grid.addWidget(self.author_name_ifo, 1, 1)
        grid.addWidget(self.publishing_house_label, 2, 0)
        grid.addWidget(self.publishing_house_ifo, 2, 1)
        grid.addWidget(self.sell_num_label, 3, 0)
        grid.addWidget(self.sell_num_edit, 3, 1)
        grid.addWidget(self.buy_iph_label, 4, 0)
        grid.addWidget(self.buy_iph_edit, 4, 1)
        grid.addWidget(self.send, 5, 0, )
        grid.addWidget(self.send_ifo, 5, 1)
        grid.addWidget(self.buy_adr_label, 6, 0)
        grid.addWidget(self.buy_adr_edit, 6, 1)
        grid.addWidget(self.cancel_btn, 7, 0)
        grid.addWidget(self.ok_btn, 7, 1)
        self.setLayout(grid)
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def book_is_exist(self):
        book_name = self.book_name_edit.text()
        sql = 'select Book_name from Book_information where Book_name = N' + "\'" + book_name + "\'"
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        print(results)
        if len(results) == 0:
            print(111111)
            QMessageBox.critical(self, "操作失败", "仓库中不存在此书")
            print(222222)
            self.book_name_edit.clear()
            print(333333)
            self.book_name_edit.setFocus()
            print(444444)

    def show_aut_ifo(self):
        book_name = self.book_name_edit.text()
        sql = 'select Book_author from Book_information where Book_name = N' + "\'" + book_name + "\'"
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        self.author_name_ifo.clear()
        if len(results) != 0:
            print('111:', results[0])
            for ifo in results:
                self.author_name_ifo.addItem(ifo[0])
        print(results)

    def show_pub_ifo(self):
        book_name = self.book_name_edit.text()
        book_author = self.author_name_ifo.currentText()
        sql = 'select Book_Publishing_house from Book_information where Book_name = N' + "\'" + book_name + "\' and Book_author=N\'" + book_author + '\''
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        self.publishing_house_ifo.clear()
        if len(results) != 0:
            for ifo in results[0]:
                self.publishing_house_ifo.addItem(ifo)
        print(results)

    def sell_num_is_ok(self):
        book_name = self.book_name_edit.text()
        author_name = self.author_name_ifo.currentText()
        publishing_house_name = self.publishing_house_ifo.currentText()
        sql = 'select Book_stock from Book_storage inner join Book_Information on Book_information.Book_no=Book_storage.Book_no where Book_name = N' + "\'" + book_name + "\' and Book_author=N\'" + author_name + "\' and Book_Publishing_house=N\'" + publishing_house_name + "\'"
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        print(results)
        print(self.sell_num_edit.text())
        if len(results) != 0:
            if self.sell_num_edit.text() == "" or int(self.sell_num_edit.text()) <= 0:
                QMessageBox.critical(self, "操作错误", "销售量不得小于1")
                self.sell_num_edit.clear()
                self.sell_num_edit.setFocus()
            if self.sell_num_edit.text() != "" and int(self.sell_num_edit.text()) > int(results[0][0]):
                QMessageBox.critical(self, "操作错误", "库存量不足,销售量不得大于" + str(results[0][0]))
                self.sell_num_edit.clear()
                self.sell_num_edit.setFocus()
        else:
            QMessageBox.information(self, "提醒", "请先输入图书名称，并选择作者与出版社", QMessageBox.Yes, QMessageBox.Yes)
            self.sell_num_edit.clear()
            self.book_name_edit.setFocus()

    def check_iph(self):
        iph = self.buy_iph_edit.text().rstrip()
        try:
            iph_1 = int(iph)
            # if len(iph) != 11:
            #     QMessageBox.warning(self, "手机号码异常", "手机号码长度不满足11位")
        except Exception:
            QMessageBox.warning(self, "操作失败", "检测到非法输入，请输入数字")
            # self.buy_iph_edit.clear()
            # self.buy_iph_edit.setFocus()

    def find_adr(self):
        iph = self.buy_iph_edit.text()
        sql = 'select Member_address from Member_information where Member_phone =' + "\'" + iph + "\'"
        print(sql)
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        print(results)
        print(len(results))
        if len(results) != 0:
            print(results[0][0])
            self.buy_adr_edit.setText(results[0][0])

    def ok_order(self):
        if len(self.book_name_edit.text()) == 0:
            QMessageBox.information(self, "操作失败", "图书名称未填写")
            self.book_name_edit.setFocus()
        elif len(self.sell_num_edit.text()) == 0:
            QMessageBox.information(self, "操作失败", "购买数目未填写")
            self.sell_num_edit.setFocus()
        elif len(self.buy_iph_edit.text()) == 0:
            QMessageBox.information(self, "操作失败", "买方手机号码未填写")
            self.sell_num_edit.setFocus()
        else:
            if self.send_ifo.currentText() == "是":
                if len(self.buy_adr_edit.text()) == 0:
                    QMessageBox.information(self, "操作失败", "买方地址未填写")
                    self.buy_adr_edit.setFocus()
                    return
        QMessageBox.question(self, "确定确认订单", "确认订单后无法修改", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if QMessageBox.Yes:
            Book_name = self.book_name_edit.text()
            Book_author = self.author_name_ifo.currentText()
            Book_Publishing_house = self.publishing_house_ifo.currentText()
            Book_sell_num = self.sell_num_edit.text()
            Menber_phone = self.buy_iph_edit.text()
            send = self.send_ifo.currentText()
            sql3 = "select Member_no from Member_Information where Member_phone=" + "\'" + Menber_phone + "\'"
            self.cursor.execute(sql3)
            if self.cursor.fetchall() == []:
                QMessageBox.warning(self, "操作错误", "电话号码未注册，请注册会员")
            else:
                sql2 = "select Book_no from Book_Information where Book_name = N'" + Book_name + "' and Book_author = N'" + Book_author + "' and Book_Publishing_house =N'" + Book_Publishing_house + "'"
                self.cursor.execute(sql2)
                Book_no = self.cursor.fetchall()[0][0]
                sql1 = "update Book_storage set Book_stock=Book_stock - " + str(
                    Book_sell_num) + " where Book_no = '" + Book_no + "'"
                self.cursor.execute(sql1)
                self.connect.commit()
                sql3 = "select Member_no from Member_Information where Member_phone=" + "\'" + Menber_phone + "\'"
                self.cursor.execute(sql3)
                Member_no = self.cursor.fetchall()[0][0]
                sql4 = "select top 1 Number from Buy_Book order by Number desc"
                self.cursor.execute(sql4)
                number = int(self.cursor.fetchall()[0][0] + 1)
                sql5 = "insert into Buy_Book values (" + str(
                    number) + ",N'" + Member_no + "'" + ",N'" + Book_no + "'," + str(
                    Book_sell_num) + "," + "N'" + send + "'," + "getdate()" + ")"
                print(sql5)
                self.cursor.execute(sql5)
                self.connect.commit()
        else:
            Book_name = self.book_name_edit.text()
            Book_author = self.author_name_ifo.currentText()
            Book_Publishing_house = self.publishing_house_ifo.currentText()
            Book_sell_num = self.sell_num_edit.text()
            Menber_phone = self.buy_iph_edit.text()
            send = self.send_ifo.currentText()
            sql2 = "select Book_no from Book_Information where Book_name = N'" + Book_name + "' and Book_author = N'" + Book_author + "' and Book_Publishing_house =N'" + Book_Publishing_house + "'"
            self.cursor.execute(sql2)
            Book_no = self.cursor.fetchall()[0][0]
            sql1 = "update Book_storage set Book_stock=Book_stock - " + str(
                Book_sell_num) + " where Book_no = '" + Book_no + "'"
            self.cursor.execute(sql1)
            self.connect.commit()
            sql3 = "select Member_no from Member_Information where Member_phone=" + "\'" + Menber_phone + "\'"
            self.cursor.execute(sql3)
            Member_no = self.cursor.fetchall()[0][0]
            sql4 = "select top 1 Number from Buy_Book order by Number desc"
            self.cursor.execute(sql4)
            number = int(self.cursor.fetchall()[0][0] + 1)
            sql5 = "insert into Buy_Book values (" + str(
                number) + ",N'" + Member_no + "'" + ",N'" + Book_no + "'," + str(
                Book_sell_num) + "," + "N'" + send + "'," + "getdate()" + ")"
            print(sql5)
            self.cursor.execute(sql5)
            self.connect.commit()
        self.book_name_edit.clear()
        self.author_name_ifo.clear()
        self.publishing_house_ifo.clear()
        self.sell_num_edit.clear()
        self.buy_iph_edit.clear()
        self.send_ifo.currentText()
        self.buy_adr_edit.clear()


                # sql5 = 'select Book_stock from Book_storage inner join Book_Information on Book_information.Book_no=Book_storage.Book_no where Book_name = N' + "\'" + book_name + "\' and Book_author=N\'" + author_name + "\' and Book_Publishing_house=N\'" + publishing_house_name + "\'"
                # self.cursor.execute(sql5)
                # new_stock = self.cursor.fetchall()[0][0]

                # if results[0][0]==Book_sell_num:

    def cancel_order(self):
        QMessageBox.question(self, "确定取消订单", "取消订单后返回上一级", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if QMessageBox.Yes:
            self.back_home()
        else:
            return

    def back_home(self):
        self.switch_window1.emit()

    def order_is_ok(self):
        self.switch_window2.emit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Sell_bookUI()
    sys.exit(app.exec_())

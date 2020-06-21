import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget
from LoginUI import LoginUI
from MainUI import MainUI
from Book_informationUI import Book_informationUI
from Member_informationUI import Member_informationUI
from Sell_bookUI import Sell_bookUI
from Add_bookUI import Add_bookUI
from Change_bookUI import Change_bookUI
from Buy_OrderUI import Buy_OrderUI


class Controller(QWidget):
    def __init__(self):
        super(Controller, self).__init__()
        pass

    def show_login(self):
        self.LoginUI = LoginUI()
        self.LoginUI.switch_window.connect(self.show_Main)

    def show_Main(self):
        self.MainUI = MainUI()
        self.MainUI.switch_window1.connect(self.show_B_ifoUI0)
        self.MainUI.switch_window2.connect(self.show_M_ifoUI)
        self.MainUI.switch_window3.connect(self.show_Buy_OrderUI)
        self.LoginUI.close()
        self.MainUI.show()

    def show_B_ifoUI0(self):
        self.b_ifo_UI = Book_informationUI()
        self.b_ifo_UI.switch_window1.connect(self.Back_home_1)
        self.b_ifo_UI.switch_window2.connect(self.show_SellUI)
        self.b_ifo_UI.switch_window3.connect(self.show_AddUI)
        self.b_ifo_UI.switch_window4.connect(self.show_ChangeUI)
        self.MainUI.close()
        self.b_ifo_UI.show()

    def show_B_ifoUI1(self):
        self.b_ifo_UI = Book_informationUI()
        self.b_ifo_UI.switch_window1.connect(self.Back_home_1)
        self.b_ifo_UI.switch_window2.connect(self.show_SellUI)
        self.b_ifo_UI.switch_window3.connect(self.show_AddUI)
        self.b_ifo_UI.switch_window4.connect(self.show_ChangeUI)
        self.Sell_bookUI.close()
        self.b_ifo_UI.show()

    def show_B_ifoUI2(self):
        self.b_ifo_UI = Book_informationUI()
        self.b_ifo_UI.switch_window1.connect(self.Back_home_1)
        self.b_ifo_UI.switch_window2.connect(self.show_SellUI)
        self.b_ifo_UI.switch_window3.connect(self.show_AddUI)
        self.b_ifo_UI.switch_window4.connect(self.show_ChangeUI)
        self.Add_bookUI.close()
        self.b_ifo_UI.show()

    def show_B_ifoUI3(self):
        self.b_ifo_UI = Book_informationUI()
        self.b_ifo_UI.switch_window1.connect(self.Back_home_1)
        self.b_ifo_UI.switch_window2.connect(self.show_SellUI)
        self.b_ifo_UI.switch_window3.connect(self.show_AddUI)
        self.b_ifo_UI.switch_window4.connect(self.show_ChangeUI)
        self.Change_bookUI.close()
        self.b_ifo_UI.show()

    def show_M_ifoUI(self):
        self.M_ifo_UI = Member_informationUI()
        self.M_ifo_UI.switch_window.connect(self.Back_home_2)
        self.MainUI.close()
        self.M_ifo_UI.show()

    def show_SellUI(self):
        self.Sell_bookUI = Sell_bookUI()
        self.Sell_bookUI.switch_window1.connect(self.show_B_ifoUI1)
        self.b_ifo_UI.close()
        self.Sell_bookUI.show()

    def show_AddUI(self):
        self.Add_bookUI = Add_bookUI()
        self.Add_bookUI.switch_window.connect(self.show_B_ifoUI2)
        self.b_ifo_UI.close()
        self.Add_bookUI.show()

    def show_ChangeUI(self):
        self.Change_bookUI = Change_bookUI()
        self.Change_bookUI.switch_window.connect(self.show_B_ifoUI3)
        self.b_ifo_UI.close()
        self.Change_bookUI.show()

    def show_Buy_OrderUI(self):
        self.Buy_OrderUI = Buy_OrderUI()
        self.Buy_OrderUI.switch_window.connect(self.Back_home_3)
        self.MainUI.close()
        self.Buy_OrderUI.show()

    def Back_home_1(self):
        self.MainUI = MainUI()
        self.MainUI.switch_window1.connect(self.show_B_ifoUI0)
        self.MainUI.switch_window2.connect(self.show_M_ifoUI)
        self.MainUI.switch_window3.connect(self.show_Buy_OrderUI)
        self.b_ifo_UI.close()
        self.MainUI.show()

    def Back_home_2(self):
        self.MainUI = MainUI()
        self.MainUI.switch_window1.connect(self.show_B_ifoUI0)
        self.MainUI.switch_window2.connect(self.show_M_ifoUI)
        self.MainUI.switch_window3.connect(self.show_Buy_OrderUI)
        self.M_ifo_UI.close()
        self.MainUI.show()

    # def Back_home_3(self):
    #     self.MainUI = MainUI()
    #     self.MainUI.switch_window1.connect(self.show_B_ifoUI)
    #     self.MainUI.switch_window2.connect(self.show_M_ifoUI)
    #     self.MainUI.switch_window3.connect(self.show_Buy_OrderUI)
    #     self.Sell_bookUI.close()
    #     self.MainUI.show()
    #
    # def Back_home_4(self):
    #     self.MainUI = MainUI()
    #     self.MainUI.switch_window1.connect(self.show_B_ifoUI)
    #     self.MainUI.switch_window2.connect(self.show_M_ifoUI)
    #     self.MainUI.switch_window3.connect(self.show_Buy_OrderUI)
    #     self.Add_bookUI.close()
    #     self.MainUI.show()
    #
    # def Back_home_5(self):
    #     self.MainUI = MainUI()
    #     self.MainUI.switch_window1.connect(self.show_B_ifoUI)
    #     self.MainUI.switch_window2.connect(self.show_M_ifoUI)
    #     self.MainUI.switch_window3.connect(self.show_Buy_OrderUI)
    #     self.Change_bookUI.close()
    #     self.MainUI.show()

    def Back_home_3(self):
        self.MainUI = MainUI()
        self.MainUI.switch_window1.connect(self.show_B_ifoUI0)
        self.MainUI.switch_window2.connect(self.show_M_ifoUI)
        self.MainUI.switch_window3.connect(self.show_Buy_OrderUI)
        self.Buy_OrderUI.close()
        self.MainUI.show()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    controller = Controller()
    controller.show_login()
    sys.exit(app.exec_())

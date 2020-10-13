from PyQt5 import QtWidgets, QtGui
from untitled import Ui_MainWindow
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import QSettings
from PyQt5.Qt import *
from PyQt5.QtCore import *


class MyWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setupUi(self)
        self.process()


    def SetButtonGP(self):  # 设置按钮组
        btGroup = QButtonGroup(self)
        btGroup.addButton(self.radioButton)  # 添加按键
        btGroup.addButton(self.radioButton_2)
        btGroup.setId(self.radioButton, 1)  # 设置按键ID
        btGroup.setId(self.radioButton_2, 2)

    def closeEvent(self, a0: QtGui.QCloseEvent):
        mySet = MySettings()
        isRadioBt = self.radioButton.isChecked()
        if isRadioBt == 1:
            mySet.WriteSettings('./Project.ini', '/Settings/bit', 0)
        else:
            mySet.WriteSettings('./Project.ini', '/Settings/bit', 1)

    def iniSettings(self):

        mySet = MySettings()
        value_list = mySet.ReadSettings('./Project.ini', '/Options')  # 读取配置文件信息
        for i in value_list:  # 循环添加组合框项目
            self.comboBox.addItem(i)
        self.SetButtonGP()
        isRadioBt = mySet.ReadSettings('./Project.ini', '/Settings/bit')
        debugValue = mySet.ReadSettings('./Project.ini', '/Settings/debug')
        WDKpath = mySet.ReadSettings('./Project.ini', '/Path/WDK')
        driverPath = mySet.ReadSettings('./Project.ini', '/Path/driver')
        infPath = mySet.ReadSettings('./Project.ini', '/Path/INF')

        # 设置位数
        if isRadioBt == 0:
            self.radioButton.setChecked(True)
        else:
            self.radioButton_2.setChecked(True)

        # 设置debug模式
        if debugValue == 0:
            self.checkBox.setChecked(False)
        else:
            self.checkBox.setChecked(True)

        # 设置Driver地址
        if driverPath is not None:
            self.lineEdit.setText(driverPath)

        # 设置WDK地址
        if WDKpath is not None:
            self.lineEdit_2.setText(WDKpath)

        # 设置INF地址
        if infPath is not None:
            self.lineEdit_3.setText(infPath)

        # 调整光标位置至开头
        self.lineEdit.setCursorPosition(0)
        self.lineEdit_2.setCursorPosition(0)
        self.lineEdit_3.setCursorPosition(0)





    def process(self):  # 主处理函数
        self.iniSettings()  # 读取设置


# 读写配置文件
class MySettings:
    def __init__(self):
        self.user_valueList = []
        self.user_value = 0

    def ReadSettings(self, path, user_key):
        if path is None:
            return False
        else:
            self.settings = QSettings(path, QSettings.IniFormat)  # ini文件格式

            if user_key == '/Options':
                self.settings.beginGroup(user_key)  # 读取所有键
                user_childKey = self.settings.childKeys()
                for i in user_childKey:  # 读取所有值
                    self.user_valueList.append(self.settings.value(i))
                self.settings.endGroup()
                return self.user_valueList
            else:
                self.user_value = self.settings.value(user_key)
                return self.user_value

    def WriteSettings(self, path, user_key, user_value):
        settings = QSettings(path, QSettings.IniFormat)
        settings.setValue(user_key, user_value)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    ui = MyWindow()
    ui.show()
    sys.exit(app.exec_())

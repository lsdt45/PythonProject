from PyQt5 import QtWidgets, QtGui
from untitled import Ui_MainWindow
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import QSettings
from PyQt5.Qt import *


class MyWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setupUi(self)
        self.Process()

    def SetButtonGP(self):  # 设置按钮组
        btGroup = QButtonGroup(self)
        btGroup.addButton(self.radioButton) # 添加按键
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

    def Process(self):  # 主处理函数
        mySet = MySettings()
        value_list = mySet.ReadSettings('./Project.ini', '/Options')  # 读取配置文件信息
        for i in value_list:  # 循环添加组合框项目
            self.comboBox.addItem(i)
        self.SetButtonGP()
        isRadioBt = mySet.ReadSettings('./Project.ini', '/Settings/bit')
        debugValue = mySet.ReadSettings('./Project.ini', '/Settings/debug')

        # 设置位数
        if int(isRadioBt) == 0:
            self.radioButton.setChecked(True)
        else:
            self.radioButton_2.setChecked(True)

        # 设置debug模式
        if int(debugValue) == 0:
            self.checkBox.setChecked(False)
        else:
            self.checkBox.setChecked(True)


# 读写配置文件
class MySettings:
    def __init__(self):
        self.user_valueList = []
        self.user_value = 0

    def ReadSettings(self, path, user_key):
        if path is None:
            return False
        else:
            settings = QSettings(path, QSettings.IniFormat)  # ini文件格式
            settings.beginGroup(user_key)  # 读取所有键
            user_childKey = settings.childKeys()
            if user_key == '/Options':
                for i in user_childKey:  # 读取所有值
                    self.user_valueList.append(settings.value(i))
                return self.user_valueList
            else:
                for i in user_childKey:  # 读取所有值
                    self.user_value = settings.value(i)
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

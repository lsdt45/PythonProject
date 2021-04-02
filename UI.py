from PyQt5 import QtWidgets, QtGui
from untitled import Ui_MainWindow
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import QSettings
from PyQt5.Qt import *
from PyQt5.QtCore import *
from pathlib import Path
import os
import re
import sys
import win32print

# noinspection SpellCheckingInspection
class MyWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setupUi(self)
        self.packPath = ''
        self.infPath = ''
        self.printerName = ''
        self.modelName = []
        self.process()

    def SetButtonGP(self):  # 设置按钮组
        btGroup = QButtonGroup(self)
        btGroup.addButton(self.radioButton)  # 添加按键
        btGroup.addButton(self.radioButton_2)
        btGroup.setId(self.radioButton, 1)  # 设置按键ID
        btGroup.setId(self.radioButton_2, 2)

    def closeEvent(self, a0: QtGui.QCloseEvent):
        self.SaveSettings()

    def iniSettings(self):
        mySet = MySettings()
        project_list = mySet.ReadSettings('./Project.ini', '/Project', 1)  # 读取配置文件信息
        # model_list = mySet.ReadSettings('./Project.ini', '/Model', 1)

        for i in project_list:  # 循环添加组合框项目
            self.comboBox.addItem(i)

        self.SetButtonGP()
        isRadioBt = mySet.ReadSettings('./Project.ini', '/Settings/bit')
        debugValue = mySet.ReadSettings('./Project.ini', '/Settings/debug')
        WDKpath = mySet.ReadSettings('./Project.ini', '/Path/WDK')
        driverPath = mySet.ReadSettings('./Project.ini', '/Path/driver')
        packPath = mySet.ReadSettings('./Project.ini', '/Path/INF')
        install_value = mySet.ReadSettings('./Project.ini', '/Settings/install')
        pj_pos = mySet.ReadSettings('./Project.ini', '/Settings/pj_pos')
        model_pos = mySet.ReadSettings('./Project.ini', '/Settings/model_pos')

        # 设置位数
        if isRadioBt == "0":
            self.radioButton.setChecked(True)
        else:
            self.radioButton_2.setChecked(True)

        # 设置debug模式
        if debugValue == "0":
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
        if packPath is not None:
            self.lineEdit_3.setText(packPath)

        # 设置install/uninstall
        if install_value == "0":
            self.radioButton_5.setChecked(True)
        else:
            self.radioButton_6.setChecked(True)

        # 设置地址
        self.GetInfPath()
        # self.packPath = self.lineEdit_3.text()
        # path = Path(self.packPath)
        # infPath = path.glob('*.inf')
        # for i in infPath:
        #     if i is not None:
        #         self.infPath = i
        # 读取INF的model名
        self.ReadInf(self.infPath)
        # 设置Project保存项
        self.comboBox.setCurrentIndex(int(pj_pos))

        # 设置Model保存项
        self.comboBox_2.setCurrentIndex(int(model_pos))

        # 调整光标位置至开头
        self.lineEdit.setCursorPosition(0)
        self.lineEdit_2.setCursorPosition(0)
        self.lineEdit_3.setCursorPosition(0)

    def SaveSettings(self):
        mySet = MySettings()
        isRadioBt = self.radioButton.isChecked()
        # 保存bit options
        if isRadioBt == 1:
            mySet.WriteSettings('./Project.ini', '/Settings/bit', 0)
        else:
            mySet.WriteSettings('./Project.ini', '/Settings/bit', 1)
        # 保存debug
        if self.checkBox.clicked == 0:
            mySet.WriteSettings('./Project.ini', '/Settings/debug', 0)
        else:
            mySet.WriteSettings('./Project.ini', '/Settings/debug', 1)
        # 保存ProjectOptions
        mySet.WriteSettings('./Project.ini', '/Settings/pj_pos', self.comboBox.currentIndex())
        # 保存ModelOptions
        mySet.WriteSettings('./Project.ini', '/Settings/model_pos', self.comboBox_2.currentIndex())
        # 保存DriverPath
        mySet.WriteSettings('./Project.ini', '/Path/driver', self.lineEdit.text())
        # 保存INFPath
        mySet.WriteSettings('./Project.ini', '/Path/INF', self.lineEdit_3.text())

    def DriverInstall(self):

        # cmd = '''rundll32 printui.dll,PrintUIEntry /if /b %s /f %s /r "lpt1:" /m %s && \
        # rundll32 printui.dll,PrintUIEntry /y /n %s  && \
        # ''' % (PrintName, infPath, PrintName, PrintName)
        self.printerName = self.comboBox_2.itemText(self.comboBox_2.currentIndex())  # 当前选择的printer名
        if self.radioButton_5.isChecked():
            cmd = '''rundll32 printui.dll,PrintUIEntry /if /b "%s" /f %s /r "lpt1:" /m "%s" \
                   ''' % (self.printerName, self.infPath, self.printerName)
        else:
            cmd = '''rundll32 printui.dll,PrintUIEntry /n "%s" /dl && \
            rundll32 printui.dll,PrintUIEntry /m "%s" /dd
                               ''' % (self.printerName, self.printerName)
        # 执行cmd

        # print(cmd)
        if cmd:
            result = os.popen(cmd, 'r')
            if result:
                QMessageBox.warning(self, 'Warning', 'Success')
            else:
                QMessageBox.warning(self, 'Warning', 'operation failed')
        else:
            print('invalid cmd')
        # cmd = result.read()
        # QMessageBox.warning(self, 'Warning', cmd)

        # --------------Test---------------
        # result = os.popen('ipconfig', 'r')
        # cmd = result.read()
        # QMessageBox.warning(self, 'Warning', cmd)
        # print(cmd)
        # --------------Test---------------

    # 从INF文件中读取所有的model名
    def ReadInf(self, infPath):
        if infPath is None:
            return False
        modelLine = []
        self.modelName = []
        try:
            file = open(infPath, 'r')
        except IOError:
            QMessageBox.warning(self, 'Warning', '读取INF路径失败')
            return
        pattern_list = "(PS\")|(PCL6\")|(PS\))|(PCL6\))"
        pattern = re.compile(pattern_list)  # 利用正则寻找model名
        for line in file.readlines():
            result = re.search(pattern, line)
            if result:
                modelLine.append(line)
        file.close()
        for i in range(len(modelLine)):
            tempName = str(modelLine[i]).split('"')  # 筛选model名
            if tempName[1] in self.modelName:
                continue
            else:
                self.modelName.append(tempName[1])  # 将获取的model名存入列表

        self.comboBox_2.clear()  # 添加前清空组合框内容
        for i in self.modelName:  # 循环添加组合框项目
            self.comboBox_2.addItem(i)
        print(self.modelName)
        print_name_tuple = win32print.EnumPrinters(win32print.PRINTER_ENUM_NAME, None, 4)
        for i in range(len(print_name_tuple)):
            print(print_name_tuple[i].get("pPrinterName"))

    # 获取INF的地址
    def GetInfPath(self):
        temp = None
        self.packPath = self.lineEdit_3.text()
        path = Path(self.packPath)
        infPath = path.glob('*.INF')

        for temp in infPath:
            if temp is not None:
                self.infPath = temp  # 重新设置地址

        # 判断地址是否为空，如果是，则将地址和组合框置空
        if temp is None:
            self.infPath = 'None'
            self.comboBox_2.clear()

    # 各种事件的触发
    def EventTrigger(self):
        # 文本改变时重新读取Inf文件
        self.lineEdit_3.editingFinished.connect(self.GetInfPath)
        self.lineEdit_3.editingFinished.connect(lambda: self.ReadInf(self.infPath))
        # Install按钮被按下时进行驱动安装
        self.pushButton_5.clicked.connect(self.DriverInstall)

    def process(self):  # 主处理函数
        self.iniSettings()  # 读取设置
        self.EventTrigger()  # 事件触发


# 读写配置文件
class MySettings:
    def __init__(self):
        self.user_valueList = []
        self.user_value = 0

    def ReadSettings(self, path, user_key, settingType=0):
        if path is None:
            return False
        else:
            self.settings = QSettings(path, QSettings.IniFormat)  # ini文件格式

            if settingType == 1:
                self.settings.beginGroup(user_key)  # 读取所有键
                user_childKey = self.settings.childKeys()
                self.user_valueList = []  # 清空之前的列表
                for i in user_childKey:  # 读取所有值
                    self.user_valueList.append(self.settings.value(i))
                self.settings.endGroup()
                return self.user_valueList
            else:
                self.user_value = self.settings.value(user_key)
                return self.user_value

    # 将设置写入ini文件
    def WriteSettings(self, path, user_key, user_value):
        settings = QSettings(path, QSettings.IniFormat)
        settings.setValue(user_key, user_value)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = MyWindow()
    ui.show()
    sys.exit(app.exec_())

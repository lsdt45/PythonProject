#coding=UTF-8

import os

adb = 'ipconfig /all'
str_GBK = str(os.system(adb)).encode('UTF-8')
st = input(str_GBK)

print(st)

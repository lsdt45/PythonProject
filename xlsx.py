import xlrd
import datetime

# 打开文件

wb = xlrd.open_workbook('testxlsx.xlsx')
# 获取所有sheet的名字

print(wb.sheet_names())
# 获取第二个sheet的表名

sheet2 = wb.sheet_names()[3]
print(sheet2)

#sheet1索引从0开始，得到sheet1表的句柄
sheet1 = wb.sheet_by_index(3)
rowNum = sheet1.nrows
colNum = sheet1.ncols
print(rowNum, colNum)

#获取某一个位置的数据类型
# 1 ctype : 0 empty,1 string, 2 number, 3 date, 4 boolean, 5 error
print(sheet1.cell(3,6).ctype)
print(sheet1.cell(3,6).value)

#获取整行和整列的数据
"""
for i in range(19):
	row1 = sheet1.row_values(i)
	print(row1)
row1 = sheet1.row_values(3)
print(row1)
"""

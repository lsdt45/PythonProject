from bs4 import BeautifulSoup

list_green = []
list_red = []
soup = BeautifulSoup(open('Init_ColorDlg.html'), features='html.parser')
# print(soup.span)
# for result in soup.children:
#     print(result)
# print(soup.find_all("span", style="background-color:#fdd"))

# 所有绿色的行
green = soup.find_all("span", style="background-color:#dfd")
# 所有红色的行
red = soup.find_all("span", style="background-color:#fdd")

#

greenLen = len(green)  #
redLen = len(red)  # 红行的行数
dfdCount = 0    # 列表中包含dfd的元素个数
fddCount = 0    # 红行中包含fdd的元素个数
for i in range(greenLen):
    dfdNum = str(green[i]).count('\n')
    dfdNum += 1
    dfdCount += dfdNum

for i in range(redLen):
    fddNum = str(red[i]).count('\n')
    fddNum += 1
    fddCount += fddNum
# 覆盖率
coverage = dfdCount/(dfdCount + fddCount)
coverage = format(coverage, '.2f')
coverage = float(coverage) * 100
print('green line = ' + str(dfdCount))
print('red line = ' + str(fddCount))
print('Coverage = %d%%' % coverage)

# print(type(list[1]))

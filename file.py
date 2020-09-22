from pathlib import Path

list1 = []
list2 = []
nameList = []
delFolder = ['amd64', 'i386', 'svn']
indexTemp = 0
boolTemp = -1
folderPath = Path.cwd()
p = Path(folderPath)
for folder in p.iterdir():
	if folder.is_dir():
		list1.append(folder)

num = len(list1)

# 遍历所有文件夹，删除与语言不相关的文件夹
for z in range(num):
	boolTemp = -1
	for i in list1:
		if boolTemp != -1:
			break
		tempStr = str(i)
		for j in range(3):
			boolTemp = tempStr.find(delFolder[j])
			if boolTemp != -1:
				indexTemp = list1.index(i)
				del (list1[indexTemp])
				break

# for i in list1:
# 	print(i)

for i in list1:
	p = Path(i)
	for index, item in enumerate(p.rglob('*.*')):	
		sStable1 = str(item).find('OK')
		sStable2 = str(item).find('Ok')
		if (sStable1 != -1):
			tempStr = str(item).replace('OK', 'OM')		
			name = item.with_name(tempStr[sStable1:])
			item.rename(name)
		elif (sStable2 != -1):
			tempStr = str(item).replace('Ok', 'OM')
			name = item.with_name(tempStr[sStable2:])
			item.rename(name)
		print(name)
		# print(index)
	# print(sorted(p.rglob('*.')))

'''
for i in list2:
	print(i)
'''
# print(len(nameList))
# print(str(list2[0]).replace('OK', 'OM'))


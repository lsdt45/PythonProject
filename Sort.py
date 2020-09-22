# Bubble Sort
"""
def bubbleSort(arr):
    n = len(arr)

    # 遍历所有数组元素
    for i in range(n):

        # Last i elements are already in place
        for j in range(0, n - i - 1):

            if arr[j] > arr[j + 1]:  
                arr[j], arr[j + 1] = arr[j + 1], arr[j]


arr = [64, 34, 25, 12, 22, 11, 90]

bubbleSort(arr)

print("排序后的数组:")
for i in range(len(arr)):
    print("%d" % arr[i]),
"""


# list1 = [2, 3, 1, 4]
# for i in range(len(list1)):
# 	print(i)
"""
def BubbleSort(list):
    length = len(list)

    for i in range(length):
        for j in range(length - i - 1):
            if list[j] > list[j + 1]:
                temp = list[j]
                list[j] = list[j + 1]
                list[j + 1] = temp
    for i in list:
        print(str(i) + " ", end="")



print("排序之后：\n")
list1 = [3, 2, 4, 1, 6, 9, 0]
BubbleSort(list1)
"""



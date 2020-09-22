# 创建迭代器
# list = [1,2,3,4]
# it =iter(list)
# print(next(it))

# 将一个类作为迭代器
# class MyNumbers:
#     def __iter__(self):
#         self.a = 1
#         return self
#
#     def __next__(self):
#         x = self.a
#         self.a += 1
#         return x
# myClass = MyNumbers()
# myIter = iter(myClass)

class MyNumbers:
    def __iter__(self):
        self.a = 1
        return self

    def __next__(self):
        if self.a <= 20:  # 指定循环次数
            x = self.a
            self.a += 1
            return x
        else:
            raise StopIteration  # 达到循环次数后结束循环


myclass = MyNumbers()
myiter = iter(myclass)

for x in myiter:
    print(x)

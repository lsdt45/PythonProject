import multiprocessing


def workerA(myList):
    myList.append("数据编号AAA")


def workerB(myList):
    myList.append("数据编号BBB")


def workerC(myList):
    myList.append("数据编号CCC")


def main():
    mainList = ["First"]
    manager = multiprocessing.Manager()
    mrgList = manager.list([mainList])
    processA = multiprocessing.Process(target=workerA, args=(mrgList,), name="A")
    processB = multiprocessing.Process(target=workerB, args=(mrgList,), name="B")
    processC = multiprocessing.Process(target=workerC, args=(mrgList,), name="C")
    processA.start()
    processB.start()
    processC.start()
    processA.join()
    processB.join()
    processC.join()
    print(mrgList)


if __name__ == '__main__':
    main()

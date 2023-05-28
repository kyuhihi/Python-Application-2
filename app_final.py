import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import *
from mainwindow import MainWindow

from NaverCrawler import NaverCrawler
from multiprocessing import Process, Manager, Queue

from Loading import MyWindow, Consumer

window = None

m_NaverDict = {}

def Naver_Scrapping(iProccessCnt, Shared_Dict,Process_Queue, urlQueue):
    navercrawler = NaverCrawler(iProccessCnt, urlQueue)
    Shared_Dict.update(navercrawler.m_NaverDict)
    Process_Queue.put(f"Process {iProccessCnt} is complete!!!!")

def ProgressBar(LoadingQueue):
    LoadingProcs = QApplication(sys.argv)

    new_window = MainWindow()
    new_window.show()
    bLoadingNotFinish = True
    iCount = 0
    while bLoadingNotFinish:
        if LoadingQueue.qsize() == 5:
            bLoadingNotFinish = False
            break

    LoadingProcs.exec_()


def Naver_Proccessing():
    global m_NaverDict
    manager = Manager()
    Shared_Dict = manager.dict()
    queue = Queue()
    urlQueue = Queue()
    # Loadingproc = Process(target=ProgressBar, args=(queue,))
    # Loadingproc.start()

    procs = []
    for n in range(5):
        proc = Process(target=Naver_Scrapping, args=(n, Shared_Dict, queue,urlQueue), daemon=True)
        procs.append(proc)
        proc.start()

    app = QApplication(sys.argv)
    myWindow = MyWindow(queue,urlQueue)
    myWindow.show()

    # Loadingproc.join()
    for proc in procs:
        proc.join()

    m_NaverDict = dict(Shared_Dict)
    app.exec_()


if __name__ == '__main__':

    Naver_Proccessing()

    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    window.Set_NaverDict(m_NaverDict)
    sys.exit(app.exec_())



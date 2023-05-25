import sys

from PyQt5.QtWidgets import QApplication

from mainwindow import MainWindow

from NaverCrawler import NaverCrawler
from multiprocessing import Process, Manager

window = None

m_NaverDict = {}
def Naver_Scrapping(iProccessCnt, Shared_Dict):
    navercrawler = NaverCrawler(iProccessCnt)
    Shared_Dict.update(navercrawler.m_NaverDict)

def Naver_Proccessing():
    global m_NaverDict
    manager = Manager()
    Shared_Dict = manager.dict()

    procs = []
    for n in range(5):
        proc = Process(target=Naver_Scrapping, args=(n, Shared_Dict))
        procs.append(proc)
        proc.start()

    for proc in procs:
        proc.join()

    m_NaverDict = dict(Shared_Dict)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    Naver_Proccessing()

    window = MainWindow(m_NaverDict)

    window.show()
    sys.exit(app.exec_())


#참고: https://wikidocs.net/87141

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class Consumer(QThread):
    poped = pyqtSignal(str)
    urls = pyqtSignal(str)
    progress = pyqtSignal(int)

    def __init__(self, q,urlqueue):
        super().__init__()
        self.q = q
        self.urlqueue = urlqueue

    def run(self):
        iCountProccessing =0
        bPrintFinish = False
        while True:
            if not self.q.empty():
                data = self.q.get()
                self.poped.emit(data)# emit라는 메소드를 통해 다른 클래스에 값을 전달 가능.
                iCountProccessing += 1
                self.progress.emit(iCountProccessing *20)


            if not self.urlqueue.empty():
                self.urls.emit(self.urlqueue.get())
            else:
                if (iCountProccessing == 5) and (bPrintFinish is False):
                    bPrintFinish = True
                    self.urls.emit("\n\n\n!!!!!Loading completely Finish!!!!")


class MyWindow(QMainWindow):
    def __init__(self, q, urlQueue):
        super().__init__()
        self.setWindowTitle("Status Window!!")

        self.setGeometry(1500, 200, 300, 200)

        self.consumer = Consumer(q,urlQueue)

        self.consumer.poped.connect(self.print_data)
        self.consumer.urls.connect(self.print_data)
        self.consumer.progress.connect(self.updateProgressBar)
        self.consumer.start()


        self.layout = QVBoxLayout()
        self.widget = QWidget()
        self.progress_bar = QProgressBar()

        self.text_edit = QPlainTextEdit(self)
        self.text_edit.setReadOnly(True)  # 텍스트 편집 비활성화

        self.layout.addWidget(self.progress_bar)
        self.layout.addWidget(self.text_edit)
        self.widget.setLayout(self.layout)

        self.setCentralWidget(self.widget)

    def updateProgressBar(self, data):
        self.progress_bar.setValue(data)

    def Append_Text(self, text):
        self.text_edit.appendPlainText(text)


    # @pyqtSlot(str)
    def print_data(self, data):
        self.Append_Text(data)
        self.statusBar().showMessage(data)
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QDesktopWidget, QMainWindow, \
    QPushButton, QVBoxLayout

from FoodFinder import FoodFinder

class MainWindow(QMainWindow):
    def __init__(self, NaverDict):
        super().__init__()

        self.m_timer = QTimer(self)
        self.m_timer.timeout.connect(self.Tick)
        self.m_timer.start(10)

        self.setWindowTitle("Main Window")
        screen_size = QDesktopWidget().screenGeometry()
        width, height = 700, 600
        self.setGeometry((screen_size.width() - width) // 2, (screen_size.height() - height) // 2, width, height)

        layout = QVBoxLayout()

        self.m_background_image = QLabel(self)
        self.m_background_image.setGeometry(0, 0, width, height)
        self.m_background_image.setScaledContents(True)
        self.m_background_image.setPixmap(QPixmap("Logo.png"))
        layout.addWidget(self.m_background_image)

        self.ImageViewerOpen = QPushButton('오늘 뭐먹지', self)
        self.ImageViewerOpen.clicked.connect(self.open_Food_Finder)
        self.ImageViewerOpen.setGeometry(250, 460, 200, 50)
        layout.addWidget(self.ImageViewerOpen)

        self.m_FoodFinder = None
        self.m_NaverDict = NaverDict


    def open_Food_Finder(self):
        if not self.m_FoodFinder:
            self.m_FoodFinder = FoodFinder(self.m_NaverDict)
        else:
            self.m_FoodFinder.close()
            self.m_FoodFinder = None
            self.m_FoodFinder = FoodFinder()

        self.m_FoodFinder.show()


    def Tick(self):
        if self.m_FoodFinder is not None:
            self.m_FoodFinder.Tick()

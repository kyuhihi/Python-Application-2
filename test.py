# https://map.naver.com/v5/search/%EB%A7%9B%EC%A7%91

import re
import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import time

def FindAll(strREtag):
    elms = soup.find_all(class_=re.compile(strREtag))
    elms_counter = 0
    for e in elms:
        # print(e.find_next().find_next().text)
        print(e.text)
        elms_counter += 1
    print(elms_counter)
    return elms


headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
}
html = None
# url = "https://search.naver.com/search.naver?sm=tab_sug.top&where=nexearch&query=%EC%A3%BC%EB%B3%80%EB%A7%9B%EC%A7%91"
# with sync_playwright() as playwright:
#     browser = playwright.chromium.launch(headless=False)
#     page = browser.new_page()
#     page.goto(url)
#     page.get_by_text("'주변맛집' 관련 인기 주제 둘러보기").click()
#     time.sleep(5)
#     html = page.content()
#
# r = requests.get(url, headers=headers)
#
# soup = BeautifulSoup(html, 'lxml')
#
# FindAll(r"^KCMnt")# 음식종류
# print("===================")
# FindAll(r"^place_bluelink")# 가게 이름
# print("===================")
# FindAll(r"^h69bs a2RFq") #별점
# print("===================페이지")
# elms = FindAll(r"^K0PDV") #별점
# print("===================url")
#
# url_regex = r'url\("([^"]+)"\)'
#
# div_elements = soup.find_all("div", class_="yLaWz")
#
# for url_elms in div_elements:
#     matches = re.findall(url_regex, str(url_elms.next_element.contents[0]))
#     if matches:
#         image_url = matches[0]
#         if 'profile' in image_url:
#             continue
#         print(image_url)
#         print(url_elms.next_element.text)
#     else:
#         print("URL not found.")
#
#
#
# r.close()

url = "https://www.google.com/search?tbs=lf:1,lf_ui:9&tbm=lcl&sxsrf=APwXEdf66iI7YMg-xVszqNYRIzCdCa6Fig:1684396093911&q=%EB%A7%9B%EC%A7%91"
r = requests.get(url, headers=headers)

soup = BeautifulSoup(r.content, 'lxml')
# <span class="gqguwf OSrXXb btbrud"><span>"불향 고기 구이에 넉넉하고 다양한 쌈 종류가 잘 준비되어 있는 <b>맛집</b>입니다."</span></span>
Google_elms = FindAll(r"^rllt__details") # 전체 긁어오기.
print("===================구글")
for e in Google_elms:
    print(e.find_next().next_sibling.next_sibling.text)
print("===================구글1")
Google_elms = FindAll(r"^yi40Hd YrbPuc")    #리뷰 점수
print("===================구글2")
Google_elms = FindAll(r"^dbg0pd")           #음식점 이름
print("===================구글3")
#여긴 음식점 타입.
iCount = 0
for e in Google_elms:
    res = e.next_sibling.text.replace(" ","")
    res = re.split('·', res)
    for strFoodType in res:
        if (strFoodType.isascii() is False) and '리뷰없음' not in strFoodType:
            if "₩" not in strFoodType:
                print(strFoodType)
                iCount += 1

print(iCount)
print("===================구글4")
Google_elms = FindAll(r"^gqguwf OSrXXb btbrud")
print("===================url")
Google_elms = FindAll(r"^gTrj3e")

for e in Google_elms:
    print(e.find_next()['src'])

# gqguwf OSrXXb btbrud
# RDApEe YrbPuc
# <g-img class="gTrj3e"><img id="dimg_85" src="data:image/jpeg;base64,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" data-deferred="2" class="YQ4gaf zr758c wA1Bge" height="90" width="90" alt="" data-iml="1685033026713" data-atf="1" data-frt="0"></g-img>r.close()
# <div class="rllt__details"><div class="dbg0pd" aria-level="3" role="heading"><span class="OSrXXb">전라도연탄구이</span></div><div><span><span class="Y0A0hc"><span class="yi40Hd YrbPuc" aria-hidden="true">4.2</span><span class="z3HNkc" aria-label="별 5개 중 4.2개" role="img"><span style="width:56px"></span></span><span class="RDApEe YrbPuc">(163)</span></span></span> · 음식점</div><div>정왕동 1731-19 명동프라자 109호</div><div class="pJ3Ci RGCvMc RCQpbe"><span class="X37Bwb"><g-img class="MJ1Rwc raB6Pe"><img id="dimg_3" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACgAAAAoCAMAAAC7IEhfAAAAflBMVEVHcEzs8v/b6P/a5//V5P+91f+jxP+gw/+hxP+ox//B1//X5P/4+v/M3v/Q4f/9/f/u9P+ty/+xzf/z9/+jxv+yzf+81P+avv13ne9PfOM5bt+BpvIyat4+cd9DdOCStvmIrfVeiOdslOuTtf+Qsv+HrP+NsP+4zv9Tg/Kpw/9P6VkYAAAAKnRSTlMAJUtjcbD2///qplcQin4ELNzPHv/OtP///////////////9rPsKlt8ITWgCk1AAABgUlEQVR4AX2VBZLDMAwAw1LK4AsYAoft/z94obHk0BaGdkQmb44fhFEUBr63SxgngD0A6eG4ZZ3OCTAQ08t1zYtIs6ThMlwMqxxmQW932ODxdLwUNrkz88TioRhAsHxQ9gwsIi9KKcsiF6xO2y/zlDZVh9GKmeGUOCGv0NWELshMx+RnsNTW68ya6rz03pUFLCtGyUL2YgiWXHNR5xTy6LSMjeSibNBpPCFRuaJCnvsGexEtT+/IxO0aIeDTBtEa8kwrgM/8AgTO50hEjghCWZPWcBIjcMzGyC5999d0npP6CA6Iqi3LViGCQ2DHQyrbjnw8XjKLOIqziKm7azunborPjkLVKNDduyFpTSulNANS6laBoE1B20yoqmuY0cnFVEHKNi62slogy3wwL3QU+OoxTIV0FPqZY6MXEu21kI4rFmZdNJ8CDuwCEDvix5VfKdvi3b18vrbEb+51nH7Wxd/lXfr3Wmqvv9Wr+f2aaW83HOP487LW79HbxQ/+OpbPxz+OulJiB8BuewAAAABJRU5ErkJggg==" data-deferred="2" class="YQ4gaf zr758c" height="16" width="16" alt="" data-iml="1684396138078" data-atf="1" data-frt="0"></g-img></span><span class="gqguwf OSrXXb btbrud"><span>"어떻게 <b>맛집</b>이 됬는지 모르겠지만 생각보다 별로입니다."</span></span></div></div>
# import sys
# from PyQt5.QtWidgets import *
# from PyQt5.QtCore import *
# from multiprocessing import Process, Queue
# import multiprocessing as mp
# import datetime
# import time
#
#
# def producer(q):
#     proc = mp.current_process()
#     print(proc.name)
#
#     while True:
#         now = datetime.datetime.now()
#         data = str(now)
#         q.put(data)
#         time.sleep(1)
#
#
# class Consumer(QThread):
#     poped = pyqtSignal(str)
#
#     def __init__(self, q):
#         super().__init__()
#         self.q = q
#
#     def run(self):
#         while True:
#             if not self.q.empty():
#                 data = q.get()
#                 self.poped.emit(data)
#
#
# class MyWindow(QMainWindow):
#     def __init__(self, q):
#         super().__init__()
#         self.setGeometry(200, 200, 300, 200)
#
#         # thread for data consumer
#         self.consumer = Consumer(q)
#         self.consumer.poped.connect(self.print_data)
#         self.consumer.start()
#
#
#     @pyqtSlot(str)
#     def print_data(self, data):
#         self.statusBar().showMessage(data)
#
#
# if __name__ == "__main__":
#     q = Queue()
#
#     # producer process
#     p = Process(name="producer", target=producer, args=(q, ), daemon=True)
#     p.start()
#
#     # Main process
#     app = QApplication(sys.argv)
#     mywindow = MyWindow(q)
#     mywindow.show()
#     app.exec_()


# import sys
# from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QGraphicsView, QVBoxLayout, QPushButton
# from PyQt5.QtCore import Qt, QPointF, QTimer
# from PyQt5.QtGui import QPainter, QPen, QColor, QBrush
# from PyQt5.QtWidgets import QWidget
#
#
# class LadderGameWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Ladder Game")
#         self.setGeometry(100, 100, 600, 400)
#
#         self.central_widget = QWidget()
#         self.setCentralWidget(self.central_widget)
#
#         self.layout = QVBoxLayout()
#         self.central_widget.setLayout(self.layout)
#
#         self.view = QGraphicsView()
#         self.scene = QGraphicsScene()
#         self.view.setScene(self.scene)
#         self.layout.addWidget(self.view)
#
#         self.play_button = QPushButton("Play")
#         self.play_button.clicked.connect(self.play_game)
#         self.layout.addWidget(self.play_button)
#
#         self.ladder_positions = []
#         self.ball_position = QPointF(0, 0)
#         self.Timer = None
#
#     def play_game(self):
#         self.initialize_ladder_positions()
#         self.ball_position = QPointF(0, 0)
#         self.update_scene()
#         QTimer.singleShot(1000, self.animate_ball)
#
#     def initialize_ladder_positions(self):
#         self.ladder_positions = [
#             QPointF(50, 50),
#             QPointF(150, 150),
#             QPointF(250, 100),
#             QPointF(350, 200),
#             QPointF(450, 150)
#         ]
#
#     def animate_ball(self):
#         self.Timer = QTimer()
#         self.Timer.setInterval(100)
#         self.Timer.timeout.connect(self.move_ball)
#         self.Timer.start()
#
#     def move_ball(self):
#         if self.ball_position.y() < self.view.height() - 50:
#             self.ball_position += QPointF(0, 50)
#             self.update_scene()
#
#     def update_scene(self):
#         self.scene.clear()
#         self.draw_ladders()
#         self.draw_ball()
#
#     def draw_ladders(self):
#         pen = QPen(Qt.black)
#         brush = QBrush(Qt.gray)
#
#         for position in self.ladder_positions:
#             x, y = position.x(), position.y()
#             self.scene.addLine(x, y, x + 50, y, pen)
#
#     def draw_ball(self):
#         pen = QPen(Qt.black)
#         brush = QBrush(Qt.red)
#
#         self.scene.addEllipse(self.ball_position.x(), self.ball_position.y(), 20, 20, pen, brush)
#
#
# def main():
#     app = QApplication(sys.argv)
#     window = LadderGameWindow()
#     window.show()
#
#     sys.exit(app.exec_())
#
#
# if __name__ == '__main__':
#     main()
#
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QGraphicsView, QVBoxLayout, QPushButton
from PyQt5.QtCore import Qt, QPointF, QTimer
from PyQt5.QtGui import QPainter, QPen, QColor, QBrush
from PyQt5.QtWidgets import QWidget
import random


class LadderGameWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ladder Game")
        self.setGeometry(100, 100, 1200, 800)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.view = QGraphicsView()
        self.scene = QGraphicsScene()
        self.view.setScene(self.scene)
        self.layout.addWidget(self.view)

        self.play_button = QPushButton("Play")
        self.play_button.clicked.connect(self.play_game)
        self.layout.addWidget(self.play_button)

        self.ladder_positions = []
        self.ladder_Sero = []
        self.ball_position = QPointF(0, 0)
        self.Timer = None
        self.MakeEveryDict = {}

        self.DestY = self.view.height() - 50

    def play_game(self):
        self.initialize_ladder_positions()
        self.ball_position = QPointF(50, 0)
        self.update_scene()
        QTimer.singleShot(1000, self.animate_ball)

    def initialize_ladder_positions(self):
        self.ladder_Sero = [50,150,250,350,450,550,650,750,850,950]
        #50 + 100 * 0~8        Y 50 + 50 * 0~7
        #래더는 50,850까지 가능. Y는 50 ~ 400까지 가능.
        MakeX_List = []
        MakeY_List = []

        NeccesaryDict = {}
        for n in range(8):
            NeccesaryDict[n] = 0

        for n in range(20):
            RandX = random.randint(0, 8)
            MakeX_List.append(50 + 100 * RandX)
            MakeY_List.append(50 + 50 * random.randint(0, 7))
            NeccesaryDict[RandX] = 50 + 100 * RandX

        for key, value in NeccesaryDict.items():
            if value == 0:
                MakeX_List.append(50 + 100 * key)
                MakeY_List.append(50 + 50 * random.randint(0, 7))


        for i,n in enumerate(MakeY_List):
            key = MakeY_List[i]
            if MakeX_List[i] in self.MakeEveryDict:
                self.MakeEveryDict[MakeX_List[i]].append(key)
            else:
                self.MakeEveryDict[MakeX_List[i]] = [key]

        for key, Pre_List in self.MakeEveryDict.items():
            if key + 100 in self.MakeEveryDict:
                SpareList = []
                for n in range(8):
                    SpareList.append(50 + 50 * random.randint(0, 7))

                Next_List = self.MakeEveryDict[key+100]
                intersect = set(Pre_List) & set(Next_List)
                if intersect:
                    for PreValue in Pre_List:
                        for i, n in enumerate(SpareList):
                            if n == PreValue:
                                SpareList.remove(n)

                    for common_value in intersect:
                        index = Next_List.index(common_value)
                        Next_List[index] = SpareList[random.randint(0, len(SpareList) - 1)]
                    self.MakeEveryDict[key+100] = Next_List

        for key, value_list in self.MakeEveryDict.items():
            self.MakeEveryDict[key] = list(set(value_list))

        for key, value_list in self.MakeEveryDict.items():
            for value in value_list:
                self.ladder_positions.append(QPointF(int(key), int(value)))


    def animate_ball(self):
        self.Timer = QTimer()
        self.Timer.setInterval(100)
        self.Timer.timeout.connect(self.move_ball)
        self.Timer.start()

    def move_ball(self):
        if self.ball_position.y() < self.DestY:
            self.ball_position += QPointF(0, 10)
            self.update_scene()

    def update_scene(self):
        self.scene.clear()
        self.draw_ladders()
        self.draw_ball()

    def draw_ladders(self):
        pen = QPen(Qt.black)
        brush = QBrush(Qt.gray)

        finalX =0
        for position in self.ladder_positions:
            x, y = position.x(), position.y()
            self.scene.addLine(x, y, x + 100, y, pen)  # 가로선

        for positionX in self.ladder_Sero:
            self.scene.addLine(positionX, 30, positionX, self.DestY, pen)  # 세로선


    def draw_ball(self):
        pen = QPen(Qt.black)
        brush = QBrush(Qt.red)

        self.scene.addEllipse(self.ball_position.x()-10, self.ball_position.y() - 10, 20, 20, pen, brush)


def main():
    app = QApplication(sys.argv)
    window = LadderGameWindow()
    window.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

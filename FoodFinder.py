from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QFont, QPainter
from PyQt5.QtWidgets import *

import urls
import re
import requests
import os
from multiprocessing import Process

from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

class FoodFinder(QMainWindow):
    def __init__(self, NaverDict):
        super().__init__()
        self.setWindowTitle("Food Finder")
        self.setFixedSize(1280, 720)
        self.layout = QVBoxLayout(self)

        self.m_GoogleDict = {}
        self.m_Google_All_List = []
        self.Google_Scrapping()

        self.m_NaverDict = NaverDict #여기로 들어온 첫번째인자는 음식점이름, 두번째인자{음식타입: 사진url}
        #참고: google의 이미지url은 encoding되어있음.
        self.m_FoodTypeList = []

        self.Add_FoodTypeList()

        self.m_list_widget = QListWidget(self)
        self.m_list_widget_Text = QLineEdit(self)
        self.layout.addWidget(self.m_list_widget_Text)

        self.Add_List_Items()

        self.m_list_widget.itemSelectionChanged.connect(self.on_item_changed)
        self.m_list_widget.setGeometry(50, 80, 300, 500)

        self.m_FoodFilter_List = QListWidget(self)
        self.m_FoodFilter_List.setSelectionMode(QListWidget.MultiSelection)
        for value in self.m_FoodTypeList:
            self.m_FoodFilter_List.addItem(QListWidgetItem(value))
        self.m_FoodFilter_List.setGeometry(350, 80, 300, 500)
        self.m_FoodFilter_List.itemSelectionChanged.connect(self.on_filter_changed)


        self.m_PreviewImageLabel = QLabel(self)

        self.m_PreviewImageLabel.setGeometry(700, 0, 500, 500)
        self.layout.addWidget(self.m_PreviewImageLabel)

        self.m_WebPage_Button = QPushButton("Search!", self)
        self.m_WebPage_Button.setGeometry(750, 500, 200, 50)
        self.layout.addWidget(self.m_WebPage_Button)

        self.m_WebPage_Button.clicked.connect(self.on_button_clicked)
        self.m_WebPage = None
        self.m_Web_Browser = None
        self.m_p = None

    def on_button_clicked(self):
        if self.m_WebPage is not None:
            self.m_WebPage.close()
            self.m_Web_Browser.close()
            self.m_WebPage = None
            self.m_Web_Browser = None
            self.m_p.stop()

        url = urls.Default_Naver_url
        self.m_p = sync_playwright().start()
        self.m_Web_Browser = self.m_p.chromium.launch(headless=False).new_context(
            viewport={"width": 800, "height": 600}
        )


        self.m_WebPage = self.m_Web_Browser.new_page()
        self.m_WebPage.goto(url)
        self.m_WebPage.get_by_placeholder("검색어를 입력해 주세요.").click()
        selected_items = self.m_list_widget.selectedItems()
        strStoreName = ""
        strFoodName = ""
        if selected_items:
            selected_item =selected_items[0]
            strStoreName = selected_item.text()
        else:
            strStoreName = self.m_list_widget.item(0).text()

        if strStoreName in self.m_NaverDict:
            strFoodName = list(self.m_NaverDict[strStoreName].keys())[0]
        elif strStoreName in self.m_GoogleDict:
            strFoodName = self.m_GoogleDict[strStoreName]

        self.m_WebPage.get_by_placeholder("검색어를 입력해 주세요.").fill(strFoodName + " " + strStoreName)
        self.m_WebPage.get_by_role("button", name="검색", exact=True).click()

    def Add_FoodTypeList(self):
        for value in self.m_GoogleDict.values():
            self.m_FoodTypeList.append(value)
        for value in self.m_NaverDict.values():
            self.m_FoodTypeList.append(list(value.keys())[0])

        self.m_FoodTypeList = set(self.m_FoodTypeList)
        self.m_FoodTypeList = list(self.m_FoodTypeList)

    def on_item_changed(self):
        selected_items = self.m_list_widget.selectedItems()
        if selected_items:
            selected_item = selected_items[0]
            print("선택된 항목:", selected_item.text())

            if selected_item.text() in self.m_GoogleDict:
                print(self.m_GoogleDict[selected_item.text()])
                self.m_PreviewImageLabel.clear()
            elif selected_item.text() in self.m_NaverDict:
                print(self.m_NaverDict[selected_item.text()])
                self.ShowNaverImage(self.m_NaverDict[selected_item.text()])

    def on_filter_changed(self):
        selected_items = self.m_FoodFilter_List.selectedItems()
        if selected_items:
            fixed_list = []
            self.m_list_widget.clear()
            self.Add_List_Items()

            for n in range(self.m_list_widget.count()):
                fixed_list.append(self.m_list_widget.item(n).text())


            for dest_item in fixed_list:#여기엔 음식점 이름이 잡힘..
                for item in selected_items: #여기엔 음식 타입이 잡힘.
                    compare_dest_item = None
                    if dest_item in self.m_NaverDict:
                        compare_dest_item = list(self.m_NaverDict[dest_item].keys())[0]
                    elif dest_item in self.m_GoogleDict:
                        compare_dest_item = self.m_GoogleDict[dest_item]
                    else:
                        print("큰일...")


                    if compare_dest_item == item.text():
                        fixed_list.remove(dest_item)

            self.m_list_widget.clear()

            for key in fixed_list:
                if key == "":
                    separator_widget = QFrame(self)
                    separator_widget.setFrameShape(QFrame.HLine)  # 여기서 말하는 HLine은 horizontal
                    separator_item = QListWidgetItem()
                    separator_item.setSizeHint(separator_widget.sizeHint())
                    self.m_list_widget.addItem(separator_item)
                    self.m_list_widget.setItemWidget(separator_item, separator_widget)
                    continue

                list_item = QListWidgetItem(key)
                self.m_list_widget.addItem(list_item)



    def ShowNaverImage(self, selected_item):
        Image_url = list(selected_item.values())[0]
        response = requests.get(Image_url)
        image_data = response.content

        pixmap = QPixmap()
        pixmap.loadFromData(image_data)

        self.m_PreviewImageLabel.setPixmap(pixmap)

    def Add_List_Items(self):
        # 읽어온 정보를 구글부터 QListWidget에 추가
        for key, value in self.m_GoogleDict.items():
            list_item = QListWidgetItem(key)
            self.m_list_widget.addItem(list_item)

        separator_widget = QFrame(self)
        separator_widget.setFrameShape(QFrame.HLine)  # 여기서 말하는 HLine은 horizontal
        separator_item = QListWidgetItem()
        separator_item.setSizeHint(separator_widget.sizeHint())
        self.m_list_widget.addItem(separator_item)
        self.m_list_widget.setItemWidget(separator_item, separator_widget)

        for key, value in self.m_NaverDict.items():
            list_item = QListWidgetItem(key)
            self.m_list_widget.addItem(list_item)

    def FindAll(self, soup, strRetag, SaveList = None):
        elms = soup.find_all(class_=re.compile(strRetag))
        for e in elms:
            if SaveList is not None:
                SaveList.append(e.text)
        return elms
    def Google_Scrapping(self):
        url = urls.google_url
        r = requests.get(url, headers=urls.headers)
        soup = BeautifulSoup(r.content, 'lxml')

        self.FindAll(soup, r"^rllt__details", SaveList=self.m_Google_All_List)     # 전체 긁어 오기.

        Google_Store_Name_elms = self.FindAll(soup, r"^dbg0pd")     # 음식점 이름.

        for i ,e in enumerate(Google_Store_Name_elms): #여기서는 음식 종류를 알려줌.
            res = e.next_sibling.text.replace(" ", "")
            res = re.split('·', res)
            for strFoodType in res:
                if (strFoodType.isascii() is False) and '리뷰없음' not in strFoodType:
                    if "₩" not in strFoodType:
                        self.m_GoogleDict[Google_Store_Name_elms[i].text] = strFoodType # first = 음식점이름, second = 음식 종류

        r.close()

    def Tick(self):
        i = 0



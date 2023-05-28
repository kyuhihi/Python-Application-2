import time

from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright


class sadariTagi:
    def __init__(self, WebPage,ten_number_list):
        time.sleep(3.5)

        WebPage.locator("#ladders_canvas").click(position={"x": 373, "y": 152})
        WebPage.locator("#ladders_canvas").click(position={"x": 373, "y": 152})
        WebPage.locator("#ladders_canvas").click(position={"x": 373, "y": 152})
        WebPage.locator("#ladders_canvas").click(position={"x": 373, "y": 152})
        WebPage.locator("#ladders_canvas").click(position={"x": 284, "y": 234})
        time.sleep(3)
        for n in range(6):
            self.click_and_Tab(WebPage,str(n+1), True)

        # WebPage.locator("#ladders").get_by_role("textbox").fill("1")
        # WebPage.locator("#ladders").get_by_role("textbox").press("Tab")
        # WebPage.locator("#ladders").get_by_role("textbox").fill("2")
        # WebPage.locator("#ladders").get_by_role("textbox").press("Tab")
        # WebPage.locator("#ladders").get_by_role("textbox").fill("3")
        # WebPage.locator("#ladders").get_by_role("textbox").press("Tab")
        # WebPage.locator("#ladders").get_by_role("textbox").fill("4")
        # WebPage.locator("#ladders").get_by_role("textbox").press("Tab")
        # WebPage.locator("#ladders").get_by_role("textbox").fill("5")
        # WebPage.locator("#ladders").get_by_role("textbox").press("Tab")
        # WebPage.locator("#ladders").get_by_role("textbox").fill("6")
        # WebPage.locator("#ladders").get_by_role("textbox").press("Tab")
        time.sleep(0.5)

        self.click_and_Tab(WebPage, str(7), True)

        # WebPage.locator("#ladders").get_by_role("textbox").fill("7")
        # WebPage.locator("#ladders").get_by_role("textbox").press("Tab")
        time.sleep(0.5)
        self.click_and_Tab(WebPage, str(8), True)

        # WebPage.locator("#ladders").get_by_role("textbox").fill("8")
        # WebPage.locator("#ladders").get_by_role("textbox").press("Tab")
        time.sleep(0.5)
        self.click_and_Tab(WebPage, str(9), True)
        # WebPage.locator("#ladders").get_by_role("textbox").fill("9")
        # WebPage.locator("#ladders").get_by_role("textbox").press("Tab")
        time.sleep(0.5)
        self.click_and_Tab(WebPage, str(10), True)

        # WebPage.locator("#ladders").get_by_role("textbox").fill("10")
        # WebPage.locator("#ladders").get_by_role("textbox").press("Tab")
        time.sleep(0.7)

        for n in range(6):
            self.click_and_Tab(WebPage,str(ten_number_list[n]), True)

        # self.click_and_Tab(WebPage, str(10), True)
        # WebPage.locator("#ladders").get_by_role("textbox").fill("음식1")
        # WebPage.locator("#ladders").get_by_role("textbox").press("Tab")
        # WebPage.locator("#ladders").get_by_role("textbox").fill("음식2")
        # WebPage.locator("#ladders").get_by_role("textbox").press("Tab")
        # WebPage.locator("#ladders").get_by_role("textbox").fill("음식3")
        # WebPage.locator("#ladders").get_by_role("textbox").press("Tab")
        # WebPage.locator("#ladders").get_by_role("textbox").fill("음식4")
        # WebPage.locator("#ladders").get_by_role("textbox").press("Tab")
        # WebPage.locator("#ladders").get_by_role("textbox").fill("음식5")
        # WebPage.locator("#ladders").get_by_role("textbox").press("Tab")
        # WebPage.locator("#ladders").get_by_role("textbox").fill("음식6")
        # WebPage.locator("#ladders").get_by_role("textbox").press("Tab")
        time.sleep(0.5)

        self.click_and_Tab(WebPage, str(ten_number_list[6]), True)

        # WebPage.locator("#ladders").get_by_role("textbox").fill("음식7")
        # WebPage.locator("#ladders").get_by_role("textbox").press("Tab")
        time.sleep(0.5)
        self.click_and_Tab(WebPage, str(ten_number_list[7]), True)

        # WebPage.locator("#ladders").get_by_role("textbox").fill("음식8")
        # WebPage.locator("#ladders").get_by_role("textbox").press("Tab")

        time.sleep(0.5)
        self.click_and_Tab(WebPage, str(ten_number_list[8]), True)

        # WebPage.locator("#ladders").get_by_role("textbox").fill("음식9")
        # WebPage.locator("#ladders").get_by_role("textbox").press("Tab")
        time.sleep(0.5)
        self.click_and_Tab(WebPage, str(ten_number_list[9]), False)

        # WebPage.locator("#ladders").get_by_role("textbox").fill("음식10")
        time.sleep(1)
        WebPage.locator("#ladders_canvas").click(position={"x": 381, "y": 256})

    def click_and_Tab(self,WebPage,InputText,bPressTab):
        print(InputText)
        time.sleep(0.5)

        WebPage.locator("#ladders").get_by_role("textbox").fill(InputText)

        if bPressTab:
            print("여기지나긴하냐")
            time.sleep(0.5)
            WebPage.locator("#ladders").get_by_role("textbox").press("Tab")


import urls
import re
import time

from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright


class NaverCrawler:
    def __init__(self, iProcsCnt):
        self.m_NaverDict = {}
        self.m_FoodTypeList = []

        self.Naver_Scrapping(iProcsCnt)



    def __del__(self):
        self.browser.close()
        self.page.close()

    def FindAll(self, soup, strRetag, SaveList = None):
        elms = soup.find_all(class_=re.compile(strRetag))
        for e in elms:
            if SaveList is not None:
                SaveList.append(e.text)
        return elms

    def FindImageUrls(self, soup, FoodTypeList):
        RetList = []
        url_regex = r'url\("([^"]+)"\)'

        div_elements = soup.find_all("div", class_="yLaWz")
        iCountFoodList = 0

        for url_elms in div_elements:
            matches = re.findall(url_regex, str(url_elms.next_element.contents[0]))
            if matches:
                image_url = matches[0]
                if 'profile' in image_url:
                    continue

                NewDict = {FoodTypeList[iCountFoodList].text : image_url}
                RetList.append(NewDict)
                print(image_url)
                iCountFoodList += 1
            else:
                print("URL not found.")

        return RetList
    def Naver_Scrapping(self, iProccessCnt):
        url = urls.naver_url
        p = sync_playwright().start()

        self.browser = p.chromium.launch(headless=False).new_context(
            viewport={"width": 800, "height": 600}
        )

        self.page = self.browser.new_page()
        self.page.goto(url)

        if iProccessCnt == 0:
            self.Add_Naver_List(page=self.page)
            return

        self.page.locator("div").filter(has_text=re.compile(r"^이전현재1전체5다음$")).get_by_role("button", name="다음").click()

        if iProccessCnt == 1:
            self.Add_Naver_List(page=self.page)
            return

        self.page.locator("div").filter(has_text=re.compile(r"^이전현재2전체5다음$")).get_by_role("button", name="다음").click()

        if iProccessCnt == 2:
            self.Add_Naver_List(page=self.page)
            return

        self.page.locator("div").filter(has_text=re.compile(r"^이전현재3전체5다음$")).get_by_role("button", name="다음").click()

        if iProccessCnt == 3:
            self.Add_Naver_List(page=self.page)
            return

        self.page.locator("div").filter(has_text=re.compile(r"^이전현재4전체5다음$")).get_by_role("button", name="다음").click()
        if iProccessCnt == 4:
            self.Add_Naver_List(page=self.page)



    def Add_Naver_List(self,page):
        page.get_by_text("'주변맛집' 관련 인기 주제 둘러보기").click()
        time.sleep(3)

        content = page.content()
        soup = BeautifulSoup(content, 'lxml')
        SecondElm = self.FindAll(soup, r"^KCMnt")  # 음식종류
        FirstElm = self.FindAll(soup, r"^place_bluelink TYaxT")  # 가게 이름
        SecondElm = self.FindImageUrls(soup, SecondElm)

        for i, e in enumerate(FirstElm):
            self.m_NaverDict[FirstElm[i].text] = SecondElm[i]
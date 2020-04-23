import os,time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

_currentdir = os.path.abspath(os.path.dirname(__file__))

class TestSelenium:
    _URL = "http://127.0.0.1:5000"

    def __init__(self):
        driverpath = os.path.join(_currentdir,'chromedriver')
        self.driver = webdriver.Chrome(executable_path=driverpath)

    def navigation_to(self,path: str) -> "TestSelenium":
        self.driver.get(self._URL + path)

    def close_browser(self) -> "TestSelenium":
        time.sleep(1)
        self.driver.close()

    def click_element_by_id(self,id: str) -> "TestSelenium":
        self.driver.find_element(By.ID,id).click()

    def send_data_to_form(self,title: str,content: str) -> "TestSelenium":
        self.driver.find_element(By.NAME,"title").send_keys(title)
        self.driver.find_element(By.NAME,"content").send_keys(content)
        self.driver.find_element(By.ID,"post-form").submit()

    def extract_list(self) -> "TestSelenium":
        WebDriverWait(self.driver,5).until(EC.visibility_of_element_located((By.ID,"posts")))
        elements = self.driver.find_elements(By.CLASS_NAME,"post-link")
        element_text = [x.text for x in elements]
        print(element_text)
        elements[-1].click()
        WebDriverWait(self.driver,5).until(EC.url_changes(self._URL + '/blog'))


if __name__ == '__main__':
    scrape = TestSelenium()
    scrape.navigation_to("/")
    scrape.click_element_by_id("blog-link")
    scrape.click_element_by_id("add-post-link")
    scrape.send_data_to_form("test","dqwdwq")
    scrape.extract_list()
    scrape.close_browser()

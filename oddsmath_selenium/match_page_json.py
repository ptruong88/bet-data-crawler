from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.webdriver import WebDriver
import json

class MatchPageJSon:
    def __init__(self, match_page_content_driver: WebDriver):
        self.match_page_content_driver = match_page_content_driver

    def get_match_data(self):
        pre = self.match_page_content_driver.find_element(By.TAG_NAME, 'pre').text
        return json.loads(pre)


    
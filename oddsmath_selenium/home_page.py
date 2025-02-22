from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.webdriver import WebDriver

class HomePage:

    def __init__(self, home_page_content_driver: WebDriver):
        self.home_page_content_driver = home_page_content_driver

    def get_date_event_links(self):
        date_event_links = []

        days_games = self.home_page_content_driver.find_element(By.ID, "days_games")
        event_items = days_games.find_elements(By.CLASS_NAME, 'item')

        for event_item in event_items:
            tag_a = event_item.find_element(By.TAG_NAME, 'a')
            href = tag_a.get_attribute('href')
            date_event_links.append(href)
        return date_event_links
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.webdriver import WebDriver

class DatePage:

    def __init__(self, date_page_content_driver: WebDriver):
        self.date_page_content_driver = date_page_content_driver        

    def get_match_links(self):    
        match_links = []

        center_column = self.date_page_content_driver.find_element(By.ID, "center_column")
        home_teams = center_column.find_elements(By.CLASS_NAME, 'homeTeam')

        for home_team in home_teams:
            event = home_team.find_element(By.CLASS_NAME, 'event')
            link = home_team.find_element(By.LINK_TEXT, event.text)
            href = link.get_attribute('href')
            match_links.append(href)
        return match_links
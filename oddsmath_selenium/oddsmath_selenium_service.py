from selenium import webdriver
from typing import List, Callable, TypeVar
from oddsmath_selenium.match_page_json import MatchPageJSon
from oddsmath_selenium.match_page import MatchPage
from oddsmath_selenium.date_page import DatePage
from oddsmath_selenium.home_page import HomePage
from services.config_service import get_selenium_url

T = TypeVar("T")  # Generic return type for functions that use WebDriver

def with_driver(func: Callable[[webdriver.Chrome], T]) -> T:
    """Handles WebDriver setup, execution, and teardown."""
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")  # Run in headless mode
    driver = webdriver.Remote(command_executor=get_selenium_url(), options=options)
    try:
        return func(driver)
    finally:
        # print("Tear down")
        driver.quit()

def get_date_event_links(home_link: str) -> List[str]:
    """Fetches date event links from the homepage."""
    def fetch_links(driver: webdriver.Chrome) -> List[str]:
        driver.get(home_link)
        home_page = HomePage(driver)
        return home_page.get_date_event_links()
    
    return with_driver(fetch_links)

def get_match_links_for_a_date(date_link: str) -> List[str]:
    """Fetches match links for a given date."""
    def fetch_links(driver: webdriver.Chrome) -> List[str]:
        driver.get(date_link)
        date_page = DatePage(driver)
        return date_page.get_match_links()
    
    return with_driver(fetch_links)

def get_bet_data_for_a_date(date_link: str) -> List:
    """Fetches betting data list for matches in a day."""
    def fetch_bet_data(driver: webdriver.Chrome):
        date_data = []
        driver.get(date_link)
        date_page = DatePage(driver)
        match_links = date_page.get_match_links()
        for match_link in match_links:
            print(match_link)
            driver.get(match_link)
            match_page = MatchPage(driver)
            bet_data = match_page.get_bet_data()
            print(bet_data)
            date_data.append(bet_data)
        return date_data
    
    return with_driver(fetch_bet_data)

def get_bet_data_for_a_match(match_link: str):
    """Fetches betting data for a match."""
    def fetch_bet_data(driver: webdriver.Chrome):
        driver.get(match_link)
        match_page = MatchPage(driver)
        return match_page.get_bet_data()
    
    return with_driver(fetch_bet_data)

def get_match_info(match_api: str):
    def fetch_match_data(driver: webdriver.Chrome):
        driver.get(match_api)
        matchPageJson = MatchPageJSon(driver)
        return matchPageJson.get_match_data()
    
    return with_driver(fetch_match_data)

from typing import List
import oddsmath_selenium.oddsmath_selenium_service as oddsmath_selenium_service

def get_date_event_links(home_link: str) -> List[str]:
    return oddsmath_selenium_service.get_date_event_links(home_link)

def get_match_links_for_a_date(date_link: str) -> List[str]:
    return oddsmath_selenium_service.get_match_links_for_a_date(date_link)

def get_bet_data_for_a_date(date_link: str) -> List:
    return oddsmath_selenium_service.get_bet_data_for_a_date(date_link)

def get_bet_data_for_a_match(match_link: str):
    return oddsmath_selenium_service.get_bet_data_for_a_match(match_link)


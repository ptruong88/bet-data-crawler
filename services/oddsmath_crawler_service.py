import re
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor
from typing import List
import oddsmath_selenium.oddsmath_selenium_service as oddsmath_selenium_service

def process_oddsmath_link(oddsmath_link: str):
    try:
        print(f'oddsmath_link {oddsmath_link}')
        if is_oddsmath_link(oddsmath_link) is False:
                print(f'The application supports only oddsmath.com links.')
                return
        
        if is_match_link(oddsmath_link):
            process_match_link(oddsmath_link)
        elif is_date_link(oddsmath_link):
            process_date_link(oddsmath_link)
        else:    
            # Fetch event links (most pages have this)
            event_date_links = get_date_event_links(oddsmath_link)
            print(f'EVENT_LINKS\n{event_date_links}')
            with ThreadPoolExecutor(max_workers=5) as executor:
                executor.map(process_date_link, event_date_links)
    except:
        print(f'ERROR: ERROR when processing the link {oddsmath_link}')

def process_match_link(oddsmath_link: str):
    try:
        bet_data = get_bet_data_for_a_match(oddsmath_link)
        print(f'\nBET_DATA\n{bet_data}')

        match_id = extract_match_id(oddsmath_link)
        if match_id:
            match_api = f'https://www.oddsmath.com/api/v1/live-odds.json/?event_id={match_id}&cat_id=0&include_exchanges=1&language=en&country_code=US'
            match_data = get_match_data_from_match_api(match_api)
            print(f'\nMATCH_DATA\n{match_data}')
    except:
        print(f'ERROR: ERROR when processing the link {oddsmath_link}')

def extract_match_id(match_link: str):
    match = re.search(r"-(\d+)/$", match_link)

    if match:
        match_id = match.group(1)
        return match_id
    return None

def process_date_link(oddsmath_link: str):
    try:
        print(f'Processing date link -> {oddsmath_link}')
        match_links = get_match_links_for_a_date(oddsmath_link)
        print(f'\nMATCH_LINKS\n{match_links}')
        with ThreadPoolExecutor(max_workers=5) as executor:
            bet_data_results = list(executor.map(process_match_link, match_links))

        print("\nBET DATA (per match):")
        for match, bet_data in zip(match_links, bet_data_results):
            print(f"{match} -> {bet_data}")
    except:
        print(f'ERROR: ERROR when processing the link {oddsmath_link}')

def is_oddsmath_link(oddsmath_link: str):
    parsed_url = urlparse(oddsmath_link)
    return parsed_url.netloc.endswith("oddsmath.com")

def is_date_link(oddsmath_link: str):
    pattern = r"^https://www\.oddsmath\.com/football/matches/(today|\d{4}-\d{2}-\d{2})/$"
    return bool(re.match(pattern, oddsmath_link))

def is_match_link(oddsmath_link: str):
    pattern = re.compile(
        r"^https://www\.oddsmath\.com/football/[\w-]+/[\w-]+-\d+/"
        r"\d{4}-\d{2}-\d{2}/[\w-]+-vs-[\w-]+-\d+/$"
    )
    return bool(pattern.match(oddsmath_link))

def get_date_event_links(home_link: str) -> List[str]:
    return oddsmath_selenium_service.get_date_event_links(home_link)

def get_match_links_for_a_date(date_link: str) -> List[str]:
    return oddsmath_selenium_service.get_match_links_for_a_date(date_link)

def get_bet_data_for_a_date(date_link: str) -> List:
    return oddsmath_selenium_service.get_bet_data_for_a_date(date_link)

def get_bet_data_for_a_match(match_link: str):
    return oddsmath_selenium_service.get_bet_data_for_a_match(match_link)

def get_match_data_from_match_api(match_api: str):
    return oddsmath_selenium_service.get_match_info(match_api)



import oddsmath_crawler_service
import argparse
import re
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor

def main():
    parser = argparse.ArgumentParser(description="Pass a date link from oddsmath to get matches' bet data.", allow_abbrev=False)
    # Define CLI arguments
    parser.add_argument("--oddsmath_link", type=str, required=True, help="Pass a date link")
    # Parse CLI arguments
    args = parser.parse_args()
    oddsmath_link = args.oddsmath_link

    if is_oddsmath_link(oddsmath_link) is False:
            print(f'The application supports only oddsmath.com links.')
            return
    
    # Fetch event links (most pages have this)
    event_date_links = oddsmath_crawler_service.get_date_event_links(oddsmath_link)
    print(f'EVENT_LINKS\n{event_date_links}')
    print(f'Test multithread with 2 event links, {event_date_links[0:2]}')
    with ThreadPoolExecutor(max_workers=5) as executor:
       executor.map(process_date_link, event_date_links[0:2])

    if is_date_link(oddsmath_link):
        process_date_link(oddsmath_link)

    if is_match_link(oddsmath_link):
        bet_data = oddsmath_crawler_service.get_bet_data_for_a_match(oddsmath_link)
        print(f'\nBET_DATA\n{bet_data}')

def process_date_link(oddsmath_link):
    print(f'Processing date link -> {oddsmath_link}')
    match_links = oddsmath_crawler_service.get_match_links_for_a_date(oddsmath_link)
    print(f'\nMATCH_LINKS\n{match_links}')
    print(f'Test multithread with 5 match links for date match.')
    test_match_links = match_links[0:5]
    with ThreadPoolExecutor(max_workers=5) as executor:
        bet_data_results = list(executor.map(oddsmath_crawler_service.get_bet_data_for_a_match, test_match_links))

    print("\nBET DATA (per match):")
    for match, bet_data in zip(test_match_links, bet_data_results):
        print(f"{match} -> {bet_data}")

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

if __name__ == "__main__":
    main()
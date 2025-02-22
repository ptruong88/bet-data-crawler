import oddsmath_crawler_service
import argparse
import re
from urllib.parse import urlparse

def main():
    parser = argparse.ArgumentParser(description="Pass a date link from oddsmath to get matches' bet data.", allow_abbrev=False)
    # Define CLI arguments
    parser.add_argument("--oddsmath_link", type=str, required=True, help="Pass a date link")
    # Parse CLI arguments
    args = parser.parse_args()
    if args.oddsmath_link:
        oaddsmath_link = args.oddsmath_link

        if is_oddsmath_link(oaddsmath_link) is False:
            print(f'The application supports only oddsmath.com links.')
            return
        
        # Most pages have the events info
        event_links = oddsmath_crawler_service.get_date_event_links(oaddsmath_link)
        print(f'EVENT_LINKS\n{event_links}')

        if is_date_link(oaddsmath_link):
            match_links = oddsmath_crawler_service.get_match_links_for_a_date(oaddsmath_link)
            print(f'\nMATCH_LINKS\n{match_links}')

        if is_match_link(oaddsmath_link):
            bet_data = oddsmath_crawler_service.get_bet_data_for_a_match(oaddsmath_link)
            print(f'\nBET_DATA\n{bet_data}')

def is_oddsmath_link(oddsmath_link: str):
    parsed_url = urlparse(oddsmath_link)
    return parsed_url.netloc.endswith("oddsmath.com")

def is_date_link(oddsmath_link: str):
    pattern = r"^https://www\.oddsmath\.com/football/matches/(today|\d{4}-\d{2}-\d{2})/$"
    return bool(re.match(pattern, oddsmath_link))

def is_match_link(oaddsmath_link: str):
    pattern = re.compile(
        r"^https://www\.oddsmath\.com/football/[\w-]+/[\w-]+-\d+/"
        r"\d{4}-\d{2}-\d{2}/[\w-]+-vs-[\w-]+-\d+/$"
    )
    return bool(pattern.match(oaddsmath_link))

if __name__ == "__main__":
    main()
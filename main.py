from services.config_service import get_oddsmath_links
from services.oddsmath_crawler_service import process_oddsmath_link

def main():
    print(f'Processing oddsmath links from environment: {get_oddsmath_links()}')
    for oddsmath_link in get_oddsmath_links():
        process_oddsmath_link(oddsmath_link)

if __name__ == "__main__":
    main()
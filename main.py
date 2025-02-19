from selenium import webdriver
from selenium.webdriver.common.by import By
import single_match_service

def main():

    # set up ChromeOptions
    options = webdriver.ChromeOptions()

    # add headless Chrome option
    options.add_argument("--headless=new")

    # set up Chrome in headless mode
    driver = webdriver.Chrome(options=options)

    # open the target website
    match_link = "https://www.oddsmath.com/football/international/afc-asian-cup-clubs-2424/2025-02-20/jeonbuk-hyundai-motors-vs-port-fc-4714094/"
    # driver.get("https://www.scrapingcourse.com/ecommerce/")
    # driver.get("https://www.oddsmath.com/football/international/afc-asian-cup-clubs-2424/2025-02-20/jeonbuk-hyundai-motors-vs-port-fc-4714094/")

    # print the current URL and page title
    # print(f"Page URL: {driver.current_url}")
    # print(f"Page Title: {driver.title}")

    match_bet_data = single_match_service.get_bet_data_for_a_match(driver, match_link)

    #     # append the scraped data to the empty list
    #     scraped_data.append(data)

    # print the scraped data
    print(match_bet_data)

    # close the driver instance and release its resources
    driver.quit()

# get bet data for a match link
# data returns with a list of elements {name, odds_1, odds_X, odds_2}



main()
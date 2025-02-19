from selenium.webdriver.common.by import By

def get_bet_data_for_a_match(driver, match_link: str):
    driver.get(match_link)

    # define an empty list to collect scraped data
    match_bet_data = {}

    #check if value is not exist
    team_1 = driver.find_element(By.CLASS_NAME, 't1')
    match_bet_data['team_t1'] = team_1.text

    team_2 = driver.find_element(By.CLASS_NAME, 't2')
    match_bet_data['team_t2'] = team_2.text


    bet_data_list = []

    bet_table = driver.find_element(By.ID, "table-odds-cat-0")
    # print(bet_table)

    bet_table_body = bet_table.find_element(By.TAG_NAME, "tbody")
    bet_table_body_rows = bet_table_body.find_elements(By.TAG_NAME, "tr")

    for bet_table_body_row in bet_table_body_rows:
        # bet name
        bet_name = bet_table_body_row.find_element(By.CLASS_NAME, "bookmaker-name")
        # print(f"{bet_name.text}")

        # odds-1
        odds_1 = bet_table_body_row.find_element(By.CLASS_NAME, "odds-1").find_element(By.CLASS_NAME, 'odds-value')
        # print(f"{odds_1.text}")

        # odds-X
        odds_X = bet_table_body_row.find_element(By.CLASS_NAME, "odds-X").find_element(By.CLASS_NAME, 'odds-value')
        # print(f"{odds_X.text}")

        # odds-2
        odds_2 = bet_table_body_row.find_element(By.CLASS_NAME, "odds-2").find_element(By.CLASS_NAME, 'odds-value')
        # print(f"{odds_2.text}")

        # print('\n---------------')
        bet_data = {
            'name': bet_name.text,
            'odds_1': odds_1.text,
            'odds_X': odds_X.text,
            'odds_2': odds_2.text,
        }

        bet_data_list.append(bet_data)

    match_bet_data['bets'] = bet_data_list

    return match_bet_data
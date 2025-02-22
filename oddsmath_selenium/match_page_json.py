from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.webdriver import WebDriver
import json

class MatchPageJSon:
    def __init__(self, match_page_content_driver: WebDriver):
        self.match_page_content_driver = match_page_content_driver

    def get_match_data(self):
        pre = self.match_page_content_driver.find_element(By.TAG_NAME, 'pre').text
        pre_js = json.loads(pre)
        
        match_info = {}
        event = pre_js['event']
        match_info['team_t1'] = event['hometeam']['name']
        match_info['team_t2'] = event['awayteam']['name']
        match_info['event_time'] = event['time']

        data = pre_js['data']
        bets = []
        for bet_house in data.keys():
            bet_house_data = data[bet_house]
            live_bet_data = bet_house_data['live']
            bet_data = {
                'name': bet_house,
                'odds_1': live_bet_data['1'],
                'odds_X': live_bet_data['X'],
                'odds_2': live_bet_data['2'],
            }            
            bets.append(bet_data)

        match_info['bets'] = bets

        return match_info



    
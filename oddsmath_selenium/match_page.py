from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.webdriver import WebDriver

class MatchPage:
    def __init__(self, match_page_content_driver: WebDriver):
        self.match_page_content_driver = match_page_content_driver

    def get_bet_data(self):
        """Public method to extract match betting data."""
        match_bet_data = self._extract_match_info()
        match_bet_data["bets"] = self._extract_bet_data()
        return match_bet_data

    def _extract_match_info(self):
        """Private method to extract basic match details (teams & event time)."""
        match_info = {}
        try:
            center_column = self.match_page_content_driver.find_element(By.ID, "center_column")
            match_info["team_t1"] = center_column.find_element(By.CLASS_NAME, "t1").text
            match_info["team_t2"] = center_column.find_element(By.CLASS_NAME, "t2").text
            match_info["event_time"] = center_column.find_element(By.CLASS_NAME, "event-time").text
        except Exception as e:
            print(f"Error extracting match info: {e}")
        return match_info

    def _extract_bet_data(self):
        """Private method to extract betting odds."""
        bet_data_list = []
        try:
            bet_table = self.match_page_content_driver.find_element(By.ID, "table-odds-cat-0")
            bet_rows = bet_table.find_element(By.TAG_NAME, "tbody").find_elements(By.TAG_NAME, "tr")

            for row in bet_rows:
                try:
                    bet_data = {
                        "name": row.find_element(By.CLASS_NAME, "bookmaker-name").text,
                        "odds_1": row.find_element(By.CLASS_NAME, "odds-1").find_element(By.CLASS_NAME, "odds-value").text,
                        "odds_X": row.find_element(By.CLASS_NAME, "odds-X").find_element(By.CLASS_NAME, "odds-value").text,
                        "odds_2": row.find_element(By.CLASS_NAME, "odds-2").find_element(By.CLASS_NAME, "odds-value").text,
                    }
                    bet_data_list.append(bet_data)
                except Exception as e:
                    print(f"Skipping a bet row due to error: {e}")
        except Exception as e:
            print(f"Error extracting bet data: {e}")
        
        return bet_data_list
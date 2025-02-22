# bet-data-crawler
This program looks through the contents of the website https://www.oddsmath.com/ on a specific day, extract and store matches' bet data 

User can send
- any oddsmath link, such as https://www.oddsmath.com/, to get date event links.
- a date link, such as https://www.oddsmath.com/football/matches/2025-02-21/, to get the date's match links.
- a match link, such as https://www.oddsmath.com/football/international/africa-caf-nations-cup-women-44344/2025-02-21/kenya-women-vs-tunisia-women-4715230/, to get the match bet data.

# System design
<img width="532" alt="Screenshot 2025-02-21 at 10 36 43 PM" src="https://github.com/user-attachments/assets/6eea9a8d-7c25-4af2-9f49-3e3fb582a0b8" />

# Requirements
The application is test with Python3.

The application requires:
- selenium 4.29.0

# Setup
The best way is running the application in python virtual environment.

- Create a virtual environment:

        python3 -m venv myenv

- Run the virtual environment:

        source myenv/bin/activate

- Installs requirement packages:

        pip install -r requirements.txt

# How to use
After you have a virtual environment and install requirement packages, you can test the application by running this command line:

    python3 main.py --oddsmath_link <oddsmath link>

**Example:**

- With a oddsmath's match link, such as https://www.oddsmath.com/football/international/afc-championship-u20-103495/2025-02-22/saudi-arabia-u20-vs-china-u20-4715157/, the output shows the match' bet data.

        python3 main.py --oddsmath_link https://www.oddsmath.com/football/international/afc-championship-u20-103495/2025-02-22/saudi-arabia-u20-vs-china-u20-4715157/

        BET_DATA
        {'team_t1': 'SAUDI ARABIA U20', 'team_t2': 'CHINA U20', 'event_time': 'Saturday, Feb 22, 2025, 08:15', 'bets': [{'name': '1XBET', 'odds_1': '3.27', 'odds_X': '3.25', 'odds_2': '2.06'}, {'name': 'Bettogoal', 'odds_1': '3.17', 'odds_X': '3.37', 'odds_2': '2.05'}, {'name': 'Betway', 'odds_1': '3.10', 'odds_X': '3.30', 'odds_2': '2.10'}, {'name': 'FEZbet', 'odds_1': '3.40', 'odds_X': '3.25', 'odds_2': '2.05'}, ...]}

- With a oddsmath's date link, such as https://www.oddsmath.com/football/matches/today/, the output shows all the matches' links for that date, and the bet data for each match.

        python3 main.py --oddsmath_link https://www.oddsmath.com/football/matches/today/
        
        MATCH_LINKS
        ['https://www.oddsmath.com/football/international/afc-championship-u20-103495/2025-02-22/saudi-arabia-u20-vs-china-u20-4715157/', ...]

        BET_DATA
        {'team_t1': 'SAUDI ARABIA U20', 'team_t2': 'CHINA U20', 'event_time': 'Saturday, Feb 22, 2025, 08:15', 'bets': [{'name': '1XBET', 'odds_1': '3.27', 'odds_X': '3.25', 'odds_2': '2.06'}, {'name': 'Bettogoal', 'odds_1': '3.17', 'odds_X': '3.37', 'odds_2': '2.05'}, {'name': 'Betway', 'odds_1': '3.10', 'odds_X': '3.30', 'odds_2': '2.10'}, {'name': 'FEZbet', 'odds_1': '3.40', 'odds_X': '3.25', 'odds_2': '2.05'}, ...]}

- With the oddsmath's homepage's link https://www.oddsmath.com/, the output shows all event links, matches for each link, and bet data for each match.

        python3 main.py --oddsmath_link https://www.oddsmath.com/

        EVENT_LINKS
        ['https://www.oddsmath.com/football/matches/2025-02-21/', 'https://www.oddsmath.com/football/matches/today/', 'https://www.oddsmath.com/football/matches/2025-02-23/',
        ...]

        MATCH_LINKS
        ['https://www.oddsmath.com/football/international/afc-championship-u20-103495/2025-02-22/saudi-arabia-u20-vs-china-u20-4715157/', ...]

        BET_DATA
        {'team_t1': 'SAUDI ARABIA U20', 'team_t2': 'CHINA U20', 'event_time': 'Saturday, Feb 22, 2025, 08:15', 'bets': [{'name': '1XBET', 'odds_1': '3.27', 'odds_X': '3.25', 'odds_2': '2.06'}, {'name': 'Bettogoal', 'odds_1': '3.17', 'odds_X': '3.37', 'odds_2': '2.05'}, {'name': 'Betway', 'odds_1': '3.10', 'odds_X': '3.30', 'odds_2': '2.10'}, {'name': 'FEZbet', 'odds_1': '3.40', 'odds_X': '3.25', 'odds_2': '2.05'}, ...]}

# Database
Bet data is updating frequently for a match, and whenever the new data is showed, we want to keep its historical data, instead of updating its existing data. Also, it can be helpful when we analyze bet data. A database needs to support time-series data or append-only operation.

For the oddsmath, it supports to get future matches' bet data for today and tomorrow, and one day can have over 800 matches. When a match starts, the system needs to fetch bet data frequently for 90-120 minutes. 

Let assume we have some conditions on how many data the database needs to store, and those matches start at the end of a date:
- in 90 minutes, 800 matches keep update bet data every 1 minute.

        1 update/min * 90 min/match * 800 matches = 72,000 updates

- 20% of 800 matches go to extra time (30 minutes), update bet data every 1 minute.

        1 update/min * 30 min/match * 0.2 * 800 matches = 4,800 updates

- For the other times, 800 matches keep update bet data every 15 minute.

        1 update/ 15 min * 60 min/hr * 10 hrs * 800 matches = 32,000 updates

- Assume each match has an average of bet houses is 6, so we have the amount of data to store is

            For match times, (72,000 updates + 4,800 updates) * 6 = 460,800 records.

            For non-match times, 32,000 updates * 6 = 192,000 records.

            Total = 460,800 + 192,000 = 652,800 records

**Database's requirements:**
- Number of records being ingested per second: 4,800 records (800 updates * 6)
- Number of records being ingested per day: 652,800 records
- Support time-series data
- Support append-only operation
- Low-cost
- Self-hosted
- Require less efforts as much as it can for DevOps

With a help from chatGPT, I get some suggestions to consider. Look like VictoriaMetrics is a good option for this case.

![Screenshot 2025-02-21 at 10 42 12 PM](https://github.com/user-attachments/assets/c9ad7fe3-fe85-4fc6-becd-bab11a015737)

# To-do
- Set up a docker image for the application (I have tested [selenium-docker](https://github.com/ptruong88/docker-selenium/blob/trunk/docker-compose-v2.yml), but I can't have my application docker to hit the selenium hub's IP adress).
- Flow chart.
- Store a date's matches' bet data as a csv.

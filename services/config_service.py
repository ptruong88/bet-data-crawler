import os

print('Load environments')

def __get_env_value(env_key, default_key=None):
    return os.getenv(env_key, default_key)

def get_oddsmath_links():
    return __get_env_value('ODDSMATH_LINKS', '').split(',')

def get_selenium_url():
    return __get_env_value('SELENIUM_URL', 'http://selenium-hub:4444')

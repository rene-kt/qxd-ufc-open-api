from selenium import webdriver
from retrying import retry

@retry(wait_fixed=3000, stop_max_attempt_number=5)
def try_connection():
    print("Trying to connect to selenium server...") 
    opts = webdriver.ChromeOptions()
    opts.add_argument('--no-sandbox')
    opts.add_argument('--headless')
    opts.add_argument('--disable-popup-blocking')

    return webdriver.Remote(
        command_executor='http://selenium:4444',
        options=opts
    )

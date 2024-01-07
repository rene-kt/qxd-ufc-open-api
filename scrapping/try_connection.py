from selenium import webdriver
    
def try_connection(isLocal = False):
    print("Trying to connect to selenium server...") 
    result = None
    while result is None:
        try:
            opts = webdriver.ChromeOptions()
            opts.add_argument('--no-sandbox')
            opts.add_argument('--headless')

            if isLocal: driver = webdriver.Chrome(options=opts)
            else: driver = webdriver.Remote(command_executor="http://selenium:4444", options=opts)
            return driver
        except:
            print("It was not possiblee to connect") 
            pass
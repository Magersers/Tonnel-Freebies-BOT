from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent

def create_driver():

    chromedriver_autoinstaller.install()
    ua = UserAgent()
    #Конфигурации браузера 
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--disable-blink-features=AutomationControlled") 
    chrome_options.add_argument(f"user-agent={ua.random}")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)
    chrome_options.add_argument("--headless")  
    chrome_options.add_argument("--disable-gpu")  
    # chrome_options.add_argument("--no-sandbox")  
    chrome_options.add_argument("--window-size=1920,600")
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument("--disable-software-rasterizer")
    chrome_options.add_argument('--ignore-certificate-errors')  # Игнорировать ошибки SSL
    chrome_options.add_argument('--ignore-ssl-errors') 

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get('http://web.telegram.org/a/')  # Замените на нужный URL
    return driver


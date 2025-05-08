from parsel import Selector
from selenium import webdriver
from urllib.parse import urljoin
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

def crawler(url):
    driver.get(url)
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, "site-roster-card-image-link"))
    )

    selector = Selector(text=driver.page_source)

    agent_link_xpath = "//a[@class='site-roster-card-image-link']/@href"
    agent_links = selector.xpath(agent_link_xpath).getall()

    driver.quit()
    return [urljoin(url,link) for link in agent_links]

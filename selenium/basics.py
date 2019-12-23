from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--headless")

driver = webdriver.Chrome(executable_path=".\drivers\chromedriver.exe", options=chrome_options)
driver.get("https://duckduckgo.com")

search_box = driver.find_element_by_name("q")
search_box.send_keys("My user agent")

#search_btn = driver.find_element_by_xpath("//input[@class='search__button  js-search-button']")
#search_btn.click()

search_box.send_keys(Keys.ENTER)

print(driver.page_source)

driver.close()
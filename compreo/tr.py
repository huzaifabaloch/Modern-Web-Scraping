from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from shutil import which


firefox_dr = which('geckodriver')

driver = webdriver.Firefox(executable_path=firefox_dr)

driver.get('https://www.google.com/')

search = driver.find_element_by_xpath("//input[@title='Search']")

search.send_keys('jerry')
search.send_keys(Keys.ENTER)
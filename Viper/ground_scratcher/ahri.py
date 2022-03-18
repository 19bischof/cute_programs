from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

driver = webdriver.Firefox(firefox_binary=r"C:\Users\m.bischof\AppData\Local\Mozilla Firefox\firefox.exe")
driver.get("http://www.python.org")
assert "Python" in driver.title
elem = driver.find_element(By.ID,"id-search-field")
elem.clear()
elem.send_keys("pycon")
elem.send_keys(Keys.RETURN)

assert "Hotel Mediterraneo" in driver.page_source
driver.close()
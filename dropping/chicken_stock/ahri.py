from multiprocessing.connection import wait
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.options import Options
import config as cg
import time
options = Options()
options.headless = True
browser = webdriver.Firefox


def exchange_icoin(driver: browser):
    driver.get(cg.icoin_url)
    elem = driver.find_element(By.ID, "value")
    while 1:
        assert float(elem.text)
        print(time.perf_counter(), elem.text)
        time.sleep(0.1)


def _wait_until_elem_found(driver: browser, selector, timeout=5):
    interval = 0.3
    for _ in range(int(timeout / interval)):
        try:
            elem = driver.find_element(By.CSS_SELECTOR, selector)
        except NoSuchElementException:
            time.sleep(interval)
            continue
        return elem.text


def get_game(driver: browser):
    driver.get(cg.url)
    return _wait_until_elem_found(driver, "a[data-a-target='stream-game-link']")


def get_banner(driver: browser):
    driver.get(cg.url)
    return _wait_until_elem_found(driver, "div.Layout-sc-nxg1ff-0")


if __name__ == "__main__":
    with browser(options=options, firefox_binary=r"C:\Users\m.bischof\AppData\Local\Mozilla Firefox\firefox.exe") as driver:
        # exchange_icoin(driver)
        print(game := get_game(driver))
        print(banner:= get_banner(driver))
        #not correctly implemented yet

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.options import Options
import config as cg
import time

pink = '\033[38;5;206m'
reset = '\033[0m'

def pink_print(s):
    print(pink+s+reset)

options = Options()
options.headless = cg.headless
browser = webdriver.Firefox

def get_icoin(driver: browser):
    driver.get(cg.icoin_url)
    elem = driver.find_element(By.ID, "value")
    while 1:
        assert float(elem.text)
        print(time.perf_counter(), elem.text)
        time.sleep(0.1)


def _wait_until_elem_found(driver: browser, selector,endless=False, timeout=20,multiple=False):
    interval = 0.3
    start_time = time.perf_counter()
    while endless or time.perf_counter() - start_time < timeout:
        try:
            if multiple: 
                elem = driver.find_elements(By.CSS_SELECTOR, selector)
                if not elem:
                    print(len(elem))
                    time.sleep(interval)
                    continue
            else:
                elem = driver.find_element(By.CSS_SELECTOR, selector)
        except NoSuchElementException:
            time.sleep(interval)
            continue
        return elem


def get_game(driver: browser):
    driver.get(cg.tw_url)
    return _wait_until_elem_found(driver, "a[data-a-target='stream-game-link']").text


def get_prediction_results(driver:browser):
    driver.get(cg.tw_url+"/chat")
    elems=  _wait_until_elem_found(driver,
     'div.prediction-summary-outcome',
     endless=True,
     multiple=True)
    print("length",len(elems))
    for i in range(len(elems)):
        if elems[i].text.find("__winner-label") != -1:
            print("winner is",i)
    "put here the logic to extract valuable data from that"

def get_new_prediction(driver: browser):
    driver.get(cg.tw_url+"/chat")
    elem =  _wait_until_elem_found(driver,
     'p[data-test-selector="community-prediction-highlight-header__title"]',
     endless=True)
    print(elem.text)
    assert elem.text.find("Predict with Channel Points")




if __name__ == "__main__":
    print("starting browser")
    with browser(options=options, firefox_binary=cg.fire_bin,firefox_profile=cg.profile) as driver:
        # get_icoin(driver)
        # pink_print("getting game")
        # print(game := get_game(driver))
        pink_print("getting banner")
        # print(banner:= get_new_prediction(driver))
        print(banner:= get_prediction_results(driver))
        #not correctly implemented yet

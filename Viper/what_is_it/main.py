from infi.systray import SysTrayIcon
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time
import os
user_path = os.path.expanduser('~')
options = Options()
options.headless = True
options.log
fp = webdriver.FirefoxProfile(
    user_path+r"\AppData\Roaming\Mozilla\Firefox\Profiles\uwojlef0.automat")
driver = webdriver.Firefox(options=options,
                           firefox_profile=fp, firefox_binary=user_path+r"\AppData\Local\Mozilla Firefox\firefox.exe")
driver.get("https://web.whatsapp.com")
# driver.minimize_window()
try:
    elem = WebDriverWait(driver, 10).until(
        # tries to find intro-title within 30 seconds
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, '[data-testid="intro-title"]'))
    )
except TimeoutException:
    print("Couldn't load Whatsapp Web!")
    driver.save_screenshot("what_happened.png")
    driver.quit()
    quit()
print("Whatsapp Web loaded successfully!")

chats, chat_dick = None, None


def load_chats():
    global chats, chat_dick
    chats = driver.find_elements(
        By.CSS_SELECTOR, '[aria-label="Chat list"] > div')
    # print("chats:", chats)
    chat_dick = {}
    for c in chats:
        try:
            span = c.find_element(
                By.CSS_SELECTOR, "div > div > div:nth-child(2) > div > div > span")
            # print(span.text)
            chat_dick[span.text] = c
        except StaleElementReferenceException:
            break
    print(f"loaded {len(chat_dick)} chats")


def check_if_got_unread():
    global chat_dick
    not_vips = []
    with open("unimportant_chats.secret", "r") as f:
        for line in f:
            if line:
                not_vips.append(line.strip())
    got_one = False
    for name, element in chat_dick.items():
        if name in not_vips:
            continue
        try:
            div_of_unread_msg = element.find_element(
                By.CSS_SELECTOR, "div > div > div:nth-child(2) > div:nth-child(2) > div:nth-child(2)")
        except StaleElementReferenceException:
            continue
        if div_of_unread_msg.text.strip() == "":
            continue
        print("You've got unread messages from", name)
        got_one = True
    if got_one:
        user_name = os.environ['USERNAME']
        os.system("C:\\ProgramData\\"+user_name+r"\WhatsApp\WhatsApp.exe")
    else:
        print("no unread messages!")


i = 0
running = True


def stop(*args):
    global running
    running = False


menu_options = (("Stop Whatsapp daemon", None, stop),)
systray = SysTrayIcon("./Dapino-Summer-Holiday-Palm-tree.ico", "Whatsapp", menu_options)
systray.start()

while running:
    if i % 20 == 0:
        driver.save_full_page_screenshot("no_shot.png")
        load_chats()
    check_if_got_unread()
    time.sleep(1)
    i += 1
driver.quit()
systray.shutdown()
quit()
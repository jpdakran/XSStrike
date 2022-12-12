from contextlib import contextmanager
import re
import os
import sys

from core.utils import writer
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import UnexpectedAlertPresentException, NoAlertPresentException


@contextmanager
def get_chromedriver():
    chrome_options = Options()
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument("start-maximized")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-browser-side-navigation")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.headless = True
    driver = webdriver.Chrome(options=chrome_options)
    driver.set_page_load_timeout(10)
    try:
        yield driver
    finally:
        driver.quit()


def validate_alert(response):
    with get_chromedriver() as driver:
        response = re.sub(r'<script.*?src=.*?>', '<script src=#>', response, re.I)
        response = re.sub(r'href=.*?>', 'href=#>', response, re.I)
        writer(response, 'test.html')

        driver.get('file://' + sys.path[0] + '/test.html')

        popUp = False
        actions = webdriver.ActionChains(driver)

        try:
            actions.move_by_offset(2, 2)
            actions.move_by_offset(-2, -2)
            actions.perform()
            alert = driver.switch_to.alert.dismiss()
            if alert:
                popUp = True
            else:
                popUp = False
        except UnexpectedAlertPresentException:
            popUp = True
        except NoAlertPresentException:
            popUp = False
        except Exception as e:
            print(e)

        return popUp

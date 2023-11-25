"""Utility module.
"""

from youtube_notification_playlist.common import *

from time import sleep
from retrying import retry
from io import StringIO
from threading import current_thread
from contextlib import contextmanager

import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

import streamlit as st
from streamlit.runtime.scriptrunner.script_run_context import SCRIPT_RUN_CONTEXT_ATTR_NAME


# Reference: https://discuss.streamlit.io/t/cannot-print-the-terminal-output-in-streamlit/6602/9
@contextmanager
def st_redirect(src, dst):
    placeholder = st.empty()
    output_func = getattr(placeholder, dst)

    with StringIO() as buffer:
        old_write = src.write

        def new_write(b):
            if getattr(current_thread(), SCRIPT_RUN_CONTEXT_ATTR_NAME, None):
                buffer.write(b)
                output_func(buffer.getvalue())
            else:
                old_write(b)

        try:
            src.write = new_write
            yield
        finally:
            src.write = old_write

@contextmanager
def st_stdout(dst):
    with st_redirect(sys.stdout, dst):
        yield


def get_chromedriver(url):
    options = uc.ChromeOptions()
    # options.add_argument('--no-sandbox')
    # options.add_argument('--disable-setuid-sandbox')
    # options.add_argument('--headless')
    # options.add_argument('--disable-dev-shm-usage')

    driver = uc.Chrome(options)
    driver.get(url)
    return driver


@retry(wait_fixed=2000)
def submit_text_retry(driver, text, sleep_before=2, sleep_after=0):
    sleep(sleep_before)
    input_element = driver.switch_to.active_element
    input_element.send_keys(text)
    input_element.send_keys(Keys.RETURN)
    sleep(sleep_after)


@retry(wait_fixed=2000)
def click_button_retry(driver, selector, sleep_before=2, sleep_after=0):
    sleep(sleep_before)
    button = driver.find_element(By.CSS_SELECTOR, selector)
    button.click()
    sleep(sleep_after)


@retry(wait_fixed=2000)
def scroll_notifications_retry(driver, idx, sleep_before=1, sleep_after=0):
    sleep(sleep_before)
    driver.execute_script("arguments[0].scrollIntoView();",
                          driver.find_element(By.CSS_SELECTOR, f"#items > ytd-notification-renderer:nth-child({idx})"))
    sleep(sleep_after)


def scroll_notifications(driver, interval=10):
    scroll_notifications_retry(driver, idx=interval)

    idx = interval
    while True:
        try:
            idx += interval
            driver.execute_script("arguments[0].scrollIntoView();", driver.find_element(By.CSS_SELECTOR, f"#items > ytd-notification-renderer:nth-child({idx})"))
            sleep(0.25)
        except NoSuchElementException:
            break

def get_notification_links(driver):
    videos = driver.find_elements(By.CSS_SELECTOR, f"#items > ytd-notification-renderer")
    texts  = [video.find_element(By.CSS_SELECTOR, 'a').text for video in videos]
    links  = [video.find_element(By.CSS_SELECTOR, 'a').get_attribute('href') for video in videos]
    return texts, links

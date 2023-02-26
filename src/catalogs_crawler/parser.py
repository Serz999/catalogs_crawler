import time
from bs4 import BeautifulSoup


def get_catalog(browser, website, page, output):
    # Emulation of user action
    # browser.get(page)
    # cookies_1 = ...
    # cookies_2 = ...
    # cookies_3 = ...
    # browser.add_cookie(cookies_1)
    # browser.add_cookie(cookies_2)
    # browser.add_cookie(cookies_3)

    browser.get(page)
    source_data = browser.page_source

    soup = BeautifulSoup(source_data, 'html.parser')

    pass

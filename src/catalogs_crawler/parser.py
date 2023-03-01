import time
import os
from typing import List, Dict
from bs4 import BeautifulSoup


def get_catalog(browser, site: Dict, initial_page, catalog_name) -> List:
    products = list()

    # TODO
    #   Emulation of user action
    #   browser.get(page)
    #   cookies_1 = ...
    #   cookies_2 = ...
    #   cookies_3 = ...
    #   browser.add_cookie(cookies_1)
    #   browser.add_cookie(cookies_2)
    #   browser.add_cookie(cookies_3)
    #
    # TODO
    #  Buy proxy???

    browser.get(initial_page)
    source = browser.page_source

    html = BeautifulSoup(source, 'html.parser')
    # print(html.text)
    return products



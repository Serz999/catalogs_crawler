import time
import os
from typing import List, Dict
from bs4 import BeautifulSoup
import re
import argparse


def get_catalog(browser, site: Dict, initial_page, catalog_name) -> List:
    products = dict()

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

    pages_nums = html.select(site['css_selectors']['page_num_links'])
    last_page = 0
    if pages_nums:
        last_page = int(pages_nums[-1].text)

    # html-file Parsing loop
    for p in range(1, last_page + 1):
        # Page turning
        if p != 1:
            next_page = ''.join([initial_page, site['site_properties']['getreq_attr'], str(p)])
            browser.get(next_page)
            source = browser.page_source
            pages_nums = html.select(site['css_selectors']['page_num_links'])
            if pages_nums:
                last_page = int(pages_nums[-1].text)

        # Field the array values
        data_products_ids = html.select(site['css_selectors']['data_products_ids'])
        for data_products_id in data_products_ids:
            # key
            k = site['site_properties']['data_product_id']
            key = data_products_id.attrs[k]

            # values
            name = ""
            price = ""
            availability = "false"
            link = ""

            # Name
            expr = f"{site['css_selectors']['divs_select']}[{site['site_properties']['data_product_id']}=\"{key}\"] {site['css_selectors']['names']}"
            name = html.select(expr)[0].text
            # Price
            expr = f"{site['css_selectors']['divs_select']}[{site['site_properties']['data_product_id']}=\"{key}\"] {site['css_selectors']['prices']}"
            price = re.sub('![^0-9]+!', '', html.select(expr)[0].text)
            if price:
                availability = "true"
            # Link
            expr = f"{site['css_selectors']['divs_select']}[{site['site_properties']['data_product_id']}=\"{key}\"] {site['css_selectors']['links']}"
            link = f"{site['domain']}{html.select(expr)[0].attrs['href']}"
            # Push the product
            products[key] = {"name": name, "price": price, "availability": availability, "link": link}
            if products[key]:
                pass
    return products

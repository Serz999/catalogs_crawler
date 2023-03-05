from typing import List, Dict
from bs4 import BeautifulSoup
import re


def get_catalog(browser, site: Dict, initial_page, catalog_name, console=None) -> dict[str, dict[str, str]]:
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
    if console and console.print_mode != 'void':
        print(f"    From page --> {initial_page}")
    browser.get(initial_page)
    source = browser.page_source
    html = BeautifulSoup(source, 'html.parser')

    pages_nums = html.select(site['css_selectors']['page_num_links'])
    last_page = 0
    if pages_nums:
        last_page = int(pages_nums[-1].text)

    # html-file Parsing loop
    n = 0
    for p in range(1, last_page + 1):
        # Page turning
        if p != 1:
            next_page = ''.join([initial_page, site['site_properties']['getreq_attr'], str(p)])
            if console and console.print_mode != 'void':
                print(f"    From page --> {next_page}")
            browser.get(next_page)
            source = browser.page_source
            html = BeautifulSoup(source, 'html.parser')
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
            tags = html.select(expr)
            if tags:
                name = tags[0].text

            # Price
            expr = f"{site['css_selectors']['divs_select']}[{site['site_properties']['data_product_id']}=\"{key}\"] {site['css_selectors']['prices']}"
            tags = html.select(expr)
            if tags:
                price = re.sub('![^0-9]+!', '', tags[0].text)
                if price:
                    availability = "true"

            # Link
            expr = f"{site['css_selectors']['divs_select']}[{site['site_properties']['data_product_id']}=\"{key}\"] {site['css_selectors']['links']}"
            tags = html.select(expr)
            if tags:
                link = f"{site['domain']}{tags[0].attrs['href']}"

            # Push the product
            products[key] = {"name": name, "price": price, "availability": availability, "link": link}
            if console and console.print_mode == 'products':
                print(f"        [{n}] {products[key]}")
            n += 1
    return products

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from sys import argv, platform
import os
import time
import json
from parser import get_catalog
import argparse


def main():
    # TODO
    #   how to invoke modul from ahy places and without interpretaitor name writing in console?
    # TODO
    #   install poetry for wsl
    #   need to wrap code in cli parser
    filename = argv[1]
    with open(filename) as file:
        targets = json.load(file)

    if platform == "linux" or platform == "linux2":
        options = webdriver.ChromeOptions()
        driver = ChromeDriverManager()
        service = Service(driver.install())
    elif platform == "win32":
        options = webdriver.FirefoxOptions()
        driver = GeckoDriverManager()
        service = Service(driver.install())
    options.add_argument("--headless")

    with webdriver.Firefox(service=service, options=options) as browser:
        sites = targets["available"]
        for site in sites:
            print(f"-------------<{site['name']}>-------------\n")
            for link in site["links"]:
                root_page = link["src"]
                catalog_name = link["category"]
                print(get_catalog(browser, site, root_page, catalog_name))


if __name__ == "__main__":
    main()

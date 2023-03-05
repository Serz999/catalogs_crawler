from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from sys import platform
import json
from .parser import get_catalog
import argparse


def main():
    # TODO
    #   how to invoke modul from ahy places and without interpretaitor name writing in console?
    # TODO
    #   install poetry for wsl

    # Cli argument parsing
    cli_parser = argparse.ArgumentParser(description="Web-market catalog crawler")
    cli_parser.add_argument('-i', "--input", dest="filename", type=str, default="targets.json", help="Specify the path to target.json")
    cli_parser.add_argument('-s', "--site", dest="sites_list", type=str, default=None, help="Select specific sites like string: -s \"SITE0, SITE1, SITE2, ...\"")
    cli_parser.add_argument('-o', "--output", dest="output", type=str, default="void", help="Select output way")
    cli_parser.add_argument('-p', "--print", dest="print_mode", type=str, default="void", help="Select output way")
    cli_parser.add_argument('-l', "--list", help="Only show available sites", action="store_true")
    args = cli_parser.parse_args()

    if args.sites_list:
        args.sites_list = args.sites_list.split(", ")

    with open(args.filename) as file:
        targets = json.load(file)

    if args.list:
        print("ALL AVAILABLE TARGETS")
        print("---------------------")
        for site in targets['available']:
            print(f"{site['name']}", end="")
            if site['flag'] != '':
                print(f" : {site['flag']}")
        print("---------------------")
        print("In order to add a new site as a target,\nyou need to enter this in targets.json")
        exit()

    # Check client platform
    if platform == "linux" or platform == "linux2":
        options = webdriver.ChromeOptions()
        driver = ChromeDriverManager()
        service = Service(driver.install())
    elif platform == "win32":
        options = webdriver.FirefoxOptions()
        driver = GeckoDriverManager()
        service = Service(driver.install())
    options.add_argument("--headless")

    # Scrape catalog from targets
    parse_data = dict()
    with webdriver.Firefox(service=service, options=options) as browser:
        sites = targets["available"]
        for site in sites:
            if not args.sites_list or site['name'] in args.sites_list:
                parse_data[site['name']] = dict()
                if args.print_mode != 'void':
                    print(f"-------------<{site['name']}>-------------")
                for link in site["links"]:
                    if args.print_mode != 'void':
                        print(f"Starting to scrape \"{link['category']}\" :")
                    root_page = link["src"]
                    catalog_name = link["category"]
                    parse_data[site['name']][link["category"]] = dict()
                    parse_data[site['name']][link["category"]].update(
                        get_catalog(browser, site, root_page, catalog_name, console=args)
                    )

    # Output parse data
    with open(args.output, 'w') as f:
        f.write(json.dumps(parse_data, indent=4))


if __name__ == "__main__":
    main()

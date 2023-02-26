from selenium import webdriver
import json
from parser import get_catalog


def main():
    # install poetry for wsl
    # need to wrap code in cli parser
    # filename = input()
    with open("../../targets.json") as f:
        targets = json.load(f)

    # if linux os
    # options = webdriver.ChromeOptions()
    # driver_name = "../../chromedriver/chromedriver"
    # if win os
    options = webdriver.FirefoxOptions()
    driver_name = "../../firefoxdriver/geckodriver.exe"
    options.add_argument("--headless")
    browser = webdriver.Firefox(
        executable_path=driver_name,
        options=options
    )
    try:
        sites = targets["available"]
        for site in sites:
            print(f"-------------<{site['name']}>-------------\n")
            for link in site["links"]:
                get_catalog(browser, site, link["src"], link["category"])
    except Exception as ex:
        print(ex)
    finally:
        browser.close()
        browser.quit()


if __name__ == "__main__":
    main()

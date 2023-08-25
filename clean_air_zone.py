
import argparse
import json

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

# https://selenium-python.readthedocs.io/index.html

service = Service()
options = webdriver.ChromeOptions()
options.add_argument("headless")  # don't open a browser window
driver = webdriver.Chrome(service=service, options=options)


def parse_args():
    parser = argparse.ArgumentParser(description="Get clean air zone information from DVLA website",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("reg", help="car registration")
    parser.add_argument("-n", "--nonuk", action="store_true",
                        help="car not registered in the UK")
    return parser.parse_args()


def resolve_url(url):
    try:
        driver.get(url)
    except exceptions.WebDriverException as e:
        exit(f"url could not be resolved\n{e.msg}")


def find_element_by_id(id):
    try:
        return driver.find_element(By.ID, id)
    except exceptions.NoSuchElementException as e:
        exit(f"unable to find element \"{id}\" on page\n{e.msg}")


def remove_span(html):
    soup = BeautifulSoup(html, 'html.parser')
    soup.span.decompose()
    return str(soup)


def main(args):
    resolve_url(
        "https://vehiclecheck.drive-clean-air-zone.service.gov.uk/vehicle_checkers/enter_details")

    try:
        # On page 1, enter the registration...
        vrn = find_element_by_id("vrn")
        vrn.send_keys(args.reg)
        # select if car registered in the UK...
        vrc = find_element_by_id(
            "registration-country-2" if args.nonuk else "registration-country-1")
        vrc.click()
        # and submit
        sub = find_element_by_id("submit_enter_details_button")
        sub.click()
    except exceptions.NoSuchElementException as e:
        exit(f"the page may have changed or registration incorrect\n{e.msg}")

    try:
        # On page 2, confirm details are correct...
        confirm = find_element_by_id("confirm_details-1")
        confirm.click()
        # and submit again
        sub = find_element_by_id("submit_confirm_details_button")
        sub.click()
    except exceptions.NoSuchElementException as e:
        exit(f"the page may have changed\n{e.msg}")

    # On page 3, collect results from table
    table_data = driver.find_element(By.ID, "compliance-table")
    table_data = table_data.get_attribute("innerHTML")

    # Extract rows from table
    table_data = [[cell.text.strip() for cell in row(["td", "th"])]
                  for row in BeautifulSoup(table_data, "html.parser")("tr")]
    # Reduce to first 3 entries in the list
    table_data = [i[:3] for i in table_data]
    # Seperate header and the data
    table_header = table_data[0]
    table_data = table_data[1:]
    # Make form into the following structure {city: {charge:<out>, live:<out>}}
    as_dict = dict()
    for data in table_data:
        city = data[0]
        values = {table_header[e+1]: data[e+1] for e in range(len(data)-1)}
        as_dict.update({city: values})

    print(json.dumps(as_dict, indent=4))
    driver.quit()


if __name__ == "__main__":
    main(parse_args())

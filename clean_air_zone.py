
import json

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

# https://selenium-python.readthedocs.io/index.html


def remove_span(html):
    soup = BeautifulSoup(html, 'html.parser')
    soup.span.decompose()
    return str(soup)


def main():
    service = Service()
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)

    url = "https://vehiclecheck.drive-clean-air-zone.service.gov.uk/vehicle_checkers/enter_details"
    driver.get(url)

    # On page 1, enter the registration...
    vrn = driver.find_element(By.ID, "vrn")
    vrn.send_keys("S211APN")
    # confirm registered in UK (Non-UK: registration-country-2)...
    vrc = driver.find_element(By.ID, "registration-country-1")
    vrc.click()
    # and submit
    sub = driver.find_element(By.ID, "submit_enter_details_button")
    sub.click()

    # On page 2, confirm details are correct...
    confirm = driver.find_element(By.ID, "confirm_details-1")
    confirm.click()
    # and submit again
    sub = driver.find_element(By.ID, "submit_confirm_details_button")
    sub.click()

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
    main()

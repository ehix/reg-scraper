from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

service = Service()
options = webdriver.ChromeOptions()
options.add_argument("headless")
driver = webdriver.Chrome(service=service, options=options)


# def parse_args(**kwargs):
#     parser = argparse.ArgumentParser(description="Get clean air zone information from DVLA website",
#                                      formatter_class=argparse.ArgumentDefaultsHelpFormatter)
#     parser.add_argument("reg", help="car registration")
#     parser.add_argument("-n", "--nonuk", action="store_true",
#                         help="car not registered in the UK")
#     if kwargs:
#         # if called from a script rather than over CLI
#         # Maybe add a field to say it's automated? It's only a Namespace..
#         return parser.parse_args([kwargs.get("reg")])

#     return parser.parse_args()

class PageHandler():
    def __init__(self, args=None):
        self.args = args
        self.route = [self.page_1, self.page_2, self.page_3]
        self.output = None
        self.handle()

    def handle(self):
        for func in self.route:
            # formatted_msg(f"on page {i}")
            try:
                self.output = func(self.args.get(func.__name__))
            except exceptions.NoSuchElementException as e:
                formatted_msg(e.msg)
                break

    def find_element_by_id(self, id, click=False, keys=False):
        try:
            element = driver.find_element(By.ID, id)
            if click:
                element.click()
            elif keys:
                element.send_keys(keys)
            return element
        except exceptions.NoSuchElementException:
            raise

    def page_1(self, args):
        self.find_element_by_id("vrn", keys=args)
        self.find_element_by_id("registration-country-1", click=True)
        self.find_element_by_id("submit_enter_details_button", click=True)

    def page_2(self, args):
        self.find_element_by_id("confirm_details-1", click=True)
        self.find_element_by_id("submit_confirm_details_button", click=True)

    def page_3(self, args):
        table_data = self.find_element_by_id("compliance-table")
        data = table_data.get_attribute("innerHTML")
        return data


def formatted_msg(*messages):
    for m in messages:
        print(f"|-{m}")


def resolve_url(url):
    success = False
    try:
        driver.get(url)
        success = True
    except exceptions.WebDriverException as e:
        formatted_msg("url could not be resolved", e.msg)
    return success


def remove_span(html):
    soup = BeautifulSoup(html, 'html.parser')
    soup.span.decompose()
    return str(soup)


def remove_pay(string):
    return string.replace("\n\npay", "")


def process_table(html):
    # Extract rows from table
    table_data = [[cell.text.strip().lower() for cell in row(["td", "th"])]
                  for row in BeautifulSoup(html, "html.parser")("tr")]
    # Reduce to first 3 entries in the list
    table_data = [i[:3] for i in table_data]
    # Seperate header and the data
    table_header = table_data[0]
    table_data = table_data[1:]
    # Make form into the following structure {city: {charge:<out>, live:<out>}}
    as_dict = {}
    for data in table_data:
        city = data[0]
        values = {
            table_header[e+1]: remove_pay(data[e+1]) for e in range(len(data)-1)}
        as_dict.update({city: values})
    return as_dict


def run(*args):
    print(">", __name__)
    url, reg = args
    return_dict = {__name__: dict()}

    if resolve_url(url):
        ph = PageHandler({"page_1": reg})
        driver.quit()
        if ph.output is not None:
            return_dict.get(__name__).update(process_table(ph.output))

    return return_dict


# if __name__ == "__main__":
#     main(parse_args())

import argparse
import json

import requests
from bs4 import BeautifulSoup


def parse_args():
    parser = argparse.ArgumentParser(description="Get tax information from third party website",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("reg", help="car registration")
    return parser.parse_args()


def striplower(string):
    return string.strip().lower()


def main(args):
    url = f"https://www.honestjohn.co.uk/road-tax/by-vrm/?vrm={args.reg}"
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    specs = soup.find_all("div", {"class": "profile-box"})
    if specs:
        rows = specs[0].select("tr")
        as_dict = dict()
        for e in rows:
            as_dict.update(
                {striplower(e("th")[0].text): striplower(e("td")[0].text)})
        print(json.dumps(as_dict, indent=4))
    else:
        if not page.ok:
            print(f"{page.status_code}: page {page.reason.lower()}")
        else:
            print("reg not found")


if __name__ == "__main__":
    main(parse_args())

import requests
from bs4 import BeautifulSoup


# def parse_args(**kwargs):
#     parser = argparse.ArgumentParser(description="Get tax information from third party website",
#                                      formatter_class=argparse.ArgumentDefaultsHelpFormatter)
#     parser.add_argument("reg", help="car registration")
#     if kwargs:
#         # if called from a script rather than over CLI
#         # Maybe add a field to say it's automated? It's only a Namespace..
#         return parser.parse_args([kwargs.get("reg")])
#     return parser.parse_args()


def striplower(string):
    return string.strip().lower()


def formatted_msg(*messages):
    for m in messages:
        print(f"|-{m}")


def run(*args):
    print(">", __name__)
    url, reg = args
    return_dict = {__name__: dict()}

    page = requests.get(f"{url}?vrm={reg}")
    soup = BeautifulSoup(page.text, "html.parser")
    specs = soup.find_all("div", {"class": "profile-box"})
    if specs:
        rows = specs[0].select("tr")
        for e in rows:
            return_dict.get(__name__).update(
                {striplower(e("th")[0].text): striplower(e("td")[0].text)})
    else:
        if not page.ok:
            formatted_msg(f"{page.status_code}: page {page.reason.lower()}")
        else:
            formatted_msg("registration not found")

    return return_dict

# if __name__ == "__main__":
#     main(parse_args())

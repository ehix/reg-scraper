# reg-scraper
Utility to automate the collection of data to help inform the purchase of a car given its registration.

<h3>clean_air_zone.py</h3>

Uses [`selenium-python`](https://selenium-python.readthedocs.io/index.html) to automate the submission of forms to the [UK Gov website](https://www.gov.uk/clean-air-zones).

Example output:
```json
{
    "bath": {
        "daily charge": "no charge",
        "zone live": "now"
    },
    "birmingham": {
        "daily charge": "\u00a38.00",
        "zone live": "now"
    },
    "bradford": {
        "daily charge": "no charge",
        "zone live": "now"
    },
    "bristol": {
        "daily charge": "\u00a39.00",
        "zone live": "now"
    },
    "greater manchester": {
        "daily charge": "no charge",
        "zone live": "under review"
    },
    "portsmouth": {
        "daily charge": "no charge",
        "zone live": "now"
    },
    "sheffield": {
        "daily charge": "no charge",
        "zone live": "now"
    },
    "tyneside - newcastle and gateshead": {
        "daily charge": "no charge",
        "zone live": "now"
    }
}
```

<h3>vehicle_exise_duty.py</h3>

Scrapes tax data from third party website using `requests`.

Example output:

```json
{
    "fuel": "heavy oil",
    "co2 emissions": "163 g/km",
    "date of registration": "31 mar 2011",
    "ved rate": "band g",
    "annually": "\u00a3240.00",
    "six-monthly": "\u00a3132.00",
    "six-monthly direct debit": "\u00a3126.00",
    "monthly direct debit": "\u00a321.00"
}
```
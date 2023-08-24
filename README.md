# reg-scraper
Utility to automate the collection of data to help inform the purchase of a car given its registration.

<h3>clean_air_zone.py</h3>

Uses [`selenium-python`](https://selenium-python.readthedocs.io/index.html) to automate the submission of forms to the [UK Gov website](https://www.gov.uk/clean-air-zones).

Example output:
```json
{
    "Bath": {
        "Daily charge": "No Charge",
        "Zone live": "Now"
    },
    "Birmingham": {
        "Daily charge": "\u00a38.00\n\nPay",
        "Zone live": "Now"
    },
    "Bradford": {
        "Daily charge": "No Charge",
        "Zone live": "Now"
    },
    "Bristol": {
        "Daily charge": "\u00a39.00\n\nPay",
        "Zone live": "Now"
    },
    "Greater Manchester": {
        "Daily charge": "No Charge",
        "Zone live": "Under review"
    },
    "Portsmouth": {
        "Daily charge": "No Charge",
        "Zone live": "Now"
    },
    "Sheffield": {
        "Daily charge": "No Charge",
        "Zone live": "Now"
    },
    "Tyneside - Newcastle and Gateshead": {
        "Daily charge": "No Charge",
        "Zone live": "Now"
    }
}
```

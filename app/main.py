import logging
import os

import requests
from requests.exceptions import HTTPError

from dotenv import find_dotenv, load_dotenv

from table_manager import TableManager


def get_regions(regions_api: str) -> list:
    """Get regions information"""
    logging.info("Geting regions from API")

    try:
        response = requests.get(
            regions_api,
            headers={
                "x-rapidapi-host": "restcountries-v1.p.rapidapi.com",
                "x-rapidapi-key": os.getenv("X_RAPIDAPI_KEY"),
            },
        )
    except Exception as err:
        logging.error(f"An error occurred:: {http_err}")
        return

    return list(set(map(lambda x: x["region"], response.json())))


def main():
    regions = get_regions(os.getenv("REGIONS_API"))
    logging.info(f"regions: {regions} of type: {type(regions)}")
    TableManager.create_table(regions)


if __name__ == "__main__":
    load_dotenv()
    logging.basicConfig(
        format="%(asctime)s %(levelname)s: %(message)s", level=logging.DEBUG
    )
    main()

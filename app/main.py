import logging
import os

import requests

from dotenv import load_dotenv
from table_manager import TableManager
from integrations.mongo import Mongo
from integrations.auth import Auth


def get_regions(regions_api: str) -> list:
    """Gets regions information"""
    logging.info("Geting regions from API ...")

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
    regions = list(set(map(lambda x: x["region"], response.json())))
    return list(set(filter(None, regions)))


def main():
    mongodb = Mongo()
    table_mng = TableManager()
    auth = Auth()

    regions = get_regions(os.getenv("REGIONS_API"))
    table_mng.create_table(regions)

    auth.get_authorization()
    if not auth.is_authenticated:
        logging.info("User is not authenticated so database can't be shown")
        return

    mongodb.insert_documents(table_mng.table_df)
    mongodb.list_documents()


if __name__ == "__main__":
    load_dotenv()
    logging.basicConfig(
        format="%(asctime)s %(levelname)s: %(message)s", level=logging.INFO
    )
    main()

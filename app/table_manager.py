import logging
import os
import time
import json
import requests
import hashlib
import pandas as pd


class TableManager:
    """ A class to control different operations with tables"""

    def __init__(self):
        self.table_df = pd.DataFrame()

    def get_calculations(self):
        logging.info(f"Max time: {self.table_df.max(axis=0)['time']:0.2f} seconds")
        logging.info(f"Min time: {self.table_df.mean(axis=0)['time']:0.2f} seconds")
        logging.info(f"Mean time: {self.table_df.mean(axis=0)['time']:0.2f} seconds")
        logging.info(f"Total time: {self.table_df.sum(axis=0)['time']:0.2f} seconds")

    def get_country(self, region: list) -> dict:
        try:
            response = requests.get(
                os.getenv("COUNTRIES_API") + region,
                headers={
                    "x-rapidapi-host": "restcountries-v1.p.rapidapi.com",
                    "x-rapidapi-key": os.getenv("X_RAPIDAPI_KEY"),
                },
            )
        except Exception as err:
            logging.error(f"An error occurred:: {err}")
            # maybe raise an error here ?
            return
        return response.json()[0]

    def create_row(self, region: str) -> list:
        s = time.perf_counter()
        country = self.get_country(region)
        language_sha = hashlib.sha1(country["languages"][0].encode())
        elapsed = time.perf_counter() - s
        return {
            "region": region,
            "country": country["name"],
            "language": language_sha.hexdigest(),
            "time": elapsed,
        }

    def create_table(self, regions: list):
        rows = list(map(lambda country: self.create_row(country), regions))
        self.table_df = pd.DataFrame.from_dict(rows)
        self.get_calculations()

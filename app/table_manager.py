import hashlib
import json
import logging
import os
import sqlite3
import time
import json

import requests

import pandas as pd


class TableManager:
    """ A class to manage the creation of tables"""

    def __init__(self):
        self.table_df = pd.DataFrame()

    def write_table_json(self):
        """Writes a json file the table information"""
        table_json = self.table_df.to_json(
            path_or_buf=r"integrations/data.json", orient="records"
        )
        logging.info(f"Json file wrote")

    def save_table(self):
        """Saves DataFrame in a sqlite database"""
        try:
            conn = sqlite3.connect(r"integrations/data.sqlite")
        except sqlite3.OperationalError:
            logging.error(f"An error occurred connecting sqlite db: {err}")
            return
        finally:
            self.table_df.to_sql("data", conn, if_exists="replace", index=False)
            logging.info(f"Table saved in sqlite database")
            conn.close()

    def get_calculations(self):
        """Computes and prints some calculations over the dataframe"""
        logging.info(f"Max time: {self.table_df.max(axis=0)['time']:0.2f} seconds")
        logging.info(f"Min time: {self.table_df.mean(axis=0)['time']:0.2f} seconds")
        logging.info(f"Mean time: {self.table_df.mean(axis=0)['time']:0.2f} seconds")
        logging.info(f"Total time: {self.table_df.sum(axis=0)['time']:0.2f} seconds")

    def get_country(self, region: list) -> dict:
        """Obtains the first country of a region"""
        logging.info(f"Getting country from region: {region} ...")
        try:
            response = requests.get(
                os.getenv("COUNTRIES_API") + region,
                headers={
                    "x-rapidapi-host": "restcountries-v1.p.rapidapi.com",
                    "x-rapidapi-key": os.getenv("X_RAPIDAPI_KEY"),
                },
            )
        except Exception as err:
            logging.error(f"An error occurred: {err}")
            # maybe raise an error here ?
            return
        return response.json()[0]

    def create_row(self, region: str) -> list:
        """Handles the creation of each table row"""
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
        self.save_table()
        self.write_table_json()

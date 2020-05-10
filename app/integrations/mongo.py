import pymongo
import os
import logging
import pandas as pd


class Mongo:
    """A class to handle mongodb operations"""

    def __init__(self):
        try:
            self.client = pymongo.MongoClient(
                "mongodb://db:27017/",
                username=os.getenv("DB_USER"),
                password=os.getenv("DB_PASS"),
            )
            self.db = self.client.regions
        except Exception as e:
            logging.error(f"An error occurred instantiating the mongo db: {e}")
            self.client = None

    def list_databases(self):
        """Lists all databases"""
        databases = self.client.list_database_names()
        logging.info(f"Databases: {databases}")

    def insert_documents(self, table_df: pd.DataFrame):
        """Adds documents to a collection"""
        self.clean_collection()
        self.db.regions_resume.insert_many(table_df.to_dict("records"))

    def clean_collection(self):
        """Cleans a collection if already exists"""
        if "regions_resume" in self.db.list_collection_names():
            self.db.regions_resume.drop()
            logging.info(f"Collection cleaned")

    def list_documents(self):
        """Lists elements in a collection"""
        parameters = {"_id": 0, "region": 1, "country": 1, "language": 1, "time": 1}
        logging.info("SHow collection information")
        df = pd.DataFrame(self.db.regions_resume.find({}, parameters))
        print(df)

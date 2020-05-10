import unittest
import os
import pandas as pd
from table_manager import TableManager
from dotenv import load_dotenv


ROWS = [
    {
        "region": "Americas",
        "country": "Colombia",
        "language": "K34HB34K3434N4J3K43G2F3C2FU2767OPK",
        "time": 0.3453434,
    },
    {
        "region": "Americas",
        "country": "Venezuela",
        "language": "K34HB3DFGHDFN4J3K43G2F3C2FU2767OPK",
        "time": 0.534333,
    },
]


class TestSum(unittest.TestCase):
    """Automatic tests"""

    def setUp(self):
        self.table_mng = TableManager()
        self.table_mng.table_df.from_dict(ROWS)

    def test_write_json(self):
        """
        Test if the file is created properly.When the path is 
        passed as parameter to pands.to_json, the return should be None
        """
        result = self.table_mng.write_table_json()
        self.assertIsNone(result, "Should be a None")
        self.assertEqual(True, os.path.exists(r"../app/integrations/data.json"))

    def test_dataframe_columns(self):
        """Test integrity of columns"""
        self.table_mng.create_table(["Oceania", "Americas"])
        self.assertIn(
            "country",
            self.table_mng.table_df.columns,
            "Country should be a column in df",
        )
        self.assertEqual(self.table_mng.table_df.shape[1], 4, "Should be 4 columns")
        self.assertEqual(
            self.table_mng.table_df.columns.values.tolist(),
            ["region", "country", "language", "time"],
        )


if __name__ == "__main__":
    load_dotenv()
    unittest.main()

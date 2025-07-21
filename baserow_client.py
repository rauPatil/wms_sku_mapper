import requests
import pandas as pd  
import os

from dotenv import load_dotenv
load_dotenv()

class BaserowClient:
    def __init__(self, api_token, database_id, table_ids):
        self.api_token = api_token
        self.database_id = database_id
        self.table_ids = table_ids
        self.api_base = "https://api.baserow.io/api/database"
        self.headers = {
            "Authorization": f"Token {self.api_token}"
        }

    def list_rows(self, table_name):
        table_id = self.table_ids[table_name]
        url = f"{self.api_base}/rows/table/{table_id}/"
        
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()["results"]

    def create_row(self, table_name, data):
        table_id = self.table_ids[table_name]
        url = f"{self.api_base}/rows/table/{table_id}/"
        print(f"Posting to Baserow Table: {table_name} | Data: {data}")  
        response = requests.post(url, headers=self.headers, json=data)
        response.raise_for_status()
        return response.json()

    def update_row(self, table_name, row_id, data):
        table_id = self.table_ids[table_name]
        url = f"{self.api_base}/rows/table/{table_id}/{row_id}/"
        response = requests.patch(url, headers=self.headers, json=data)
        response.raise_for_status()
        return response.json()

    def delete_row(self, table_name, row_id):
        table_id = self.table_ids[table_name]
        url = f"{self.api_base}/rows/table/{table_id}/{row_id}/"
        response = requests.delete(url, headers=self.headers)
        response.raise_for_status()
        return response.status_code == 204

    def get_table_as_dataframe(self, table_name):
        """Returns all rows from the specified table as a pandas DataFrame."""
        rows = self.list_rows(table_name)
        if not rows:
            return pd.DataFrame()
        return pd.DataFrame(rows)
    

# Standalone function moved outside the class
def post_to_baserow(table_id, data):
    token = os.getenv("BASEROW_API_TOKEN")
    url = f"https://api.baserow.io/api/database/rows/table/{table_id}/?user_field_names=true"
    headers = {
        "Authorization": f"Token {token}",
        "Content-Type": "application/json"
    }
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
import os
import requests

class DataDownloader:
    def __init__(self, api_key, base_id, table_name):
        self.api_key = api_key
        self.base_id = base_id
        self.table_name = table_name

    def download_file(self):
        print(self.api_key)
# Importacion de los archivos
import os
from dotenv import load_dotenv

# funcion que hace la importacion
from data.import_download import DataDownloader

# carga de .env
load_dotenv()

def main():
    API_KEY = os.getenv("API_KEY")
    BASE_ID = os.getenv("BASE_ID")
    TABLE_NAME = os.getenv("TABLE_NAME")

    # funcion que hace la importacion
    downloader = DataDownloader(API_KEY, BASE_ID, TABLE_NAME)
    downloader.download_file()

if __name__ == "__main__":
    main()
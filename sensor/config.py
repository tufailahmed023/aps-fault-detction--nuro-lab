import pymongo
import pandas
import json 
import os
from dataclasses import dataclass

@dataclass
class EnviromentVariable:
    mongo_db_url = os.getenv('MONGO_DB_URL')

evr_obj = EnviromentVariable()
mongo_client = pymongo.MongoClient(evr_obj.mongo_db_url)
TARGET_COLUMN = "class"
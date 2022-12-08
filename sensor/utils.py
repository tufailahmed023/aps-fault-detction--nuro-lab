import pandas as pd
from sensor.logger import logging
from sensor.exception import SensorExeception
from sensor.config import mongo_client
import json
import os, sys 
import yaml

def get_dataframe(database_name:str,collection_name:str):
    try:

        logging.info(f"Geting data from database:{database_name} and collection: {collection_name}")
        df = pd.DataFrame(list(mongo_client[database_name][collection_name].find()))
        if '_id' in df.columns:
           logging.info(f"Droping the id colomns")
           df.drop("_id",axis=1,inplace=True)
        logging.info(f"Data Row:{df.shape[0]} and Columns: {df.shape[1]}")
        return df
    except Exception as e :
        raise SensorExeception(e, sys)
       
        
def convert_columns_to_float(df:pd.DataFrame,column_to_exclude:str):
    for col in df.columns:
        if col != column_to_exclude:
            df[col] = df[col].astype("float")
    return df 

def write_yaml_file(filepath,data):
    try:
        file_dir = os.path.dirname(filepath)
        os.makedirs(file_dir,exist_ok = True )
        with open(filepath,'w') as writer:
           yaml.dump(data,writer)
    except Exception as e:
        print(SensorExeception(e, error_details =sys))


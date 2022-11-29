import pymongo
import pandas as pd 
import json

client = pymongo.MongoClient("mongodb://localhost:27017/neurolabDB")

DATABASE = "aps"
COLLECTION = "sensor"

if __name__== "__main__":

    df = pd.read_csv("aps_failure_training_set1.csv")
    df.reset_index(drop=True,inplace=True)

    json_record = list(json.loads(df.T.to_json()).values())
    #print(json_record[0])

    #insert converted json record to mongo db
    client[DATABASE][COLLECTION].insert_many(json_record)



from sensor.logger import logging
from sensor.exception import SensorExeception
import os,sys 

from sensor.utils import get_dataframe
from sensor.entity.config_entity import TrainingPiplineconfig
from sensor.entity.config_entity import DataIngestionInput
from sensor.entity.artifact_entity import DataIngestionOutput
import numpy as np
from sklearn.model_selection import train_test_split

class DataIngestion:

    def  __init__(self,data_ingestion_input:DataIngestionInput):
        try:
           self.data_ingestion_input = data_ingestion_input
        except Exception as e:
            raise SensorExeception(e, error_details = sys)
    
    def initiate_data_ingestion(self):

        try:
            logging.info(f"Geting the data from MongoDb")
            df  = get_dataframe(database_name = self.data_ingestion_input.database_name, collection_name = self.data_ingestion_input.collection_name)

            logging.info("saving the data in feature store")
            df.replace(to_replace="na",value=np.NAN,inplace=True)

            #crating feature store dir of not avaliable
            logging.info("crating feature store dir of not avaliable")

            feature_store_dir = os.path.dirname(self.data_ingestion_input.feature_store_path)
            os.makedirs(feature_store_dir,exist_ok=True)
            logging.info("saving df in feature store")            
            df.to_csv(self.data_ingestion_input.feature_store_path,index=False,header=True)
               
            logging.info("spliting data into test and train")
            train_df,test_df = train_test_split(df,test_size= self.data_ingestion_input.test_size)

            logging.info("creating dir folder if not avaliable")
            dataset_dir = os.path.dirname(self.data_ingestion_input.train_file_path)
            os.makedirs(dataset_dir,exist_ok = True)

            logging.info("saving tarin and test to dataset folder")
            train_df.to_csv(self.data_ingestion_input.train_file_path, index = False, header = True)
            test_df.to_csv(self.data_ingestion_input.test_file_path, index = False, header = True)

            #prepar artifact
            logging.info("preparing artifact")

            data_ingestion_artifact = DataIngestionOutput(file_store_path = self.data_ingestion_input.feature_store_path,
                                                        train_file_path = self.data_ingestion_input.train_file_path,
                                                        test_file_path = self.data_ingestion_input.test_file_path)
            logging.info(f"Data ingestion artifact : {data_ingestion_artifact}")
            return data_ingestion_artifact
        except Exception as e:
            raise SensorExeception(e, error_details = sys)

    


            



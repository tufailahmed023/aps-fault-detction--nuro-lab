import os,sys
from sensor.logger import logging
from sensor.exception import SensorExeception
from datetime import datetime

DATA_FILE_NAME = "sensor.csv"
TRAIN_FILE_NAME = "taining.csv"
TEST_FILE_NAME = "test.csv"

class TrainingPiplineconfig:

    def __init__(self):
        self.artifact_dir = os.path.join(os.getcwd(),"artifact",f"{datetime.now().strftime('%m%d%Y__%H%M%S')}")

class DataIngestionInput:

    def __init__(self,training_pipline_config:TrainingPiplineconfig):
        self.database_name = "aps"
        self.collection_name = "sensor"
        self.data_ingestion_dir = os.path.join(training_pipline_config.artifact_dir,"data_ingestion")
        self.feature_store_path = os.path.join(self.data_ingestion_dir,"feature_store",DATA_FILE_NAME)
        self.train_file_path = os.path.join(self.data_ingestion_dir,"dataset",TRAIN_FILE_NAME)
        self.test_file_path = os.path.join(self.data_ingestion_dir,"dataset",TEST_FILE_NAME)
        self.test_size = 0.2

    def to_dict(self) ->dict:
        try:
            return self.__dict__
        except Exception as e:
            raise SensorExeception(e, error_details = sys)

class DataValidationInput:
    def __init__(self,training_pipline_config:TrainingPiplineconfig):
        self.data_validation_dir = os.path.join(training_pipline_config.artifact_dir,"data_validation")
        self.report_file = os.path.join(self.data_validation_dir,"report_file.ymal")
        self.thersholde = 0.1
        self.base_dataframe_path = "/config/workspace/aps_failure_training_set1.csv"
    
class DataTransformationInput:...
class ModelTrainingInput:...
class ModelPusherInput:...
class ModelEvaluationInput:...
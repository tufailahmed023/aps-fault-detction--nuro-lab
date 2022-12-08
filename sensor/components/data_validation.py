from sensor.logger import logging
from sensor.exception import SensorExeception
import os,sys
from sensor.entity import config_entity, artifact_entity
import pandas as pd
from typing import Optional
from scipy.stats import ks_2samp
from sensor import utils
from sensor.config import TARGET_COLUMN
from sensor.entity.artifact_entity import DataValidationOutput
class DataValidation:
    def __init__(self, data_validation_config:config_entity.DataValidationInput, 
                 data_ingestion_artificat : artifact_entity.DataIngestionOutput):


                try:
                    self.data_validation_config = data_validation_config
                    self.data_ingestion_artificat = data_ingestion_artificat
                    self.thersholde = data_validation_config.thersholde
                    self.validation_erorr = dict()
                except Exception as e:
                    print(SensorExeception(error_message = e, error_details = sys))

    def drop_missing_values(self,df:pd.DataFrame,report_name:str) -> Optional[pd.DataFrame]:
        """ This function will take a data frame path and read the data frame and drop all the columns that have missing values
        persentage grater than thr provided thresholed and return the dataframe if it has atleast one columns else return None

        Args:
            df (pd.DataFrame):Take the  DataFrame
            report_name(str): name of the report 

        Returns:
            df: return DataFrame if it has columns else None
        """
        try:
        
            logging.info("geting all columns missing value persentage")
            missing_values_col = df.isna().sum()/df.shape[0]
            missing_values_col = missing_values_col[missing_values_col > self.thersholde].index

            logging.info(f"droping all columns that dont meet our thresholed : {missing_values_col}")
            self.validation_erorr[report_name] =  missing_values_col 
            df.drop(missing_values_col,axis=1,inplace=True)
            logging.info("checking the length of columns after droping is greater than zero or not ")
            if len(df.columns) > 0:
                logging.info("returing the dataframe")
                return df
            logging.info("returing None as No columns exist")
            return None 

        except Exception as e:
            print(SensorExeception(e, error_details = sys ))


    def columns_check(self,base_dataframe: pd.DataFrame,datafram_to_compare:pd.DataFrame,report_name:str) -> bool:
        """This function will check that wheather all columns in base dataframe and all columns in dataframe to compare are same or not  

        Args:
            base_dataframe (pd.DataFrame): base dataframe
            datafram_to_compare (pd.DataFrame): dataframe to compare 
            report_name(str): take the report name 

        Returns:
            bool: True if all are same , False if not.
        """
        try:
            logging.info("reading both dataframe and getting there columns")
            base_columns = base_dataframe.columns
            datafram_to_compare_columns = datafram_to_compare.columns
            logging.info("checking all columns exist or not")
            missig_columns = []
            for columns in base_columns:
                if columns not in datafram_to_compare_columns:
                    missig_columns.append(columns)
            self.validation_erorr[report_name] = missig_columns
            if len(missig_columns) > 0:
                return False
            return True 
            
        except Exception as e:
            print(SensorExeception(e, error_details = sys))

    def check_distrubtion(self,base_dataframe: pd.DataFrame,datafram_to_compare:pd.DataFrame, report_name:str):
        """This function checks the distrubtion of two DataFrame 

        Args:
            base_dataframe (pd.DataFrame): base dataframe 
            datafram_to_compare (pd.DataFrame): dataframe to compare
            report_name (str): same of the report 
        """
        try:
            columns_disturbtion = dict()

            base_dataframe_columns = list(base_dataframe.columns)

            for column in base_dataframe:
                distrubtion_check = ks_2samp(base_dataframe[column], datafram_to_compare[column])
                logging.info(f"p value of the columns {column} is {float(distrubtion_check.pvalue)}")
                if distrubtion_check.pvalue < 0.5:
                    columns_disturbtion[column] = {"coulmn_name ": str(column),
                                         "p_value": float(distrubtion_check.pvalue),
                                         "status": False}
                else:
                    columns_disturbtion[column] = {"coulmn_name ": str(column),
                                         "p_value": float(distrubtion_check.pvalue),
                                         "status": True}
            self.validation_erorr[report_name] = columns_disturbtion

        except Exception as e:
            print(SensorExeception(e, error_details = sys))

    def initiate_data_validation(self):
        try:

            #Readind the data 
            base_dataframe = pd.read_csv(self.data_validation_config.base_dataframe_path,na_values = "na")
            train_dataframe = pd.read_csv(self.data_ingestion_artificat.train_file_path,na_values = "na")
            test_dataframe = pd.read_csv(self.data_ingestion_artificat.test_file_path,na_values = "na")

            #Column droping
            logging.info("droping columns from base dataframe ")
            base_dataframe = self.drop_missing_values(base_dataframe, report_name = "base_dataframe")
            logging.info("droping columns from train dataframe ")
            train_dataframe = self.drop_missing_values(train_dataframe, report_name = "train_dataframe")
            logging.info("droping columns from test dataframe ")
            test_datframe = self.drop_missing_values(test_dataframe, report_name = "test_dataframe")


            #Converting the all coulmns to Float except the target coulmn
            logging.info("converting columns to float")
            not_to_drop = TARGET_COLUMN
            base_dataframe = utils.convert_columns_to_float(base_dataframe, column_to_exclude = not_to_drop)
            train_dataframe = utils.convert_columns_to_float(train_dataframe, column_to_exclude = not_to_drop)
            test_dataframe = utils.convert_columns_to_float(test_dataframe, column_to_exclude = not_to_drop)



            #checking if all columns are same or not  
            logging.info("starting to check for coloumns ")
            base_with_train = self.columns_check(base_dataframe,train_dataframe,"base and train") 
            base_with_test = self.columns_check(base_dataframe,test_datframe,"base and test")

            #check for data drift
            logging.info("starting the data drift")
            if base_with_train:
                logging.info("checking data drift with train and base data")
                train_data_drift = self.check_distrubtion(base_dataframe=base_dataframe , datafram_to_compare = train_dataframe , report_name = 'train data drift check')
            if base_with_test:
                logging.info("checking data drift with test and base data")
                test_data_drift = self.check_distrubtion(base_dataframe=base_dataframe , datafram_to_compare = test_dataframe , report_name = 'test data drift check')

            #writing the yaml file 
            logging.info("writing the yaml file")
            utils.write_yaml_file(filepath = self.data_validation_config.report_file, data = self.validation_erorr)


            #preparing the artificat
            data_validation_output = DataValidationOutput(yaml_file_path=self.data_validation_config.report_file)
            logging.info(f"data_validation_output:{data_validation_output}")


            return data_validation_output
        except Exception as e:
            print(SensorExeception(e, error_details = sys))

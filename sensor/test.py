from sensor.components.data_ingestion import DataIngestion
from sensor.entity.config_entity import DataIngestionInput,TrainingPiplineconfig
from sensor.components.data_validation import DataValidation
from sensor.entity.config_entity import DataValidationInput
train  = TrainingPiplineconfig()

data = DataIngestionInput(train)
data_ing = DataIngestion(data)
data_inqestion_artifact = data_ing.initiate_data_ingestion()


data2 = DataValidationInput(train)
data_val = DataValidation(data2, data_ingestion_artificat = data_inqestion_artifact )
data_val_artifact = data_val.initiate_data_validation()
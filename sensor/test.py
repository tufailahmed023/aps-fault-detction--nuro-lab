from sensor.components.data_ingestion import DataIngestion
from sensor.entity.config_entity import DataIngestionInput,TrainingPiplineconfig

train  = TrainingPiplineconfig()

data = DataIngestionInput(train)

data_ing = DataIngestion(data)

print(data_ing.initiate_data_ingestion())

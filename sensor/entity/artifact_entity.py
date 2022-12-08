from dataclasses import dataclass

@dataclass
class DataIngestionOutput:
    file_store_path:str
    train_file_path:str
    test_file_path:str
@dataclass
class DataValidationOutput:
    yaml_file_path:str

class DataTransformationOutput:...
class ModelTrainingOutput:...
class ModelPusherOutput:...
class ModelEvaluationOutput:...
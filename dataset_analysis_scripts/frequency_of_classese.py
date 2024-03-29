from utils.dataset_metadata import DatasetMetadata 

class FrequencyOfClassesDatasetCounter:
    def __init__(self, 
                path_to_dataset:str, 
                dataset_name: str, 
                dataset_style: str,
                classes = ['grasper','hook','irrigator','clipper','bipolar','scissors','snare']
                ):
        self.dataset = DatasetMetadata(path_to_dataset=path_to_dataset,
                                          dataset_name=dataset_name,
                                          dataset_style=dataset_style)
        self.dataset_metadata = self.dataset.get_dataset_metadata()
        self.classes = classes
        

    def get_instances(self, distance):
        pass



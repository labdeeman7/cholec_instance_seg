import os
from os.path import join
from utils.dataset_conversion_split_partition import check_if_current_directory_structure_is_as_expected
from static_variables.dataset_variables import CholecInstanceSegVariables

SEQ_TO_SPLIT_DICT = CholecInstanceSegVariables.seq_to_split_dict

class DatasetMetadata: 
    def __init__(self, 
               path_to_dataset:str, 
               dataset_folder_style: str,
               dataset_name: str = 'cholecinstanceseg'):
        """The DatasetMetadata class stores information about a dataset, such as paths and metadata,
        for easy access and utilization by other objects.

        Args:
            path_to_dataset (str): Path to the dataset folder.
            dataset_name (str): Name of the dataset.
            dataset_folder_style (str): Style specification for the dataset. 
                                 Supported styles include dataset_split, dataset_partition, dataset_seqs, standard_mmdetection_form.
                
        """
        self.path_to_dataset = path_to_dataset
        self.dataset_name = dataset_name
        self.dataset_folder_style = dataset_folder_style
        
        ## assert that datasets are as expected
        if self.dataset_folder_style == 'dataset_split':
            check_if_current_directory_structure_is_as_expected(self.path_to_dataset, 'dataset_split', SEQ_TO_SPLIT_DICT)
        elif self.dataset_folder_style == 'dataset_seqs':
            check_if_current_directory_structure_is_as_expected(self.path_to_dataset, 'dataset_seqs', SEQ_TO_SPLIT_DICT)
        elif self.dataset_folder_style == 'dataset_partition':
            check_if_current_directory_structure_is_as_expected(self.path_to_dataset, 'dataset_partition', SEQ_TO_SPLIT_DICT)
        elif self.dataset_folder_style == 'standard_mmdetection_form':
            check_if_current_directory_structure_is_as_expected(self.path_to_dataset, 'standard_mmdetection_form', SEQ_TO_SPLIT_DICT)    
        else:
            raise ValueError('dataset_split, dataset_partition, dataset_seqs, standard_mmdetection_form are supported')   

        self.dataset_metadata = None
        self.supported_dataset_folder_styles = ['dataset_split', 'dataset_partition', 'dataset_seqs', 'standard_mmdetection_form']

        self.generate_dataset_metadata()
    
    ######################################GENERATE DATASET METADATA DEPENDING ON FOLDER STYLE#########################################
    #possible ways to improve, we can allow for people to specify what their image and annotation are?
    def generate_dataset_metadata(self):
        """
        Generate dataset metadata by reading from the filesystem.   
        """
        if self.dataset_folder_style == 'dataset_split':
            self._generate_dataset_meta_data_split_style()
        elif self.dataset_folder_style == 'dataset_partition':   
            self._generate_dataset_meta_data_parition_style()
        elif self.dataset_folder_style == 'standard_mmdetection_form': 
            self._generate_dataset_meta_mmdetection_default_style()
        elif self.dataset_folder_style == 'dataset_seqs':  
            self._generate_dataset_meta_dataset_seqs()   
        else:
            raise ValueError('dataset_split, dataset_partition, dataset_seqs, standard_mmdetection_form are supported')
        
        
        
    def _generate_dataset_meta_dataset_seqs(self):  
        # Filter out only directories
        dataset_metadata = {}
        sequences = [seq for seq in os.listdir(self.path_to_dataset) if os.path.isdir(join(self.path_to_dataset, seq))]    
        for seq in sequences:
            seq_meta_data = []
            img_names = [img_name for img_name in os.listdir(join(self.path_to_dataset, seq, 'img_dir')) 
                                if img_name.split('.')[-1] == 'png']
                                
            for img_name in img_names:
                img_path = join(self.path_to_dataset, seq, 'img_dir', img_name)
                img_path = img_path.replace('\\', '/')
                ann_path =  img_path.replace('img_dir','ann_dir').replace('png', 'json')
                                
                assert os.path.isfile(ann_path), f'there is no annotation for image {img_path}'
                seq_meta_data.append({
                    'img_path': img_path,
                    'ann_path': ann_path 
                })
            
            dataset_metadata[seq] = seq_meta_data
        self.dataset_metadata = dataset_metadata 
        
        
    def _generate_dataset_meta_data_split_style(self):
       
        dataset_metadata = {}
        # Filter out only directories
        splits = [split for split in os.listdir(self.path_to_dataset) if os.path.isdir(join(self.path_to_dataset, split))]
        for split in splits:
            #add the split as keys to the dataset_metadata
            dataset_metadata[split] = {}
            
            sequences = [seq for seq in os.listdir(join(self.path_to_dataset, split)) if os.path.isdir(join(self.path_to_dataset, split, seq))]
            
            for seq in sequences:
                seq_meta_data = []
                img_names = [img_name for img_name in os.listdir(join(self.path_to_dataset, split, seq, 'img_dir')) 
                                    if img_name.split('.')[-1] == 'png']
                                    
                for img_name in img_names:
                    img_path = join(self.path_to_dataset, split, seq, 'img_dir', img_name)
                    img_path = img_path.replace('\\', '/')
                    ann_path =  img_path.replace('img_dir','ann_dir').replace('png', 'json')
                    
                    assert os.path.isfile(ann_path), f'there is no annotation for image {img_path}'
                    seq_meta_data.append({
                        'img_path': img_path,
                        'ann_path': ann_path 
                    })
                
                dataset_metadata[split][seq] = seq_meta_data
        
        self.dataset_metadata = dataset_metadata               
        
    def _generate_dataset_meta_data_parition_style(self):
        dataset_metadata = {}
        # Filter out only directories
        partitions = [split for split in os.listdir(self.path_to_dataset) if os.path.isdir(join(self.path_to_dataset, split))]
        for partition in partitions:
            #add the split as keys to the dataset_metadata
            dataset_metadata[partition] = {}
            
            sequences = [seq for seq in os.listdir(join(self.path_to_dataset, partition)) if os.path.isdir(join(self.path_to_dataset, partition, seq))]
            
            for seq in sequences:
                seq_meta_data = []
                img_names = [img_name for img_name in os.listdir(join(self.path_to_dataset, partition, seq, 'img_dir')) 
                                    if img_name.split('.')[-1] == 'png']
                                    
                for img_name in img_names:
                    img_path = join(self.path_to_dataset, partition, seq, 'img_dir', img_name)
                    img_path = img_path.replace('\\', '/')
                    ann_path =  img_path.replace('img_dir','ann_dir').replace('png', 'json')
                    
                    assert os.path.isfile(ann_path), f'there is no annotation for image {img_path}'
                    seq_meta_data.append({
                        'img_path': img_path,
                        'ann_path': ann_path 
                    })
                
                dataset_metadata[partition][seq] = seq_meta_data
            
        self.dataset_metadata = dataset_metadata     
            
    def _generate_dataset_meta_mmdetection_default_style(self):
        dataset_metadata = {
            'dataset_name': self.dataset_name,
            'img_and_annotation_paths': []
        }
        
        img_names = [img_name for img_name in os.listdir(join(self.path_to_dataset, self.dataset_name, 'img_dir')) 
                                    if img_name.split('.')[-1] == 'png']
        img_and_annotation_paths = []                            
        for img_name in img_names:
            img_path = join(self.path_to_dataset, self.dataset_name, 'img_dir', img_name)
            img_path = img_path.replace('\\', '/')
            ann_path =  img_path.replace('img_dir','ann_dir').replace('png', 'json')
            
            assert os.path.isfile(ann_path), f'there is no annotation for image {img_path}'
            img_and_annotation_paths.append({
                'img_path': img_path,
                'ann_path': ann_path 
            })  
        dataset_metadata['img_and_annotation_paths'] = img_and_annotation_paths
     
    ######################################GET DATASET METADATA #########################################
        
    def get_dataset_metadata(self, required_style=None):
        """Gets the metadata for a given style. 

        Args:
            required_style (str): this is the style the dataset can be in options are split_style, partition_style, mmdetection_default_style, single_folder_style
            We use the conversion functions to convert from style to style.
        Returns:
            dataset_metadata: dict of the metadata in the supported style
        """ 
        if not required_style:
            required_style = self.dataset_folder_style
             
        if required_style == self.dataset_folder_style:
            return self.dataset_metadata
        else:
            assert required_style in self.supported_dataset_folder_styles, 'the value of required style is wrong, and not supported' 
            converted_dataset_meta_data = self._get_converted_dataset_metadata(required_style)
            return converted_dataset_meta_data
    
    
    ###################################### CONVERSION FROM ONE DATASET STYLE TO OTHER DATASET STYLES#########################################
    # def _get_converted_dataset_metadata(self, required_style):
    #     raise ValueError('Not yet implemented Requires 4 different functions') 
    
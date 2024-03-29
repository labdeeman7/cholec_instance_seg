import os
from os.path import join

class DatasetMetadata: 
    def __init__(self, 
               path_to_dataset:str, 
               dataset_name: str, 
               dataset_style: str):
        """The DatasetMetadata class stores information about a dataset, such as paths and metadata,
        for easy access and utilization by other objects.

        Args:
            path_to_dataset (str): Path to the dataset folder.
            dataset_name (str): Name of the dataset.
            dataset_style (str): Style specification for the dataset. 
                                 Supported styles include split_seq_img_dir-ann_dir.
                                 Future styles may include split_img_dir-ann_dir, 
                                 img_dir-ann_dir_split, and custom folder names.
                
        """
        self.path_to_dataset = path_to_dataset
        self.dataset_name = dataset_name
        self.dataset_style = dataset_style
        
        self.dataset_metadata = None
        
        self.generate_dataset_metadata()
    
    #possible ways to improve, we can allow for people to specify what their image and annotation are?
    def generate_dataset_metadata(self):
        """Generate dataset metadata by reading from the filesystem.
        
        for split_seq_img_dir-ann_dir
        
        dataset_metadata = {
            train: {
                seq_1: [
                    {
                        img_path: img_path
                        img_path: ann_path
                    },...
                ]
                
            }
        }
        
        """
        
        dataset_metadata = {}
        if self.dataset_style == 'split_seq_img_dir-ann_dir':
            
            # Filter out only directories
            splits = [split for split in os.listdir(self.path_to_dataset) if os.path.isdir(join(self.path_to_dataset, split))]
   
            for split in splits:
                #add the split as keys to the dataset_metadata
                dataset_metadata[split] = {}
                
                sequences = [seq for seq in os.listdir(join(self.path_to_dataset, split)) if os.path.isdir(join(self.path_to_dataset, split, seq))]
                
                for seq in sequences:
                    #add the sequence to the dataset_metadata as keys for that split
  
                    seq_meta_data = []
                    img_names = [img_name for img_name in os.listdir(join(self.path_to_dataset, split, seq, 'img_dir')) 
                                       if img_name.split('.')[-1] == 'png']
                                        
                    for img_name in img_names:
                        img_path = join(self.path_to_dataset, split, seq, 'img_dir', img_name)
                        ann_path =  img_path.replace('img_dir','ann_dir').replace('png', 'json')
                        
                        
                        img_path = img_path.replace('\\', '/')
                        ann_path = ann_path.replace('\\', '/')
                        
                        assert os.path.isfile(ann_path), f'there is no annotation for image {img_path}'
                        seq_meta_data.append({
                            'img_path': img_path,
                            'ann_path': ann_path 
                        })
                    
                    dataset_metadata[split][seq] = seq_meta_data   
        
            self.dataset_metadata = dataset_metadata
            
        else:
            raise ValueError('only split_seq_img_dir-ann_dir is currently supported')

        
    def get_dataset_metadata(self): 
        return self.dataset_metadata 
    

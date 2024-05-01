def ensure_dataset_size_is_correct(path_to_dataset,
                                   dataset_name = 'instance_cholec',
                                   dataset_style = 'split_seq_img_dir-ann_dir'):
    
    from utils.dataset_metadata import DatasetMetadata    
    from dataset_analysis_scripts.count_files import count_sizes_in_my_dataset  
    from static_variables.dataset_variables import CholecInstanceSegVariables 
    
    dataset_size = CholecInstanceSegVariables.dataset_size
    
    
    dataset = DatasetMetadata(path_to_dataset=path_to_dataset,
                            dataset_name=dataset_name,
                            dataset_style=dataset_style)
    
    dataset_metadata = dataset.get_dataset_metadata()
    total_count = count_sizes_in_my_dataset(dataset_metadata)
    
    if total_count == dataset_size:
        print('total count of the dataset matches with the dataset size')
    else: 
        raise ValueError('there is a major error, total count of dataset does not match with dataset size')   
                 
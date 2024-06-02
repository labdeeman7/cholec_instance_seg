import os
from os.path import join
import numpy as np

def get_seq_folder_from_ann_name(dataset_dir,
                                ann_name):
    
    if ann_name[:5] == 'seg8k': #handle seg8k
        ann_seq_num = ann_name[11:13]        
        for split in os.listdir(dataset_dir):
            split_path = join(dataset_dir, split)
            for seq_name in os.listdir(split_path):
                seq_num = seq_name[3:5]
                if ann_seq_num == seq_num:
                    return join(dataset_dir, split, seq_name)
        
    else:    
        seq_name = ann_name.split('_')[1]
        dataset_partition = ann_name.split('_')[0]
        
        seq_name_dataset_partition = f'{seq_name}_{dataset_partition}'
        
        #get the seq_names in dataset_dir
        
        for split in os.listdir(dataset_dir):
            split_path = join(dataset_dir, split)
            for seq_name in os.listdir(split_path):
                if seq_name_dataset_partition in seq_name:
                    return join(dataset_dir, split, seq_name)
                

def get_unique_class_and_instance_id_in_ann(ann: np.array) -> np.array:
    """return the unique [class_id, instance_ids] in an annotation array

    Args:
        ann (np.array): annotation array of HxWx2

    Returns:
        np.array: unique class_id, instance_ids
    """    
    reshaped_ann = ann.reshape(-1, 2)
    unique_class_id_instance_id = np.unique(reshaped_ann, axis=0)
    
    #find non_zero rows, remove background 
    non_zero_rows = np.all(unique_class_id_instance_id != 0, axis=1)

    # Filter the array to keep only rows with non-zero values
    unique_class_id_instance_id = unique_class_id_instance_id[non_zero_rows]
    
    return unique_class_id_instance_id                
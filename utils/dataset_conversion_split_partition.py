import os
from os.path import join
import shutil

##################################conversion utils############################################
def generate_split_to_seq_dict(seq_to_split_dict):
    split_to_seq_dict = {} 
    for key, value in  seq_to_split_dict.items():
        if value in split_to_seq_dict:
            split_to_seq_dict[value].append(key)  
        else:
            split_to_seq_dict[value] = [key]   
    return split_to_seq_dict


def check_if_current_directory_structure_is_as_expected(dataset_dir, style, seq_to_split_dict):
    if style == 'dataset_split':
        split_to_seq_dict = generate_split_to_seq_dict(seq_to_split_dict)
        current_dataset_dir  = os.listdir(dataset_dir)
        expected_dataset_dirs = ['test', 'train', 'val']
        assert set(expected_dataset_dirs) <= set(current_dataset_dir), "The dataset directory does not contain exactly train, test, val"  
            
        ## assert that splits contains the correct sequences.
        for split, seqs in split_to_seq_dict.items():
            seqs_in_split = os.listdir(join(dataset_dir, split))
            for seq in seqs:
                assert seq in seqs_in_split,  f'{seq} is missing from the {split} split of the dataset'  
        
        print('all sequences can be found') 
    elif style == 'dataset_partition':
        from collections import Counter
        current_dataset_dir  = os.listdir(dataset_dir)
        expected_dataset_dirs = ['Instance_CholecSeg8k', 'Instance_CholecT50_full', 'Instance_CholecT50_sparse', 'Instance_Cholec80_sparse']
        assert set(expected_dataset_dirs) <= set(current_dataset_dir), "The dataset directory does not contain Instance_CholecSeg8k, Instance_CholecT50_full, Instance_CholecT50_sparse, and Instance_Cholec80_sparse"
            
        ## assert that dataset partitions contains the correct sequences.
        Instance_CholecSeg8k_seqs = os.listdir(join(dataset_dir,'Instance_CholecSeg8k'))
        Instance_CholecT50_full_seqs = os.listdir(join(dataset_dir,'Instance_CholecT50_full'))
        Instance_CholecT50_sparse_seqs = os.listdir(join(dataset_dir,'Instance_CholecT50_sparse'))
        Instance_Cholec80_sparse_seqs = os.listdir(join(dataset_dir,'Instance_Cholec80_sparse'))
        
        for seq in seq_to_split_dict.keys():
            partition_name = seq.split('_')[-1]
            if partition_name == 'full':
                assert seq in Instance_CholecT50_full_seqs,  f'{seq} is missing from the Instance_CholecT50_full partition of the dataset'  
            elif partition_name == 'seg8k':
                assert seq in Instance_CholecSeg8k_seqs,  f'{seq} is missing from the Instance_CholecSeg8k partition of the dataset'
            elif partition_name == 'sparse':
                if seq.split('_')[-2]  == 't50':
                    assert seq in Instance_CholecT50_sparse_seqs,  f'{seq} is missing from the Instance_CholecT50_sparse partition of the dataset'    
                elif seq.split('_')[-2]  == 't80':  
                    assert seq in Instance_Cholec80_sparse_seqs,  f'{seq} is missing from the Instance_Cholec80_sparse_seqs partition of the dataset' 
                else:
                    raise ValueError(f'{seq} is an unknown folder')     
            else:
                raise ValueError(f'something is wrong with seq_to_split_dict, {seq} is not accounted for')  
    
        print('all sequences can be found')
    elif style == 'dataset_seqs':
        ## assert that all the folders are present
        expected_seq_folders = list(seq_to_split_dict.keys())
        current_dataset_dir  = os.listdir(dataset_dir) #store before adding new directories 
        assert set(expected_seq_folders) <= set(current_dataset_dir), f'the dataset dir does not match with what is expected - {set(expected_seq_folders) ^ set(current_dataset_dir)}'
    elif style ==   'standard_mmdetection_form':   
        current_dataset_dir  = os.listdir(dataset_dir)
        expected_dataset_dirs = ['test', 'train', 'val']
        assert set(expected_dataset_dirs) <= set(current_dataset_dir), "The dataset directory does not contain exactly train, test, val"  
            
        ## assert that splits contains the correct sequences.
        for split in expected_dataset_dirs:
            current_split_subfolders  = os.listdir(join(dataset_dir, split))
            expected_split_subfolders = ['img_dir', 'ann_dir']
            assert set(expected_split_subfolders) <= set(current_split_subfolders),  f'the {split} dir is missing - {set(expected_seq_folders) ^ set(current_dataset_dir)}'
        
        print('all folders can be found')
    
    return 
    
def get_folder_name_from_file_name_and_sparse_or_full_dict(filename, sparse_or_full_dict):
    if filename.split('.')[0].split('_')[0] == 'seg8k':
        seq_id = filename.split('.')[0].split('_')[1][5:]
        seq_folder_name = f'VID{seq_id}_seg8k'
    elif filename.split('.')[0].split('_')[0] == 't50':
        seq_folder_name_without_partition = filename.split('.')[0].split('_')[1]
        partition = sparse_or_full_dict[seq_folder_name_without_partition]
        seq_folder_name = f'{seq_folder_name_without_partition}_t50_{partition}'
    elif filename.split('.')[0].split('_')[0] == 't80':
        seq_folder_name_without_partition = filename.split('.')[0].split('_')[1]
        partition = sparse_or_full_dict[seq_folder_name_without_partition]
        seq_folder_name = f'{seq_folder_name_without_partition}_t80_{partition}'       
    else:
        raise ValueError('there is an issue with this logic')     
    
    return seq_folder_name    

def generate_sparse_or_full_dict(seq_to_split_dict):
    sparse_or_full_dict = {}
    for seq in seq_to_split_dict.keys():
        partition = seq.split('_')[-1]
        seq_name_without_partition = seq.split('_')[0]
        if partition == 'seg8k':
            continue
        elif partition == 'full':
            sparse_or_full_dict[seq_name_without_partition] = 'full'
        elif partition == 'sparse':
            sparse_or_full_dict[seq_name_without_partition] = 'sparse'  
    
    return sparse_or_full_dict

# Function to create directory if not exists
def check_if_dir_exists_if_not_create_it(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

# Move images and annotations to their respective sequence folders
def move_files_to_seq_folder(target_dir, source_dir, file_type, sparse_or_full_dict):
    for file_name in os.listdir(source_dir):
        # Determine the sequence folder from the file name
        seq_folder_name = get_folder_name_from_file_name_and_sparse_or_full_dict(file_name, sparse_or_full_dict)
        # print(file_name)
        # print(seq_folder_name)
        target_seq_folder_path = os.path.join(target_dir, seq_folder_name)
        
        # Ensure the sequence folder exists
        check_if_dir_exists_if_not_create_it(target_seq_folder_path)
        
        # Ensure img_dir and ann_dir exists inside the sequence folder
        if file_type == 'img':
            target_subfolder = 'img_dir'
        else:
            target_subfolder = 'ann_dir'
        
        target_img_or_ann_folder_path = os.path.join(target_seq_folder_path, target_subfolder)
        check_if_dir_exists_if_not_create_it(target_img_or_ann_folder_path)
        
        # Move the file
        shutil.move(os.path.join(source_dir, file_name), os.path.join(target_img_or_ann_folder_path, file_name))
    
    os.rmdir(source_dir) #remove the img_dir and ann_dir
    return
    
##################################conversions#############################################
def dataset_split_to_dataset_partition(dataset_dir, seq_to_split_dict):  
    #check current folder structure is correct
    check_if_current_directory_structure_is_as_expected(dataset_dir, 'dataset_split', seq_to_split_dict)   
    
    #get the list of directories before creating 
    current_dataset_dir  = os.listdir(dataset_dir)         

    ## create the new folders. 
    Instance_CholecSeg8k_path = join(dataset_dir, 'Instance_CholecSeg8k')
    Instance_CholecT50_full_path = join(dataset_dir, 'Instance_CholecT50_full')
    Instance_CholecT50_sparse_path = join(dataset_dir, 'Instance_CholecT50_sparse') 
    Instance_Cholec80_sparse_path = join(dataset_dir, 'Instance_Cholec80_sparse')  
      
    os.makedirs(Instance_CholecSeg8k_path)
    os.makedirs(Instance_CholecT50_full_path) 
    os.makedirs(Instance_CholecT50_sparse_path)  
    os.makedirs(Instance_Cholec80_sparse_path)           

    ## move files
                   
    for split in current_dataset_dir:
        if os.path.isdir(join(dataset_dir, split)):
            for seq in os.listdir(join(dataset_dir, split)):
                partition_name = seq.split('_')[-1] 
                seq_path = join(dataset_dir, split, seq)
                if partition_name == 'full':
                    shutil.move(seq_path, Instance_CholecT50_full_path)
                elif partition_name == 'seg8k':
                    shutil.move(seq_path, Instance_CholecSeg8k_path)    
                elif partition_name == 'sparse':
                    if seq.split('_')[-2]  == 't50':
                        shutil.move(seq_path, Instance_CholecT50_sparse_path)   
                    elif seq.split('_')[-2]  == 't80':  
                        shutil.move(seq_path, Instance_Cholec80_sparse_path)  
                    else:
                        raise ValueError(f'{seq} in {split} is an unknown folder')         
                else:
                    raise ValueError(f'{seq} in {split} is an unknown folder')      
            os.rmdir(join(dataset_dir, split))      
    
    print('dataset_split_to_dataset_partition completed')

def dataset_partition_to_dataset_split(dataset_dir, seq_to_split_dict):
    #check current folder structure is correct
    check_if_current_directory_structure_is_as_expected(dataset_dir, 'dataset_partition', seq_to_split_dict)
    
    #get the list of directories before creating 
    current_dataset_dir  = os.listdir(dataset_dir)  
    
    ## create the new folders. 
    train_path = join(dataset_dir, 'train')
    test_path = join(dataset_dir, 'test')
    val_path = join(dataset_dir, 'val')    
    os.makedirs(train_path)
    os.makedirs(test_path) 
    os.makedirs(val_path)        
    
    #move files
    for partition in current_dataset_dir:
        if os.path.isdir(join(dataset_dir, partition)):
            for seq in os.listdir(join(dataset_dir, partition)):
                split = seq_to_split_dict[seq]
                seq_path = join(dataset_dir, partition, seq)
                
                if split == 'train':
                    shutil.move(seq_path, train_path)
                elif split == 'test':
                    shutil.move(seq_path, test_path)    
                elif split == 'val':
                    shutil.move(seq_path, val_path)       
                else:
                    raise ValueError(f'{seq} in {partition} is an unknown file')    
                
            os.rmdir(join(dataset_dir, partition))  
            
    print('dataset_partition_to_dataset_split completed')
    
def dataset_partition_to_dataset_seqs(dataset_dir, seq_to_split_dict):
    #check current folder structure is correct
    check_if_current_directory_structure_is_as_expected(dataset_dir, 'dataset_partition', seq_to_split_dict) 
        
    #move files
    current_dataset_dir  = os.listdir(dataset_dir)
    for partition in current_dataset_dir:
        if os.path.isdir(join(dataset_dir, partition)):
            for seq in os.listdir(join(dataset_dir, partition)):
                seq_path = join(dataset_dir, partition, seq)
                shutil.move(seq_path, dataset_dir)    
            os.rmdir(join(dataset_dir, partition))      
    
    print('dataset_partition_to_single_folder completed')
                
def dataset_seqs_to_dataset_partition(dataset_dir, seq_to_split_dict): 
    #check current folder structure is correct
    check_if_current_directory_structure_is_as_expected(dataset_dir, 'dataset_seqs', seq_to_split_dict) 
    
    current_dataset_dir  = os.listdir(dataset_dir) #store before adding new directories
    
    ## create the new folders. 
    instance_cholecseg8k_path = join(dataset_dir, 'Instance_CholecSeg8k')
    instance_cholect50_full_path = join(dataset_dir, 'Instance_CholecT50_full')
    instance_cholect50_sparse_path = join(dataset_dir, 'Instance_CholecT50_sparse')
    Instance_Cholec80_sparse_path = join(dataset_dir, 'Instance_Cholec80_sparse')    

    os.makedirs(instance_cholecseg8k_path)
    os.makedirs(instance_cholect50_full_path) 
    os.makedirs(instance_cholect50_sparse_path)
    os.makedirs(Instance_Cholec80_sparse_path)
    
    #move files
    for seq in current_dataset_dir:        
        partition_name = seq.split('_')[-1]
        seq_path = join(dataset_dir, seq)
        if partition_name == 'full':
            shutil.move(seq_path, instance_cholect50_full_path)  
        elif partition_name == 'seg8k':
            shutil.move(seq_path, instance_cholecseg8k_path)  
        elif partition_name == 'sparse':
            if seq.split('_')[-2]  == 't50':
                shutil.move(seq_path, instance_cholect50_sparse_path)  
            elif seq.split('_')[-2]  == 't80':  
                shutil.move(seq_path, Instance_Cholec80_sparse_path)
        else:
            raise ValueError(f'something is wrong with the static variable that generated seq_to_split_dict, {seq} is not accounted for')  
           
    print('dataset_seqs_to_dataset_partition completed')        
    
def dataset_seqs_to_dataset_split(dataset_dir, seq_to_split_dict):
    #check current folder structure is correct
    check_if_current_directory_structure_is_as_expected(dataset_dir, 'dataset_seqs', seq_to_split_dict)
    
    ## create the new folders. 
    train_path = join(dataset_dir, 'train')
    test_path = join(dataset_dir, 'test')
    val_path = join(dataset_dir, 'val')    
    os.makedirs(train_path)
    os.makedirs(test_path) 
    os.makedirs(val_path)    
    
    for seq, split in  seq_to_split_dict.items():
        seq_path = join(dataset_dir, seq)
        shutil.move(seq_path, join(dataset_dir, split)) 
    
    print('dataset_seqs_to_dataset_split completed')                
    
def dataset_split_to_dataset_seqs(dataset_dir, seq_to_split_dict): 
    check_if_current_directory_structure_is_as_expected(dataset_dir, 'dataset_split', seq_to_split_dict)        
    ## move files
    current_dataset_dir  = os.listdir(dataset_dir)  
    
    for split in current_dataset_dir:
        if os.path.isdir(join(dataset_dir, split)):
            for seq in os.listdir(join(dataset_dir, split)):
                seq_path = join(dataset_dir, split, seq)
                shutil.move(seq_path, dataset_dir)    
            os.rmdir(join(dataset_dir, split)) 
            
    print('dataset_split_to_single_folder completed')            

def dataset_split_to_standard_mmdetection_form(dataset_dir, seq_to_split_dict):
    #check current folder structure is correct
    check_if_current_directory_structure_is_as_expected(dataset_dir, 'dataset_split', seq_to_split_dict)
    
    # Loop through each folder in the dataset directory
    current_dataset_dir  = os.listdir(dataset_dir)
    for split_folder in current_dataset_dir:
        split_folder_path = os.path.join(dataset_dir, split_folder)
        
        # Check if it is a directory and not the target directory or any other file
        if os.path.isdir(split_folder_path):
            os.makedirs(os.path.join(split_folder_path, 'img_dir'), exist_ok=True)
            os.makedirs(os.path.join(split_folder_path, 'ann_dir'), exist_ok=True)
            
            target_img_dir_path = os.path.join(split_folder_path, 'img_dir')
            target_ann_dir_path = os.path.join(split_folder_path, 'ann_dir')
            
            # for each sequence in the split folders get the seq folders
            for seq_folder in os.listdir(split_folder_path):
                seq_folder_path = os.path.join(split_folder_path, seq_folder)
                if os.path.isdir(split_folder_path) and seq_folder not in ['img_dir', 'ann_dir']:
                    source_img_dir_path = os.path.join(seq_folder_path, 'img_dir')
                    source_ann_dir_path = os.path.join(seq_folder_path, 'ann_dir')
                                   
                    if os.path.exists(source_img_dir_path):
                        for img_file in os.listdir(source_img_dir_path):
                            shutil.move(os.path.join(source_img_dir_path, img_file),
                                        os.path.join(target_img_dir_path, img_file))
                    
                    # Move each annotation file
                    if os.path.exists(source_ann_dir_path):
                        for ann_file in os.listdir(source_ann_dir_path):
                            shutil.move(os.path.join(source_ann_dir_path, ann_file),
                                        os.path.join(target_ann_dir_path, ann_file))
    
    #remove seq_folders
    for split_folder in current_dataset_dir:
        split_folder_path = os.path.join(dataset_dir, split_folder)
        if os.path.isdir(split_folder_path):
            for seq_folder in os.listdir(split_folder_path):
                seq_folder_path = os.path.join(split_folder_path, seq_folder) 
                if os.path.isdir(seq_folder_path) and seq_folder not in ['img_dir', 'ann_dir']:
                    os.rmdir(join(seq_folder_path,  'img_dir'))
                    os.rmdir(join(seq_folder_path,  'ann_dir')) 
                    os.rmdir(join(seq_folder_path))                 

    print("Files have been successfully moved.")
    
def standard_mmdetection_form_to_dataset_seqs(dataset_dir, seq_to_split_dict):
    ##Check structure
    check_if_current_directory_structure_is_as_expected(dataset_dir, 'standard_mmdetection_form', seq_to_split_dict) 
    
    sparse_or_full_dict = generate_sparse_or_full_dict(seq_to_split_dict)
    for split in os.listdir(dataset_dir):
        split_dir = join(dataset_dir, split)
        if os.path.isdir(split_dir):
            split_img_dir = join(split_dir, 'img_dir')
            split_ann_dir = join(split_dir, 'ann_dir')

            # Process image files
            move_files_to_seq_folder(dataset_dir, split_img_dir, 'img', sparse_or_full_dict)

            # Process annotation files
            move_files_to_seq_folder(dataset_dir, split_ann_dir, 'ann', sparse_or_full_dict)
    
            os.rmdir(split_dir)

    print("Files have been successfully reorganized into sequence folders.")
    return    

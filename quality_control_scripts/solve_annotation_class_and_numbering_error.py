from utils.read_files import read_from_json
import os
from os.path import join
import shutil
from quality_control_scripts.quality_control_utils import ensure_dataset_size_is_correct, get_seq_folder_from_ann_name

## todo improve quality control to use metadata. code breaks if I change my dataset structure. with metadata code does not break if I make these changes. 


def check_start_at_one(lst):
    if len(lst) > 0:
        if lst[0] != 1:
            return False
        
    return True
    
def check_ascending(lst):  
    # Check if the list is in ascending order
    if len(lst) > 1: 
        for i in range(1, len(lst)):
            if lst[i] - lst[i - 1] > 1:
                return False 
    return True    


     

#get the files in the dataset that have errors in them sequence per sequence. 
def get_ann_with_annotation_class_and_numbering_errors_in_seq_dir(seq_dir: str,
                        class_names = ['grasper', 'hook', 'irrigator', 'clipper', 'bipolar', 'scissors', 'snare'],
                        log_dir: str = 'logs/annotation_class_and_numbering_errors_in_seq_dir'):
    
    ann_with_annotation_class_and_numbering_errors_in_seq = []
    seq_name = seq_dir.split('/')[-1]
    split = seq_dir.split('/')[-2]
    
    ann_dir = join(seq_dir, 'ann_dir')
    
    annotation_class_and_numbering_errors_in_seq_dir_text_file = join(log_dir, f'{split}_{seq_name}.txt')
    
    json_annotations_list = sorted([ filename for filename in os.listdir(ann_dir) if filename.endswith('.json')])
    json_file_paths =  [join(ann_dir, json_filename ) for json_filename in json_annotations_list] 
    
    with open(annotation_class_and_numbering_errors_in_seq_dir_text_file, "a") as file:        
        for json_file_path in json_file_paths:

            json_info = read_from_json(json_file_path)
            contour_info =  json_info['shapes']
            labels = [contour['label'] for contour in contour_info]
            instance_ids = [contour['group_id'] for contour in contour_info]  
            instance_ids_for_all_classes = []
            total_amount_of_ids_for_class_names = 0
            
            for class_name in class_names:
                instance_ids_for_class  = sorted([instance_ids[i] for i,x in enumerate(labels) if x == class_name])
                total_amount_of_ids_for_class_names += len(instance_ids_for_class)
                
                instance_ids_for_all_classes.append(instance_ids_for_class)
            
            test_cases = []    
            test_if_the_class_names_are_correct = len(instance_ids) ==  total_amount_of_ids_for_class_names  
            test_cases.append(test_if_the_class_names_are_correct)
            test_if_the_instance_ids_start_from_one = [check_start_at_one(instance_ids_for_class) for instance_ids_for_class in  instance_ids_for_all_classes]
            test_cases.extend(test_if_the_instance_ids_start_from_one)
            test_if_the_instance_ids_are_ascending = [check_ascending(instance_ids_for_class) for instance_ids_for_class in  instance_ids_for_all_classes]
            test_cases.extend(test_if_the_instance_ids_are_ascending)
            
            if all(test_cases):
                print(f'{os.path.basename(json_file_path)} passes assertion tests')
            else:
                ann_with_annotation_class_and_numbering_errors_in_seq.append(json_file_path)
                
                file.write( '====================================================\n' )
                file.write(f'{os.path.basename(json_file_path)} failed assertion test \n')         
                file.write(f'test_if_the_class_names_are_correct {test_if_the_class_names_are_correct} \n')
                
                for i, instance_ids_for_class in enumerate(instance_ids_for_all_classes):
                    class_name = class_names[i]
                    file.write(f'check_start_at_one({class_name}) {check_start_at_one(instance_ids_for_class)} \n')
                    file.write(f'check_ascending({class_name}) {check_ascending(instance_ids_for_class)} \n')
    
    return ann_with_annotation_class_and_numbering_errors_in_seq 
                

def get_ann_with_annotation_class_and_numbering_errors_for_dataset(dataset_dir,
                                                                   class_names = ['grasper', 'hook', 'irrigator', 'clipper', 'bipolar', 'scissors', 'snare'],
                                                                   log_dir: str = 'logs/annotation_class_and_numbering_errors_in_seq_dir'):
    
    ann_with_annotation_class_and_numbering_errors_in_dataset = {}
    
    for split in os.listdir(dataset_dir):
        split_dir = join(dataset_dir, split)
        if os.path.isdir(split_dir):  
                
            ann_with_annotation_class_and_numbering_errors_in_dataset[split_dir] = {}
            for seq in os.listdir(split_dir):
                seq_dir = join(dataset_dir, split, seq)
                seq_dir = seq_dir.replace('\\', '/')
                ann_with_annotation_class_and_numbering_errors_in_seq = get_ann_with_annotation_class_and_numbering_errors_in_seq_dir(seq_dir=seq_dir, 
                                                                                                                                    class_names=class_names,
                                                                                                                                    log_dir=log_dir)  
                ann_with_annotation_class_and_numbering_errors_in_dataset[split_dir][seq] = ann_with_annotation_class_and_numbering_errors_in_seq
         
    return  ann_with_annotation_class_and_numbering_errors_in_dataset       
                                  

#transfer these files in the dataset to the repair folder. 
# essentially move the image files and move the annotation files. 
# Ensure that the datasetmetadata can still be calculated as a test  


#return these files after repair.
# Move the image files and the annotation files back to the corresponding folders. 
# Calculate datasetmetadata to ensure no mistakes have been made. 
# Compare the total_size to  39078 this should be a static variables


    
    
        

#main file needs to have two modes, one for getting the files to repair and another for returning the files from repair. 
def main():
    pass
    
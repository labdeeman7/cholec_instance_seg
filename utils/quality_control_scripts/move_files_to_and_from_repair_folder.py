from utils.read_files import read_from_json
import os
from os.path import join
import shutil
import numpy as np

def transfer_files_for_repair_to_repair_folder(ann_with_err_file_paths: list, 
                                               repair_dir='C:/Users/tal22/Documents/repositories/sam_annotator_tool_generate_instance/segment-anything-annotator/seq/repair'):
    

    repair_ann_dir = join(repair_dir, 'ann_dir')
    repair_img_dir = join(repair_dir, 'img_dir')
    assert os.path.isdir(repair_ann_dir), 'the repair directory does not contain an ann_dir'
    assert os.path.isdir(repair_img_dir), 'the repair directory does not contain an img_dir'
    
    for annotation_path in ann_with_err_file_paths:              
        image_path = annotation_path.replace('ann_dir', 'img_dir').replace('.json','.png') 
        annotation_name =   os.path.basename(annotation_path)
        img_name = os.path.basename(image_path)
        
        if os.path.exists(annotation_path) and os.path.exists(image_path):           
            shutil.move(annotation_path, join(repair_ann_dir, annotation_name))
            shutil.move(image_path, join(repair_img_dir, img_name ))
            print(f"Moved {annotation_name} and corresponding image to repair directory.")
        else:
            print(f"Error: {annotation_path} or corresponding image not found.")


def transfer_files_for_repair_to_repair_folder_dataset(ann_with_annotation_class_and_numbering_errors_in_dataset):
    for split_path, split_info in  ann_with_annotation_class_and_numbering_errors_in_dataset.items():
        for seq_name, ann_with_annotation_class_and_numbering_errors_in_seq in split_info.items():
            seq_path = join(split_path, seq_name)
            
            transfer_files_for_repair_to_repair_folder(ann_with_annotation_class_and_numbering_errors_in_seq)               
            

def get_back_files_from_the_repair_folder_to_the_original_folders(dataset_dir,
                                                                 repair_dir='C:/Users/tal22/Documents/repositories/sam_annotator_tool_generate_instance/segment-anything-annotator/seq/repair'
                                                                  ):
    repair_ann_dir = join(repair_dir, 'ann_dir')
    repair_img_dir = join(repair_dir, 'img_dir')
    assert os.path.isdir(repair_ann_dir), 'the repair directory does not contain an ann_dir'
    assert os.path.isdir(repair_img_dir), 'the repair directory does not contain an img_dir'
    
    repaired_annotations = os.listdir(repair_ann_dir) 
    
    for ann_name in repaired_annotations:     
        ann_path = join(repair_ann_dir, ann_name)         
        img_path = ann_path.replace('ann_dir', 'img_dir').replace('.json','.png')
        img_name = os.path.basename(img_path)
        
        dataset_seq_dir = get_seq_folder_from_ann_name(dataset_dir,
                                ann_name)
        
        assert dataset_seq_dir, 'there is an error with the ann_naming or your folder naming'
        
        dataset_ann_dir = join(dataset_seq_dir, 'ann_dir')
        dataset_img_dir = join(dataset_seq_dir, 'img_dir')
        
        
        if os.path.exists(ann_path) and os.path.exists(img_path):           
            shutil.move(ann_path, join(dataset_ann_dir, ann_name))
            shutil.move(img_path, join(dataset_img_dir, img_name ))
            print(f"Moved {ann_name} and corresponding image {img_name} to repair directory.")
        else:
            print(f"Error: {ann_name} or corresponding image {img_name} not found.")
            
    ##Ensure all images are back
    ensure_dataset_size_is_correct(dataset_dir)            
    
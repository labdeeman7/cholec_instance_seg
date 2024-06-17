from utils.read_files import read_from_json
import os
from os.path import join
import shutil
import numpy as np


def perform_quality_control_for_dataset(dataset_dir,
                                        quality_control_func_on_seq,
                                        log_dir, 
                                        ):    
    for split in os.listdir(dataset_dir):
        split_dir = join(dataset_dir, split)
        if os.path.isdir(split_dir):    
            for seq in os.listdir(split_dir):
                seq_dir = join(dataset_dir, split, seq)
                seq_dir = seq_dir.replace('\\', '/')
                quality_control_func_on_seq(seq_dir=seq_dir,log_dir=log_dir)
                print(f'{seq} completed')

def calculate_iou(mask1, mask2):
    """Calculate the Intersection over Union (IoU) of two binary masks."""
    intersection = np.logical_and(mask1, mask2).sum()
    union = np.logical_or(mask1, mask2).sum()
    iou = intersection / union if union != 0 else 0
    return iou           
    
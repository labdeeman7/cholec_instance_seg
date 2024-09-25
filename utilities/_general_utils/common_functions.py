import numpy as np
import cv2

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


def get_image_dimensions(image_path):
    img = cv2.imread(image_path)
    height, width = img.shape[:2]
    return height, width
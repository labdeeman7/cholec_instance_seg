import numpy as np
import cv2
from os.path import join
import os
import shutil 
import json

from utilities._general_utils.dataset_variables import CholecInstanceSegVariables

from os.path import join
class_name_to_color  =  CholecInstanceSegVariables.colors



def polygons_to_mask(polygons, height, width):
    mask = np.zeros((height, width), dtype=np.uint8)
    # Draw polygons on the mask
    cv2.fillPoly(mask, [np.array(polygon, dtype=np.int32).reshape((-1, 2)) for polygon in polygons], 1)
    return mask  

def get_colour_from_class_name_instance_id(class_name, 
                                           instance_id, 
                                           increment=20, 
                                           keep_instance_info=False):
    class_color = class_name_to_color[class_name]
    if keep_instance_info:
        assert instance_id != 0, 'there is an error somewhere as instance_id should not be zero' 
        if instance_id == 1: 
            return class_color
        else: 
            class_color = list(class_color)
            class_color[2] =   (class_color[2]  + (increment * (instance_id-1))  ) % 256 # the generation of instance colours.
            return(tuple(class_color))
    else:
        return class_color    



# Example function to convert points to COCO segmentation format
def generate_instance_dict_json_from_label_me_json (pred_json_path, height, width):
    with open(pred_json_path) as f:
        pred_annotation = json.load(f) 
    # Get image_id from ground-truth based on the file name
    image_path = pred_annotation["imagePath"]

    instance_dict = {}  # To group polygons by instance (label + group_id combination)  
    instance_dict['image_path'] = image_path
    instance_dict['instance_annotations'] = {}

    #combine polygons for same instance
    for i, shape in enumerate(pred_annotation["shapes"]):
        # Create a unique key using both the label and group_id
        unique_key = str( (shape["label"], shape["group_id"]) )
        
        if unique_key in instance_dict:
            instance_dict[unique_key]['instance_annotations']["polygons"].append(shape["points"]) 
        else: 
            instance_dict['instance_annotations'][unique_key] = {
                "label":  shape["label"],
                "polygons":  [shape["points"]],
                "group_id": shape["group_id"],
            }   
    
    #genreate rle       
     
    for unique_key, instance_info in instance_dict['instance_annotations'].items():
        # print(instance_info)
        label = instance_info["label"]
        polygons = instance_info["polygons"]
        group_id = instance_info["group_id"]

        instance_mask = polygons_to_mask(polygons, height, width)
        
        instance_dict['instance_annotations'][unique_key]['instance_mask'] = instance_mask.tolist()
        
    return instance_dict 
            
def convert_label_me_json_to_semantic_mask(label_me_json_path,
                                        img_path, 
                                        semantic_map_save_dir,
                                        keep_instance_info=False):
    
    assert os.path.isdir(semantic_map_save_dir), f'{semantic_map_save_dir} does not exist, please create it. first.'
    img_name = os.path.basename(img_path)
    img = cv2.cvtColor(cv2.imread(img_path), cv2.COLOR_BGR2RGB)
    height, width = img.shape[:2]
    image_instances_dict = generate_instance_dict_json_from_label_me_json (label_me_json_path, height, width)
           
    # Create an empty mask (height, width, 3 channels for RGB)
    final_semantic_mask = np.zeros((height, width, 3), dtype=np.uint8) 
    
    # Iterate over the instances and create the mask 
    for key, instance_annotations in image_instances_dict['instance_annotations'].items():
        class_name = instance_annotations['label']
        instance_id = instance_annotations['group_id']  
        
        binary_instance_mask = np.array(instance_annotations['instance_mask'])
        color = get_colour_from_class_name_instance_id(class_name, instance_id, keep_instance_info=keep_instance_info)
        
        # Apply the color where the mask is non-zero
        final_semantic_mask[binary_instance_mask > 0] = color

    # Save mask or overlap based on the format
    save_path = join(semantic_map_save_dir, img_name)

    # Save just the mask as an image (RGB format)
    final_mask_bgr = cv2.cvtColor(final_semantic_mask, cv2.COLOR_RGB2BGR)  # Convert back to BGR for OpenCV saving
    cv2.imwrite(save_path, final_mask_bgr)
    print(f'Generated semantic mask for {img_name} and stored in {save_path}')
    

def convert_label_me_json_to_semantic_mask_for_directory(label_me_json_dir, img_dir, semantic_map_save_dir, keep_instance_info=False):
    """
    Converts and saves LabelMe JSON annotations into semantic masks for all files in a given directory.

    This function processes a directory of LabelMe JSON files and corresponding images. It creates semantic maps 
    (i.e., masks where each pixel is assigned a class label) based on the annotations in each JSON file. The function 
    then saves the generated semantic masks to a specified output directory.

    Parameters:
    -----------
    label_me_json_dir : str
        Directory containing the LabelMe JSON annotation files. Each file should have a `.json` extension.
    
    img_dir : str
        Directory containing the corresponding images for the LabelMe JSON files. The image filenames should match 
        the JSON files (excluding the `.json` extension) and have a `.png` extension.
    
    semantic_map_save_dir : str
        Directory where the generated semantic masks will be saved. The masks will be saved with the same base name 
        as the corresponding image, but as semantic maps (e.g., 'image_name_mask.png').
    """    
    label_me_json_names = [label_me_json_name for label_me_json_name in os.listdir(label_me_json_dir) if label_me_json_name.endswith('.json') ] 
    
    for label_me_json_name in label_me_json_names:
        img_name = label_me_json_name.replace('.json', '.png') # get corresponding image name
        label_me_json_path = join(label_me_json_dir, label_me_json_name) # path for label_me_json.  
        img_path = join(img_dir, img_name)
        assert os.path.isfile(img_path), f'corresponding img_path {img_path} for {label_me_json_name} does not eist'
        convert_label_me_json_to_semantic_mask(label_me_json_path, img_path, semantic_map_save_dir, keep_instance_info=keep_instance_info)
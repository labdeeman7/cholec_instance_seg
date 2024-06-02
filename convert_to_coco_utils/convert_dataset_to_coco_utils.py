import numpy as np
import cv2

## Numpy ann functions

def get_bbox_info_from_mask(mask: np.ndarray) -> list:
    """get the bounding_box boundary info for an instance from binary mask.   
    format is [x_min, y_min, width, height]

    Args:
        mask (np.ndarray): numpy array of HxW 

    Returns:
        list: containing [x_min, y_min, width, height]
    """    
    
    # Find indices of non-zero elements in the mask
    rows, cols = np.where(mask > 0)
    
    # Calculate bounding box coordinates
    x_min = int(np.min(cols))
    y_min = int(np.min(rows))
    width = int(np.max(cols) - x_min)
    height = int(np.max(rows) - y_min)
    
    return [x_min, y_min, width, height]


def instance_mask_to_coco_contours_polygon_xy_or_labelme_format(binary_mask : np.ndarray,
                                                                 format: str = 'COCO')-> list: 
    """convert a binary mask to a list of lists where the list contains each contour
    store this as the xy format or [x,y] format.  

    Args:
        binary_mask (np.ndarray): binary mask to be converted. 
        format (str): 'COCO' or 'labelme'

    Returns:
        list: a list of lists which is a list that contains all 
        the contours in the x,y format
    """    
    # Find contours in the binary mask
    contours, _ = cv2.findContours(binary_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Initialize a list to store the contours in COCO format
    contour_points_for_an_instance_polygon_xy = []

    # print(contours)
    for contour in contours:
        # Convert OpenCV contour to COCO format
        segmentation = []
        
        if len(contour) > 2:
            for point in contour.squeeze():
                if format == 'COCO':
                    segmentation.extend(point.tolist())
                elif format == 'labelme':
                    segmentation.append(point.tolist())

        # Make sure the segmentation is a closed polygon
        if len(segmentation) >= 6:
            contour_points_for_an_instance_polygon_xy.append(segmentation)

    return contour_points_for_an_instance_polygon_xy



def get_list_of_contour_dicts_for_all_instances_in_img_from_ann(ann: np.ndarray, 
                                                                vis: bool= False) -> list:
    """convert ann masks in the form of a numpy array to a list of dicts. the dicts have 5 keys
        {
            'instance_id': id of instance in the image, but this is not stored in coco,
            'class_id': int -> class_id for referencing with coco,
            'contours_for_an_instance_as_list': list -> contours in the instance as a list,
            'area_for_instance':  float -> amount_of_pixels with 1 ,
            'bbox_for_instance':  list -> x_min, y_min, width, height 
            
        } 

    Args:
        ann (np.ndarray): annotation in the form of a numpy array
        vis (bool, optional): you wanna visualize the class_id, instance_id maps or not?. Defaults to False.

    Returns:
        list: list of dict  
    """    
    from  utils.vis_utils import plot_instance_from_json_contour
    from utils.get_information_from_file_name import get_unique_class_and_instance_id_in_ann
    
    unique_class_instance = get_unique_class_and_instance_id_in_ann(ann)
    list_of_contour_info_dicts_for_all_instances_in_img = [] 
    
    for class_id, instance_id in unique_class_instance:
        instance_mask = (ann[:, :, 0] == class_id) & (ann[:, :, 1] == instance_id)
        instance_mask = instance_mask.astype('uint8')        
        contour_points_for_an_instance_polygon_xy = instance_mask_to_coco_contours_polygon_xy_or_labelme_format(instance_mask, 'COCO')  
              
        single_instance_contours_info_dict = {
            'instance_id':  instance_id,
            'class_id': class_id,
            'contours_for_an_instance_as_list': contour_points_for_an_instance_polygon_xy,
            'area_for_instance':  float(np.sum(instance_mask)),
            'bbox_for_instance':  list(get_bbox_info_from_mask(instance_mask))
              
        }   
        
        if vis:
            plot_instance_from_json_contour(contour_points_for_an_instance_polygon_xy)
            
        list_of_contour_info_dicts_for_all_instances_in_img.append(single_instance_contours_info_dict) 
    
    return list_of_contour_info_dicts_for_all_instances_in_img    



## Label_me JSON functions


def refactor_label_me_json_dict_so_unique_class_instance_ids_are_keys_and_contours_are_values(json_dict: dict, 
                                               refactored_json_dict: dict):
    """the label me annotation tool stores every contour separately as its own dict and tracks 
    which contours belongs to the same instance by the group_id value. 
    This function generates anither dict where the keys are a tuple of the (class_name and instance_id)
    and the values is a list of contours belonging the that unique instance.   

    Args:
        json_dict (dict): dict from label me tool
        refactored_json_dict (dict): dict that would contain the contours as 
    """    
    assert not refactored_json_dict, 'the refactored dict is filled, it needs to be empty.'
   
    for contour_info in json_dict['shapes']:
        class_name = contour_info['label']
        instance_id =  contour_info['group_id']
        contour_pts = contour_info['points']
        
        if((class_name, instance_id) in refactored_json_dict): 
            refactored_json_dict[(class_name, instance_id)].append(contour_pts)    
        else:
            refactored_json_dict[(class_name, instance_id)] =  [contour_pts] 


def get_bbox_info_from_coco_contour_xy(contours_list: list)-> list: 
    """get the bounding_box boundary info for an instance from contour list.   
    format is [x_min, y_min, width, height]

    Args:
        contours_list (list): list containing the contours in the xy format.

    Returns:
        list: [x_min, y_min, width, height]
    """    
    contours_list = [np.array(contour_xy).reshape((-1, 2)).astype(np.int32)for contour_xy in contours_list]
    all_points = np.concatenate(contours_list, axis=0)
    
    # Find the bounding box coordinates
    x_min, y_min = np.min(all_points, axis=0)
    x_max, y_max = np.max(all_points, axis=0)
    
    # Calculate the width and height of the bounding box
    width = x_max - x_min
    height = y_max - y_min
    
    # COCO bbox format: [x, y, width, height]
    coco_bbox = [int(x_min), int(y_min), int(width), int(height)]

    return coco_bbox


def calculate_total_area_from_coco_contour_xy(contours_list: list) -> float:
    """calculate how many pixels exist in the contour 

    Args:
        contours_list (list): the contours that make up an instance, 
        coco_xy format style

    Returns:
        float: the total area covered by the contour
    """    
    total_area = 0

    for contour_xy in contours_list:
        # Reshape the flattened XY coordinates into an array of shape (num_points, 2)
        contour_np = np.array(contour_xy).reshape((-1, 2)).astype(np.int32)

        # Calculate the area of the contour and add it to the total area
        area = cv2.contourArea(contour_np)
        total_area += area

    return total_area     


def get_list_of_contour_dicts_for_all_instances_in_img_from_json(json_dict: dict, 
                                                                 vis: bool = False):
    
    """convert label_me json_dict which contains the contours masks to a list of dicts. 
    the dicts have 5 keys
        {
            'instance_id': id of instance in the image, but this is not stored in coco,
            'class_id': int -> class_id for referencing with coco,
            'contours_for_an_instance_as_list': list -> contours in the instance as a list,
            'area_for_instance':  float -> amount_of_pixels with 1 ,
            'bbox_for_instance':  list -> x_min, y_min, width, height 
            
        } 

    Args:
        json_dict (np.ndarray): label_me json_dict
        vis (bool, optional): you wanna visualize the contours?. Defaults to False.

    Returns:
        list: list of dict 
    """ 
    from utils.vis_utils import plot_instance_from_json_contour
    from static_variables.dataset_variables import CholecInstanceSegVariables 
    INSTRUMENT_ID_TO_CLASS_DICT = CholecInstanceSegVariables.instrument_id_to_instrument_class_dict
    INSTRUMENT_CLASS_TO_ID_DICT = {instrument_class: instrument_id for instrument_id, instrument_class in INSTRUMENT_ID_TO_CLASS_DICT.items()}
    
    refactored_json_dict = {}
    refactor_label_me_json_dict_so_unique_class_instance_ids_are_keys_and_contours_are_values(json_dict, 
                                               refactored_json_dict)
        
       
    list_of_contour_info_dicts_for_all_instances_in_img = [] 
    for classnameinstanceid, contour_pts_list in refactored_json_dict.items():
        class_name = classnameinstanceid[0]
        instance_id = classnameinstanceid[1]
        
        # convert to polygon_xy and use list       
        contour_points_for_an_instance_polygon_xy= [] 
        for contour_pts in contour_pts_list:
            contour_pts = np.array(contour_pts, dtype=np.int32)
            contour_pts = contour_pts.flatten().tolist()
            contour_points_for_an_instance_polygon_xy.append(contour_pts)
            
        single_instance_contours_info_dict = {
            'instance_id':  instance_id,
            'class_id': INSTRUMENT_CLASS_TO_ID_DICT[class_name],
            'contours_for_an_instance_as_list': contour_points_for_an_instance_polygon_xy,
            'area_for_instance':  calculate_total_area_from_coco_contour_xy(contour_points_for_an_instance_polygon_xy),
            'bbox_for_instance':  list(get_bbox_info_from_coco_contour_xy(contour_points_for_an_instance_polygon_xy)) 
        }  
        
        if vis:
            plot_instance_from_json_contour(contour_points_for_an_instance_polygon_xy)
            
        list_of_contour_info_dicts_for_all_instances_in_img.append(single_instance_contours_info_dict) 
    
    return list_of_contour_info_dicts_for_all_instances_in_img  



## Generate the COCO values
def mask_or_contour_to_coco(annotation_name: str, 
                            annotation_dir: str, 
                            image_id: int, 
                            coco_annotation: dict, 
                            vis: bool = False) -> None:
    """convert a binary mask in numpy format or a contour in the label_me format to the coco format.  

    Args:
        annotation_name (str): annotation name either ends as json or npy
        annotation_dir (str): annotation directory
        image_id (int): image_id
        coco_annotation (dict): the dict containing the coco_annotation, 
        it is used to keep track of the annotation id and also store values 
        for  new images/ annotations
        vis (bool, optional): visualizations activator. Defaults to False.

    Raises:
        ValueError: when we have a format different from numpy or json, raise error
    """      
    from os.path import join
    from utils.read_files import read_from_json
    
    '''
    First Get label_me_json or npy to a unified format called contour_dict. it is a list of dicts that looks like this
     {
            'instance_id': id of instance in the image, but this is not stored in coco,
            'class_id': int -> class_id for referencing with coco,
            'contours_for_an_instance_as_list': list -> contours in the instance as a list,
            'area_for_instance':  float -> amount_of_pixels with 1 ,
            'bbox_for_instance':  list -> x_min, y_min, width, height
        }  
    '''            
    if annotation_name.split('.')[-1] == 'npy':
        ann = np.load( join(annotation_dir, annotation_name )) # Convert to grayscale if needed 
        contour_dicts_for_all_instances_in_img = get_list_of_contour_dicts_for_all_instances_in_img_from_ann(ann, vis)
                  
    elif annotation_name.split('.')[-1] == 'json':   
        json_dict =  read_from_json(join(annotation_dir, annotation_name ))
        contour_dicts_for_all_instances_in_img = get_list_of_contour_dicts_for_all_instances_in_img_from_json(json_dict, vis)  
    else: 
        raise ValueError('only npy and mask are acceptable')
    
    
    
    for single_instance_contours_info_dict in contour_dicts_for_all_instances_in_img:
        contours_for_an_instance_as_list = single_instance_contours_info_dict['contours_for_an_instance_as_list']
        bbox_for_instance = single_instance_contours_info_dict['bbox_for_instance']
        area_for_instance = single_instance_contours_info_dict['area_for_instance']
        class_id = int(single_instance_contours_info_dict['class_id'])         
                
        annotation = {
            "image_id": image_id,
            "category_id": class_id,
            "segmentation": contours_for_an_instance_as_list,
            "iscrowd": 0,
            "area": area_for_instance, # float(np.sum(instance_mask))
            "bbox": bbox_for_instance, # list(get_bbox_info_from_mask(instance_mask)),
            "id": len(coco_annotation["annotations"]) + 1
        }
               
        coco_annotation["annotations"].append(annotation)
        
        
def annotations_to_coco(dataset_path: str,
                        output_json_path: str,
                        vis: bool = False):
    """generate the coco_format for my numpy  and label_me json styled annotations 

    Args:
        dataset_path (str): path to the dataset to convery
        output_json_path (str): json file store path
        vis (bool, optional): visualize things or not. Defaults to False.
    """    
    import os, json
    
    coco_annotation = {
        "images": [],
        "annotations": [],
        "categories": [{"id": 1, 
                        "name": "grasper",
                        "supercategory": "instrument"},
                       {"id": 2, 
                        "name": "hook",
                        "supercategory": "instrument"},
                       {"id": 3, 
                        "name": "irrigator",
                        "supercategory": "instrument"},
                       {"id": 4, 
                        "name": "clipper",
                        "supercategory": "instrument"},
                       {"id": 5, 
                        "name": "bipolar",
                        "supercategory": "instrument"},
                        {"id": 6, 
                        "name": "scissors",
                        "supercategory": "instrument"},
                       {"id": 7, 
                        "name": "snare",
                        "supercategory": "instrument"}                       
                       ]
    }

    img_list = sorted(os.listdir(os.path.join(dataset_path, 'img_dir')))
    ann_list = sorted(os.listdir(os.path.join(dataset_path, 'ann_dir')))
    
    for i, filename in enumerate(img_list):          
        print(f'currently on {i}, {filename}, mask {ann_list[i]}')  
            
        image_id = i + 1  # Adjust if your image IDs start from 0
        image_info = {"file_name": filename,
                      "id": image_id,
                      "width": 854,
                      "height": 480,}
        coco_annotation["images"].append(image_info)
        mask_name =  ann_list[i]
        mask_dir = os.path.join(dataset_path, 'ann_dir')
        mask_or_contour_to_coco(mask_name, mask_dir, image_id, coco_annotation=coco_annotation, vis=vis)      


    with open(output_json_path, 'w') as json_file:
        json.dump(coco_annotation, json_file)        
        

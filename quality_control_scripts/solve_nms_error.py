import os
import numpy as np
import cv2
from os.path import join
from utils.read_files import read_from_json
from quality_control_scripts.quality_control_utils import calculate_iou 
import numpy as np



def compare_masks(masks):
    """Compares each mask with every other mask in the list using IoU."""
    num_masks = len(masks)
    results = []

    for i in range(num_masks):
        for j in range(i + 1, num_masks):
            mask1 = masks[i]['mask']
            mask2 = masks[j]['mask']
            iou_score = calculate_iou(mask1, mask2)
            result = {
                'mask1_id': masks[i]['group_id'],
                'mask1_label': masks[i]['label'],
                'mask2_id': masks[j]['group_id'],
                'mask2_label': masks[j]['label'],
                'iou': iou_score
            }
            results.append(result)
    return results    




def get_contours_with_bad_nms_for_seq(seq_dir, log_dir):
    ann_dir = join(seq_dir, 'ann_dir') 
    img_dir = join(seq_dir, 'img_dir') 
    
    os.makedirs(log_dir, exist_ok=True)
    seq_name = seq_dir.split('/')[-1]
    split = seq_dir.split('/')[-2]
    nms_error_in_seq_dir_text_file = join(log_dir, f'{split}_{seq_name}.txt')
    
    with open(nms_error_in_seq_dir_text_file, "a") as file:
        for ann_filename in os.listdir(ann_dir):
            img_filename = ann_filename.split('.')[0] + '.png'

            ann_filepath = os.path.join(ann_dir, ann_filename)
            img_filepath = os.path.join(img_dir, img_filename)
            
            info = read_from_json(ann_filepath)
            info_shapes =  info['shapes']
            img = cv2.imread(img_filepath)
            shape = img.shape[:2]
            
            masks = []
            for shape_info in info_shapes:
                group_id = shape_info['group_id']
                label = shape_info['label']    
                points = shape_info['points']
                mask = np.zeros(shape, dtype=np.uint8)
                # Reshape the flattened XY coordinates into an array of shape (num_points, 2)
                contour_np = np.array(points, dtype=np.int32).reshape((-1, 2))
                # Connect the last point to the first one to ensure closure
                contour_np = np.vstack([contour_np, contour_np[0]])
                
                cv2.fillPoly(mask, [np.array(contour_np)], 255)
                
                mask_info = {
                    'group_id': group_id,
                    'label': label,
                    'mask': mask, 
                }
                
                masks.append(mask_info)
                
            iou_results = compare_masks(masks)

            # Output results
            
            
            for result in iou_results:
                if result['iou'] > 0.8:
                    file.write( '====================================================\n' )    
                    file.write(f"{ann_filename}, Comparison between {result['mask1_label']}_{result['mask1_id']} and {result['mask2_label']}_{result['mask2_id']}: IoU = {result['iou']:.2f}\n")          


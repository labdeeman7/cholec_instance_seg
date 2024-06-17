

def test_get_list_of_contour_dicts_for_all_instances_in_img_from_ann():
    import numpy as np
    from .convert_dataset_to_coco_utils import get_list_of_contour_dicts_for_all_instances_in_img_from_ann
    
    npy_ann = np.load('datasets/cholecseg8k_coco/val/ann_dir/video37_frame_0000960.npy')
    print(f'unique ids in numpy array include {np.unique(npy_ann)}')
    
    get_list_of_contour_dicts_for_all_instances_in_img_from_ann(npy_ann, vis = True) 
    
    return
    
    
def  test_get_bbox_info_from_coco_contour_xy():
    from .convert_dataset_to_coco_utils import get_bbox_info_from_coco_contour_xy
    
    contours_list = [[0, 1, 2, 1, 2, 2, 0, 2], [3, 3, 5, 3, 5, 5, 3, 5]] # Replace with your list of contour XY coordinates

    # Calculate the COCO bounding box for all contours
    coco_bbox = get_bbox_info_from_coco_contour_xy(contours_list)
    print(f'contours_list {contours_list}')
    print(f'[x_min, y_min, width, height] {coco_bbox}')
    

def test_calculate_total_area_from_coco_contour_xy():
    from.convert_dataset_to_coco_utils import calculate_total_area_from_coco_contour_xy
    contours_list = [[0, 0, 2, 0, 2, 2, 0, 2], [3, 3, 5, 3, 5, 5, 3, 5]]  # Replace with your list of contour XY coordinates

# Calculate the total area of all contours
    total_area = calculate_total_area_from_coco_contour_xy(contours_list)
    print(f'contours_list {contours_list}')
    print("Total Area:", total_area)
        
        
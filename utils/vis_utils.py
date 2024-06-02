import matplotlib.pyplot as plt
import numpy as np
import cv2
from utils.read_files import read_from_json
import os
from os.path import join


def create_overlay_image(image: np.ndarray, 
                          mask: np.ndarray, 
                          resize: tuple = None,
                          alpha: float = 0.3, 
                          id_to_colour_dict: dict = {'1': (255,0, 0)},
                          vis: bool = False,
                          background_id: int = None,
                          ) -> np.ndarray:
    """create overlay image 

    Args:
        image (np.ndarray): image in numpy array. Ensure it is already converted to rgb. HxWx3
        mask (np.ndarray): segmentation mask. It should be a uint8 mask with values corresponding to keys in the color dict HxW. 
        resize (tuple, optional): resize the images or not. Give the size of the desired overlay if you wish to 
        alpha (float, optional): _description_. Defaults to 0.3.
        id_to_color_dict (dict, optional): a dict with colours for each of the masks in the image. the keys should be strings of classid. 
                                    If not available all classes would be converted to 1 and a default colour would be used.
                                    Defaults to  {'1': (255,0,0)}.
        vis (bool, optional): should the overlay be visualized?. Defaults to False.
        background_id (int, optional): removes the background_id for ids that use another value apart from 0 as id. Defaults to None.
        
    Returns:
        np.ndarray: overlay image    
    """

    # Convert the grayscale mask to a 3-channel mask with correct color
    # Get class_ids in the image, except background.
    unique_classes = np.unique(mask)
    if background_id is not None:
        unique_classes = np.delete(unique_classes, unique_classes==background_id)    
        
    # print(unique_classes)    
    
    
    colors = np.array([id_to_colour_dict[str(class_id)] for class_id in unique_classes])
    
    # Create a blank color array and blank bool array for the class_ids
    mask_colored = np.zeros((mask.shape[0], mask.shape[1], 3), dtype=np.uint8)
    mask_bool = np.zeros((mask.shape[0], mask.shape[1], 3), dtype=bool)

    for i, class_id in enumerate(unique_classes):
         mask_colored[mask == class_id] = colors[i]
         mask_bool[mask == class_id] = True
     
    mask_colored = mask_colored.astype(np.uint8)

    #resize if needed. 
    if resize:
        image = cv2.resize(image, resize, cv2.INTER_NEAREST)
        mask_colored = cv2.resize(mask_colored, resize, cv2.INTER_NEAREST)
          
    # Blend the image and the mask
    overlay_image = image.copy()
    overlay_image[mask_bool] = alpha*mask_colored[mask_bool]  + (1-alpha)*image[mask_bool]  

    # display the result
    if vis:
        plt.imshow(overlay_image)
        plt.show()
    
    return overlay_image

 
def visualize_points_on_an_image(image: np.array,
                     points: list = None,
                     color = 'green',
                     title = None,
                     marker='*',
                     marker_size = 100):
    """
    Visualize points on an image.

    Parameters:
    - image: numpy array, the image
    - points: list of (x, y) coordinates
    - color: color of points
    - marker: marker of points - 
    - marker_size: size of markers  
    """
    plt.imshow(image)
    
    if title:
        plt.title(title)

    if points:
        points = np.array(points)
        plt.scatter(points[:, 0], points[:, 1], c=color, marker=marker, s=marker_size)

    plt.show()
    

def plot_instance_from_json_contour(contours_list: list, 
                                    img: np.ndarray = None,
                                    fill_contour: bool = False, 
                                    instance_ids: list = None,
                                    class_names: list = None,                                    
                                    title: str = None,
                                    remove_ticks: bool = False,
                                    save_filepath = None) -> None:
    """Plot the contour(s) of a single instance in COCO or labelme format.

    Args:
        contours_list (list): Contours which describe an instance.
        fill_contour (bool): If True, fill the contour(s) with a color. Default is False.
        img (np.ndarray): Numpy array representing the image. Default is None.
        save_filepath (str): Filepath where the plot should be saved. Default is None.
    """   
    height, width = img.shape[:2]  
    plt.figure(figsize=(width / 100, height / 100), dpi=130)
    plt.grid(True)
    label_name = None
    
    
    colors = {
        'grasper':       'red',
        'hook':          'green',
        'irrigator':     'yellow',
        'clipper':       'purple',
        'bipolar':       'orange',
        'scissors':      'cyan',
        'snare':         'magenta'  
    }

    if img is not None:
        plt.imshow(img)
        plt.grid(False)

    for i, contour_xy in enumerate(contours_list):
        # Reshape the flattened XY coordinates into an array of shape (num_points, 2)
        contour_np = np.array(contour_xy).reshape((-1, 2))

        # Connect the last point to the first one to ensure closure
        contour_np = np.vstack([contour_np, contour_np[0]])
        
        
        #plot the contours
        label_name = '' 
        
        if class_names:
            label_name = f'{class_names[i]} '
            
        if instance_ids:
            label_name = f'{label_name}-{instance_ids[i]}'     
        

        if fill_contour:
            plt.fill(contour_np[:, 0], contour_np[:, 1], alpha=0.3, label=label_name, color=colors[class_names[i]] )
        else:
            plt.plot(contour_np[:, 0], contour_np[:, 1], label=label_name, color=colors[class_names[i]])
        
            
        # Calculate position for the label text
        x_pos = np.mean(contour_np[:, 0])  # A simple approach: use the mean x value
        y_pos = np.max(contour_np[:, 1]) + 20  # Slightly below the min y value
        if y_pos+20 > img.shape[0]:
            # print(img.shape)
            # print(y_pos)
            y_pos = np.min(contour_np[:, 1]) - 20
        if y_pos < 0:
            # print(img.shape)
            # print(y_pos)
            y_pos = 20
        
        plt.text(x_pos, y_pos, f'{class_names[i]}-{instance_ids[i]}' , color=colors[class_names[i]], ha='center')
            
    if title:
        plt.title(title)
    
    if remove_ticks:  
        plt.xticks([])
        plt.yticks([])
  
    
    #flip contours from plt.plot.
    if img is None:
        plt.gca().invert_yaxis()
    
    if save_filepath:
        plt.margins(0)
        plt.savefig(save_filepath,  bbox_inches='tight', pad_inches=0)
        plt.close()
    else:
        plt.show() 



class VisFromLabelMeToImg:
    def __init__(self, 
                 img_dir: str, 
                 ann_dir: str,
                 vis_dir: str) -> None:
        self.img_dir = img_dir
        self.ann_dir = ann_dir
        self.vis_dir = vis_dir
        
        assert os.path.exists(img_dir), 'the image directory does not exist' 
        assert os.path.exists(ann_dir), 'the annotation directory does not exist' 
        
        if os.path.exists(vis_dir):
            raise ValueError('vis_dir exists, use a non_existing folder')
        
        os.makedirs(vis_dir)
         
    
    def create_and_save_img_from_a_single_label_me_dict(self,
                                                        img_path: str,
                                                        ann_path: str,
                                                        show_img_name: bool = False):           
        
        ann = get_json_info(ann_path)
        img = cv2.cvtColor(cv2.imread(img_path), cv2.COLOR_BGR2RGB ) 
        basename = os.path.basename(img_path)
        save_filepath = join(self.vis_dir, basename)
        
        ann_contours = ann['shapes']
        class_names = [ann['label'] for ann in ann_contours]
        instance_ids = [ann['group_id'] for ann in ann_contours] 
        points = [ann['points'] for ann in ann_contours] 
        
        if show_img_name:
            title = basename
        else:
            title = None    
        
        plot_instance_from_json_contour(points,
                                fill_contour = False,
                                img = img,
                                class_names=class_names,
                                instance_ids=instance_ids,
                                save_filepath = save_filepath,
                                remove_ticks=True,
                                title = title
                                 ) 

                
    def run(self, 
            make_video: bool,
            show_img_name: bool,
            vid_shape= None):
        
        img_names = os.listdir(self.img_dir)
        for img_name in img_names:
            img_path = join(self.img_dir, img_name)
            ann_path = join(self.ann_dir, img_name.replace('png', 'json'))
            
            self.create_and_save_img_from_a_single_label_me_dict(img_path,
                                                             ann_path,
                                                             show_img_name) 
            
        if make_video:
            parent_dir = os.path.dirname(self.vis_dir)
            video_output_path =  join(parent_dir, 'video.mp4') 
            
            from .video_utils import visualize_as_videos
            visualize_as_videos(self.vis_dir, 
                        video_output_path,
                        vid_shape) 
              

            
    def run_single_json_path(self,
                             img_path: str, 
                             ann_path: str):
        self.create_and_save_img_from_a_single_label_me_dict(img_path,
                                                             ann_path)                         
        
        
          
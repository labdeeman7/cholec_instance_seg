import cv2
import json
import numpy as np

def read_image(image_path, mode='RGB'):
    """
    Read an image from the specified path.

    Parameters:
        image_path (str): The path to the image file.
        mode (str): The mode of the image. Can be 'RGB' for color images or 'GRAY' for grayscale images.
                    Defaults to 'RGB' if not specified.

    Returns:
        numpy.ndarray: The image array.
    """
    
    # Read the image
    image = cv2.imread(image_path)
    
    # Convert to grayscale if mode is specified as 'GRAY'
    if mode == 'GRAY':
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    return image

def read_from_json(json_file_path: str):
    """get information when given the json file path 

    Args:
        json_file_path (str): path to json file.

    Returns: whatever is in the json file, typically lists or dicts.
    """  
    
    with open(json_file_path) as f:
        info = json.load(f)
        
    return info         

def read_npy(npy_file_path: str): 
    """
    Read a numpy file at the specified path.

    Parameters:
        npy_file_path (str): The path to the numpy file.

    Returns:
        numpy.ndarray: The numpy array.
    """

    info = np.load(npy_file_path)

    return info

def read_text(txt_file_path: str):
    """
    Read a text file at the specified path.

    Parameters:
        txt_file_path (str): The path to the text file.

    Returns:
        str: a string stored in the text file
    """
    
    with open(txt_file_path, 'r') as file:
        # Read the entire contents of the file
        info = file.read()
    
    return info
        
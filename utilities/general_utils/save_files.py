import cv2
import json
import numpy as np

def save_image(image, image_path):
    """
    Save an image to the specified path.

    Parameters:
        image (numpy.ndarray): The image array to save.
        image_path (str): The path where the image will be saved.
        mode (str): The mode of the image. Can be 'RGB' or 'GRAY'.
                    Only affects the file if it needs conversion; otherwise, saves as is.
                    Defaults to 'RGB' if not specified.

    Returns:
        None
    """
    
    cv2.imwrite(image_path, image)

def save_to_json(data, json_file_path: str):
    """
    Save a Python dict or list as a JSON file.

    Parameters:
        data (dict or list): The data to save.
        json_file_path (str): The path where the JSON file will be saved.

    Returns:
        None
    """
    with open(json_file_path, 'w') as f:
        json.dump(data, f, indent=4)

def save_npy(array, npy_file_path: str):
    """
    Save a numpy array to a .npy file.

    Parameters:
        array (numpy.ndarray): The numpy array to save.
        npy_file_path (str): The path where the .npy file will be saved.

    Returns:
        None
    """
    np.save(npy_file_path, array)

def save_text(text, txt_file_path: str):
    """
    Save a string to a text file.

    Parameters:
        text (str): The string to save.
        txt_file_path (str): The path where the text file will be saved.

    Returns:
        None
    """
    with open(txt_file_path, 'w') as file:
        file.write(text)

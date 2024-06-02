import imageio as iio
import imageio.v3 as iio3
from os.path import join 
import cv2
import os

class VideoWriter():
    def __init__(self, video_path, fps=5.0) -> None:
        self.writer = iio.get_writer(video_path, mode="I", fps=fps, format='FFMPEG')
   
    def write(self, image) -> None:
        self.writer.append_data(image)
 
    def close(self) -> None:
        self.writer.close()           
        

def visualize_as_videos(img_dir, 
                        video_output_path, 
                        vid_shape=None,
                        video_fps: int = 4):
    
    video_instance = VideoWriter(video_path=video_output_path, fps=video_fps)    
    img_paths = [join(img_dir, file_name) for file_name in os.listdir(img_dir)]
    
    for img_path in img_paths:  
        print(img_path)  
        img = cv2.cvtColor(cv2.imread(img_path), cv2.COLOR_BGR2RGB)    
        if vid_shape:
            img = cv2.resize(img, vid_shape, interpolation=cv2.INTER_AREA)    
        video_instance.write(img)          
    video_instance.close()    
    return
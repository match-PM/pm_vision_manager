from pathlib import Path
import os
import sys

#Import from absolute path
#sys.path.append('/home/niklas/ros2_ws/src/pm_vision/pm_vision/pm_vision_API')

#Import from relative path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from  vision_assistant_API import *


if __name__ == "__main__":
    my_vision_assistant = vision_assistant_API()
    VisionOK, _ = my_vision_assistant.start_vision_assistant( process_file = "process_demo.json", camera_config_file = "webcam_config.yaml")
    
    if VisionOK:
        #print(my_vision_assistant.vision_results_list)
        print("Vision Assistant API Test sucessfull!")
    else:
        print("Vision Assistant API Test failed!")
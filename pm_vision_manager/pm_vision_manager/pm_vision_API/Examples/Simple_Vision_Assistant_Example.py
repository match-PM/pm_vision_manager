from pathlib import Path
import os
import sys

#Import from absolute path
#sys.path.append('/home/niklas/ros2_ws/src/pm_vision/pm_vision/pm_vision_API')

#Import from relative path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from  vision_assistant_API import *
import geometry_utils as gtry

if __name__ == "__main__":
    my_vision_assistant = vision_assistant_API()
    VisionOK, _ = my_vision_assistant.run_vision( process_file = "process_demo.json", camera_config_file = "webcam_config.yaml")
    circle_list:list[gtry.Circle] = my_vision_assistant.get_circles_from_vision_results()    # The type def ':list[Cirle]' is necessary in order for vs code to propose class methods etc.
    if circle_list is not False:
        for c in circle_list:
            c.print_circle_information()

    line_list:list[gtry.Line] = my_vision_assistant.get_lines_from_vision_results()    # The type def ':list[Line]' is necessary in order for vs code to propose class methods etc.
    
    if line_list is not False:
        for l in line_list:
            l.print_Line_information()
    
    if VisionOK:
        #print(my_vision_assistant.vision_results_list)
        print("Vision Assistant API Test sucessfull!")
    else:
        print("Vision Assistant API Test failed!")
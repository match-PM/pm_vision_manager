import os
from subprocess import call
import subprocess
import json
from pathlib import Path
import uuid
import yaml
from yaml.loader import SafeLoader
import os
import time
import geometry_utils as Geometry 

class vision_assistant_API:
    def __init__(self):
        self.vision_process_libary_path="PATH_NOT_GIVEN"
        self.vision_database_path="PATH_NOT_GIVEN"
        self.camera_libary_path="PATH_NOT_GIVEN"
        self.vision_assistant_config_file="PATH_NOT_GIVEN"
        self.vision_results_list=[]
        self.vision_assistant_path_config_path = Path(__file__).parent.resolve()
        self.vision_assistant_path_config_path = os.path.dirname(os.path.dirname(self.vision_assistant_path_config_path))
        self.vision_assistant_path_config_path = self.vision_assistant_path_config_path + '/config/vision_assistant_path_config.yaml'
        self.load_path_config()
        self.default_processfile = "process_demo.json"
        self.default_camera_config = "webcam_config.yaml"
        self.image_display_time = 5 #default time the image is displayed in execution mode
        self.set_image_display_time_in_execution_mode(self.image_display_time)
        
    def load_path_config(self):
        PathNotReadSuccessfuly=True
        while(PathNotReadSuccessfuly):
            try:
                f = open(self.vision_assistant_path_config_path)
                FileData = yaml.load(f,Loader=SafeLoader)
                f.close()
                config=FileData["vision_assistant_path_config"]
                self.vision_process_libary_path=config["process_library_path"]
                self.vision_database_path=config["vision_database_path"]
                self.camera_libary_path=config["camera_config_path"]
                self.vision_assistant_config_file=config["vision_assistant_config"]
                print('Vision assistant path config loaded!')
                PathNotReadSuccessfuly=False
            except:
                print('Error opening vision assistant path configuration: ' + str(self.vision_assistant_path_config_path)+ "!")
                print("Give path to vision_assistant_path_config.yaml or enter 'exit'")
                self.vision_assistant_path_config_path = input()
                if self.vision_assistant_path_config_path == 'exit':
                    break

    def open_process_file_in_vcode(self):
        try:
            Comand = 'code '+self.vision_process_libary_path+self.current_process_file
            os.system(Comand)
        except Exception as e:
            print(e)
            print("Process File could not be opened")

    def set_image_display_time_in_execution_mode(self, display_time):
        try:
            with open(self.vision_assistant_config_file) as f:
                doc = yaml.load(f,Loader=SafeLoader)
            doc["vision_assistant_config"]['image_display_time_in_execution_mode'] = display_time
            with open(self.vision_assistant_config_file, 'w') as f:
                yaml.dump(doc, f)
            print("Change of display time sucessful!")
        except Exception as e:
            print("Error while trying to open vision_assistant_config!")
            print(e)

    def process_vision_result_file(self):
        self.current_vision_result_file = self.vision_process_libary_path + '/' + Path(self.current_process_file).stem + '_results.json' 
        try:
            f = open(self.current_vision_result_file)
            FileData = json.load(f)
            self.vision_process_name=FileData['vision_process_name']
            self.VisionOK=FileData['vision_OK']
            self.VisionOK_cross_val=FileData['VisionOK_cross_val']
            self.vision_process_id=FileData['process_UID']
            self.vision_results_list=FileData['vision_results']
            f.close()
            #print("Result File loaded!")
        except Exception as e:
            print("Error opening resutls file!")
            print(e)

    def get_circles_from_vision_results(self):
        try:
            self.check_if_results_list_empthy() # This function will raise an exeption when results list is empty
            list_of_circle_obj=[]
            for result in self.vision_results_list:
                if "Circles" in result:
                    list_of_circles=result.get('Circles')
                    #return list_of_circles
                    for circle in list_of_circles:
                        current_circle=Geometry.Circle(  ax1=circle['axis_1'],
                                                ax2=circle['axis_2'],
                                                radius=circle['radius'],
                                                ax1_suffix=circle['axis_1_suffix'],
                                                ax2_suffix=circle['axis_2_suffix'],
                                                unit=circle['Unit'])
                        list_of_circle_obj.append(current_circle)
                    
            if len(list_of_circle_obj) == 0:    
                print("No Circles in results found!")
                return False
            else:
                return list_of_circle_obj
        except:
            print("WARNING: Vision results list is empty!")      

    def get_circle_from_vision_results(self):
        # not tested!!!
        try:
            self.check_if_results_list_empthy() # This function will raise an exeption when results list is empty
            for result in self.vision_results_list:
                if "Circle" in result:
                    circle=result.get('Circle')
                    circle=Geometry.Circle(ax1=circle['axis_1'],
                        ax2=circle['axis_2'],
                        radius=circle['radius'],
                        ax1_suffix=circle['axis_1_suffix'],
                        ax2_suffix=circle['axis_2_suffix'],
                        unit=circle['Unit'])
                    return circle
            # if for-loop runs through no circle has been found
            print("No Circle in results found!")
            return False
        except:
            print("WARNING: Vision results list is empty!")  


    def get_lines_from_vision_results(self):
        try:
            self.check_if_results_list_empthy() # This function will raise an exeption when results list is empty
            list_of_line_obj=[]
            for result in self.vision_results_list:
                if "Lines" in result:
                    list_of_lines=result.get('Lines')
                    for line in list_of_lines:
                        current_point_1=Geometry.Point(ax1=line['Point_1']['axis_1'],
                                                       ax2=line['Point_1']['axis_2'],
                                                       ax1_suffix=line['axis_1_suffix'],
                                                       ax2_suffix=line['axis_2_suffix'],
                                                       unit=line['Unit']
                                                       )
                        current_point_2=Geometry.Point( ax1=line['Point_2']['axis_1'],
                                                        ax2=line['Point_2']['axis_2'],
                                                        ax1_suffix=line['axis_1_suffix'],
                                                        ax2_suffix=line['axis_2_suffix'],
                                                        unit=line['Unit']
                                                        )                      
                        current_line=Geometry.Line(current_point_1,
                                                   current_point_2,
                                                   unit=line['Unit']
                                                    )
                        list_of_line_obj.append(current_line)
                    
            if len(list_of_line_obj) == 0:    
                print("No Lines in results found!")
                return False
            else:
                return list_of_line_obj
        except:
            print("WARNING: Vision results list is empty!")

    def get_line_from_vision_results(self):
        # not tested!!!
        try:
            self.check_if_results_list_empthy() # This function will raise an exeption when results list is empty
            for result in self.vision_results_list:
                if "Line" in result:
                    circle=result.get('Line')
                    return circle
                print("No Line in results found!")
                return False
        except:
            print("WARNING: Vision results list is empty!")  

    def check_if_results_list_empthy(self):
        if len(self.vision_results_list):
            return
        else:
            raise
            
    def print_vision_result_file(self):
        # Dont call this function before "process_vision_result_file()" 
        print("###### Vision Results #####")
        print("Process Name: " + self.vision_process_name)
        print("Vision OK?: " + str(self.VisionOK))
        print("Vision Crossvalidation OK?: " + str(self.VisionOK_cross_val))
        print("Process UUID: " + self.vision_process_id)

    def run_vision(self, process_file = None, camera_config_file = None, show_node_output = False, open_new_terminal = False, image_display_time=None):
        self.VisionOK=False
        self.VisionOK_cross_val=False
        if image_display_time != None:
            self.image_display_time = image_display_time #default time

        if process_file == None:
            self.current_process_file = self.default_processfile
        else:
            self.current_process_file = process_file

        if camera_config_file == None:
            self.current_camera_config_file = self.default_camera_config
        else:
            self.current_camera_config_file = camera_config_file

        current_process_id = uuid.uuid4()

        print("Current Process ID:" + str(current_process_id))
       
        Vision_exec_Comand=('ros2 run pm_vision vision_assistant --ros-args ' + 
                ' -p ' + 'launch_as_assistant:=False' + 
                ' -p ' + 'process_UID:=' + str(current_process_id) +
                ' -p ' + 'process_filename:=' + self.current_process_file + 
                ' -p ' + 'image_display_time_in_execution_mode:=' + str(self.image_display_time) + 
                ' -p ' + 'camera_config_filename:=' + self.current_camera_config_file )
        
        if not open_new_terminal:
            node_terminal_output = subprocess.getstatusoutput(Vision_exec_Comand)
            if show_node_output:
                print(node_terminal_output[1])
        else:
            process = subprocess.Popen(
                "gnome-terminal -- "+Vision_exec_Comand, 
                stdout=subprocess.PIPE,
                stderr=None,
                shell=True
            )

        self.vision_process_id = 'empthy'
        # Set Timeout to wait for the Vision assistant to be done
        timeout_time = time.time() + 10   # 10 sek

        # Wait for the vision assistant to save the result given the current process id
        while self.vision_process_id != str(current_process_id):
            self.process_vision_result_file()
            print("Waiting for Vision assistant to finish!")
            if time.time() > timeout_time:
                print("Error! Timeout")
                break
            time.sleep(0.5)

        self.print_vision_result_file()

        return self.VisionOK , self.VisionOK_cross_val

    
    def start_vision_assistant(self, process_file = None, camera_config_file = None, open_new_terminal = False):
        if process_file == None:
            self.current_process_file = self.default_processfile
        else:
            self.current_process_file = process_file

        if camera_config_file == None:
            self.current_camera_config_file = self.default_camera_config
        else:
            self.current_camera_config_file = camera_config_file

        Vision_exec_Comand=('ros2 run pm_vision vision_assistant --ros-args ' + 
        ' -p ' + 'process_filename:=' + process_file + 
        ' -p ' + 'open_process_file:=True' + 
        ' -p ' + 'camera_config_filename:=' + camera_config_file )

        if not open_new_terminal:
            node_terminal_output = subprocess.getstatusoutput(Vision_exec_Comand)
        else:
            process = subprocess.Popen(
                "gnome-terminal -- "+Vision_exec_Comand, 
                stdout=subprocess.PIPE,
                stderr=None,
                shell=True
            )

        return

if __name__ == "__main__":
    my_vision_assistant = vision_assistant_API()
    #VisionOK, _ = my_vision_assistant.run_vision(open_new_terminal=True)
    VisionOK, _ = my_vision_assistant.run_vision( process_file = "process_demo.json", camera_config_file = "webcam_config.yaml",image_display_time=1)
    circles=my_vision_assistant.get_circles_from_vision_results()
    #print(circles)
    if VisionOK:
        #print(my_vision_assistant.vision_results_list)
        print("Vision Assistant API Test sucessfull!")
    else:
        print("Vision Assistant API Test failed!")
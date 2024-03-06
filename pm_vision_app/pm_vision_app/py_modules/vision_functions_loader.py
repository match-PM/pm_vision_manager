
import os
import yaml
import fnmatch
import copy
import sys
sys.path.append(os.getcwd())
#from py_modules.vision_functions_class import VisionFunction
from pm_vision_app.py_modules.vision_functions_class import VisionFunction
import pm_vision_app.py_modules.type_classes as TC
#import py_modules.type_classes as TC

class VisionFunctionsLoader():
    def __init__(self, lib_path) -> None:
        self.libary_path = lib_path
        self.vision_functions: list[VisionFunction] = []
        self.load_vision_functions_libary_from_path()

    def load_vision_functions_libary_from_path(self):
        self.yaml_data = []
        self.init_output = []
        for filename in os.listdir(self.libary_path):
            if filename.endswith(".yaml") or filename.endswith(".yml"):
                file_path = os.path.join(self.libary_path, filename)
                with open(file_path, 'r') as file:
                    try:
                        function_file_content = yaml.load(file, Loader=yaml.FullLoader)
                        _vision_function = VisionFunction(vision_function_name=function_file_content['function_name'], 
                                                          description= function_file_content['description'])
                        
                        for param in function_file_content['params']:
                            match param['type']:
                                case "bool":
                                    bool_param = TC.BoolParam(param_name=param['param_name'],
                                                    description=param['description'])
                                    
                                    # By default bool parameters will be initialized with a False value, however we dont want that for the 'active' parameter
                                    if bool_param.param_name == 'active':
                                        bool_param.set_value(True)
                                    _vision_function.bool_params_list.append(bool_param)

                                case "unsigned_int":
                                    _vision_function.unsigned_int_params_list.append(TC.UnsignedInt(param_name=param['param_name'],
                                                                                          description=param['description'],
                                                                                          max_value=param['max_val'],
                                                                                          min_value=param['min_val']))
                                case "string_list":
                                    _vision_function.list_param_list.append(TC.ParamList(param_name=param['param_name'],
                                                        description=param['description'],
                                                        values=list(param['values'])))

                                case "kernel":
                                    _vision_function.kernel_list.append(TC.Kernel(param_name=param['param_name'],
                                                        description=param['description'],
                                                        max_value=param['max_val'],
                                                        min_value=param['min_val']))

                                case "float":
                                    _vision_function.float_list.append(TC.ParamFloat(param_name=param['param_name'],
                                                        description=param['description'],
                                                        max_value=param['max_val'],
                                                        min_value=param['min_val']))
                                    
                                case "int":
                                    _vision_function.int_list.append(TC.ParamInt(param_name=param['param_name'],
                                                        description=param['description'],
                                                        max_value=param['max_val'],
                                                        min_value=param['min_val']))
                                case "string":
                                    _vision_function.string_list.append(TC.StringParam(param_name=param['param_name'],
                                                        description=param['description']))
                                    
                        self.vision_functions.append(_vision_function)
                        self.init_output.append(f"Function from file {filename} loaded successfully!")
                        #print(f"Function from file {filename} loaded successfully!")
                    except yaml.YAMLError as e:
                        self.init_output.append(f"Error loading {filename}: {e}")

                    except Exception as e:
                        self.init_output.append(f"Error loading {filename}: {e}")

        # Create List with vision function names
        self.names=[]
        for function in self.vision_functions:
            self.names.append(function.vision_function_name)

    def list_all_vision_functions(self):
        print("List of available vision functions:")
        for function in self.names:
            print(function)

    def list_all_function_dictionarys(self):
        for function in self.vision_functions:
            print(function.return_function_dictionary())

    def return_by_name(self, function_name: str) -> VisionFunction:
        for function in self.vision_functions:
            if function_name == function.vision_function_name:
                # early return
                return copy.copy(function)
        
        # Return False if function not found
        return None



if __name__ == '__main__':
    # functions_libary = VisionFunctionsLoader("/home/niklas/ros2_ws/src/pm_vision_manager/pm_vision_manager/vision_functions")
    # functions_libary.list_all_vision_functions()
    # functions_libary.list_all_function_dictionarys()
    # print(functions_libary.vision_functions_names)
    pass



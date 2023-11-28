from py_modules.vision_functions_class import VisionFunction
import py_modules.type_classes as TC
from py_modules.vision_functions_loader import VisionFunctionsLoader
import json
import os
import datetime
import copy

class VisionPipeline():
    def __init__(self, vision_yaml_libary_path) -> None:
        self.vision_functions: list[VisionFunction] = []
        self.process_name = None
        self.process_dict = {}
        self.vision_pipeline_json_dir = None
        self.vision_process_json_name_tag = 'vision_process_name'
        self.vision_process_json_pipeline_tag = 'vision_pipeline'
        self.vison_functions_libary = VisionFunctionsLoader(vision_yaml_libary_path)
        #self.vison_functions_libary.list_all_vision_functions()
        #self.vison_functions_libary.list_all_function_dictionarys()

    def remove_function_by_name(self, function_name):
        for index, function in enumerate(self.vision_functions):
            if function.vision_function_name == function_name:
                del self.vision_functions[index]

    def return_pipeline_as_str(self) -> str:
        return_str=""
        for function in self.vision_functions:
            return_str = return_str  + str(function.vision_function_name) +  ", "

        return return_str
    
    def append_vision_funciton_by_name(self, function_name) -> None:
        self.vision_functions.append(copy.deepcopy(self.vison_functions_libary.return_by_name(function_name)))

    def remove_function_by_index(self, function_index_in_pipeline: int):
        del self.vision_functions[function_index_in_pipeline]

    def vision_pipeline_to_process_list(self) -> list[dict]:
        process_list = []
        
        for function in self.vision_functions:
            process_list.append(function.function_dictionary())
        print(process_list)
        return process_list

    def set_vision_pipeline_from_process_json(self, file_path:str) -> bool:
        try:
            with open(file_path, "r") as file:
                file_data = json.load(file)
                if file_data[self.vision_process_json_pipeline_tag] == None:
                    raise Exception
                self.vision_pipeline_json_dir = os.path.dirname(file_path)
                filename = os.path.basename(file_path)
                self.process_name = os.path.splitext(filename)[0]               
                # Clear the vision functions to initialize functions from file
                # create a temporary list for the functions to append
                _vision_functions = []
                # iterate through file data
                for function in file_data[self.vision_process_json_pipeline_tag]:

                    function_found = False
                    # Check for match of function within the internal function libary
                    for lib_fun in self.vison_functions_libary.vision_functions:
                        if lib_fun.vision_function_name == next(iter(function)) and not function_found:
                            function_to_append = copy.copy(lib_fun)
                            function_found = True                         
                    
                    if function_found:
                        success = False
                        for function_key, function_dict in function.items():    # This should only run once
                            #print(function_dict)
                            for param_key, param_value in function_dict.items():
                                success = function_to_append.set_param_by_param_name(param_key,param_value)

                        # only append if value is set successfully
                        if success:
                            _vision_functions.append(function_to_append)

            # append functions to the functions object
            self.vision_functions.clear()
            self.vision_functions = copy.copy(_vision_functions)
            self.process_to_JSON()
            return True
        
        except Exception as e:
            print("Error opening process file! File might be corrupted!")
            return False
            print(e)
        # Save the pipeline to the file after opening it   
        


    def create_process_dict(self):
        self.process_dict = {self.vision_process_json_name_tag : self.process_name,
                             "process creation": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                             self.vision_process_json_pipeline_tag: self.vision_pipeline_to_process_list()}
        
    def process_to_JSON(self):
        self.create_process_dict()
        if self.process_name != None and self.vision_pipeline_json_dir!= None:
            with open(self.vision_pipeline_json_dir + '/' + self.process_name+".json", "w") as outfile: 
                json.dump(self.process_dict, outfile)

    def return_function_by_name(self, function_name: str) -> VisionFunction:
        for function in self.vision_functions:
            if function_name == function.vision_function_name:
                # early return
                return function
        return False
    
    def return_function_by_index(self, function_index_in_pipeline: int) -> VisionFunction:
        """Returns the function at the index of the vision pipeline (functions_list)"""
        function_to_return = self.vision_functions[function_index_in_pipeline]
        return function_to_return
    
    def return_function_names_list(self)-> list[VisionFunction]:
        function_names = []
        for function in self.vision_functions:
            function_names.append(function.vision_function_name)
        return function_names
        
    def move_function_to_indice(self, old_index: int, new_index:int) -> None:
        function_at_old_index = copy.deepcopy(self.vision_functions[old_index])
        del self.vision_functions[old_index]
        self.vision_functions.insert(new_index,function_at_old_index)

    def swap_functions_by_indices(self, index_1: int, index_2:int) -> None:
        """Swaps the functions in the vision pipeline given two indicies. """
        _function_old_index = copy.deepcopy(self.vision_functions[index_1])
        self.vision_functions[index_1] = copy.deepcopy(self.vision_functions[index_2])
        self.vision_functions[index_2] = _function_old_index


import sys
import os
sys.path.append(os.getcwd())
#import py_modules.type_classes as TC
import pm_vision_app.py_modules.type_classes as TC

class VisionFunction():
    SUPPORTED_CATEGORYS = ['Image Processing', 'Machine Vision', 'Camera Tools', 'Image Analysis', 'Image Tools', 'Image Conversion']

    def __init__(self,vision_function_name, description,category=None) -> None:
        self.vision_function_name = vision_function_name
        self.vision_function_description = description
        if category in self.SUPPORTED_CATEGORYS:
            self.category = category
        else:
            self.category = 'Not defined'

        self.bool_params_list: list[TC.BoolParam] = []
        self.unsigned_int_params_list: list[TC.UnsignedInt] = []
        self.list_param_list: list[TC.ParamList] = [] 
        self.kernel_list: list[TC.Kernel] = [] 
        self.float_list: list[TC.ParamFloat] = []
        self.int_list: list[TC.ParamInt] = []
        self.string_list: list[TC.StringParam] = []

        self.global_param_list=[self.bool_params_list, 
                                self.unsigned_int_params_list, 
                                self.list_param_list, 
                                self.kernel_list, 
                                self.float_list, 
                                self.int_list, 
                                self.string_list]

    def return_function_dictionary(self) -> dict:
        """
        This function returns the dictionary of a function. It iterates through all the parameters in the respective list and creates a dict.
        """
        func_dict = {}
        for param in self.bool_params_list:
            func_dict.update(param.to_dict())

        for param in self.unsigned_int_params_list:
            func_dict.update(param.to_dict())

        for param in self.list_param_list:
            func_dict.update(param.to_dict())

        for param in self.kernel_list:
            func_dict.update(param.to_dict())

        for param in self.float_list:
            func_dict.update(param.to_dict())

        for param in self.int_list:
            func_dict.update(param.to_dict())

        for param in self.string_list:
            func_dict.update(param.to_dict())

        return {str(self.vision_function_name): func_dict}

    def get_function_check_state(self) -> bool:
        for param in self.bool_params_list:
            if param.param_name == 'active':
                return param.get_value()

    def get_function_check_state_param(self) -> TC.BoolParam:
        for param in self.bool_params_list:
            if param.param_name == 'active':
                return param
                
    def set_param_by_param_name(self, param_to_set:str, new_param_value:any):
        # iterate through all list of param types
        for param_type_list in self.global_param_list:
            # iterate through the specific param type
            for param in param_type_list:
                # if param name mathes the param_to_set the value will be set. It is important to know that all the parameter in a function must have different names. This is mandatory by json format
                if param.param_name == param_to_set:
                    param.set_value(new_param_value)
                    return True
                
        return False

    def set_function_check_state(self,value: bool):
        for param in self.bool_params_list:
            if param.param_name == 'active':
                param.set_value(bool(value))

    def get_category(self)->str:
        return self.category
    
if __name__ == '__main__':
    pass

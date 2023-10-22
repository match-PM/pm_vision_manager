from pathlib import Path
from ament_index_python.packages import get_package_share_directory
from yaml.loader import SafeLoader


class VisionFunctionTypeBaseClass:
    def __init__(self,param_name, description) -> None:
        self.description = description
        self.param_name = param_name
        self._value = None

    def to_dict(self) -> dict:
        fun_dict = {str(self.param_name): self._value}
        return fun_dict
    
    def get_value(self):
        return self._value
    
class BoolParam(VisionFunctionTypeBaseClass):
    def __init__(self, param_name, description):
        super(BoolParam,self).__init__(param_name, description)
        self._default_value = False
        self._value = self._default_value

    def set_value(self, new_value):
        self._value = bool(new_value)

class StringParam(VisionFunctionTypeBaseClass):
    def __init__(self, param_name, description):
        super(StringParam,self).__init__(param_name, description)
        self._default_value = ""
        self._value = self._default_value

    def set_value(self, new_value):
        self._value = str(new_value)

class UnsignedInt(VisionFunctionTypeBaseClass):
    def __init__(self, param_name, description, min_value, max_value) -> None:
        super(UnsignedInt,self).__init__(param_name, description)
        self._default_value = min_value
        self._value = self._default_value
        self.min_val = min_value
        self.max_val = max_value  
        self.correct_min_val()  # In case the the definition in the yaml is faulty

    def set_value(self, new_value):
        self._value = int(new_value)

    def correct_min_val(self):
        if not isinstance(self.min_val, int):
            self.min_val = 0
            
        if self.min_val < 0.0:
            self.min_val = 0

class ParamList(VisionFunctionTypeBaseClass):
    def __init__(self, param_name, description, values: list) -> None:
        super(ParamList,self).__init__(param_name, description)
        self.values = values
        try:
            self._value = self.values[0]
        except:
            self._value = "Error in function_definition.yaml"

    def set_value(self, new_value):
        self._value = new_value

class ParamFloat(VisionFunctionTypeBaseClass):
    def __init__(self, param_name, description, min_value, max_value) -> None:
        super(ParamFloat,self).__init__(param_name, description)
        self.min_val = min_value
        self.max_val = max_value

        if (self.min_val == "-inf") and (self.max_val == "inf"):
            self._default_value = float(0)

        if (not isinstance(self.min_val,str) and not isinstance(self.max_val,str)):
            self._default_value = float((self.min_val+self.max_val)/2)

        if ( isinstance(self.min_val,str) and not isinstance(self.max_val,str)):
            self._default_value = float((self.max_val))

        if (not isinstance(self.min_val,str) and isinstance(self.max_val,str)):
            self._default_value = float(self.min_val)    

        self._value = self._default_value

    def set_value(self, new_value):
        self._value = float(new_value)

class ParamInt(VisionFunctionTypeBaseClass):
    def __init__(self, param_name, description, min_value, max_value) -> None:
        super(ParamInt,self).__init__(param_name, description)
        self.min_val = min_value
        self.max_val = max_value

        if (self.min_val == "-inf") and (self.max_val == "inf"):
            self._default_value = int(0)

        if (not isinstance(self.min_val,str) and not isinstance(self.max_val,str)):
            self._default_value = int((self.min_val+self.max_val)/2)

        if ( isinstance(self.min_val,str) and not isinstance(self.max_val,str)):
            self._default_value = int((self.max_val))

        if (not isinstance(self.min_val,str) and isinstance(self.max_val,str)):
            self._default_value = int(self.min_val)    

        self._value = self._default_value

    def set_value(self, new_value):
        self._value = int(new_value)


class Kernel(VisionFunctionTypeBaseClass):
    def __init__(self, param_name, description, min_value, max_value) -> None:
        super(Kernel,self).__init__(param_name, description)
        self._default_value = min_value
        self._value = self._default_value
        self.min_val = min_value
        self.max_val = max_value

    def set_value(self, new_value):
        if new_value % 2 == 0:
            # If the new value is odd, adjust it to the nearest even value
            adjusted_value = new_value + 1
            self._value = int(adjusted_value)
        else:
            self._value = int(new_value)

if __name__ == '__main__':
    test = BoolParam("test","test2")
    print(test.param_name)
    UnsignedInt

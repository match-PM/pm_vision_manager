from pathlib import Path
from ament_index_python.packages import get_package_share_directory
from yaml.loader import SafeLoader


class VisionFunctionTypeBaseClass:
    def __init__(self, param_name, description) -> None:
        self.description = description
        self.param_name = param_name
        self._value = None

    def to_dict(self) -> dict:
        fun_dict = {str(self.param_name): self._value}
        return fun_dict

    def get_value(self):
        return self._value


class BoolParam(VisionFunctionTypeBaseClass):
    def __init__(self, param_name, description, default_value = None):
        super(BoolParam, self).__init__(param_name, description)
        self._default_value = False
        self._value = self._default_value
        if default_value is not None:
            self._default_value = bool(default_value)
            self._value = self._default_value

    def set_value(self, new_value):
        self._value = bool(new_value)


class StringParam(VisionFunctionTypeBaseClass):
    def __init__(self, param_name, description, default_value = None):
        super(StringParam, self).__init__(param_name, description)

        if default_value is None:
            self._default_value = ""
        else:
            self._default_value = default_value

        self._default_value = ""
        self._value = self._default_value

    def set_value(self, new_value):
        self._value = str(new_value)


class UnsignedInt(VisionFunctionTypeBaseClass):
    def __init__(self, param_name, description, min_value, max_value, default_value = None) -> None:
        super(UnsignedInt, self).__init__(param_name, description)
        self.min_val = min_value
        self.max_val = max_value
        # Set the default value
        # if the min and max values are -inf and inf
        if (self.min_val == "-inf") and (self.max_val == "inf"):
            if default_value is None:
                self._default_value = int(0)
            else:
                if isinstance(default_value, int):
                    self._default_value = default_value
                else:
                    self._default_value = int(0)

        # if the min and max values are not -inf and inf
        elif not isinstance(self.min_val, str) and not isinstance(self.max_val, str):
            if default_value is None or not isinstance(default_value, int):
                self._default_value = int((self.min_val + self.max_val) / 2)
            else:
                if default_value > self.max_val or default_value < self.min_val:
                    self._default_value = int((self.min_val + self.max_val) / 2)
                else:
                    self._default_value = default_value

        # if the min value is not -inf and max value is inf
        elif not isinstance(self.min_val, str) and isinstance(self.max_val, str):
            if default_value is None or not isinstance(default_value, int):
                self._default_value = int((self.min_val))
            else:
                if default_value < self.min_val:
                    self._default_value = int((self.min_val))
                else:
                    self._default_value = default_value
        
        self._value = self._default_value
        self.correct_min_val()  # In case the the definition in the yaml is faulty

    def set_value(self, new_value):
        if not isinstance(self.max_val, str):
            if new_value > self.max_val:
                new_value = self.max_val
        if not isinstance(self.min_val, str):
            if new_value < self.min_val:
                new_value = self.min_val

        self._value = int(new_value)

    def correct_min_val(self):
        if not isinstance(self.min_val, int):
            self.min_val = 0

        if self.min_val < 0.0:
            self.min_val = 0


class ParamList(VisionFunctionTypeBaseClass):
    def __init__(self, param_name, description, values: list, default_value = None) -> None:
        super(ParamList, self).__init__(param_name, description)
        self.values = values
        try:
            if default_value is not None and default_value in self.values:
                self._default_value = default_value
            else:
                self._default_value = self.values[0]
            self._value = self._default_value

        except:
            self._value = "Error in function_definition.yaml"
        
    def set_value(self, new_value):
        self._value = new_value


class ParamFloat(VisionFunctionTypeBaseClass):
    def __init__(self, param_name, description, min_value, max_value, default_value = None) -> None:
        super(ParamFloat, self).__init__(param_name, description)
        self.min_val = min_value
        self.max_val = max_value

        # if the min and max values are -inf and inf
        if (self.min_val == "-inf") and (self.max_val == "inf"):
            if default_value is None:
                self._default_value = float(0)
            else:
                if isinstance(default_value, float):
                    self._default_value = default_value
                else:
                    self._default_value = float(0)

        # if the min and max values are not -inf and inf
        elif not isinstance(self.min_val, str) and not isinstance(self.max_val, str):
            if default_value is None or not isinstance(default_value, float):
                self._default_value = float((self.min_val + self.max_val) / 2)
            else:
                if default_value > self.max_val or default_value < self.min_val:
                    self._default_value = float((self.min_val + self.max_val) / 2)
                else:
                    self._default_value = default_value

        # if the min value is -inf and max value is not inf
        elif isinstance(self.min_val, str) and not isinstance(self.max_val, str):
            if default_value is None or not isinstance(default_value, float):
                self._default_value = float((self.max_val))
            else:
                if default_value > self.max_val:
                    self._default_value = float((self.max_val))
                else:
                    self._default_value = default_value

        # if the min value is not -inf and max value is inf
        elif not isinstance(self.min_val, str) and isinstance(self.max_val, str):
            if default_value is None or not isinstance(default_value, float):
                self._default_value = float((self.min_val))
            else:
                if default_value < self.min_val:
                    self._default_value = float((self.min_val))
                else:
                    self._default_value = default_value

        self._value = self._default_value

    def set_value(self, new_value):
        if not isinstance(self.max_val, str):
            if new_value > self.max_val:
                new_value = self.max_val
        if not isinstance(self.min_val, str):
            if new_value < self.min_val:
                new_value = self.min_val

        self._value = float(new_value)


class ParamInt(VisionFunctionTypeBaseClass):
    def __init__(self, param_name, description, min_value, max_value, default_value = None) -> None:
        super(ParamInt, self).__init__(param_name, description)
        self.min_val = min_value
        self.max_val = max_value

        # if the min and max values are -inf and inf
        if (self.min_val == "-inf") and (self.max_val == "inf"):
            if default_value is None:
                self._default_value = int(0)
            else:
                if isinstance(default_value, int):
                    self._default_value = default_value
                else:
                    self._default_value = int(0)

        # if the min and max values are not -inf and inf
        elif not isinstance(self.min_val, str) and not isinstance(self.max_val, str):
            if default_value is None or not isinstance(default_value, int):
                self._default_value = int((self.min_val + self.max_val) / 2)
            else:
                if default_value > self.max_val or default_value < self.min_val:
                    self._default_value = int((self.min_val + self.max_val) / 2)
                else:
                    self._default_value = default_value

        # if the min value is -inf and max value is not inf
        elif isinstance(self.min_val, str) and not isinstance(self.max_val, str):
            if default_value is None or not isinstance(default_value, int):
                self._default_value = int((self.max_val))
            else:
                if default_value > self.max_val:
                    self._default_value = int((self.max_val))
                else:
                    self._default_value = default_value

        # if the min value is not -inf and max value is inf
        elif not isinstance(self.min_val, str) and isinstance(self.max_val, str):
            if default_value is None or not isinstance(default_value, int):
                self._default_value = int((self.min_val))
            else:
                if default_value < self.min_val:
                    self._default_value = int((self.min_val))
                else:
                    self._default_value = default_value

        self._value = self._default_value


    def set_value(self, new_value):
        if not isinstance(self.max_val, str):
            if new_value > self.max_val:
                new_value = self.max_val
        if not isinstance(self.min_val, str):
            if new_value < self.min_val:
                new_value = self.min_val
        self._value = int(new_value)


class Kernel(VisionFunctionTypeBaseClass):
    def __init__(self, param_name, description, min_value, max_value, default_value = None) -> None:
        super(Kernel, self).__init__(param_name, description)

        # set the default value
        if default_value is None:
            self._default_value = min_value
        else:
            if default_value > max_value or default_value < min_value:
                self._default_value = min_value
            else:
                self._default_value = default_value
        self._default_value = min_value
        self._value = self._default_value
        self.min_val = min_value
        self.max_val = max_value

    def set_value(self, new_value):
        if not isinstance(self.max_val, str):
            if new_value > self.max_val:
                new_value = self.max_val
        if not isinstance(self.min_val, str):
            if new_value < self.min_val:
                new_value = self.min_val
        if new_value % 2 == 0:
            # If the new value is odd, adjust it to the nearest even value
            adjusted_value = new_value + 1
            self._value = int(adjusted_value)
        else:
            self._value = int(new_value)


if __name__ == "__main__":
    test = BoolParam("test", "test2")
    print(test.param_name)
    UnsignedInt

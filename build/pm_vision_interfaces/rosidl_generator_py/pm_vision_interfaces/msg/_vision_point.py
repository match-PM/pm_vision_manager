# generated from rosidl_generator_py/resource/_idl.py.em
# with input from pm_vision_interfaces:msg/VisionPoint.idl
# generated code does not contain a copyright notice


# Import statements for member types

import builtins  # noqa: E402, I100

import math  # noqa: E402, I100

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_VisionPoint(type):
    """Metaclass of message 'VisionPoint'."""

    _CREATE_ROS_MESSAGE = None
    _CONVERT_FROM_PY = None
    _CONVERT_TO_PY = None
    _DESTROY_ROS_MESSAGE = None
    _TYPE_SUPPORT = None

    __constants = {
    }

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('pm_vision_interfaces')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'pm_vision_interfaces.msg.VisionPoint')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__msg__vision_point
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__msg__vision_point
            cls._CONVERT_TO_PY = module.convert_to_py_msg__msg__vision_point
            cls._TYPE_SUPPORT = module.type_support_msg__msg__vision_point
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__msg__vision_point

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class VisionPoint(metaclass=Metaclass_VisionPoint):
    """Message class 'VisionPoint'."""

    __slots__ = [
        '_axis_value_1',
        '_axis_value_2',
        '_axis_suffix_1',
        '_axis_suffix_2',
    ]

    _fields_and_field_types = {
        'axis_value_1': 'float',
        'axis_value_2': 'float',
        'axis_suffix_1': 'string',
        'axis_suffix_2': 'string',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.axis_value_1 = kwargs.get('axis_value_1', float())
        self.axis_value_2 = kwargs.get('axis_value_2', float())
        self.axis_suffix_1 = kwargs.get('axis_suffix_1', str())
        self.axis_suffix_2 = kwargs.get('axis_suffix_2', str())

    def __repr__(self):
        typename = self.__class__.__module__.split('.')
        typename.pop()
        typename.append(self.__class__.__name__)
        args = []
        for s, t in zip(self.__slots__, self.SLOT_TYPES):
            field = getattr(self, s)
            fieldstr = repr(field)
            # We use Python array type for fields that can be directly stored
            # in them, and "normal" sequences for everything else.  If it is
            # a type that we store in an array, strip off the 'array' portion.
            if (
                isinstance(t, rosidl_parser.definition.AbstractSequence) and
                isinstance(t.value_type, rosidl_parser.definition.BasicType) and
                t.value_type.typename in ['float', 'double', 'int8', 'uint8', 'int16', 'uint16', 'int32', 'uint32', 'int64', 'uint64']
            ):
                if len(field) == 0:
                    fieldstr = '[]'
                else:
                    assert fieldstr.startswith('array(')
                    prefix = "array('X', "
                    suffix = ')'
                    fieldstr = fieldstr[len(prefix):-len(suffix)]
            args.append(s[1:] + '=' + fieldstr)
        return '%s(%s)' % ('.'.join(typename), ', '.join(args))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if self.axis_value_1 != other.axis_value_1:
            return False
        if self.axis_value_2 != other.axis_value_2:
            return False
        if self.axis_suffix_1 != other.axis_suffix_1:
            return False
        if self.axis_suffix_2 != other.axis_suffix_2:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def axis_value_1(self):
        """Message field 'axis_value_1'."""
        return self._axis_value_1

    @axis_value_1.setter
    def axis_value_1(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'axis_value_1' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'axis_value_1' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._axis_value_1 = value

    @builtins.property
    def axis_value_2(self):
        """Message field 'axis_value_2'."""
        return self._axis_value_2

    @axis_value_2.setter
    def axis_value_2(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'axis_value_2' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'axis_value_2' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._axis_value_2 = value

    @builtins.property
    def axis_suffix_1(self):
        """Message field 'axis_suffix_1'."""
        return self._axis_suffix_1

    @axis_suffix_1.setter
    def axis_suffix_1(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'axis_suffix_1' field must be of type 'str'"
        self._axis_suffix_1 = value

    @builtins.property
    def axis_suffix_2(self):
        """Message field 'axis_suffix_2'."""
        return self._axis_suffix_2

    @axis_suffix_2.setter
    def axis_suffix_2(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'axis_suffix_2' field must be of type 'str'"
        self._axis_suffix_2 = value

# generated from rosidl_generator_py/resource/_idl.py.em
# with input from pm_vision_interfaces:msg/VisionLine.idl
# generated code does not contain a copyright notice


# Import statements for member types

import builtins  # noqa: E402, I100

import math  # noqa: E402, I100

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_VisionLine(type):
    """Metaclass of message 'VisionLine'."""

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
                'pm_vision_interfaces.msg.VisionLine')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__msg__vision_line
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__msg__vision_line
            cls._CONVERT_TO_PY = module.convert_to_py_msg__msg__vision_line
            cls._TYPE_SUPPORT = module.type_support_msg__msg__vision_line
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__msg__vision_line

            from pm_vision_interfaces.msg import VisionPoint
            if VisionPoint.__class__._TYPE_SUPPORT is None:
                VisionPoint.__class__.__import_type_support__()

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class VisionLine(metaclass=Metaclass_VisionLine):
    """Message class 'VisionLine'."""

    __slots__ = [
        '_point_1',
        '_point_2',
        '_point_mid',
        '_angle',
        '_length',
    ]

    _fields_and_field_types = {
        'point_1': 'pm_vision_interfaces/VisionPoint',
        'point_2': 'pm_vision_interfaces/VisionPoint',
        'point_mid': 'pm_vision_interfaces/VisionPoint',
        'angle': 'float',
        'length': 'float',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.NamespacedType(['pm_vision_interfaces', 'msg'], 'VisionPoint'),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['pm_vision_interfaces', 'msg'], 'VisionPoint'),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['pm_vision_interfaces', 'msg'], 'VisionPoint'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        from pm_vision_interfaces.msg import VisionPoint
        self.point_1 = kwargs.get('point_1', VisionPoint())
        from pm_vision_interfaces.msg import VisionPoint
        self.point_2 = kwargs.get('point_2', VisionPoint())
        from pm_vision_interfaces.msg import VisionPoint
        self.point_mid = kwargs.get('point_mid', VisionPoint())
        self.angle = kwargs.get('angle', float())
        self.length = kwargs.get('length', float())

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
        if self.point_1 != other.point_1:
            return False
        if self.point_2 != other.point_2:
            return False
        if self.point_mid != other.point_mid:
            return False
        if self.angle != other.angle:
            return False
        if self.length != other.length:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def point_1(self):
        """Message field 'point_1'."""
        return self._point_1

    @point_1.setter
    def point_1(self, value):
        if __debug__:
            from pm_vision_interfaces.msg import VisionPoint
            assert \
                isinstance(value, VisionPoint), \
                "The 'point_1' field must be a sub message of type 'VisionPoint'"
        self._point_1 = value

    @builtins.property
    def point_2(self):
        """Message field 'point_2'."""
        return self._point_2

    @point_2.setter
    def point_2(self, value):
        if __debug__:
            from pm_vision_interfaces.msg import VisionPoint
            assert \
                isinstance(value, VisionPoint), \
                "The 'point_2' field must be a sub message of type 'VisionPoint'"
        self._point_2 = value

    @builtins.property
    def point_mid(self):
        """Message field 'point_mid'."""
        return self._point_mid

    @point_mid.setter
    def point_mid(self, value):
        if __debug__:
            from pm_vision_interfaces.msg import VisionPoint
            assert \
                isinstance(value, VisionPoint), \
                "The 'point_mid' field must be a sub message of type 'VisionPoint'"
        self._point_mid = value

    @builtins.property
    def angle(self):
        """Message field 'angle'."""
        return self._angle

    @angle.setter
    def angle(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'angle' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'angle' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._angle = value

    @builtins.property
    def length(self):
        """Message field 'length'."""
        return self._length

    @length.setter
    def length(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'length' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'length' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._length = value

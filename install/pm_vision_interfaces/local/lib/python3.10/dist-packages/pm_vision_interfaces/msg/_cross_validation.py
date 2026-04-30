# generated from rosidl_generator_py/resource/_idl.py.em
# with input from pm_vision_interfaces:msg/CrossValidation.idl
# generated code does not contain a copyright notice


# Import statements for member types

import builtins  # noqa: E402, I100

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_CrossValidation(type):
    """Metaclass of message 'CrossValidation'."""

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
                'pm_vision_interfaces.msg.CrossValidation')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__msg__cross_validation
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__msg__cross_validation
            cls._CONVERT_TO_PY = module.convert_to_py_msg__msg__cross_validation
            cls._TYPE_SUPPORT = module.type_support_msg__msg__cross_validation
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__msg__cross_validation

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class CrossValidation(metaclass=Metaclass_CrossValidation):
    """Message class 'CrossValidation'."""

    __slots__ = [
        '_image_source_name',
        '_vision_ok',
        '_failed_images',
        '_numb_images',
        '_counter_error',
    ]

    _fields_and_field_types = {
        'image_source_name': 'string',
        'vision_ok': 'boolean',
        'failed_images': 'sequence<string>',
        'numb_images': 'int32',
        'counter_error': 'int32',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
        rosidl_parser.definition.UnboundedSequence(rosidl_parser.definition.UnboundedString()),  # noqa: E501
        rosidl_parser.definition.BasicType('int32'),  # noqa: E501
        rosidl_parser.definition.BasicType('int32'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.image_source_name = kwargs.get('image_source_name', str())
        self.vision_ok = kwargs.get('vision_ok', bool())
        self.failed_images = kwargs.get('failed_images', [])
        self.numb_images = kwargs.get('numb_images', int())
        self.counter_error = kwargs.get('counter_error', int())

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
        if self.image_source_name != other.image_source_name:
            return False
        if self.vision_ok != other.vision_ok:
            return False
        if self.failed_images != other.failed_images:
            return False
        if self.numb_images != other.numb_images:
            return False
        if self.counter_error != other.counter_error:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def image_source_name(self):
        """Message field 'image_source_name'."""
        return self._image_source_name

    @image_source_name.setter
    def image_source_name(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'image_source_name' field must be of type 'str'"
        self._image_source_name = value

    @builtins.property
    def vision_ok(self):
        """Message field 'vision_ok'."""
        return self._vision_ok

    @vision_ok.setter
    def vision_ok(self, value):
        if __debug__:
            assert \
                isinstance(value, bool), \
                "The 'vision_ok' field must be of type 'bool'"
        self._vision_ok = value

    @builtins.property
    def failed_images(self):
        """Message field 'failed_images'."""
        return self._failed_images

    @failed_images.setter
    def failed_images(self, value):
        if __debug__:
            from collections.abc import Sequence
            from collections.abc import Set
            from collections import UserList
            from collections import UserString
            assert \
                ((isinstance(value, Sequence) or
                  isinstance(value, Set) or
                  isinstance(value, UserList)) and
                 not isinstance(value, str) and
                 not isinstance(value, UserString) and
                 all(isinstance(v, str) for v in value) and
                 True), \
                "The 'failed_images' field must be a set or sequence and each value of type 'str'"
        self._failed_images = value

    @builtins.property
    def numb_images(self):
        """Message field 'numb_images'."""
        return self._numb_images

    @numb_images.setter
    def numb_images(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'numb_images' field must be of type 'int'"
            assert value >= -2147483648 and value < 2147483648, \
                "The 'numb_images' field must be an integer in [-2147483648, 2147483647]"
        self._numb_images = value

    @builtins.property
    def counter_error(self):
        """Message field 'counter_error'."""
        return self._counter_error

    @counter_error.setter
    def counter_error(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'counter_error' field must be of type 'int'"
            assert value >= -2147483648 and value < 2147483648, \
                "The 'counter_error' field must be an integer in [-2147483648, 2147483647]"
        self._counter_error = value

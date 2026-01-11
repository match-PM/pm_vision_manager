# generated from rosidl_generator_py/resource/_idl.py.em
# with input from pm_vision_interfaces:msg/VisionResponse.idl
# generated code does not contain a copyright notice


# Import statements for member types

import builtins  # noqa: E402, I100

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_VisionResponse(type):
    """Metaclass of message 'VisionResponse'."""

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
                'pm_vision_interfaces.msg.VisionResponse')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__msg__vision_response
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__msg__vision_response
            cls._CONVERT_TO_PY = module.convert_to_py_msg__msg__vision_response
            cls._TYPE_SUPPORT = module.type_support_msg__msg__vision_response
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__msg__vision_response

            from pm_vision_interfaces.msg import CrossValidation
            if CrossValidation.__class__._TYPE_SUPPORT is None:
                CrossValidation.__class__.__import_type_support__()

            from pm_vision_interfaces.msg import VisionResults
            if VisionResults.__class__._TYPE_SUPPORT is None:
                VisionResults.__class__.__import_type_support__()

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class VisionResponse(metaclass=Metaclass_VisionResponse):
    """Message class 'VisionResponse'."""

    __slots__ = [
        '_vision_ok',
        '_process_name',
        '_process_uid',
        '_exec_timestamp',
        '_cross_validation',
        '_results',
    ]

    _fields_and_field_types = {
        'vision_ok': 'boolean',
        'process_name': 'string',
        'process_uid': 'string',
        'exec_timestamp': 'string',
        'cross_validation': 'pm_vision_interfaces/CrossValidation',
        'results': 'pm_vision_interfaces/VisionResults',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['pm_vision_interfaces', 'msg'], 'CrossValidation'),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['pm_vision_interfaces', 'msg'], 'VisionResults'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.vision_ok = kwargs.get('vision_ok', bool())
        self.process_name = kwargs.get('process_name', str())
        self.process_uid = kwargs.get('process_uid', str())
        self.exec_timestamp = kwargs.get('exec_timestamp', str())
        from pm_vision_interfaces.msg import CrossValidation
        self.cross_validation = kwargs.get('cross_validation', CrossValidation())
        from pm_vision_interfaces.msg import VisionResults
        self.results = kwargs.get('results', VisionResults())

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
        if self.vision_ok != other.vision_ok:
            return False
        if self.process_name != other.process_name:
            return False
        if self.process_uid != other.process_uid:
            return False
        if self.exec_timestamp != other.exec_timestamp:
            return False
        if self.cross_validation != other.cross_validation:
            return False
        if self.results != other.results:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

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
    def process_name(self):
        """Message field 'process_name'."""
        return self._process_name

    @process_name.setter
    def process_name(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'process_name' field must be of type 'str'"
        self._process_name = value

    @builtins.property
    def process_uid(self):
        """Message field 'process_uid'."""
        return self._process_uid

    @process_uid.setter
    def process_uid(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'process_uid' field must be of type 'str'"
        self._process_uid = value

    @builtins.property
    def exec_timestamp(self):
        """Message field 'exec_timestamp'."""
        return self._exec_timestamp

    @exec_timestamp.setter
    def exec_timestamp(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'exec_timestamp' field must be of type 'str'"
        self._exec_timestamp = value

    @builtins.property
    def cross_validation(self):
        """Message field 'cross_validation'."""
        return self._cross_validation

    @cross_validation.setter
    def cross_validation(self, value):
        if __debug__:
            from pm_vision_interfaces.msg import CrossValidation
            assert \
                isinstance(value, CrossValidation), \
                "The 'cross_validation' field must be a sub message of type 'CrossValidation'"
        self._cross_validation = value

    @builtins.property
    def results(self):
        """Message field 'results'."""
        return self._results

    @results.setter
    def results(self, value):
        if __debug__:
            from pm_vision_interfaces.msg import VisionResults
            assert \
                isinstance(value, VisionResults), \
                "The 'results' field must be a sub message of type 'VisionResults'"
        self._results = value

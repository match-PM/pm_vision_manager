# generated from rosidl_generator_py/resource/_idl.py.em
# with input from pm_vision_interfaces:msg/VisionResults.idl
# generated code does not contain a copyright notice


# Import statements for member types

import builtins  # noqa: E402, I100

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_VisionResults(type):
    """Metaclass of message 'VisionResults'."""

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
                'pm_vision_interfaces.msg.VisionResults')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__msg__vision_results
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__msg__vision_results
            cls._CONVERT_TO_PY = module.convert_to_py_msg__msg__vision_results
            cls._TYPE_SUPPORT = module.type_support_msg__msg__vision_results
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__msg__vision_results

            from pm_vision_interfaces.msg import ImageSharpness
            if ImageSharpness.__class__._TYPE_SUPPORT is None:
                ImageSharpness.__class__.__import_type_support__()

            from pm_vision_interfaces.msg import VisionArea
            if VisionArea.__class__._TYPE_SUPPORT is None:
                VisionArea.__class__.__import_type_support__()

            from pm_vision_interfaces.msg import VisionCircle
            if VisionCircle.__class__._TYPE_SUPPORT is None:
                VisionCircle.__class__.__import_type_support__()

            from pm_vision_interfaces.msg import VisionLine
            if VisionLine.__class__._TYPE_SUPPORT is None:
                VisionLine.__class__.__import_type_support__()

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


class VisionResults(metaclass=Metaclass_VisionResults):
    """Message class 'VisionResults'."""

    __slots__ = [
        '_points',
        '_lines',
        '_areas',
        '_circles',
        '_image_sharpness',
    ]

    _fields_and_field_types = {
        'points': 'sequence<pm_vision_interfaces/VisionPoint>',
        'lines': 'sequence<pm_vision_interfaces/VisionLine>',
        'areas': 'sequence<pm_vision_interfaces/VisionArea>',
        'circles': 'sequence<pm_vision_interfaces/VisionCircle>',
        'image_sharpness': 'pm_vision_interfaces/ImageSharpness',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.UnboundedSequence(rosidl_parser.definition.NamespacedType(['pm_vision_interfaces', 'msg'], 'VisionPoint')),  # noqa: E501
        rosidl_parser.definition.UnboundedSequence(rosidl_parser.definition.NamespacedType(['pm_vision_interfaces', 'msg'], 'VisionLine')),  # noqa: E501
        rosidl_parser.definition.UnboundedSequence(rosidl_parser.definition.NamespacedType(['pm_vision_interfaces', 'msg'], 'VisionArea')),  # noqa: E501
        rosidl_parser.definition.UnboundedSequence(rosidl_parser.definition.NamespacedType(['pm_vision_interfaces', 'msg'], 'VisionCircle')),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['pm_vision_interfaces', 'msg'], 'ImageSharpness'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.points = kwargs.get('points', [])
        self.lines = kwargs.get('lines', [])
        self.areas = kwargs.get('areas', [])
        self.circles = kwargs.get('circles', [])
        from pm_vision_interfaces.msg import ImageSharpness
        self.image_sharpness = kwargs.get('image_sharpness', ImageSharpness())

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
        if self.points != other.points:
            return False
        if self.lines != other.lines:
            return False
        if self.areas != other.areas:
            return False
        if self.circles != other.circles:
            return False
        if self.image_sharpness != other.image_sharpness:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def points(self):
        """Message field 'points'."""
        return self._points

    @points.setter
    def points(self, value):
        if __debug__:
            from pm_vision_interfaces.msg import VisionPoint
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
                 all(isinstance(v, VisionPoint) for v in value) and
                 True), \
                "The 'points' field must be a set or sequence and each value of type 'VisionPoint'"
        self._points = value

    @builtins.property
    def lines(self):
        """Message field 'lines'."""
        return self._lines

    @lines.setter
    def lines(self, value):
        if __debug__:
            from pm_vision_interfaces.msg import VisionLine
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
                 all(isinstance(v, VisionLine) for v in value) and
                 True), \
                "The 'lines' field must be a set or sequence and each value of type 'VisionLine'"
        self._lines = value

    @builtins.property
    def areas(self):
        """Message field 'areas'."""
        return self._areas

    @areas.setter
    def areas(self, value):
        if __debug__:
            from pm_vision_interfaces.msg import VisionArea
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
                 all(isinstance(v, VisionArea) for v in value) and
                 True), \
                "The 'areas' field must be a set or sequence and each value of type 'VisionArea'"
        self._areas = value

    @builtins.property
    def circles(self):
        """Message field 'circles'."""
        return self._circles

    @circles.setter
    def circles(self, value):
        if __debug__:
            from pm_vision_interfaces.msg import VisionCircle
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
                 all(isinstance(v, VisionCircle) for v in value) and
                 True), \
                "The 'circles' field must be a set or sequence and each value of type 'VisionCircle'"
        self._circles = value

    @builtins.property
    def image_sharpness(self):
        """Message field 'image_sharpness'."""
        return self._image_sharpness

    @image_sharpness.setter
    def image_sharpness(self, value):
        if __debug__:
            from pm_vision_interfaces.msg import ImageSharpness
            assert \
                isinstance(value, ImageSharpness), \
                "The 'image_sharpness' field must be a sub message of type 'ImageSharpness'"
        self._image_sharpness = value

// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from pm_vision_interfaces:msg/VisionPoint.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "pm_vision_interfaces/msg/detail/vision_point__rosidl_typesupport_introspection_c.h"
#include "pm_vision_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "pm_vision_interfaces/msg/detail/vision_point__functions.h"
#include "pm_vision_interfaces/msg/detail/vision_point__struct.h"


// Include directives for member types
// Member `axis_suffix_1`
// Member `axis_suffix_2`
#include "rosidl_runtime_c/string_functions.h"

#ifdef __cplusplus
extern "C"
{
#endif

void pm_vision_interfaces__msg__VisionPoint__rosidl_typesupport_introspection_c__VisionPoint_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  pm_vision_interfaces__msg__VisionPoint__init(message_memory);
}

void pm_vision_interfaces__msg__VisionPoint__rosidl_typesupport_introspection_c__VisionPoint_fini_function(void * message_memory)
{
  pm_vision_interfaces__msg__VisionPoint__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember pm_vision_interfaces__msg__VisionPoint__rosidl_typesupport_introspection_c__VisionPoint_message_member_array[4] = {
  {
    "axis_value_1",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(pm_vision_interfaces__msg__VisionPoint, axis_value_1),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "axis_value_2",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(pm_vision_interfaces__msg__VisionPoint, axis_value_2),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "axis_suffix_1",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(pm_vision_interfaces__msg__VisionPoint, axis_suffix_1),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "axis_suffix_2",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(pm_vision_interfaces__msg__VisionPoint, axis_suffix_2),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers pm_vision_interfaces__msg__VisionPoint__rosidl_typesupport_introspection_c__VisionPoint_message_members = {
  "pm_vision_interfaces__msg",  // message namespace
  "VisionPoint",  // message name
  4,  // number of fields
  sizeof(pm_vision_interfaces__msg__VisionPoint),
  pm_vision_interfaces__msg__VisionPoint__rosidl_typesupport_introspection_c__VisionPoint_message_member_array,  // message members
  pm_vision_interfaces__msg__VisionPoint__rosidl_typesupport_introspection_c__VisionPoint_init_function,  // function to initialize message memory (memory has to be allocated)
  pm_vision_interfaces__msg__VisionPoint__rosidl_typesupport_introspection_c__VisionPoint_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t pm_vision_interfaces__msg__VisionPoint__rosidl_typesupport_introspection_c__VisionPoint_message_type_support_handle = {
  0,
  &pm_vision_interfaces__msg__VisionPoint__rosidl_typesupport_introspection_c__VisionPoint_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_pm_vision_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, pm_vision_interfaces, msg, VisionPoint)() {
  if (!pm_vision_interfaces__msg__VisionPoint__rosidl_typesupport_introspection_c__VisionPoint_message_type_support_handle.typesupport_identifier) {
    pm_vision_interfaces__msg__VisionPoint__rosidl_typesupport_introspection_c__VisionPoint_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &pm_vision_interfaces__msg__VisionPoint__rosidl_typesupport_introspection_c__VisionPoint_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from pm_vision_interfaces:msg/CrossValidation.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "pm_vision_interfaces/msg/detail/cross_validation__rosidl_typesupport_introspection_c.h"
#include "pm_vision_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "pm_vision_interfaces/msg/detail/cross_validation__functions.h"
#include "pm_vision_interfaces/msg/detail/cross_validation__struct.h"


// Include directives for member types
// Member `image_source_name`
// Member `failed_images`
#include "rosidl_runtime_c/string_functions.h"

#ifdef __cplusplus
extern "C"
{
#endif

void pm_vision_interfaces__msg__CrossValidation__rosidl_typesupport_introspection_c__CrossValidation_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  pm_vision_interfaces__msg__CrossValidation__init(message_memory);
}

void pm_vision_interfaces__msg__CrossValidation__rosidl_typesupport_introspection_c__CrossValidation_fini_function(void * message_memory)
{
  pm_vision_interfaces__msg__CrossValidation__fini(message_memory);
}

size_t pm_vision_interfaces__msg__CrossValidation__rosidl_typesupport_introspection_c__size_function__CrossValidation__failed_images(
  const void * untyped_member)
{
  const rosidl_runtime_c__String__Sequence * member =
    (const rosidl_runtime_c__String__Sequence *)(untyped_member);
  return member->size;
}

const void * pm_vision_interfaces__msg__CrossValidation__rosidl_typesupport_introspection_c__get_const_function__CrossValidation__failed_images(
  const void * untyped_member, size_t index)
{
  const rosidl_runtime_c__String__Sequence * member =
    (const rosidl_runtime_c__String__Sequence *)(untyped_member);
  return &member->data[index];
}

void * pm_vision_interfaces__msg__CrossValidation__rosidl_typesupport_introspection_c__get_function__CrossValidation__failed_images(
  void * untyped_member, size_t index)
{
  rosidl_runtime_c__String__Sequence * member =
    (rosidl_runtime_c__String__Sequence *)(untyped_member);
  return &member->data[index];
}

void pm_vision_interfaces__msg__CrossValidation__rosidl_typesupport_introspection_c__fetch_function__CrossValidation__failed_images(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const rosidl_runtime_c__String * item =
    ((const rosidl_runtime_c__String *)
    pm_vision_interfaces__msg__CrossValidation__rosidl_typesupport_introspection_c__get_const_function__CrossValidation__failed_images(untyped_member, index));
  rosidl_runtime_c__String * value =
    (rosidl_runtime_c__String *)(untyped_value);
  *value = *item;
}

void pm_vision_interfaces__msg__CrossValidation__rosidl_typesupport_introspection_c__assign_function__CrossValidation__failed_images(
  void * untyped_member, size_t index, const void * untyped_value)
{
  rosidl_runtime_c__String * item =
    ((rosidl_runtime_c__String *)
    pm_vision_interfaces__msg__CrossValidation__rosidl_typesupport_introspection_c__get_function__CrossValidation__failed_images(untyped_member, index));
  const rosidl_runtime_c__String * value =
    (const rosidl_runtime_c__String *)(untyped_value);
  *item = *value;
}

bool pm_vision_interfaces__msg__CrossValidation__rosidl_typesupport_introspection_c__resize_function__CrossValidation__failed_images(
  void * untyped_member, size_t size)
{
  rosidl_runtime_c__String__Sequence * member =
    (rosidl_runtime_c__String__Sequence *)(untyped_member);
  rosidl_runtime_c__String__Sequence__fini(member);
  return rosidl_runtime_c__String__Sequence__init(member, size);
}

static rosidl_typesupport_introspection_c__MessageMember pm_vision_interfaces__msg__CrossValidation__rosidl_typesupport_introspection_c__CrossValidation_message_member_array[5] = {
  {
    "image_source_name",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(pm_vision_interfaces__msg__CrossValidation, image_source_name),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "vision_ok",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_BOOLEAN,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(pm_vision_interfaces__msg__CrossValidation, vision_ok),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "failed_images",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(pm_vision_interfaces__msg__CrossValidation, failed_images),  // bytes offset in struct
    NULL,  // default value
    pm_vision_interfaces__msg__CrossValidation__rosidl_typesupport_introspection_c__size_function__CrossValidation__failed_images,  // size() function pointer
    pm_vision_interfaces__msg__CrossValidation__rosidl_typesupport_introspection_c__get_const_function__CrossValidation__failed_images,  // get_const(index) function pointer
    pm_vision_interfaces__msg__CrossValidation__rosidl_typesupport_introspection_c__get_function__CrossValidation__failed_images,  // get(index) function pointer
    pm_vision_interfaces__msg__CrossValidation__rosidl_typesupport_introspection_c__fetch_function__CrossValidation__failed_images,  // fetch(index, &value) function pointer
    pm_vision_interfaces__msg__CrossValidation__rosidl_typesupport_introspection_c__assign_function__CrossValidation__failed_images,  // assign(index, value) function pointer
    pm_vision_interfaces__msg__CrossValidation__rosidl_typesupport_introspection_c__resize_function__CrossValidation__failed_images  // resize(index) function pointer
  },
  {
    "numb_images",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_INT32,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(pm_vision_interfaces__msg__CrossValidation, numb_images),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "counter_error",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_INT32,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(pm_vision_interfaces__msg__CrossValidation, counter_error),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers pm_vision_interfaces__msg__CrossValidation__rosidl_typesupport_introspection_c__CrossValidation_message_members = {
  "pm_vision_interfaces__msg",  // message namespace
  "CrossValidation",  // message name
  5,  // number of fields
  sizeof(pm_vision_interfaces__msg__CrossValidation),
  pm_vision_interfaces__msg__CrossValidation__rosidl_typesupport_introspection_c__CrossValidation_message_member_array,  // message members
  pm_vision_interfaces__msg__CrossValidation__rosidl_typesupport_introspection_c__CrossValidation_init_function,  // function to initialize message memory (memory has to be allocated)
  pm_vision_interfaces__msg__CrossValidation__rosidl_typesupport_introspection_c__CrossValidation_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t pm_vision_interfaces__msg__CrossValidation__rosidl_typesupport_introspection_c__CrossValidation_message_type_support_handle = {
  0,
  &pm_vision_interfaces__msg__CrossValidation__rosidl_typesupport_introspection_c__CrossValidation_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_pm_vision_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, pm_vision_interfaces, msg, CrossValidation)() {
  if (!pm_vision_interfaces__msg__CrossValidation__rosidl_typesupport_introspection_c__CrossValidation_message_type_support_handle.typesupport_identifier) {
    pm_vision_interfaces__msg__CrossValidation__rosidl_typesupport_introspection_c__CrossValidation_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &pm_vision_interfaces__msg__CrossValidation__rosidl_typesupport_introspection_c__CrossValidation_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

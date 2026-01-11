// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from pm_vision_interfaces:msg/VisionResults.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "pm_vision_interfaces/msg/detail/vision_results__rosidl_typesupport_introspection_c.h"
#include "pm_vision_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "pm_vision_interfaces/msg/detail/vision_results__functions.h"
#include "pm_vision_interfaces/msg/detail/vision_results__struct.h"


// Include directives for member types
// Member `points`
#include "pm_vision_interfaces/msg/vision_point.h"
// Member `points`
#include "pm_vision_interfaces/msg/detail/vision_point__rosidl_typesupport_introspection_c.h"
// Member `lines`
#include "pm_vision_interfaces/msg/vision_line.h"
// Member `lines`
#include "pm_vision_interfaces/msg/detail/vision_line__rosidl_typesupport_introspection_c.h"
// Member `areas`
#include "pm_vision_interfaces/msg/vision_area.h"
// Member `areas`
#include "pm_vision_interfaces/msg/detail/vision_area__rosidl_typesupport_introspection_c.h"
// Member `circles`
#include "pm_vision_interfaces/msg/vision_circle.h"
// Member `circles`
#include "pm_vision_interfaces/msg/detail/vision_circle__rosidl_typesupport_introspection_c.h"
// Member `image_sharpness`
#include "pm_vision_interfaces/msg/image_sharpness.h"
// Member `image_sharpness`
#include "pm_vision_interfaces/msg/detail/image_sharpness__rosidl_typesupport_introspection_c.h"

#ifdef __cplusplus
extern "C"
{
#endif

void pm_vision_interfaces__msg__VisionResults__rosidl_typesupport_introspection_c__VisionResults_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  pm_vision_interfaces__msg__VisionResults__init(message_memory);
}

void pm_vision_interfaces__msg__VisionResults__rosidl_typesupport_introspection_c__VisionResults_fini_function(void * message_memory)
{
  pm_vision_interfaces__msg__VisionResults__fini(message_memory);
}

size_t pm_vision_interfaces__msg__VisionResults__rosidl_typesupport_introspection_c__size_function__VisionResults__points(
  const void * untyped_member)
{
  const pm_vision_interfaces__msg__VisionPoint__Sequence * member =
    (const pm_vision_interfaces__msg__VisionPoint__Sequence *)(untyped_member);
  return member->size;
}

const void * pm_vision_interfaces__msg__VisionResults__rosidl_typesupport_introspection_c__get_const_function__VisionResults__points(
  const void * untyped_member, size_t index)
{
  const pm_vision_interfaces__msg__VisionPoint__Sequence * member =
    (const pm_vision_interfaces__msg__VisionPoint__Sequence *)(untyped_member);
  return &member->data[index];
}

void * pm_vision_interfaces__msg__VisionResults__rosidl_typesupport_introspection_c__get_function__VisionResults__points(
  void * untyped_member, size_t index)
{
  pm_vision_interfaces__msg__VisionPoint__Sequence * member =
    (pm_vision_interfaces__msg__VisionPoint__Sequence *)(untyped_member);
  return &member->data[index];
}

void pm_vision_interfaces__msg__VisionResults__rosidl_typesupport_introspection_c__fetch_function__VisionResults__points(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const pm_vision_interfaces__msg__VisionPoint * item =
    ((const pm_vision_interfaces__msg__VisionPoint *)
    pm_vision_interfaces__msg__VisionResults__rosidl_typesupport_introspection_c__get_const_function__VisionResults__points(untyped_member, index));
  pm_vision_interfaces__msg__VisionPoint * value =
    (pm_vision_interfaces__msg__VisionPoint *)(untyped_value);
  *value = *item;
}

void pm_vision_interfaces__msg__VisionResults__rosidl_typesupport_introspection_c__assign_function__VisionResults__points(
  void * untyped_member, size_t index, const void * untyped_value)
{
  pm_vision_interfaces__msg__VisionPoint * item =
    ((pm_vision_interfaces__msg__VisionPoint *)
    pm_vision_interfaces__msg__VisionResults__rosidl_typesupport_introspection_c__get_function__VisionResults__points(untyped_member, index));
  const pm_vision_interfaces__msg__VisionPoint * value =
    (const pm_vision_interfaces__msg__VisionPoint *)(untyped_value);
  *item = *value;
}

bool pm_vision_interfaces__msg__VisionResults__rosidl_typesupport_introspection_c__resize_function__VisionResults__points(
  void * untyped_member, size_t size)
{
  pm_vision_interfaces__msg__VisionPoint__Sequence * member =
    (pm_vision_interfaces__msg__VisionPoint__Sequence *)(untyped_member);
  pm_vision_interfaces__msg__VisionPoint__Sequence__fini(member);
  return pm_vision_interfaces__msg__VisionPoint__Sequence__init(member, size);
}

size_t pm_vision_interfaces__msg__VisionResults__rosidl_typesupport_introspection_c__size_function__VisionResults__lines(
  const void * untyped_member)
{
  const pm_vision_interfaces__msg__VisionLine__Sequence * member =
    (const pm_vision_interfaces__msg__VisionLine__Sequence *)(untyped_member);
  return member->size;
}

const void * pm_vision_interfaces__msg__VisionResults__rosidl_typesupport_introspection_c__get_const_function__VisionResults__lines(
  const void * untyped_member, size_t index)
{
  const pm_vision_interfaces__msg__VisionLine__Sequence * member =
    (const pm_vision_interfaces__msg__VisionLine__Sequence *)(untyped_member);
  return &member->data[index];
}

void * pm_vision_interfaces__msg__VisionResults__rosidl_typesupport_introspection_c__get_function__VisionResults__lines(
  void * untyped_member, size_t index)
{
  pm_vision_interfaces__msg__VisionLine__Sequence * member =
    (pm_vision_interfaces__msg__VisionLine__Sequence *)(untyped_member);
  return &member->data[index];
}

void pm_vision_interfaces__msg__VisionResults__rosidl_typesupport_introspection_c__fetch_function__VisionResults__lines(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const pm_vision_interfaces__msg__VisionLine * item =
    ((const pm_vision_interfaces__msg__VisionLine *)
    pm_vision_interfaces__msg__VisionResults__rosidl_typesupport_introspection_c__get_const_function__VisionResults__lines(untyped_member, index));
  pm_vision_interfaces__msg__VisionLine * value =
    (pm_vision_interfaces__msg__VisionLine *)(untyped_value);
  *value = *item;
}

void pm_vision_interfaces__msg__VisionResults__rosidl_typesupport_introspection_c__assign_function__VisionResults__lines(
  void * untyped_member, size_t index, const void * untyped_value)
{
  pm_vision_interfaces__msg__VisionLine * item =
    ((pm_vision_interfaces__msg__VisionLine *)
    pm_vision_interfaces__msg__VisionResults__rosidl_typesupport_introspection_c__get_function__VisionResults__lines(untyped_member, index));
  const pm_vision_interfaces__msg__VisionLine * value =
    (const pm_vision_interfaces__msg__VisionLine *)(untyped_value);
  *item = *value;
}

bool pm_vision_interfaces__msg__VisionResults__rosidl_typesupport_introspection_c__resize_function__VisionResults__lines(
  void * untyped_member, size_t size)
{
  pm_vision_interfaces__msg__VisionLine__Sequence * member =
    (pm_vision_interfaces__msg__VisionLine__Sequence *)(untyped_member);
  pm_vision_interfaces__msg__VisionLine__Sequence__fini(member);
  return pm_vision_interfaces__msg__VisionLine__Sequence__init(member, size);
}

size_t pm_vision_interfaces__msg__VisionResults__rosidl_typesupport_introspection_c__size_function__VisionResults__areas(
  const void * untyped_member)
{
  const pm_vision_interfaces__msg__VisionArea__Sequence * member =
    (const pm_vision_interfaces__msg__VisionArea__Sequence *)(untyped_member);
  return member->size;
}

const void * pm_vision_interfaces__msg__VisionResults__rosidl_typesupport_introspection_c__get_const_function__VisionResults__areas(
  const void * untyped_member, size_t index)
{
  const pm_vision_interfaces__msg__VisionArea__Sequence * member =
    (const pm_vision_interfaces__msg__VisionArea__Sequence *)(untyped_member);
  return &member->data[index];
}

void * pm_vision_interfaces__msg__VisionResults__rosidl_typesupport_introspection_c__get_function__VisionResults__areas(
  void * untyped_member, size_t index)
{
  pm_vision_interfaces__msg__VisionArea__Sequence * member =
    (pm_vision_interfaces__msg__VisionArea__Sequence *)(untyped_member);
  return &member->data[index];
}

void pm_vision_interfaces__msg__VisionResults__rosidl_typesupport_introspection_c__fetch_function__VisionResults__areas(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const pm_vision_interfaces__msg__VisionArea * item =
    ((const pm_vision_interfaces__msg__VisionArea *)
    pm_vision_interfaces__msg__VisionResults__rosidl_typesupport_introspection_c__get_const_function__VisionResults__areas(untyped_member, index));
  pm_vision_interfaces__msg__VisionArea * value =
    (pm_vision_interfaces__msg__VisionArea *)(untyped_value);
  *value = *item;
}

void pm_vision_interfaces__msg__VisionResults__rosidl_typesupport_introspection_c__assign_function__VisionResults__areas(
  void * untyped_member, size_t index, const void * untyped_value)
{
  pm_vision_interfaces__msg__VisionArea * item =
    ((pm_vision_interfaces__msg__VisionArea *)
    pm_vision_interfaces__msg__VisionResults__rosidl_typesupport_introspection_c__get_function__VisionResults__areas(untyped_member, index));
  const pm_vision_interfaces__msg__VisionArea * value =
    (const pm_vision_interfaces__msg__VisionArea *)(untyped_value);
  *item = *value;
}

bool pm_vision_interfaces__msg__VisionResults__rosidl_typesupport_introspection_c__resize_function__VisionResults__areas(
  void * untyped_member, size_t size)
{
  pm_vision_interfaces__msg__VisionArea__Sequence * member =
    (pm_vision_interfaces__msg__VisionArea__Sequence *)(untyped_member);
  pm_vision_interfaces__msg__VisionArea__Sequence__fini(member);
  return pm_vision_interfaces__msg__VisionArea__Sequence__init(member, size);
}

size_t pm_vision_interfaces__msg__VisionResults__rosidl_typesupport_introspection_c__size_function__VisionResults__circles(
  const void * untyped_member)
{
  const pm_vision_interfaces__msg__VisionCircle__Sequence * member =
    (const pm_vision_interfaces__msg__VisionCircle__Sequence *)(untyped_member);
  return member->size;
}

const void * pm_vision_interfaces__msg__VisionResults__rosidl_typesupport_introspection_c__get_const_function__VisionResults__circles(
  const void * untyped_member, size_t index)
{
  const pm_vision_interfaces__msg__VisionCircle__Sequence * member =
    (const pm_vision_interfaces__msg__VisionCircle__Sequence *)(untyped_member);
  return &member->data[index];
}

void * pm_vision_interfaces__msg__VisionResults__rosidl_typesupport_introspection_c__get_function__VisionResults__circles(
  void * untyped_member, size_t index)
{
  pm_vision_interfaces__msg__VisionCircle__Sequence * member =
    (pm_vision_interfaces__msg__VisionCircle__Sequence *)(untyped_member);
  return &member->data[index];
}

void pm_vision_interfaces__msg__VisionResults__rosidl_typesupport_introspection_c__fetch_function__VisionResults__circles(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const pm_vision_interfaces__msg__VisionCircle * item =
    ((const pm_vision_interfaces__msg__VisionCircle *)
    pm_vision_interfaces__msg__VisionResults__rosidl_typesupport_introspection_c__get_const_function__VisionResults__circles(untyped_member, index));
  pm_vision_interfaces__msg__VisionCircle * value =
    (pm_vision_interfaces__msg__VisionCircle *)(untyped_value);
  *value = *item;
}

void pm_vision_interfaces__msg__VisionResults__rosidl_typesupport_introspection_c__assign_function__VisionResults__circles(
  void * untyped_member, size_t index, const void * untyped_value)
{
  pm_vision_interfaces__msg__VisionCircle * item =
    ((pm_vision_interfaces__msg__VisionCircle *)
    pm_vision_interfaces__msg__VisionResults__rosidl_typesupport_introspection_c__get_function__VisionResults__circles(untyped_member, index));
  const pm_vision_interfaces__msg__VisionCircle * value =
    (const pm_vision_interfaces__msg__VisionCircle *)(untyped_value);
  *item = *value;
}

bool pm_vision_interfaces__msg__VisionResults__rosidl_typesupport_introspection_c__resize_function__VisionResults__circles(
  void * untyped_member, size_t size)
{
  pm_vision_interfaces__msg__VisionCircle__Sequence * member =
    (pm_vision_interfaces__msg__VisionCircle__Sequence *)(untyped_member);
  pm_vision_interfaces__msg__VisionCircle__Sequence__fini(member);
  return pm_vision_interfaces__msg__VisionCircle__Sequence__init(member, size);
}

static rosidl_typesupport_introspection_c__MessageMember pm_vision_interfaces__msg__VisionResults__rosidl_typesupport_introspection_c__VisionResults_message_member_array[5] = {
  {
    "points",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(pm_vision_interfaces__msg__VisionResults, points),  // bytes offset in struct
    NULL,  // default value
    pm_vision_interfaces__msg__VisionResults__rosidl_typesupport_introspection_c__size_function__VisionResults__points,  // size() function pointer
    pm_vision_interfaces__msg__VisionResults__rosidl_typesupport_introspection_c__get_const_function__VisionResults__points,  // get_const(index) function pointer
    pm_vision_interfaces__msg__VisionResults__rosidl_typesupport_introspection_c__get_function__VisionResults__points,  // get(index) function pointer
    pm_vision_interfaces__msg__VisionResults__rosidl_typesupport_introspection_c__fetch_function__VisionResults__points,  // fetch(index, &value) function pointer
    pm_vision_interfaces__msg__VisionResults__rosidl_typesupport_introspection_c__assign_function__VisionResults__points,  // assign(index, value) function pointer
    pm_vision_interfaces__msg__VisionResults__rosidl_typesupport_introspection_c__resize_function__VisionResults__points  // resize(index) function pointer
  },
  {
    "lines",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(pm_vision_interfaces__msg__VisionResults, lines),  // bytes offset in struct
    NULL,  // default value
    pm_vision_interfaces__msg__VisionResults__rosidl_typesupport_introspection_c__size_function__VisionResults__lines,  // size() function pointer
    pm_vision_interfaces__msg__VisionResults__rosidl_typesupport_introspection_c__get_const_function__VisionResults__lines,  // get_const(index) function pointer
    pm_vision_interfaces__msg__VisionResults__rosidl_typesupport_introspection_c__get_function__VisionResults__lines,  // get(index) function pointer
    pm_vision_interfaces__msg__VisionResults__rosidl_typesupport_introspection_c__fetch_function__VisionResults__lines,  // fetch(index, &value) function pointer
    pm_vision_interfaces__msg__VisionResults__rosidl_typesupport_introspection_c__assign_function__VisionResults__lines,  // assign(index, value) function pointer
    pm_vision_interfaces__msg__VisionResults__rosidl_typesupport_introspection_c__resize_function__VisionResults__lines  // resize(index) function pointer
  },
  {
    "areas",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(pm_vision_interfaces__msg__VisionResults, areas),  // bytes offset in struct
    NULL,  // default value
    pm_vision_interfaces__msg__VisionResults__rosidl_typesupport_introspection_c__size_function__VisionResults__areas,  // size() function pointer
    pm_vision_interfaces__msg__VisionResults__rosidl_typesupport_introspection_c__get_const_function__VisionResults__areas,  // get_const(index) function pointer
    pm_vision_interfaces__msg__VisionResults__rosidl_typesupport_introspection_c__get_function__VisionResults__areas,  // get(index) function pointer
    pm_vision_interfaces__msg__VisionResults__rosidl_typesupport_introspection_c__fetch_function__VisionResults__areas,  // fetch(index, &value) function pointer
    pm_vision_interfaces__msg__VisionResults__rosidl_typesupport_introspection_c__assign_function__VisionResults__areas,  // assign(index, value) function pointer
    pm_vision_interfaces__msg__VisionResults__rosidl_typesupport_introspection_c__resize_function__VisionResults__areas  // resize(index) function pointer
  },
  {
    "circles",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(pm_vision_interfaces__msg__VisionResults, circles),  // bytes offset in struct
    NULL,  // default value
    pm_vision_interfaces__msg__VisionResults__rosidl_typesupport_introspection_c__size_function__VisionResults__circles,  // size() function pointer
    pm_vision_interfaces__msg__VisionResults__rosidl_typesupport_introspection_c__get_const_function__VisionResults__circles,  // get_const(index) function pointer
    pm_vision_interfaces__msg__VisionResults__rosidl_typesupport_introspection_c__get_function__VisionResults__circles,  // get(index) function pointer
    pm_vision_interfaces__msg__VisionResults__rosidl_typesupport_introspection_c__fetch_function__VisionResults__circles,  // fetch(index, &value) function pointer
    pm_vision_interfaces__msg__VisionResults__rosidl_typesupport_introspection_c__assign_function__VisionResults__circles,  // assign(index, value) function pointer
    pm_vision_interfaces__msg__VisionResults__rosidl_typesupport_introspection_c__resize_function__VisionResults__circles  // resize(index) function pointer
  },
  {
    "image_sharpness",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(pm_vision_interfaces__msg__VisionResults, image_sharpness),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers pm_vision_interfaces__msg__VisionResults__rosidl_typesupport_introspection_c__VisionResults_message_members = {
  "pm_vision_interfaces__msg",  // message namespace
  "VisionResults",  // message name
  5,  // number of fields
  sizeof(pm_vision_interfaces__msg__VisionResults),
  pm_vision_interfaces__msg__VisionResults__rosidl_typesupport_introspection_c__VisionResults_message_member_array,  // message members
  pm_vision_interfaces__msg__VisionResults__rosidl_typesupport_introspection_c__VisionResults_init_function,  // function to initialize message memory (memory has to be allocated)
  pm_vision_interfaces__msg__VisionResults__rosidl_typesupport_introspection_c__VisionResults_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t pm_vision_interfaces__msg__VisionResults__rosidl_typesupport_introspection_c__VisionResults_message_type_support_handle = {
  0,
  &pm_vision_interfaces__msg__VisionResults__rosidl_typesupport_introspection_c__VisionResults_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_pm_vision_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, pm_vision_interfaces, msg, VisionResults)() {
  pm_vision_interfaces__msg__VisionResults__rosidl_typesupport_introspection_c__VisionResults_message_member_array[0].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, pm_vision_interfaces, msg, VisionPoint)();
  pm_vision_interfaces__msg__VisionResults__rosidl_typesupport_introspection_c__VisionResults_message_member_array[1].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, pm_vision_interfaces, msg, VisionLine)();
  pm_vision_interfaces__msg__VisionResults__rosidl_typesupport_introspection_c__VisionResults_message_member_array[2].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, pm_vision_interfaces, msg, VisionArea)();
  pm_vision_interfaces__msg__VisionResults__rosidl_typesupport_introspection_c__VisionResults_message_member_array[3].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, pm_vision_interfaces, msg, VisionCircle)();
  pm_vision_interfaces__msg__VisionResults__rosidl_typesupport_introspection_c__VisionResults_message_member_array[4].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, pm_vision_interfaces, msg, ImageSharpness)();
  if (!pm_vision_interfaces__msg__VisionResults__rosidl_typesupport_introspection_c__VisionResults_message_type_support_handle.typesupport_identifier) {
    pm_vision_interfaces__msg__VisionResults__rosidl_typesupport_introspection_c__VisionResults_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &pm_vision_interfaces__msg__VisionResults__rosidl_typesupport_introspection_c__VisionResults_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

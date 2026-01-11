// generated from rosidl_typesupport_fastrtps_c/resource/idl__type_support_c.cpp.em
// with input from pm_vision_interfaces:msg/VisionLine.idl
// generated code does not contain a copyright notice
#include "pm_vision_interfaces/msg/detail/vision_line__rosidl_typesupport_fastrtps_c.h"


#include <cassert>
#include <limits>
#include <string>
#include "rosidl_typesupport_fastrtps_c/identifier.h"
#include "rosidl_typesupport_fastrtps_c/wstring_conversion.hpp"
#include "rosidl_typesupport_fastrtps_cpp/message_type_support.h"
#include "pm_vision_interfaces/msg/rosidl_typesupport_fastrtps_c__visibility_control.h"
#include "pm_vision_interfaces/msg/detail/vision_line__struct.h"
#include "pm_vision_interfaces/msg/detail/vision_line__functions.h"
#include "fastcdr/Cdr.h"

#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-parameter"
# ifdef __clang__
#  pragma clang diagnostic ignored "-Wdeprecated-register"
#  pragma clang diagnostic ignored "-Wreturn-type-c-linkage"
# endif
#endif
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif

// includes and forward declarations of message dependencies and their conversion functions

#if defined(__cplusplus)
extern "C"
{
#endif

#include "pm_vision_interfaces/msg/detail/vision_point__functions.h"  // point_1, point_2, point_mid

// forward declare type support functions
size_t get_serialized_size_pm_vision_interfaces__msg__VisionPoint(
  const void * untyped_ros_message,
  size_t current_alignment);

size_t max_serialized_size_pm_vision_interfaces__msg__VisionPoint(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

const rosidl_message_type_support_t *
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, pm_vision_interfaces, msg, VisionPoint)();


using _VisionLine__ros_msg_type = pm_vision_interfaces__msg__VisionLine;

static bool _VisionLine__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  const _VisionLine__ros_msg_type * ros_message = static_cast<const _VisionLine__ros_msg_type *>(untyped_ros_message);
  // Field name: point_1
  {
    const message_type_support_callbacks_t * callbacks =
      static_cast<const message_type_support_callbacks_t *>(
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(
        rosidl_typesupport_fastrtps_c, pm_vision_interfaces, msg, VisionPoint
      )()->data);
    if (!callbacks->cdr_serialize(
        &ros_message->point_1, cdr))
    {
      return false;
    }
  }

  // Field name: point_2
  {
    const message_type_support_callbacks_t * callbacks =
      static_cast<const message_type_support_callbacks_t *>(
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(
        rosidl_typesupport_fastrtps_c, pm_vision_interfaces, msg, VisionPoint
      )()->data);
    if (!callbacks->cdr_serialize(
        &ros_message->point_2, cdr))
    {
      return false;
    }
  }

  // Field name: point_mid
  {
    const message_type_support_callbacks_t * callbacks =
      static_cast<const message_type_support_callbacks_t *>(
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(
        rosidl_typesupport_fastrtps_c, pm_vision_interfaces, msg, VisionPoint
      )()->data);
    if (!callbacks->cdr_serialize(
        &ros_message->point_mid, cdr))
    {
      return false;
    }
  }

  // Field name: angle
  {
    cdr << ros_message->angle;
  }

  // Field name: length
  {
    cdr << ros_message->length;
  }

  return true;
}

static bool _VisionLine__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  _VisionLine__ros_msg_type * ros_message = static_cast<_VisionLine__ros_msg_type *>(untyped_ros_message);
  // Field name: point_1
  {
    const message_type_support_callbacks_t * callbacks =
      static_cast<const message_type_support_callbacks_t *>(
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(
        rosidl_typesupport_fastrtps_c, pm_vision_interfaces, msg, VisionPoint
      )()->data);
    if (!callbacks->cdr_deserialize(
        cdr, &ros_message->point_1))
    {
      return false;
    }
  }

  // Field name: point_2
  {
    const message_type_support_callbacks_t * callbacks =
      static_cast<const message_type_support_callbacks_t *>(
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(
        rosidl_typesupport_fastrtps_c, pm_vision_interfaces, msg, VisionPoint
      )()->data);
    if (!callbacks->cdr_deserialize(
        cdr, &ros_message->point_2))
    {
      return false;
    }
  }

  // Field name: point_mid
  {
    const message_type_support_callbacks_t * callbacks =
      static_cast<const message_type_support_callbacks_t *>(
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(
        rosidl_typesupport_fastrtps_c, pm_vision_interfaces, msg, VisionPoint
      )()->data);
    if (!callbacks->cdr_deserialize(
        cdr, &ros_message->point_mid))
    {
      return false;
    }
  }

  // Field name: angle
  {
    cdr >> ros_message->angle;
  }

  // Field name: length
  {
    cdr >> ros_message->length;
  }

  return true;
}  // NOLINT(readability/fn_size)

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_pm_vision_interfaces
size_t get_serialized_size_pm_vision_interfaces__msg__VisionLine(
  const void * untyped_ros_message,
  size_t current_alignment)
{
  const _VisionLine__ros_msg_type * ros_message = static_cast<const _VisionLine__ros_msg_type *>(untyped_ros_message);
  (void)ros_message;
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // field.name point_1

  current_alignment += get_serialized_size_pm_vision_interfaces__msg__VisionPoint(
    &(ros_message->point_1), current_alignment);
  // field.name point_2

  current_alignment += get_serialized_size_pm_vision_interfaces__msg__VisionPoint(
    &(ros_message->point_2), current_alignment);
  // field.name point_mid

  current_alignment += get_serialized_size_pm_vision_interfaces__msg__VisionPoint(
    &(ros_message->point_mid), current_alignment);
  // field.name angle
  {
    size_t item_size = sizeof(ros_message->angle);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name length
  {
    size_t item_size = sizeof(ros_message->length);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  return current_alignment - initial_alignment;
}

static uint32_t _VisionLine__get_serialized_size(const void * untyped_ros_message)
{
  return static_cast<uint32_t>(
    get_serialized_size_pm_vision_interfaces__msg__VisionLine(
      untyped_ros_message, 0));
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_pm_vision_interfaces
size_t max_serialized_size_pm_vision_interfaces__msg__VisionLine(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  size_t last_member_size = 0;
  (void)last_member_size;
  (void)padding;
  (void)wchar_size;

  full_bounded = true;
  is_plain = true;

  // member: point_1
  {
    size_t array_size = 1;


    last_member_size = 0;
    for (size_t index = 0; index < array_size; ++index) {
      bool inner_full_bounded;
      bool inner_is_plain;
      size_t inner_size;
      inner_size =
        max_serialized_size_pm_vision_interfaces__msg__VisionPoint(
        inner_full_bounded, inner_is_plain, current_alignment);
      last_member_size += inner_size;
      current_alignment += inner_size;
      full_bounded &= inner_full_bounded;
      is_plain &= inner_is_plain;
    }
  }
  // member: point_2
  {
    size_t array_size = 1;


    last_member_size = 0;
    for (size_t index = 0; index < array_size; ++index) {
      bool inner_full_bounded;
      bool inner_is_plain;
      size_t inner_size;
      inner_size =
        max_serialized_size_pm_vision_interfaces__msg__VisionPoint(
        inner_full_bounded, inner_is_plain, current_alignment);
      last_member_size += inner_size;
      current_alignment += inner_size;
      full_bounded &= inner_full_bounded;
      is_plain &= inner_is_plain;
    }
  }
  // member: point_mid
  {
    size_t array_size = 1;


    last_member_size = 0;
    for (size_t index = 0; index < array_size; ++index) {
      bool inner_full_bounded;
      bool inner_is_plain;
      size_t inner_size;
      inner_size =
        max_serialized_size_pm_vision_interfaces__msg__VisionPoint(
        inner_full_bounded, inner_is_plain, current_alignment);
      last_member_size += inner_size;
      current_alignment += inner_size;
      full_bounded &= inner_full_bounded;
      is_plain &= inner_is_plain;
    }
  }
  // member: angle
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }
  // member: length
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }

  size_t ret_val = current_alignment - initial_alignment;
  if (is_plain) {
    // All members are plain, and type is not empty.
    // We still need to check that the in-memory alignment
    // is the same as the CDR mandated alignment.
    using DataType = pm_vision_interfaces__msg__VisionLine;
    is_plain =
      (
      offsetof(DataType, length) +
      last_member_size
      ) == ret_val;
  }

  return ret_val;
}

static size_t _VisionLine__max_serialized_size(char & bounds_info)
{
  bool full_bounded;
  bool is_plain;
  size_t ret_val;

  ret_val = max_serialized_size_pm_vision_interfaces__msg__VisionLine(
    full_bounded, is_plain, 0);

  bounds_info =
    is_plain ? ROSIDL_TYPESUPPORT_FASTRTPS_PLAIN_TYPE :
    full_bounded ? ROSIDL_TYPESUPPORT_FASTRTPS_BOUNDED_TYPE : ROSIDL_TYPESUPPORT_FASTRTPS_UNBOUNDED_TYPE;
  return ret_val;
}


static message_type_support_callbacks_t __callbacks_VisionLine = {
  "pm_vision_interfaces::msg",
  "VisionLine",
  _VisionLine__cdr_serialize,
  _VisionLine__cdr_deserialize,
  _VisionLine__get_serialized_size,
  _VisionLine__max_serialized_size
};

static rosidl_message_type_support_t _VisionLine__type_support = {
  rosidl_typesupport_fastrtps_c__identifier,
  &__callbacks_VisionLine,
  get_message_typesupport_handle_function,
};

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, pm_vision_interfaces, msg, VisionLine)() {
  return &_VisionLine__type_support;
}

#if defined(__cplusplus)
}
#endif

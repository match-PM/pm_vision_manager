// generated from rosidl_typesupport_fastrtps_cpp/resource/idl__type_support.cpp.em
// with input from pm_vision_interfaces:msg/VisionPoint.idl
// generated code does not contain a copyright notice
#include "pm_vision_interfaces/msg/detail/vision_point__rosidl_typesupport_fastrtps_cpp.hpp"
#include "pm_vision_interfaces/msg/detail/vision_point__struct.hpp"

#include <limits>
#include <stdexcept>
#include <string>
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_fastrtps_cpp/identifier.hpp"
#include "rosidl_typesupport_fastrtps_cpp/message_type_support.h"
#include "rosidl_typesupport_fastrtps_cpp/message_type_support_decl.hpp"
#include "rosidl_typesupport_fastrtps_cpp/wstring_conversion.hpp"
#include "fastcdr/Cdr.h"


// forward declaration of message dependencies and their conversion functions

namespace pm_vision_interfaces
{

namespace msg
{

namespace typesupport_fastrtps_cpp
{

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_pm_vision_interfaces
cdr_serialize(
  const pm_vision_interfaces::msg::VisionPoint & ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  // Member: axis_value_1
  cdr << ros_message.axis_value_1;
  // Member: axis_value_2
  cdr << ros_message.axis_value_2;
  // Member: axis_suffix_1
  cdr << ros_message.axis_suffix_1;
  // Member: axis_suffix_2
  cdr << ros_message.axis_suffix_2;
  return true;
}

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_pm_vision_interfaces
cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  pm_vision_interfaces::msg::VisionPoint & ros_message)
{
  // Member: axis_value_1
  cdr >> ros_message.axis_value_1;

  // Member: axis_value_2
  cdr >> ros_message.axis_value_2;

  // Member: axis_suffix_1
  cdr >> ros_message.axis_suffix_1;

  // Member: axis_suffix_2
  cdr >> ros_message.axis_suffix_2;

  return true;
}

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_pm_vision_interfaces
get_serialized_size(
  const pm_vision_interfaces::msg::VisionPoint & ros_message,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // Member: axis_value_1
  {
    size_t item_size = sizeof(ros_message.axis_value_1);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // Member: axis_value_2
  {
    size_t item_size = sizeof(ros_message.axis_value_2);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // Member: axis_suffix_1
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message.axis_suffix_1.size() + 1);
  // Member: axis_suffix_2
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message.axis_suffix_2.size() + 1);

  return current_alignment - initial_alignment;
}

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_pm_vision_interfaces
max_serialized_size_VisionPoint(
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


  // Member: axis_value_1
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }

  // Member: axis_value_2
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }

  // Member: axis_suffix_1
  {
    size_t array_size = 1;

    full_bounded = false;
    is_plain = false;
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += padding +
        eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
        1;
    }
  }

  // Member: axis_suffix_2
  {
    size_t array_size = 1;

    full_bounded = false;
    is_plain = false;
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += padding +
        eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
        1;
    }
  }

  size_t ret_val = current_alignment - initial_alignment;
  if (is_plain) {
    // All members are plain, and type is not empty.
    // We still need to check that the in-memory alignment
    // is the same as the CDR mandated alignment.
    using DataType = pm_vision_interfaces::msg::VisionPoint;
    is_plain =
      (
      offsetof(DataType, axis_suffix_2) +
      last_member_size
      ) == ret_val;
  }

  return ret_val;
}

static bool _VisionPoint__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  auto typed_message =
    static_cast<const pm_vision_interfaces::msg::VisionPoint *>(
    untyped_ros_message);
  return cdr_serialize(*typed_message, cdr);
}

static bool _VisionPoint__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  auto typed_message =
    static_cast<pm_vision_interfaces::msg::VisionPoint *>(
    untyped_ros_message);
  return cdr_deserialize(cdr, *typed_message);
}

static uint32_t _VisionPoint__get_serialized_size(
  const void * untyped_ros_message)
{
  auto typed_message =
    static_cast<const pm_vision_interfaces::msg::VisionPoint *>(
    untyped_ros_message);
  return static_cast<uint32_t>(get_serialized_size(*typed_message, 0));
}

static size_t _VisionPoint__max_serialized_size(char & bounds_info)
{
  bool full_bounded;
  bool is_plain;
  size_t ret_val;

  ret_val = max_serialized_size_VisionPoint(full_bounded, is_plain, 0);

  bounds_info =
    is_plain ? ROSIDL_TYPESUPPORT_FASTRTPS_PLAIN_TYPE :
    full_bounded ? ROSIDL_TYPESUPPORT_FASTRTPS_BOUNDED_TYPE : ROSIDL_TYPESUPPORT_FASTRTPS_UNBOUNDED_TYPE;
  return ret_val;
}

static message_type_support_callbacks_t _VisionPoint__callbacks = {
  "pm_vision_interfaces::msg",
  "VisionPoint",
  _VisionPoint__cdr_serialize,
  _VisionPoint__cdr_deserialize,
  _VisionPoint__get_serialized_size,
  _VisionPoint__max_serialized_size
};

static rosidl_message_type_support_t _VisionPoint__handle = {
  rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
  &_VisionPoint__callbacks,
  get_message_typesupport_handle_function,
};

}  // namespace typesupport_fastrtps_cpp

}  // namespace msg

}  // namespace pm_vision_interfaces

namespace rosidl_typesupport_fastrtps_cpp
{

template<>
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_EXPORT_pm_vision_interfaces
const rosidl_message_type_support_t *
get_message_type_support_handle<pm_vision_interfaces::msg::VisionPoint>()
{
  return &pm_vision_interfaces::msg::typesupport_fastrtps_cpp::_VisionPoint__handle;
}

}  // namespace rosidl_typesupport_fastrtps_cpp

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, pm_vision_interfaces, msg, VisionPoint)() {
  return &pm_vision_interfaces::msg::typesupport_fastrtps_cpp::_VisionPoint__handle;
}

#ifdef __cplusplus
}
#endif

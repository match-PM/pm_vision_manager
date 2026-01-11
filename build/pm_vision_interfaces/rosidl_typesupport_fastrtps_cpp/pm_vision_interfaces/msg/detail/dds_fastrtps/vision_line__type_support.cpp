// generated from rosidl_typesupport_fastrtps_cpp/resource/idl__type_support.cpp.em
// with input from pm_vision_interfaces:msg/VisionLine.idl
// generated code does not contain a copyright notice
#include "pm_vision_interfaces/msg/detail/vision_line__rosidl_typesupport_fastrtps_cpp.hpp"
#include "pm_vision_interfaces/msg/detail/vision_line__struct.hpp"

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
bool cdr_serialize(
  const pm_vision_interfaces::msg::VisionPoint &,
  eprosima::fastcdr::Cdr &);
bool cdr_deserialize(
  eprosima::fastcdr::Cdr &,
  pm_vision_interfaces::msg::VisionPoint &);
size_t get_serialized_size(
  const pm_vision_interfaces::msg::VisionPoint &,
  size_t current_alignment);
size_t
max_serialized_size_VisionPoint(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);
}  // namespace typesupport_fastrtps_cpp
}  // namespace msg
}  // namespace pm_vision_interfaces

// functions for pm_vision_interfaces::msg::VisionPoint already declared above

// functions for pm_vision_interfaces::msg::VisionPoint already declared above


namespace pm_vision_interfaces
{

namespace msg
{

namespace typesupport_fastrtps_cpp
{

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_pm_vision_interfaces
cdr_serialize(
  const pm_vision_interfaces::msg::VisionLine & ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  // Member: point_1
  pm_vision_interfaces::msg::typesupport_fastrtps_cpp::cdr_serialize(
    ros_message.point_1,
    cdr);
  // Member: point_2
  pm_vision_interfaces::msg::typesupport_fastrtps_cpp::cdr_serialize(
    ros_message.point_2,
    cdr);
  // Member: point_mid
  pm_vision_interfaces::msg::typesupport_fastrtps_cpp::cdr_serialize(
    ros_message.point_mid,
    cdr);
  // Member: angle
  cdr << ros_message.angle;
  // Member: length
  cdr << ros_message.length;
  return true;
}

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_pm_vision_interfaces
cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  pm_vision_interfaces::msg::VisionLine & ros_message)
{
  // Member: point_1
  pm_vision_interfaces::msg::typesupport_fastrtps_cpp::cdr_deserialize(
    cdr, ros_message.point_1);

  // Member: point_2
  pm_vision_interfaces::msg::typesupport_fastrtps_cpp::cdr_deserialize(
    cdr, ros_message.point_2);

  // Member: point_mid
  pm_vision_interfaces::msg::typesupport_fastrtps_cpp::cdr_deserialize(
    cdr, ros_message.point_mid);

  // Member: angle
  cdr >> ros_message.angle;

  // Member: length
  cdr >> ros_message.length;

  return true;
}

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_pm_vision_interfaces
get_serialized_size(
  const pm_vision_interfaces::msg::VisionLine & ros_message,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // Member: point_1

  current_alignment +=
    pm_vision_interfaces::msg::typesupport_fastrtps_cpp::get_serialized_size(
    ros_message.point_1, current_alignment);
  // Member: point_2

  current_alignment +=
    pm_vision_interfaces::msg::typesupport_fastrtps_cpp::get_serialized_size(
    ros_message.point_2, current_alignment);
  // Member: point_mid

  current_alignment +=
    pm_vision_interfaces::msg::typesupport_fastrtps_cpp::get_serialized_size(
    ros_message.point_mid, current_alignment);
  // Member: angle
  {
    size_t item_size = sizeof(ros_message.angle);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // Member: length
  {
    size_t item_size = sizeof(ros_message.length);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  return current_alignment - initial_alignment;
}

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_pm_vision_interfaces
max_serialized_size_VisionLine(
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


  // Member: point_1
  {
    size_t array_size = 1;


    last_member_size = 0;
    for (size_t index = 0; index < array_size; ++index) {
      bool inner_full_bounded;
      bool inner_is_plain;
      size_t inner_size =
        pm_vision_interfaces::msg::typesupport_fastrtps_cpp::max_serialized_size_VisionPoint(
        inner_full_bounded, inner_is_plain, current_alignment);
      last_member_size += inner_size;
      current_alignment += inner_size;
      full_bounded &= inner_full_bounded;
      is_plain &= inner_is_plain;
    }
  }

  // Member: point_2
  {
    size_t array_size = 1;


    last_member_size = 0;
    for (size_t index = 0; index < array_size; ++index) {
      bool inner_full_bounded;
      bool inner_is_plain;
      size_t inner_size =
        pm_vision_interfaces::msg::typesupport_fastrtps_cpp::max_serialized_size_VisionPoint(
        inner_full_bounded, inner_is_plain, current_alignment);
      last_member_size += inner_size;
      current_alignment += inner_size;
      full_bounded &= inner_full_bounded;
      is_plain &= inner_is_plain;
    }
  }

  // Member: point_mid
  {
    size_t array_size = 1;


    last_member_size = 0;
    for (size_t index = 0; index < array_size; ++index) {
      bool inner_full_bounded;
      bool inner_is_plain;
      size_t inner_size =
        pm_vision_interfaces::msg::typesupport_fastrtps_cpp::max_serialized_size_VisionPoint(
        inner_full_bounded, inner_is_plain, current_alignment);
      last_member_size += inner_size;
      current_alignment += inner_size;
      full_bounded &= inner_full_bounded;
      is_plain &= inner_is_plain;
    }
  }

  // Member: angle
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }

  // Member: length
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
    using DataType = pm_vision_interfaces::msg::VisionLine;
    is_plain =
      (
      offsetof(DataType, length) +
      last_member_size
      ) == ret_val;
  }

  return ret_val;
}

static bool _VisionLine__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  auto typed_message =
    static_cast<const pm_vision_interfaces::msg::VisionLine *>(
    untyped_ros_message);
  return cdr_serialize(*typed_message, cdr);
}

static bool _VisionLine__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  auto typed_message =
    static_cast<pm_vision_interfaces::msg::VisionLine *>(
    untyped_ros_message);
  return cdr_deserialize(cdr, *typed_message);
}

static uint32_t _VisionLine__get_serialized_size(
  const void * untyped_ros_message)
{
  auto typed_message =
    static_cast<const pm_vision_interfaces::msg::VisionLine *>(
    untyped_ros_message);
  return static_cast<uint32_t>(get_serialized_size(*typed_message, 0));
}

static size_t _VisionLine__max_serialized_size(char & bounds_info)
{
  bool full_bounded;
  bool is_plain;
  size_t ret_val;

  ret_val = max_serialized_size_VisionLine(full_bounded, is_plain, 0);

  bounds_info =
    is_plain ? ROSIDL_TYPESUPPORT_FASTRTPS_PLAIN_TYPE :
    full_bounded ? ROSIDL_TYPESUPPORT_FASTRTPS_BOUNDED_TYPE : ROSIDL_TYPESUPPORT_FASTRTPS_UNBOUNDED_TYPE;
  return ret_val;
}

static message_type_support_callbacks_t _VisionLine__callbacks = {
  "pm_vision_interfaces::msg",
  "VisionLine",
  _VisionLine__cdr_serialize,
  _VisionLine__cdr_deserialize,
  _VisionLine__get_serialized_size,
  _VisionLine__max_serialized_size
};

static rosidl_message_type_support_t _VisionLine__handle = {
  rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
  &_VisionLine__callbacks,
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
get_message_type_support_handle<pm_vision_interfaces::msg::VisionLine>()
{
  return &pm_vision_interfaces::msg::typesupport_fastrtps_cpp::_VisionLine__handle;
}

}  // namespace rosidl_typesupport_fastrtps_cpp

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, pm_vision_interfaces, msg, VisionLine)() {
  return &pm_vision_interfaces::msg::typesupport_fastrtps_cpp::_VisionLine__handle;
}

#ifdef __cplusplus
}
#endif

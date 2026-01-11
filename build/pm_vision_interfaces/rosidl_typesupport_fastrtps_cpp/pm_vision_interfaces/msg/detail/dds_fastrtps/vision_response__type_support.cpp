// generated from rosidl_typesupport_fastrtps_cpp/resource/idl__type_support.cpp.em
// with input from pm_vision_interfaces:msg/VisionResponse.idl
// generated code does not contain a copyright notice
#include "pm_vision_interfaces/msg/detail/vision_response__rosidl_typesupport_fastrtps_cpp.hpp"
#include "pm_vision_interfaces/msg/detail/vision_response__struct.hpp"

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
  const pm_vision_interfaces::msg::CrossValidation &,
  eprosima::fastcdr::Cdr &);
bool cdr_deserialize(
  eprosima::fastcdr::Cdr &,
  pm_vision_interfaces::msg::CrossValidation &);
size_t get_serialized_size(
  const pm_vision_interfaces::msg::CrossValidation &,
  size_t current_alignment);
size_t
max_serialized_size_CrossValidation(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);
}  // namespace typesupport_fastrtps_cpp
}  // namespace msg
}  // namespace pm_vision_interfaces

namespace pm_vision_interfaces
{
namespace msg
{
namespace typesupport_fastrtps_cpp
{
bool cdr_serialize(
  const pm_vision_interfaces::msg::VisionResults &,
  eprosima::fastcdr::Cdr &);
bool cdr_deserialize(
  eprosima::fastcdr::Cdr &,
  pm_vision_interfaces::msg::VisionResults &);
size_t get_serialized_size(
  const pm_vision_interfaces::msg::VisionResults &,
  size_t current_alignment);
size_t
max_serialized_size_VisionResults(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);
}  // namespace typesupport_fastrtps_cpp
}  // namespace msg
}  // namespace pm_vision_interfaces


namespace pm_vision_interfaces
{

namespace msg
{

namespace typesupport_fastrtps_cpp
{

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_pm_vision_interfaces
cdr_serialize(
  const pm_vision_interfaces::msg::VisionResponse & ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  // Member: vision_ok
  cdr << (ros_message.vision_ok ? true : false);
  // Member: process_name
  cdr << ros_message.process_name;
  // Member: process_uid
  cdr << ros_message.process_uid;
  // Member: exec_timestamp
  cdr << ros_message.exec_timestamp;
  // Member: cross_validation
  pm_vision_interfaces::msg::typesupport_fastrtps_cpp::cdr_serialize(
    ros_message.cross_validation,
    cdr);
  // Member: results
  pm_vision_interfaces::msg::typesupport_fastrtps_cpp::cdr_serialize(
    ros_message.results,
    cdr);
  return true;
}

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_pm_vision_interfaces
cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  pm_vision_interfaces::msg::VisionResponse & ros_message)
{
  // Member: vision_ok
  {
    uint8_t tmp;
    cdr >> tmp;
    ros_message.vision_ok = tmp ? true : false;
  }

  // Member: process_name
  cdr >> ros_message.process_name;

  // Member: process_uid
  cdr >> ros_message.process_uid;

  // Member: exec_timestamp
  cdr >> ros_message.exec_timestamp;

  // Member: cross_validation
  pm_vision_interfaces::msg::typesupport_fastrtps_cpp::cdr_deserialize(
    cdr, ros_message.cross_validation);

  // Member: results
  pm_vision_interfaces::msg::typesupport_fastrtps_cpp::cdr_deserialize(
    cdr, ros_message.results);

  return true;
}

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_pm_vision_interfaces
get_serialized_size(
  const pm_vision_interfaces::msg::VisionResponse & ros_message,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // Member: vision_ok
  {
    size_t item_size = sizeof(ros_message.vision_ok);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // Member: process_name
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message.process_name.size() + 1);
  // Member: process_uid
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message.process_uid.size() + 1);
  // Member: exec_timestamp
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message.exec_timestamp.size() + 1);
  // Member: cross_validation

  current_alignment +=
    pm_vision_interfaces::msg::typesupport_fastrtps_cpp::get_serialized_size(
    ros_message.cross_validation, current_alignment);
  // Member: results

  current_alignment +=
    pm_vision_interfaces::msg::typesupport_fastrtps_cpp::get_serialized_size(
    ros_message.results, current_alignment);

  return current_alignment - initial_alignment;
}

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_pm_vision_interfaces
max_serialized_size_VisionResponse(
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


  // Member: vision_ok
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }

  // Member: process_name
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

  // Member: process_uid
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

  // Member: exec_timestamp
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

  // Member: cross_validation
  {
    size_t array_size = 1;


    last_member_size = 0;
    for (size_t index = 0; index < array_size; ++index) {
      bool inner_full_bounded;
      bool inner_is_plain;
      size_t inner_size =
        pm_vision_interfaces::msg::typesupport_fastrtps_cpp::max_serialized_size_CrossValidation(
        inner_full_bounded, inner_is_plain, current_alignment);
      last_member_size += inner_size;
      current_alignment += inner_size;
      full_bounded &= inner_full_bounded;
      is_plain &= inner_is_plain;
    }
  }

  // Member: results
  {
    size_t array_size = 1;


    last_member_size = 0;
    for (size_t index = 0; index < array_size; ++index) {
      bool inner_full_bounded;
      bool inner_is_plain;
      size_t inner_size =
        pm_vision_interfaces::msg::typesupport_fastrtps_cpp::max_serialized_size_VisionResults(
        inner_full_bounded, inner_is_plain, current_alignment);
      last_member_size += inner_size;
      current_alignment += inner_size;
      full_bounded &= inner_full_bounded;
      is_plain &= inner_is_plain;
    }
  }

  size_t ret_val = current_alignment - initial_alignment;
  if (is_plain) {
    // All members are plain, and type is not empty.
    // We still need to check that the in-memory alignment
    // is the same as the CDR mandated alignment.
    using DataType = pm_vision_interfaces::msg::VisionResponse;
    is_plain =
      (
      offsetof(DataType, results) +
      last_member_size
      ) == ret_val;
  }

  return ret_val;
}

static bool _VisionResponse__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  auto typed_message =
    static_cast<const pm_vision_interfaces::msg::VisionResponse *>(
    untyped_ros_message);
  return cdr_serialize(*typed_message, cdr);
}

static bool _VisionResponse__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  auto typed_message =
    static_cast<pm_vision_interfaces::msg::VisionResponse *>(
    untyped_ros_message);
  return cdr_deserialize(cdr, *typed_message);
}

static uint32_t _VisionResponse__get_serialized_size(
  const void * untyped_ros_message)
{
  auto typed_message =
    static_cast<const pm_vision_interfaces::msg::VisionResponse *>(
    untyped_ros_message);
  return static_cast<uint32_t>(get_serialized_size(*typed_message, 0));
}

static size_t _VisionResponse__max_serialized_size(char & bounds_info)
{
  bool full_bounded;
  bool is_plain;
  size_t ret_val;

  ret_val = max_serialized_size_VisionResponse(full_bounded, is_plain, 0);

  bounds_info =
    is_plain ? ROSIDL_TYPESUPPORT_FASTRTPS_PLAIN_TYPE :
    full_bounded ? ROSIDL_TYPESUPPORT_FASTRTPS_BOUNDED_TYPE : ROSIDL_TYPESUPPORT_FASTRTPS_UNBOUNDED_TYPE;
  return ret_val;
}

static message_type_support_callbacks_t _VisionResponse__callbacks = {
  "pm_vision_interfaces::msg",
  "VisionResponse",
  _VisionResponse__cdr_serialize,
  _VisionResponse__cdr_deserialize,
  _VisionResponse__get_serialized_size,
  _VisionResponse__max_serialized_size
};

static rosidl_message_type_support_t _VisionResponse__handle = {
  rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
  &_VisionResponse__callbacks,
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
get_message_type_support_handle<pm_vision_interfaces::msg::VisionResponse>()
{
  return &pm_vision_interfaces::msg::typesupport_fastrtps_cpp::_VisionResponse__handle;
}

}  // namespace rosidl_typesupport_fastrtps_cpp

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, pm_vision_interfaces, msg, VisionResponse)() {
  return &pm_vision_interfaces::msg::typesupport_fastrtps_cpp::_VisionResponse__handle;
}

#ifdef __cplusplus
}
#endif

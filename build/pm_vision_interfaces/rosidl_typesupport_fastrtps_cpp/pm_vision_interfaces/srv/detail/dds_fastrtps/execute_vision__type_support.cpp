// generated from rosidl_typesupport_fastrtps_cpp/resource/idl__type_support.cpp.em
// with input from pm_vision_interfaces:srv/ExecuteVision.idl
// generated code does not contain a copyright notice
#include "pm_vision_interfaces/srv/detail/execute_vision__rosidl_typesupport_fastrtps_cpp.hpp"
#include "pm_vision_interfaces/srv/detail/execute_vision__struct.hpp"

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

namespace srv
{

namespace typesupport_fastrtps_cpp
{

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_pm_vision_interfaces
cdr_serialize(
  const pm_vision_interfaces::srv::ExecuteVision_Request & ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  // Member: process_filename
  cdr << ros_message.process_filename;
  // Member: camera_config_filename
  cdr << ros_message.camera_config_filename;
  // Member: process_uid
  cdr << ros_message.process_uid;
  // Member: image_display_time
  cdr << ros_message.image_display_time;
  // Member: run_cross_validation
  cdr << (ros_message.run_cross_validation ? true : false);
  return true;
}

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_pm_vision_interfaces
cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  pm_vision_interfaces::srv::ExecuteVision_Request & ros_message)
{
  // Member: process_filename
  cdr >> ros_message.process_filename;

  // Member: camera_config_filename
  cdr >> ros_message.camera_config_filename;

  // Member: process_uid
  cdr >> ros_message.process_uid;

  // Member: image_display_time
  cdr >> ros_message.image_display_time;

  // Member: run_cross_validation
  {
    uint8_t tmp;
    cdr >> tmp;
    ros_message.run_cross_validation = tmp ? true : false;
  }

  return true;
}

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_pm_vision_interfaces
get_serialized_size(
  const pm_vision_interfaces::srv::ExecuteVision_Request & ros_message,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // Member: process_filename
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message.process_filename.size() + 1);
  // Member: camera_config_filename
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message.camera_config_filename.size() + 1);
  // Member: process_uid
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message.process_uid.size() + 1);
  // Member: image_display_time
  {
    size_t item_size = sizeof(ros_message.image_display_time);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // Member: run_cross_validation
  {
    size_t item_size = sizeof(ros_message.run_cross_validation);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  return current_alignment - initial_alignment;
}

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_pm_vision_interfaces
max_serialized_size_ExecuteVision_Request(
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


  // Member: process_filename
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

  // Member: camera_config_filename
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

  // Member: image_display_time
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint64_t);
    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }

  // Member: run_cross_validation
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }

  size_t ret_val = current_alignment - initial_alignment;
  if (is_plain) {
    // All members are plain, and type is not empty.
    // We still need to check that the in-memory alignment
    // is the same as the CDR mandated alignment.
    using DataType = pm_vision_interfaces::srv::ExecuteVision_Request;
    is_plain =
      (
      offsetof(DataType, run_cross_validation) +
      last_member_size
      ) == ret_val;
  }

  return ret_val;
}

static bool _ExecuteVision_Request__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  auto typed_message =
    static_cast<const pm_vision_interfaces::srv::ExecuteVision_Request *>(
    untyped_ros_message);
  return cdr_serialize(*typed_message, cdr);
}

static bool _ExecuteVision_Request__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  auto typed_message =
    static_cast<pm_vision_interfaces::srv::ExecuteVision_Request *>(
    untyped_ros_message);
  return cdr_deserialize(cdr, *typed_message);
}

static uint32_t _ExecuteVision_Request__get_serialized_size(
  const void * untyped_ros_message)
{
  auto typed_message =
    static_cast<const pm_vision_interfaces::srv::ExecuteVision_Request *>(
    untyped_ros_message);
  return static_cast<uint32_t>(get_serialized_size(*typed_message, 0));
}

static size_t _ExecuteVision_Request__max_serialized_size(char & bounds_info)
{
  bool full_bounded;
  bool is_plain;
  size_t ret_val;

  ret_val = max_serialized_size_ExecuteVision_Request(full_bounded, is_plain, 0);

  bounds_info =
    is_plain ? ROSIDL_TYPESUPPORT_FASTRTPS_PLAIN_TYPE :
    full_bounded ? ROSIDL_TYPESUPPORT_FASTRTPS_BOUNDED_TYPE : ROSIDL_TYPESUPPORT_FASTRTPS_UNBOUNDED_TYPE;
  return ret_val;
}

static message_type_support_callbacks_t _ExecuteVision_Request__callbacks = {
  "pm_vision_interfaces::srv",
  "ExecuteVision_Request",
  _ExecuteVision_Request__cdr_serialize,
  _ExecuteVision_Request__cdr_deserialize,
  _ExecuteVision_Request__get_serialized_size,
  _ExecuteVision_Request__max_serialized_size
};

static rosidl_message_type_support_t _ExecuteVision_Request__handle = {
  rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
  &_ExecuteVision_Request__callbacks,
  get_message_typesupport_handle_function,
};

}  // namespace typesupport_fastrtps_cpp

}  // namespace srv

}  // namespace pm_vision_interfaces

namespace rosidl_typesupport_fastrtps_cpp
{

template<>
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_EXPORT_pm_vision_interfaces
const rosidl_message_type_support_t *
get_message_type_support_handle<pm_vision_interfaces::srv::ExecuteVision_Request>()
{
  return &pm_vision_interfaces::srv::typesupport_fastrtps_cpp::_ExecuteVision_Request__handle;
}

}  // namespace rosidl_typesupport_fastrtps_cpp

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, pm_vision_interfaces, srv, ExecuteVision_Request)() {
  return &pm_vision_interfaces::srv::typesupport_fastrtps_cpp::_ExecuteVision_Request__handle;
}

#ifdef __cplusplus
}
#endif

// already included above
// #include <limits>
// already included above
// #include <stdexcept>
// already included above
// #include <string>
// already included above
// #include "rosidl_typesupport_cpp/message_type_support.hpp"
// already included above
// #include "rosidl_typesupport_fastrtps_cpp/identifier.hpp"
// already included above
// #include "rosidl_typesupport_fastrtps_cpp/message_type_support.h"
// already included above
// #include "rosidl_typesupport_fastrtps_cpp/message_type_support_decl.hpp"
// already included above
// #include "rosidl_typesupport_fastrtps_cpp/wstring_conversion.hpp"
// already included above
// #include "fastcdr/Cdr.h"


// forward declaration of message dependencies and their conversion functions
namespace pm_vision_interfaces
{
namespace msg
{
namespace typesupport_fastrtps_cpp
{
bool cdr_serialize(
  const pm_vision_interfaces::msg::VisionResponse &,
  eprosima::fastcdr::Cdr &);
bool cdr_deserialize(
  eprosima::fastcdr::Cdr &,
  pm_vision_interfaces::msg::VisionResponse &);
size_t get_serialized_size(
  const pm_vision_interfaces::msg::VisionResponse &,
  size_t current_alignment);
size_t
max_serialized_size_VisionResponse(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);
}  // namespace typesupport_fastrtps_cpp
}  // namespace msg
}  // namespace pm_vision_interfaces


namespace pm_vision_interfaces
{

namespace srv
{

namespace typesupport_fastrtps_cpp
{

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_pm_vision_interfaces
cdr_serialize(
  const pm_vision_interfaces::srv::ExecuteVision_Response & ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  // Member: success
  cdr << (ros_message.success ? true : false);
  // Member: results_path
  cdr << ros_message.results_path;
  // Member: vision_response
  pm_vision_interfaces::msg::typesupport_fastrtps_cpp::cdr_serialize(
    ros_message.vision_response,
    cdr);
  return true;
}

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_pm_vision_interfaces
cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  pm_vision_interfaces::srv::ExecuteVision_Response & ros_message)
{
  // Member: success
  {
    uint8_t tmp;
    cdr >> tmp;
    ros_message.success = tmp ? true : false;
  }

  // Member: results_path
  cdr >> ros_message.results_path;

  // Member: vision_response
  pm_vision_interfaces::msg::typesupport_fastrtps_cpp::cdr_deserialize(
    cdr, ros_message.vision_response);

  return true;
}

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_pm_vision_interfaces
get_serialized_size(
  const pm_vision_interfaces::srv::ExecuteVision_Response & ros_message,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // Member: success
  {
    size_t item_size = sizeof(ros_message.success);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // Member: results_path
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message.results_path.size() + 1);
  // Member: vision_response

  current_alignment +=
    pm_vision_interfaces::msg::typesupport_fastrtps_cpp::get_serialized_size(
    ros_message.vision_response, current_alignment);

  return current_alignment - initial_alignment;
}

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_pm_vision_interfaces
max_serialized_size_ExecuteVision_Response(
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


  // Member: success
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }

  // Member: results_path
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

  // Member: vision_response
  {
    size_t array_size = 1;


    last_member_size = 0;
    for (size_t index = 0; index < array_size; ++index) {
      bool inner_full_bounded;
      bool inner_is_plain;
      size_t inner_size =
        pm_vision_interfaces::msg::typesupport_fastrtps_cpp::max_serialized_size_VisionResponse(
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
    using DataType = pm_vision_interfaces::srv::ExecuteVision_Response;
    is_plain =
      (
      offsetof(DataType, vision_response) +
      last_member_size
      ) == ret_val;
  }

  return ret_val;
}

static bool _ExecuteVision_Response__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  auto typed_message =
    static_cast<const pm_vision_interfaces::srv::ExecuteVision_Response *>(
    untyped_ros_message);
  return cdr_serialize(*typed_message, cdr);
}

static bool _ExecuteVision_Response__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  auto typed_message =
    static_cast<pm_vision_interfaces::srv::ExecuteVision_Response *>(
    untyped_ros_message);
  return cdr_deserialize(cdr, *typed_message);
}

static uint32_t _ExecuteVision_Response__get_serialized_size(
  const void * untyped_ros_message)
{
  auto typed_message =
    static_cast<const pm_vision_interfaces::srv::ExecuteVision_Response *>(
    untyped_ros_message);
  return static_cast<uint32_t>(get_serialized_size(*typed_message, 0));
}

static size_t _ExecuteVision_Response__max_serialized_size(char & bounds_info)
{
  bool full_bounded;
  bool is_plain;
  size_t ret_val;

  ret_val = max_serialized_size_ExecuteVision_Response(full_bounded, is_plain, 0);

  bounds_info =
    is_plain ? ROSIDL_TYPESUPPORT_FASTRTPS_PLAIN_TYPE :
    full_bounded ? ROSIDL_TYPESUPPORT_FASTRTPS_BOUNDED_TYPE : ROSIDL_TYPESUPPORT_FASTRTPS_UNBOUNDED_TYPE;
  return ret_val;
}

static message_type_support_callbacks_t _ExecuteVision_Response__callbacks = {
  "pm_vision_interfaces::srv",
  "ExecuteVision_Response",
  _ExecuteVision_Response__cdr_serialize,
  _ExecuteVision_Response__cdr_deserialize,
  _ExecuteVision_Response__get_serialized_size,
  _ExecuteVision_Response__max_serialized_size
};

static rosidl_message_type_support_t _ExecuteVision_Response__handle = {
  rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
  &_ExecuteVision_Response__callbacks,
  get_message_typesupport_handle_function,
};

}  // namespace typesupport_fastrtps_cpp

}  // namespace srv

}  // namespace pm_vision_interfaces

namespace rosidl_typesupport_fastrtps_cpp
{

template<>
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_EXPORT_pm_vision_interfaces
const rosidl_message_type_support_t *
get_message_type_support_handle<pm_vision_interfaces::srv::ExecuteVision_Response>()
{
  return &pm_vision_interfaces::srv::typesupport_fastrtps_cpp::_ExecuteVision_Response__handle;
}

}  // namespace rosidl_typesupport_fastrtps_cpp

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, pm_vision_interfaces, srv, ExecuteVision_Response)() {
  return &pm_vision_interfaces::srv::typesupport_fastrtps_cpp::_ExecuteVision_Response__handle;
}

#ifdef __cplusplus
}
#endif

#include "rmw/error_handling.h"
// already included above
// #include "rosidl_typesupport_fastrtps_cpp/identifier.hpp"
#include "rosidl_typesupport_fastrtps_cpp/service_type_support.h"
#include "rosidl_typesupport_fastrtps_cpp/service_type_support_decl.hpp"

namespace pm_vision_interfaces
{

namespace srv
{

namespace typesupport_fastrtps_cpp
{

static service_type_support_callbacks_t _ExecuteVision__callbacks = {
  "pm_vision_interfaces::srv",
  "ExecuteVision",
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, pm_vision_interfaces, srv, ExecuteVision_Request)(),
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, pm_vision_interfaces, srv, ExecuteVision_Response)(),
};

static rosidl_service_type_support_t _ExecuteVision__handle = {
  rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
  &_ExecuteVision__callbacks,
  get_service_typesupport_handle_function,
};

}  // namespace typesupport_fastrtps_cpp

}  // namespace srv

}  // namespace pm_vision_interfaces

namespace rosidl_typesupport_fastrtps_cpp
{

template<>
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_EXPORT_pm_vision_interfaces
const rosidl_service_type_support_t *
get_service_type_support_handle<pm_vision_interfaces::srv::ExecuteVision>()
{
  return &pm_vision_interfaces::srv::typesupport_fastrtps_cpp::_ExecuteVision__handle;
}

}  // namespace rosidl_typesupport_fastrtps_cpp

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, pm_vision_interfaces, srv, ExecuteVision)() {
  return &pm_vision_interfaces::srv::typesupport_fastrtps_cpp::_ExecuteVision__handle;
}

#ifdef __cplusplus
}
#endif

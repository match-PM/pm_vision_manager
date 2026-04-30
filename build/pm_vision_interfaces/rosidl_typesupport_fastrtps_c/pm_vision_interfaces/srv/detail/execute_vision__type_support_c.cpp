// generated from rosidl_typesupport_fastrtps_c/resource/idl__type_support_c.cpp.em
// with input from pm_vision_interfaces:srv/ExecuteVision.idl
// generated code does not contain a copyright notice
#include "pm_vision_interfaces/srv/detail/execute_vision__rosidl_typesupport_fastrtps_c.h"


#include <cassert>
#include <limits>
#include <string>
#include "rosidl_typesupport_fastrtps_c/identifier.h"
#include "rosidl_typesupport_fastrtps_c/wstring_conversion.hpp"
#include "rosidl_typesupport_fastrtps_cpp/message_type_support.h"
#include "pm_vision_interfaces/msg/rosidl_typesupport_fastrtps_c__visibility_control.h"
#include "pm_vision_interfaces/srv/detail/execute_vision__struct.h"
#include "pm_vision_interfaces/srv/detail/execute_vision__functions.h"
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

#include "rosidl_runtime_c/string.h"  // camera_config_filename, process_filename, process_uid
#include "rosidl_runtime_c/string_functions.h"  // camera_config_filename, process_filename, process_uid

// forward declare type support functions


using _ExecuteVision_Request__ros_msg_type = pm_vision_interfaces__srv__ExecuteVision_Request;

static bool _ExecuteVision_Request__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  const _ExecuteVision_Request__ros_msg_type * ros_message = static_cast<const _ExecuteVision_Request__ros_msg_type *>(untyped_ros_message);
  // Field name: process_filename
  {
    const rosidl_runtime_c__String * str = &ros_message->process_filename;
    if (str->capacity == 0 || str->capacity <= str->size) {
      fprintf(stderr, "string capacity not greater than size\n");
      return false;
    }
    if (str->data[str->size] != '\0') {
      fprintf(stderr, "string not null-terminated\n");
      return false;
    }
    cdr << str->data;
  }

  // Field name: camera_config_filename
  {
    const rosidl_runtime_c__String * str = &ros_message->camera_config_filename;
    if (str->capacity == 0 || str->capacity <= str->size) {
      fprintf(stderr, "string capacity not greater than size\n");
      return false;
    }
    if (str->data[str->size] != '\0') {
      fprintf(stderr, "string not null-terminated\n");
      return false;
    }
    cdr << str->data;
  }

  // Field name: process_uid
  {
    const rosidl_runtime_c__String * str = &ros_message->process_uid;
    if (str->capacity == 0 || str->capacity <= str->size) {
      fprintf(stderr, "string capacity not greater than size\n");
      return false;
    }
    if (str->data[str->size] != '\0') {
      fprintf(stderr, "string not null-terminated\n");
      return false;
    }
    cdr << str->data;
  }

  // Field name: image_display_time
  {
    cdr << ros_message->image_display_time;
  }

  // Field name: run_cross_validation
  {
    cdr << (ros_message->run_cross_validation ? true : false);
  }

  return true;
}

static bool _ExecuteVision_Request__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  _ExecuteVision_Request__ros_msg_type * ros_message = static_cast<_ExecuteVision_Request__ros_msg_type *>(untyped_ros_message);
  // Field name: process_filename
  {
    std::string tmp;
    cdr >> tmp;
    if (!ros_message->process_filename.data) {
      rosidl_runtime_c__String__init(&ros_message->process_filename);
    }
    bool succeeded = rosidl_runtime_c__String__assign(
      &ros_message->process_filename,
      tmp.c_str());
    if (!succeeded) {
      fprintf(stderr, "failed to assign string into field 'process_filename'\n");
      return false;
    }
  }

  // Field name: camera_config_filename
  {
    std::string tmp;
    cdr >> tmp;
    if (!ros_message->camera_config_filename.data) {
      rosidl_runtime_c__String__init(&ros_message->camera_config_filename);
    }
    bool succeeded = rosidl_runtime_c__String__assign(
      &ros_message->camera_config_filename,
      tmp.c_str());
    if (!succeeded) {
      fprintf(stderr, "failed to assign string into field 'camera_config_filename'\n");
      return false;
    }
  }

  // Field name: process_uid
  {
    std::string tmp;
    cdr >> tmp;
    if (!ros_message->process_uid.data) {
      rosidl_runtime_c__String__init(&ros_message->process_uid);
    }
    bool succeeded = rosidl_runtime_c__String__assign(
      &ros_message->process_uid,
      tmp.c_str());
    if (!succeeded) {
      fprintf(stderr, "failed to assign string into field 'process_uid'\n");
      return false;
    }
  }

  // Field name: image_display_time
  {
    cdr >> ros_message->image_display_time;
  }

  // Field name: run_cross_validation
  {
    uint8_t tmp;
    cdr >> tmp;
    ros_message->run_cross_validation = tmp ? true : false;
  }

  return true;
}  // NOLINT(readability/fn_size)

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_pm_vision_interfaces
size_t get_serialized_size_pm_vision_interfaces__srv__ExecuteVision_Request(
  const void * untyped_ros_message,
  size_t current_alignment)
{
  const _ExecuteVision_Request__ros_msg_type * ros_message = static_cast<const _ExecuteVision_Request__ros_msg_type *>(untyped_ros_message);
  (void)ros_message;
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // field.name process_filename
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message->process_filename.size + 1);
  // field.name camera_config_filename
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message->camera_config_filename.size + 1);
  // field.name process_uid
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message->process_uid.size + 1);
  // field.name image_display_time
  {
    size_t item_size = sizeof(ros_message->image_display_time);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name run_cross_validation
  {
    size_t item_size = sizeof(ros_message->run_cross_validation);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  return current_alignment - initial_alignment;
}

static uint32_t _ExecuteVision_Request__get_serialized_size(const void * untyped_ros_message)
{
  return static_cast<uint32_t>(
    get_serialized_size_pm_vision_interfaces__srv__ExecuteVision_Request(
      untyped_ros_message, 0));
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_pm_vision_interfaces
size_t max_serialized_size_pm_vision_interfaces__srv__ExecuteVision_Request(
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

  // member: process_filename
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
  // member: camera_config_filename
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
  // member: process_uid
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
  // member: image_display_time
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint64_t);
    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }
  // member: run_cross_validation
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
    using DataType = pm_vision_interfaces__srv__ExecuteVision_Request;
    is_plain =
      (
      offsetof(DataType, run_cross_validation) +
      last_member_size
      ) == ret_val;
  }

  return ret_val;
}

static size_t _ExecuteVision_Request__max_serialized_size(char & bounds_info)
{
  bool full_bounded;
  bool is_plain;
  size_t ret_val;

  ret_val = max_serialized_size_pm_vision_interfaces__srv__ExecuteVision_Request(
    full_bounded, is_plain, 0);

  bounds_info =
    is_plain ? ROSIDL_TYPESUPPORT_FASTRTPS_PLAIN_TYPE :
    full_bounded ? ROSIDL_TYPESUPPORT_FASTRTPS_BOUNDED_TYPE : ROSIDL_TYPESUPPORT_FASTRTPS_UNBOUNDED_TYPE;
  return ret_val;
}


static message_type_support_callbacks_t __callbacks_ExecuteVision_Request = {
  "pm_vision_interfaces::srv",
  "ExecuteVision_Request",
  _ExecuteVision_Request__cdr_serialize,
  _ExecuteVision_Request__cdr_deserialize,
  _ExecuteVision_Request__get_serialized_size,
  _ExecuteVision_Request__max_serialized_size
};

static rosidl_message_type_support_t _ExecuteVision_Request__type_support = {
  rosidl_typesupport_fastrtps_c__identifier,
  &__callbacks_ExecuteVision_Request,
  get_message_typesupport_handle_function,
};

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, pm_vision_interfaces, srv, ExecuteVision_Request)() {
  return &_ExecuteVision_Request__type_support;
}

#if defined(__cplusplus)
}
#endif

// already included above
// #include <cassert>
// already included above
// #include <limits>
// already included above
// #include <string>
// already included above
// #include "rosidl_typesupport_fastrtps_c/identifier.h"
// already included above
// #include "rosidl_typesupport_fastrtps_c/wstring_conversion.hpp"
// already included above
// #include "rosidl_typesupport_fastrtps_cpp/message_type_support.h"
// already included above
// #include "pm_vision_interfaces/msg/rosidl_typesupport_fastrtps_c__visibility_control.h"
// already included above
// #include "pm_vision_interfaces/srv/detail/execute_vision__struct.h"
// already included above
// #include "pm_vision_interfaces/srv/detail/execute_vision__functions.h"
// already included above
// #include "fastcdr/Cdr.h"

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

#include "pm_vision_interfaces/msg/detail/vision_response__functions.h"  // vision_response
// already included above
// #include "rosidl_runtime_c/string.h"  // results_path
// already included above
// #include "rosidl_runtime_c/string_functions.h"  // results_path

// forward declare type support functions
size_t get_serialized_size_pm_vision_interfaces__msg__VisionResponse(
  const void * untyped_ros_message,
  size_t current_alignment);

size_t max_serialized_size_pm_vision_interfaces__msg__VisionResponse(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

const rosidl_message_type_support_t *
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, pm_vision_interfaces, msg, VisionResponse)();


using _ExecuteVision_Response__ros_msg_type = pm_vision_interfaces__srv__ExecuteVision_Response;

static bool _ExecuteVision_Response__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  const _ExecuteVision_Response__ros_msg_type * ros_message = static_cast<const _ExecuteVision_Response__ros_msg_type *>(untyped_ros_message);
  // Field name: success
  {
    cdr << (ros_message->success ? true : false);
  }

  // Field name: results_path
  {
    const rosidl_runtime_c__String * str = &ros_message->results_path;
    if (str->capacity == 0 || str->capacity <= str->size) {
      fprintf(stderr, "string capacity not greater than size\n");
      return false;
    }
    if (str->data[str->size] != '\0') {
      fprintf(stderr, "string not null-terminated\n");
      return false;
    }
    cdr << str->data;
  }

  // Field name: vision_response
  {
    const message_type_support_callbacks_t * callbacks =
      static_cast<const message_type_support_callbacks_t *>(
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(
        rosidl_typesupport_fastrtps_c, pm_vision_interfaces, msg, VisionResponse
      )()->data);
    if (!callbacks->cdr_serialize(
        &ros_message->vision_response, cdr))
    {
      return false;
    }
  }

  return true;
}

static bool _ExecuteVision_Response__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  _ExecuteVision_Response__ros_msg_type * ros_message = static_cast<_ExecuteVision_Response__ros_msg_type *>(untyped_ros_message);
  // Field name: success
  {
    uint8_t tmp;
    cdr >> tmp;
    ros_message->success = tmp ? true : false;
  }

  // Field name: results_path
  {
    std::string tmp;
    cdr >> tmp;
    if (!ros_message->results_path.data) {
      rosidl_runtime_c__String__init(&ros_message->results_path);
    }
    bool succeeded = rosidl_runtime_c__String__assign(
      &ros_message->results_path,
      tmp.c_str());
    if (!succeeded) {
      fprintf(stderr, "failed to assign string into field 'results_path'\n");
      return false;
    }
  }

  // Field name: vision_response
  {
    const message_type_support_callbacks_t * callbacks =
      static_cast<const message_type_support_callbacks_t *>(
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(
        rosidl_typesupport_fastrtps_c, pm_vision_interfaces, msg, VisionResponse
      )()->data);
    if (!callbacks->cdr_deserialize(
        cdr, &ros_message->vision_response))
    {
      return false;
    }
  }

  return true;
}  // NOLINT(readability/fn_size)

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_pm_vision_interfaces
size_t get_serialized_size_pm_vision_interfaces__srv__ExecuteVision_Response(
  const void * untyped_ros_message,
  size_t current_alignment)
{
  const _ExecuteVision_Response__ros_msg_type * ros_message = static_cast<const _ExecuteVision_Response__ros_msg_type *>(untyped_ros_message);
  (void)ros_message;
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // field.name success
  {
    size_t item_size = sizeof(ros_message->success);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name results_path
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message->results_path.size + 1);
  // field.name vision_response

  current_alignment += get_serialized_size_pm_vision_interfaces__msg__VisionResponse(
    &(ros_message->vision_response), current_alignment);

  return current_alignment - initial_alignment;
}

static uint32_t _ExecuteVision_Response__get_serialized_size(const void * untyped_ros_message)
{
  return static_cast<uint32_t>(
    get_serialized_size_pm_vision_interfaces__srv__ExecuteVision_Response(
      untyped_ros_message, 0));
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_pm_vision_interfaces
size_t max_serialized_size_pm_vision_interfaces__srv__ExecuteVision_Response(
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

  // member: success
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }
  // member: results_path
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
  // member: vision_response
  {
    size_t array_size = 1;


    last_member_size = 0;
    for (size_t index = 0; index < array_size; ++index) {
      bool inner_full_bounded;
      bool inner_is_plain;
      size_t inner_size;
      inner_size =
        max_serialized_size_pm_vision_interfaces__msg__VisionResponse(
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
    using DataType = pm_vision_interfaces__srv__ExecuteVision_Response;
    is_plain =
      (
      offsetof(DataType, vision_response) +
      last_member_size
      ) == ret_val;
  }

  return ret_val;
}

static size_t _ExecuteVision_Response__max_serialized_size(char & bounds_info)
{
  bool full_bounded;
  bool is_plain;
  size_t ret_val;

  ret_val = max_serialized_size_pm_vision_interfaces__srv__ExecuteVision_Response(
    full_bounded, is_plain, 0);

  bounds_info =
    is_plain ? ROSIDL_TYPESUPPORT_FASTRTPS_PLAIN_TYPE :
    full_bounded ? ROSIDL_TYPESUPPORT_FASTRTPS_BOUNDED_TYPE : ROSIDL_TYPESUPPORT_FASTRTPS_UNBOUNDED_TYPE;
  return ret_val;
}


static message_type_support_callbacks_t __callbacks_ExecuteVision_Response = {
  "pm_vision_interfaces::srv",
  "ExecuteVision_Response",
  _ExecuteVision_Response__cdr_serialize,
  _ExecuteVision_Response__cdr_deserialize,
  _ExecuteVision_Response__get_serialized_size,
  _ExecuteVision_Response__max_serialized_size
};

static rosidl_message_type_support_t _ExecuteVision_Response__type_support = {
  rosidl_typesupport_fastrtps_c__identifier,
  &__callbacks_ExecuteVision_Response,
  get_message_typesupport_handle_function,
};

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, pm_vision_interfaces, srv, ExecuteVision_Response)() {
  return &_ExecuteVision_Response__type_support;
}

#if defined(__cplusplus)
}
#endif

#include "rosidl_typesupport_fastrtps_cpp/service_type_support.h"
#include "rosidl_typesupport_cpp/service_type_support.hpp"
// already included above
// #include "rosidl_typesupport_fastrtps_c/identifier.h"
// already included above
// #include "pm_vision_interfaces/msg/rosidl_typesupport_fastrtps_c__visibility_control.h"
#include "pm_vision_interfaces/srv/execute_vision.h"

#if defined(__cplusplus)
extern "C"
{
#endif

static service_type_support_callbacks_t ExecuteVision__callbacks = {
  "pm_vision_interfaces::srv",
  "ExecuteVision",
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, pm_vision_interfaces, srv, ExecuteVision_Request)(),
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, pm_vision_interfaces, srv, ExecuteVision_Response)(),
};

static rosidl_service_type_support_t ExecuteVision__handle = {
  rosidl_typesupport_fastrtps_c__identifier,
  &ExecuteVision__callbacks,
  get_service_typesupport_handle_function,
};

const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, pm_vision_interfaces, srv, ExecuteVision)() {
  return &ExecuteVision__handle;
}

#if defined(__cplusplus)
}
#endif

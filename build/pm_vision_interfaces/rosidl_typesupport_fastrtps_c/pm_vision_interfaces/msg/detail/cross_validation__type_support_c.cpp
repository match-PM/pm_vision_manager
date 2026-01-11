// generated from rosidl_typesupport_fastrtps_c/resource/idl__type_support_c.cpp.em
// with input from pm_vision_interfaces:msg/CrossValidation.idl
// generated code does not contain a copyright notice
#include "pm_vision_interfaces/msg/detail/cross_validation__rosidl_typesupport_fastrtps_c.h"


#include <cassert>
#include <limits>
#include <string>
#include "rosidl_typesupport_fastrtps_c/identifier.h"
#include "rosidl_typesupport_fastrtps_c/wstring_conversion.hpp"
#include "rosidl_typesupport_fastrtps_cpp/message_type_support.h"
#include "pm_vision_interfaces/msg/rosidl_typesupport_fastrtps_c__visibility_control.h"
#include "pm_vision_interfaces/msg/detail/cross_validation__struct.h"
#include "pm_vision_interfaces/msg/detail/cross_validation__functions.h"
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

#include "rosidl_runtime_c/string.h"  // failed_images, image_source_name
#include "rosidl_runtime_c/string_functions.h"  // failed_images, image_source_name

// forward declare type support functions


using _CrossValidation__ros_msg_type = pm_vision_interfaces__msg__CrossValidation;

static bool _CrossValidation__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  const _CrossValidation__ros_msg_type * ros_message = static_cast<const _CrossValidation__ros_msg_type *>(untyped_ros_message);
  // Field name: image_source_name
  {
    const rosidl_runtime_c__String * str = &ros_message->image_source_name;
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

  // Field name: vision_ok
  {
    cdr << (ros_message->vision_ok ? true : false);
  }

  // Field name: failed_images
  {
    size_t size = ros_message->failed_images.size;
    auto array_ptr = ros_message->failed_images.data;
    cdr << static_cast<uint32_t>(size);
    for (size_t i = 0; i < size; ++i) {
      const rosidl_runtime_c__String * str = &array_ptr[i];
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
  }

  // Field name: numb_images
  {
    cdr << ros_message->numb_images;
  }

  // Field name: counter_error
  {
    cdr << ros_message->counter_error;
  }

  return true;
}

static bool _CrossValidation__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  _CrossValidation__ros_msg_type * ros_message = static_cast<_CrossValidation__ros_msg_type *>(untyped_ros_message);
  // Field name: image_source_name
  {
    std::string tmp;
    cdr >> tmp;
    if (!ros_message->image_source_name.data) {
      rosidl_runtime_c__String__init(&ros_message->image_source_name);
    }
    bool succeeded = rosidl_runtime_c__String__assign(
      &ros_message->image_source_name,
      tmp.c_str());
    if (!succeeded) {
      fprintf(stderr, "failed to assign string into field 'image_source_name'\n");
      return false;
    }
  }

  // Field name: vision_ok
  {
    uint8_t tmp;
    cdr >> tmp;
    ros_message->vision_ok = tmp ? true : false;
  }

  // Field name: failed_images
  {
    uint32_t cdrSize;
    cdr >> cdrSize;
    size_t size = static_cast<size_t>(cdrSize);
    if (ros_message->failed_images.data) {
      rosidl_runtime_c__String__Sequence__fini(&ros_message->failed_images);
    }
    if (!rosidl_runtime_c__String__Sequence__init(&ros_message->failed_images, size)) {
      fprintf(stderr, "failed to create array for field 'failed_images'");
      return false;
    }
    auto array_ptr = ros_message->failed_images.data;
    for (size_t i = 0; i < size; ++i) {
      std::string tmp;
      cdr >> tmp;
      auto & ros_i = array_ptr[i];
      if (!ros_i.data) {
        rosidl_runtime_c__String__init(&ros_i);
      }
      bool succeeded = rosidl_runtime_c__String__assign(
        &ros_i,
        tmp.c_str());
      if (!succeeded) {
        fprintf(stderr, "failed to assign string into field 'failed_images'\n");
        return false;
      }
    }
  }

  // Field name: numb_images
  {
    cdr >> ros_message->numb_images;
  }

  // Field name: counter_error
  {
    cdr >> ros_message->counter_error;
  }

  return true;
}  // NOLINT(readability/fn_size)

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_pm_vision_interfaces
size_t get_serialized_size_pm_vision_interfaces__msg__CrossValidation(
  const void * untyped_ros_message,
  size_t current_alignment)
{
  const _CrossValidation__ros_msg_type * ros_message = static_cast<const _CrossValidation__ros_msg_type *>(untyped_ros_message);
  (void)ros_message;
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // field.name image_source_name
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message->image_source_name.size + 1);
  // field.name vision_ok
  {
    size_t item_size = sizeof(ros_message->vision_ok);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name failed_images
  {
    size_t array_size = ros_message->failed_images.size;
    auto array_ptr = ros_message->failed_images.data;
    current_alignment += padding +
      eprosima::fastcdr::Cdr::alignment(current_alignment, padding);
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += padding +
        eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
        (array_ptr[index].size + 1);
    }
  }
  // field.name numb_images
  {
    size_t item_size = sizeof(ros_message->numb_images);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name counter_error
  {
    size_t item_size = sizeof(ros_message->counter_error);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  return current_alignment - initial_alignment;
}

static uint32_t _CrossValidation__get_serialized_size(const void * untyped_ros_message)
{
  return static_cast<uint32_t>(
    get_serialized_size_pm_vision_interfaces__msg__CrossValidation(
      untyped_ros_message, 0));
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_pm_vision_interfaces
size_t max_serialized_size_pm_vision_interfaces__msg__CrossValidation(
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

  // member: image_source_name
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
  // member: vision_ok
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }
  // member: failed_images
  {
    size_t array_size = 0;
    full_bounded = false;
    is_plain = false;
    current_alignment += padding +
      eprosima::fastcdr::Cdr::alignment(current_alignment, padding);

    full_bounded = false;
    is_plain = false;
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += padding +
        eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
        1;
    }
  }
  // member: numb_images
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }
  // member: counter_error
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
    using DataType = pm_vision_interfaces__msg__CrossValidation;
    is_plain =
      (
      offsetof(DataType, counter_error) +
      last_member_size
      ) == ret_val;
  }

  return ret_val;
}

static size_t _CrossValidation__max_serialized_size(char & bounds_info)
{
  bool full_bounded;
  bool is_plain;
  size_t ret_val;

  ret_val = max_serialized_size_pm_vision_interfaces__msg__CrossValidation(
    full_bounded, is_plain, 0);

  bounds_info =
    is_plain ? ROSIDL_TYPESUPPORT_FASTRTPS_PLAIN_TYPE :
    full_bounded ? ROSIDL_TYPESUPPORT_FASTRTPS_BOUNDED_TYPE : ROSIDL_TYPESUPPORT_FASTRTPS_UNBOUNDED_TYPE;
  return ret_val;
}


static message_type_support_callbacks_t __callbacks_CrossValidation = {
  "pm_vision_interfaces::msg",
  "CrossValidation",
  _CrossValidation__cdr_serialize,
  _CrossValidation__cdr_deserialize,
  _CrossValidation__get_serialized_size,
  _CrossValidation__max_serialized_size
};

static rosidl_message_type_support_t _CrossValidation__type_support = {
  rosidl_typesupport_fastrtps_c__identifier,
  &__callbacks_CrossValidation,
  get_message_typesupport_handle_function,
};

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, pm_vision_interfaces, msg, CrossValidation)() {
  return &_CrossValidation__type_support;
}

#if defined(__cplusplus)
}
#endif

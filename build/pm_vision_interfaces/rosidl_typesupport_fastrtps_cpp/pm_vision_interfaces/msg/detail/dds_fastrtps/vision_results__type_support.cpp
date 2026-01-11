// generated from rosidl_typesupport_fastrtps_cpp/resource/idl__type_support.cpp.em
// with input from pm_vision_interfaces:msg/VisionResults.idl
// generated code does not contain a copyright notice
#include "pm_vision_interfaces/msg/detail/vision_results__rosidl_typesupport_fastrtps_cpp.hpp"
#include "pm_vision_interfaces/msg/detail/vision_results__struct.hpp"

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

namespace pm_vision_interfaces
{
namespace msg
{
namespace typesupport_fastrtps_cpp
{
bool cdr_serialize(
  const pm_vision_interfaces::msg::VisionLine &,
  eprosima::fastcdr::Cdr &);
bool cdr_deserialize(
  eprosima::fastcdr::Cdr &,
  pm_vision_interfaces::msg::VisionLine &);
size_t get_serialized_size(
  const pm_vision_interfaces::msg::VisionLine &,
  size_t current_alignment);
size_t
max_serialized_size_VisionLine(
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
  const pm_vision_interfaces::msg::VisionArea &,
  eprosima::fastcdr::Cdr &);
bool cdr_deserialize(
  eprosima::fastcdr::Cdr &,
  pm_vision_interfaces::msg::VisionArea &);
size_t get_serialized_size(
  const pm_vision_interfaces::msg::VisionArea &,
  size_t current_alignment);
size_t
max_serialized_size_VisionArea(
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
  const pm_vision_interfaces::msg::VisionCircle &,
  eprosima::fastcdr::Cdr &);
bool cdr_deserialize(
  eprosima::fastcdr::Cdr &,
  pm_vision_interfaces::msg::VisionCircle &);
size_t get_serialized_size(
  const pm_vision_interfaces::msg::VisionCircle &,
  size_t current_alignment);
size_t
max_serialized_size_VisionCircle(
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
  const pm_vision_interfaces::msg::ImageSharpness &,
  eprosima::fastcdr::Cdr &);
bool cdr_deserialize(
  eprosima::fastcdr::Cdr &,
  pm_vision_interfaces::msg::ImageSharpness &);
size_t get_serialized_size(
  const pm_vision_interfaces::msg::ImageSharpness &,
  size_t current_alignment);
size_t
max_serialized_size_ImageSharpness(
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
  const pm_vision_interfaces::msg::VisionResults & ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  // Member: points
  {
    size_t size = ros_message.points.size();
    cdr << static_cast<uint32_t>(size);
    for (size_t i = 0; i < size; i++) {
      pm_vision_interfaces::msg::typesupport_fastrtps_cpp::cdr_serialize(
        ros_message.points[i],
        cdr);
    }
  }
  // Member: lines
  {
    size_t size = ros_message.lines.size();
    cdr << static_cast<uint32_t>(size);
    for (size_t i = 0; i < size; i++) {
      pm_vision_interfaces::msg::typesupport_fastrtps_cpp::cdr_serialize(
        ros_message.lines[i],
        cdr);
    }
  }
  // Member: areas
  {
    size_t size = ros_message.areas.size();
    cdr << static_cast<uint32_t>(size);
    for (size_t i = 0; i < size; i++) {
      pm_vision_interfaces::msg::typesupport_fastrtps_cpp::cdr_serialize(
        ros_message.areas[i],
        cdr);
    }
  }
  // Member: circles
  {
    size_t size = ros_message.circles.size();
    cdr << static_cast<uint32_t>(size);
    for (size_t i = 0; i < size; i++) {
      pm_vision_interfaces::msg::typesupport_fastrtps_cpp::cdr_serialize(
        ros_message.circles[i],
        cdr);
    }
  }
  // Member: image_sharpness
  pm_vision_interfaces::msg::typesupport_fastrtps_cpp::cdr_serialize(
    ros_message.image_sharpness,
    cdr);
  return true;
}

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_pm_vision_interfaces
cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  pm_vision_interfaces::msg::VisionResults & ros_message)
{
  // Member: points
  {
    uint32_t cdrSize;
    cdr >> cdrSize;
    size_t size = static_cast<size_t>(cdrSize);
    ros_message.points.resize(size);
    for (size_t i = 0; i < size; i++) {
      pm_vision_interfaces::msg::typesupport_fastrtps_cpp::cdr_deserialize(
        cdr, ros_message.points[i]);
    }
  }

  // Member: lines
  {
    uint32_t cdrSize;
    cdr >> cdrSize;
    size_t size = static_cast<size_t>(cdrSize);
    ros_message.lines.resize(size);
    for (size_t i = 0; i < size; i++) {
      pm_vision_interfaces::msg::typesupport_fastrtps_cpp::cdr_deserialize(
        cdr, ros_message.lines[i]);
    }
  }

  // Member: areas
  {
    uint32_t cdrSize;
    cdr >> cdrSize;
    size_t size = static_cast<size_t>(cdrSize);
    ros_message.areas.resize(size);
    for (size_t i = 0; i < size; i++) {
      pm_vision_interfaces::msg::typesupport_fastrtps_cpp::cdr_deserialize(
        cdr, ros_message.areas[i]);
    }
  }

  // Member: circles
  {
    uint32_t cdrSize;
    cdr >> cdrSize;
    size_t size = static_cast<size_t>(cdrSize);
    ros_message.circles.resize(size);
    for (size_t i = 0; i < size; i++) {
      pm_vision_interfaces::msg::typesupport_fastrtps_cpp::cdr_deserialize(
        cdr, ros_message.circles[i]);
    }
  }

  // Member: image_sharpness
  pm_vision_interfaces::msg::typesupport_fastrtps_cpp::cdr_deserialize(
    cdr, ros_message.image_sharpness);

  return true;
}

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_pm_vision_interfaces
get_serialized_size(
  const pm_vision_interfaces::msg::VisionResults & ros_message,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // Member: points
  {
    size_t array_size = ros_message.points.size();

    current_alignment += padding +
      eprosima::fastcdr::Cdr::alignment(current_alignment, padding);

    for (size_t index = 0; index < array_size; ++index) {
      current_alignment +=
        pm_vision_interfaces::msg::typesupport_fastrtps_cpp::get_serialized_size(
        ros_message.points[index], current_alignment);
    }
  }
  // Member: lines
  {
    size_t array_size = ros_message.lines.size();

    current_alignment += padding +
      eprosima::fastcdr::Cdr::alignment(current_alignment, padding);

    for (size_t index = 0; index < array_size; ++index) {
      current_alignment +=
        pm_vision_interfaces::msg::typesupport_fastrtps_cpp::get_serialized_size(
        ros_message.lines[index], current_alignment);
    }
  }
  // Member: areas
  {
    size_t array_size = ros_message.areas.size();

    current_alignment += padding +
      eprosima::fastcdr::Cdr::alignment(current_alignment, padding);

    for (size_t index = 0; index < array_size; ++index) {
      current_alignment +=
        pm_vision_interfaces::msg::typesupport_fastrtps_cpp::get_serialized_size(
        ros_message.areas[index], current_alignment);
    }
  }
  // Member: circles
  {
    size_t array_size = ros_message.circles.size();

    current_alignment += padding +
      eprosima::fastcdr::Cdr::alignment(current_alignment, padding);

    for (size_t index = 0; index < array_size; ++index) {
      current_alignment +=
        pm_vision_interfaces::msg::typesupport_fastrtps_cpp::get_serialized_size(
        ros_message.circles[index], current_alignment);
    }
  }
  // Member: image_sharpness

  current_alignment +=
    pm_vision_interfaces::msg::typesupport_fastrtps_cpp::get_serialized_size(
    ros_message.image_sharpness, current_alignment);

  return current_alignment - initial_alignment;
}

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_pm_vision_interfaces
max_serialized_size_VisionResults(
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


  // Member: points
  {
    size_t array_size = 0;
    full_bounded = false;
    is_plain = false;
    current_alignment += padding +
      eprosima::fastcdr::Cdr::alignment(current_alignment, padding);


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

  // Member: lines
  {
    size_t array_size = 0;
    full_bounded = false;
    is_plain = false;
    current_alignment += padding +
      eprosima::fastcdr::Cdr::alignment(current_alignment, padding);


    last_member_size = 0;
    for (size_t index = 0; index < array_size; ++index) {
      bool inner_full_bounded;
      bool inner_is_plain;
      size_t inner_size =
        pm_vision_interfaces::msg::typesupport_fastrtps_cpp::max_serialized_size_VisionLine(
        inner_full_bounded, inner_is_plain, current_alignment);
      last_member_size += inner_size;
      current_alignment += inner_size;
      full_bounded &= inner_full_bounded;
      is_plain &= inner_is_plain;
    }
  }

  // Member: areas
  {
    size_t array_size = 0;
    full_bounded = false;
    is_plain = false;
    current_alignment += padding +
      eprosima::fastcdr::Cdr::alignment(current_alignment, padding);


    last_member_size = 0;
    for (size_t index = 0; index < array_size; ++index) {
      bool inner_full_bounded;
      bool inner_is_plain;
      size_t inner_size =
        pm_vision_interfaces::msg::typesupport_fastrtps_cpp::max_serialized_size_VisionArea(
        inner_full_bounded, inner_is_plain, current_alignment);
      last_member_size += inner_size;
      current_alignment += inner_size;
      full_bounded &= inner_full_bounded;
      is_plain &= inner_is_plain;
    }
  }

  // Member: circles
  {
    size_t array_size = 0;
    full_bounded = false;
    is_plain = false;
    current_alignment += padding +
      eprosima::fastcdr::Cdr::alignment(current_alignment, padding);


    last_member_size = 0;
    for (size_t index = 0; index < array_size; ++index) {
      bool inner_full_bounded;
      bool inner_is_plain;
      size_t inner_size =
        pm_vision_interfaces::msg::typesupport_fastrtps_cpp::max_serialized_size_VisionCircle(
        inner_full_bounded, inner_is_plain, current_alignment);
      last_member_size += inner_size;
      current_alignment += inner_size;
      full_bounded &= inner_full_bounded;
      is_plain &= inner_is_plain;
    }
  }

  // Member: image_sharpness
  {
    size_t array_size = 1;


    last_member_size = 0;
    for (size_t index = 0; index < array_size; ++index) {
      bool inner_full_bounded;
      bool inner_is_plain;
      size_t inner_size =
        pm_vision_interfaces::msg::typesupport_fastrtps_cpp::max_serialized_size_ImageSharpness(
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
    using DataType = pm_vision_interfaces::msg::VisionResults;
    is_plain =
      (
      offsetof(DataType, image_sharpness) +
      last_member_size
      ) == ret_val;
  }

  return ret_val;
}

static bool _VisionResults__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  auto typed_message =
    static_cast<const pm_vision_interfaces::msg::VisionResults *>(
    untyped_ros_message);
  return cdr_serialize(*typed_message, cdr);
}

static bool _VisionResults__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  auto typed_message =
    static_cast<pm_vision_interfaces::msg::VisionResults *>(
    untyped_ros_message);
  return cdr_deserialize(cdr, *typed_message);
}

static uint32_t _VisionResults__get_serialized_size(
  const void * untyped_ros_message)
{
  auto typed_message =
    static_cast<const pm_vision_interfaces::msg::VisionResults *>(
    untyped_ros_message);
  return static_cast<uint32_t>(get_serialized_size(*typed_message, 0));
}

static size_t _VisionResults__max_serialized_size(char & bounds_info)
{
  bool full_bounded;
  bool is_plain;
  size_t ret_val;

  ret_val = max_serialized_size_VisionResults(full_bounded, is_plain, 0);

  bounds_info =
    is_plain ? ROSIDL_TYPESUPPORT_FASTRTPS_PLAIN_TYPE :
    full_bounded ? ROSIDL_TYPESUPPORT_FASTRTPS_BOUNDED_TYPE : ROSIDL_TYPESUPPORT_FASTRTPS_UNBOUNDED_TYPE;
  return ret_val;
}

static message_type_support_callbacks_t _VisionResults__callbacks = {
  "pm_vision_interfaces::msg",
  "VisionResults",
  _VisionResults__cdr_serialize,
  _VisionResults__cdr_deserialize,
  _VisionResults__get_serialized_size,
  _VisionResults__max_serialized_size
};

static rosidl_message_type_support_t _VisionResults__handle = {
  rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
  &_VisionResults__callbacks,
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
get_message_type_support_handle<pm_vision_interfaces::msg::VisionResults>()
{
  return &pm_vision_interfaces::msg::typesupport_fastrtps_cpp::_VisionResults__handle;
}

}  // namespace rosidl_typesupport_fastrtps_cpp

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, pm_vision_interfaces, msg, VisionResults)() {
  return &pm_vision_interfaces::msg::typesupport_fastrtps_cpp::_VisionResults__handle;
}

#ifdef __cplusplus
}
#endif

// generated from rosidl_typesupport_fastrtps_cpp/resource/idl__rosidl_typesupport_fastrtps_cpp.hpp.em
// with input from pm_vision_interfaces:msg/VisionCircle.idl
// generated code does not contain a copyright notice

#ifndef PM_VISION_INTERFACES__MSG__DETAIL__VISION_CIRCLE__ROSIDL_TYPESUPPORT_FASTRTPS_CPP_HPP_
#define PM_VISION_INTERFACES__MSG__DETAIL__VISION_CIRCLE__ROSIDL_TYPESUPPORT_FASTRTPS_CPP_HPP_

#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_interface/macros.h"
#include "pm_vision_interfaces/msg/rosidl_typesupport_fastrtps_cpp__visibility_control.h"
#include "pm_vision_interfaces/msg/detail/vision_circle__struct.hpp"

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

#include "fastcdr/Cdr.h"

namespace pm_vision_interfaces
{

namespace msg
{

namespace typesupport_fastrtps_cpp
{

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_pm_vision_interfaces
cdr_serialize(
  const pm_vision_interfaces::msg::VisionCircle & ros_message,
  eprosima::fastcdr::Cdr & cdr);

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_pm_vision_interfaces
cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  pm_vision_interfaces::msg::VisionCircle & ros_message);

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_pm_vision_interfaces
get_serialized_size(
  const pm_vision_interfaces::msg::VisionCircle & ros_message,
  size_t current_alignment);

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_pm_vision_interfaces
max_serialized_size_VisionCircle(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

}  // namespace typesupport_fastrtps_cpp

}  // namespace msg

}  // namespace pm_vision_interfaces

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_pm_vision_interfaces
const rosidl_message_type_support_t *
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, pm_vision_interfaces, msg, VisionCircle)();

#ifdef __cplusplus
}
#endif

#endif  // PM_VISION_INTERFACES__MSG__DETAIL__VISION_CIRCLE__ROSIDL_TYPESUPPORT_FASTRTPS_CPP_HPP_

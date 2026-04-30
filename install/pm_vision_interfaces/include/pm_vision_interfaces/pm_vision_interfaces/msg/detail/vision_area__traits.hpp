// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from pm_vision_interfaces:msg/VisionArea.idl
// generated code does not contain a copyright notice

#ifndef PM_VISION_INTERFACES__MSG__DETAIL__VISION_AREA__TRAITS_HPP_
#define PM_VISION_INTERFACES__MSG__DETAIL__VISION_AREA__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "pm_vision_interfaces/msg/detail/vision_area__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace pm_vision_interfaces
{

namespace msg
{

inline void to_flow_style_yaml(
  const VisionArea & msg,
  std::ostream & out)
{
  (void)msg;
  out << "null";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const VisionArea & msg,
  std::ostream & out, size_t indentation = 0)
{
  (void)msg;
  (void)indentation;
  out << "null\n";
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const VisionArea & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace msg

}  // namespace pm_vision_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use pm_vision_interfaces::msg::to_block_style_yaml() instead")]]
inline void to_yaml(
  const pm_vision_interfaces::msg::VisionArea & msg,
  std::ostream & out, size_t indentation = 0)
{
  pm_vision_interfaces::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use pm_vision_interfaces::msg::to_yaml() instead")]]
inline std::string to_yaml(const pm_vision_interfaces::msg::VisionArea & msg)
{
  return pm_vision_interfaces::msg::to_yaml(msg);
}

template<>
inline const char * data_type<pm_vision_interfaces::msg::VisionArea>()
{
  return "pm_vision_interfaces::msg::VisionArea";
}

template<>
inline const char * name<pm_vision_interfaces::msg::VisionArea>()
{
  return "pm_vision_interfaces/msg/VisionArea";
}

template<>
struct has_fixed_size<pm_vision_interfaces::msg::VisionArea>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<pm_vision_interfaces::msg::VisionArea>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<pm_vision_interfaces::msg::VisionArea>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // PM_VISION_INTERFACES__MSG__DETAIL__VISION_AREA__TRAITS_HPP_

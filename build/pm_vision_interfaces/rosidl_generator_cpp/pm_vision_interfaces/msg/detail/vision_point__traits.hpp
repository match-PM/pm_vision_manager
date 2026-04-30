// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from pm_vision_interfaces:msg/VisionPoint.idl
// generated code does not contain a copyright notice

#ifndef PM_VISION_INTERFACES__MSG__DETAIL__VISION_POINT__TRAITS_HPP_
#define PM_VISION_INTERFACES__MSG__DETAIL__VISION_POINT__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "pm_vision_interfaces/msg/detail/vision_point__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace pm_vision_interfaces
{

namespace msg
{

inline void to_flow_style_yaml(
  const VisionPoint & msg,
  std::ostream & out)
{
  out << "{";
  // member: axis_value_1
  {
    out << "axis_value_1: ";
    rosidl_generator_traits::value_to_yaml(msg.axis_value_1, out);
    out << ", ";
  }

  // member: axis_value_2
  {
    out << "axis_value_2: ";
    rosidl_generator_traits::value_to_yaml(msg.axis_value_2, out);
    out << ", ";
  }

  // member: axis_suffix_1
  {
    out << "axis_suffix_1: ";
    rosidl_generator_traits::value_to_yaml(msg.axis_suffix_1, out);
    out << ", ";
  }

  // member: axis_suffix_2
  {
    out << "axis_suffix_2: ";
    rosidl_generator_traits::value_to_yaml(msg.axis_suffix_2, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const VisionPoint & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: axis_value_1
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "axis_value_1: ";
    rosidl_generator_traits::value_to_yaml(msg.axis_value_1, out);
    out << "\n";
  }

  // member: axis_value_2
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "axis_value_2: ";
    rosidl_generator_traits::value_to_yaml(msg.axis_value_2, out);
    out << "\n";
  }

  // member: axis_suffix_1
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "axis_suffix_1: ";
    rosidl_generator_traits::value_to_yaml(msg.axis_suffix_1, out);
    out << "\n";
  }

  // member: axis_suffix_2
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "axis_suffix_2: ";
    rosidl_generator_traits::value_to_yaml(msg.axis_suffix_2, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const VisionPoint & msg, bool use_flow_style = false)
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
  const pm_vision_interfaces::msg::VisionPoint & msg,
  std::ostream & out, size_t indentation = 0)
{
  pm_vision_interfaces::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use pm_vision_interfaces::msg::to_yaml() instead")]]
inline std::string to_yaml(const pm_vision_interfaces::msg::VisionPoint & msg)
{
  return pm_vision_interfaces::msg::to_yaml(msg);
}

template<>
inline const char * data_type<pm_vision_interfaces::msg::VisionPoint>()
{
  return "pm_vision_interfaces::msg::VisionPoint";
}

template<>
inline const char * name<pm_vision_interfaces::msg::VisionPoint>()
{
  return "pm_vision_interfaces/msg/VisionPoint";
}

template<>
struct has_fixed_size<pm_vision_interfaces::msg::VisionPoint>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<pm_vision_interfaces::msg::VisionPoint>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<pm_vision_interfaces::msg::VisionPoint>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // PM_VISION_INTERFACES__MSG__DETAIL__VISION_POINT__TRAITS_HPP_

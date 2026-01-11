// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from pm_vision_interfaces:msg/VisionCircle.idl
// generated code does not contain a copyright notice

#ifndef PM_VISION_INTERFACES__MSG__DETAIL__VISION_CIRCLE__TRAITS_HPP_
#define PM_VISION_INTERFACES__MSG__DETAIL__VISION_CIRCLE__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "pm_vision_interfaces/msg/detail/vision_circle__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'center_point'
#include "pm_vision_interfaces/msg/detail/vision_point__traits.hpp"

namespace pm_vision_interfaces
{

namespace msg
{

inline void to_flow_style_yaml(
  const VisionCircle & msg,
  std::ostream & out)
{
  out << "{";
  // member: center_point
  {
    out << "center_point: ";
    to_flow_style_yaml(msg.center_point, out);
    out << ", ";
  }

  // member: radius
  {
    out << "radius: ";
    rosidl_generator_traits::value_to_yaml(msg.radius, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const VisionCircle & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: center_point
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "center_point:\n";
    to_block_style_yaml(msg.center_point, out, indentation + 2);
  }

  // member: radius
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "radius: ";
    rosidl_generator_traits::value_to_yaml(msg.radius, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const VisionCircle & msg, bool use_flow_style = false)
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
  const pm_vision_interfaces::msg::VisionCircle & msg,
  std::ostream & out, size_t indentation = 0)
{
  pm_vision_interfaces::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use pm_vision_interfaces::msg::to_yaml() instead")]]
inline std::string to_yaml(const pm_vision_interfaces::msg::VisionCircle & msg)
{
  return pm_vision_interfaces::msg::to_yaml(msg);
}

template<>
inline const char * data_type<pm_vision_interfaces::msg::VisionCircle>()
{
  return "pm_vision_interfaces::msg::VisionCircle";
}

template<>
inline const char * name<pm_vision_interfaces::msg::VisionCircle>()
{
  return "pm_vision_interfaces/msg/VisionCircle";
}

template<>
struct has_fixed_size<pm_vision_interfaces::msg::VisionCircle>
  : std::integral_constant<bool, has_fixed_size<pm_vision_interfaces::msg::VisionPoint>::value> {};

template<>
struct has_bounded_size<pm_vision_interfaces::msg::VisionCircle>
  : std::integral_constant<bool, has_bounded_size<pm_vision_interfaces::msg::VisionPoint>::value> {};

template<>
struct is_message<pm_vision_interfaces::msg::VisionCircle>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // PM_VISION_INTERFACES__MSG__DETAIL__VISION_CIRCLE__TRAITS_HPP_

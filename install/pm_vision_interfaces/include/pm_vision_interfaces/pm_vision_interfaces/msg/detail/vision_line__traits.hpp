// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from pm_vision_interfaces:msg/VisionLine.idl
// generated code does not contain a copyright notice

#ifndef PM_VISION_INTERFACES__MSG__DETAIL__VISION_LINE__TRAITS_HPP_
#define PM_VISION_INTERFACES__MSG__DETAIL__VISION_LINE__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "pm_vision_interfaces/msg/detail/vision_line__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'point_1'
// Member 'point_2'
// Member 'point_mid'
#include "pm_vision_interfaces/msg/detail/vision_point__traits.hpp"

namespace pm_vision_interfaces
{

namespace msg
{

inline void to_flow_style_yaml(
  const VisionLine & msg,
  std::ostream & out)
{
  out << "{";
  // member: point_1
  {
    out << "point_1: ";
    to_flow_style_yaml(msg.point_1, out);
    out << ", ";
  }

  // member: point_2
  {
    out << "point_2: ";
    to_flow_style_yaml(msg.point_2, out);
    out << ", ";
  }

  // member: point_mid
  {
    out << "point_mid: ";
    to_flow_style_yaml(msg.point_mid, out);
    out << ", ";
  }

  // member: angle
  {
    out << "angle: ";
    rosidl_generator_traits::value_to_yaml(msg.angle, out);
    out << ", ";
  }

  // member: length
  {
    out << "length: ";
    rosidl_generator_traits::value_to_yaml(msg.length, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const VisionLine & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: point_1
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "point_1:\n";
    to_block_style_yaml(msg.point_1, out, indentation + 2);
  }

  // member: point_2
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "point_2:\n";
    to_block_style_yaml(msg.point_2, out, indentation + 2);
  }

  // member: point_mid
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "point_mid:\n";
    to_block_style_yaml(msg.point_mid, out, indentation + 2);
  }

  // member: angle
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "angle: ";
    rosidl_generator_traits::value_to_yaml(msg.angle, out);
    out << "\n";
  }

  // member: length
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "length: ";
    rosidl_generator_traits::value_to_yaml(msg.length, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const VisionLine & msg, bool use_flow_style = false)
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
  const pm_vision_interfaces::msg::VisionLine & msg,
  std::ostream & out, size_t indentation = 0)
{
  pm_vision_interfaces::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use pm_vision_interfaces::msg::to_yaml() instead")]]
inline std::string to_yaml(const pm_vision_interfaces::msg::VisionLine & msg)
{
  return pm_vision_interfaces::msg::to_yaml(msg);
}

template<>
inline const char * data_type<pm_vision_interfaces::msg::VisionLine>()
{
  return "pm_vision_interfaces::msg::VisionLine";
}

template<>
inline const char * name<pm_vision_interfaces::msg::VisionLine>()
{
  return "pm_vision_interfaces/msg/VisionLine";
}

template<>
struct has_fixed_size<pm_vision_interfaces::msg::VisionLine>
  : std::integral_constant<bool, has_fixed_size<pm_vision_interfaces::msg::VisionPoint>::value> {};

template<>
struct has_bounded_size<pm_vision_interfaces::msg::VisionLine>
  : std::integral_constant<bool, has_bounded_size<pm_vision_interfaces::msg::VisionPoint>::value> {};

template<>
struct is_message<pm_vision_interfaces::msg::VisionLine>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // PM_VISION_INTERFACES__MSG__DETAIL__VISION_LINE__TRAITS_HPP_

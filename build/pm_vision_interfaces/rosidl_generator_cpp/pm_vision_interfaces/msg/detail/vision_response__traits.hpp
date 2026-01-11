// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from pm_vision_interfaces:msg/VisionResponse.idl
// generated code does not contain a copyright notice

#ifndef PM_VISION_INTERFACES__MSG__DETAIL__VISION_RESPONSE__TRAITS_HPP_
#define PM_VISION_INTERFACES__MSG__DETAIL__VISION_RESPONSE__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "pm_vision_interfaces/msg/detail/vision_response__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'cross_validation'
#include "pm_vision_interfaces/msg/detail/cross_validation__traits.hpp"
// Member 'results'
#include "pm_vision_interfaces/msg/detail/vision_results__traits.hpp"

namespace pm_vision_interfaces
{

namespace msg
{

inline void to_flow_style_yaml(
  const VisionResponse & msg,
  std::ostream & out)
{
  out << "{";
  // member: vision_ok
  {
    out << "vision_ok: ";
    rosidl_generator_traits::value_to_yaml(msg.vision_ok, out);
    out << ", ";
  }

  // member: process_name
  {
    out << "process_name: ";
    rosidl_generator_traits::value_to_yaml(msg.process_name, out);
    out << ", ";
  }

  // member: process_uid
  {
    out << "process_uid: ";
    rosidl_generator_traits::value_to_yaml(msg.process_uid, out);
    out << ", ";
  }

  // member: exec_timestamp
  {
    out << "exec_timestamp: ";
    rosidl_generator_traits::value_to_yaml(msg.exec_timestamp, out);
    out << ", ";
  }

  // member: cross_validation
  {
    out << "cross_validation: ";
    to_flow_style_yaml(msg.cross_validation, out);
    out << ", ";
  }

  // member: results
  {
    out << "results: ";
    to_flow_style_yaml(msg.results, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const VisionResponse & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: vision_ok
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "vision_ok: ";
    rosidl_generator_traits::value_to_yaml(msg.vision_ok, out);
    out << "\n";
  }

  // member: process_name
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "process_name: ";
    rosidl_generator_traits::value_to_yaml(msg.process_name, out);
    out << "\n";
  }

  // member: process_uid
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "process_uid: ";
    rosidl_generator_traits::value_to_yaml(msg.process_uid, out);
    out << "\n";
  }

  // member: exec_timestamp
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "exec_timestamp: ";
    rosidl_generator_traits::value_to_yaml(msg.exec_timestamp, out);
    out << "\n";
  }

  // member: cross_validation
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "cross_validation:\n";
    to_block_style_yaml(msg.cross_validation, out, indentation + 2);
  }

  // member: results
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "results:\n";
    to_block_style_yaml(msg.results, out, indentation + 2);
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const VisionResponse & msg, bool use_flow_style = false)
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
  const pm_vision_interfaces::msg::VisionResponse & msg,
  std::ostream & out, size_t indentation = 0)
{
  pm_vision_interfaces::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use pm_vision_interfaces::msg::to_yaml() instead")]]
inline std::string to_yaml(const pm_vision_interfaces::msg::VisionResponse & msg)
{
  return pm_vision_interfaces::msg::to_yaml(msg);
}

template<>
inline const char * data_type<pm_vision_interfaces::msg::VisionResponse>()
{
  return "pm_vision_interfaces::msg::VisionResponse";
}

template<>
inline const char * name<pm_vision_interfaces::msg::VisionResponse>()
{
  return "pm_vision_interfaces/msg/VisionResponse";
}

template<>
struct has_fixed_size<pm_vision_interfaces::msg::VisionResponse>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<pm_vision_interfaces::msg::VisionResponse>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<pm_vision_interfaces::msg::VisionResponse>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // PM_VISION_INTERFACES__MSG__DETAIL__VISION_RESPONSE__TRAITS_HPP_

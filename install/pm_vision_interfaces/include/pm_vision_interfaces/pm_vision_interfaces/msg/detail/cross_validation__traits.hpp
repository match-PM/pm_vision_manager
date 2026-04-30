// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from pm_vision_interfaces:msg/CrossValidation.idl
// generated code does not contain a copyright notice

#ifndef PM_VISION_INTERFACES__MSG__DETAIL__CROSS_VALIDATION__TRAITS_HPP_
#define PM_VISION_INTERFACES__MSG__DETAIL__CROSS_VALIDATION__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "pm_vision_interfaces/msg/detail/cross_validation__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace pm_vision_interfaces
{

namespace msg
{

inline void to_flow_style_yaml(
  const CrossValidation & msg,
  std::ostream & out)
{
  out << "{";
  // member: image_source_name
  {
    out << "image_source_name: ";
    rosidl_generator_traits::value_to_yaml(msg.image_source_name, out);
    out << ", ";
  }

  // member: vision_ok
  {
    out << "vision_ok: ";
    rosidl_generator_traits::value_to_yaml(msg.vision_ok, out);
    out << ", ";
  }

  // member: failed_images
  {
    if (msg.failed_images.size() == 0) {
      out << "failed_images: []";
    } else {
      out << "failed_images: [";
      size_t pending_items = msg.failed_images.size();
      for (auto item : msg.failed_images) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: numb_images
  {
    out << "numb_images: ";
    rosidl_generator_traits::value_to_yaml(msg.numb_images, out);
    out << ", ";
  }

  // member: counter_error
  {
    out << "counter_error: ";
    rosidl_generator_traits::value_to_yaml(msg.counter_error, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const CrossValidation & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: image_source_name
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "image_source_name: ";
    rosidl_generator_traits::value_to_yaml(msg.image_source_name, out);
    out << "\n";
  }

  // member: vision_ok
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "vision_ok: ";
    rosidl_generator_traits::value_to_yaml(msg.vision_ok, out);
    out << "\n";
  }

  // member: failed_images
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.failed_images.size() == 0) {
      out << "failed_images: []\n";
    } else {
      out << "failed_images:\n";
      for (auto item : msg.failed_images) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }

  // member: numb_images
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "numb_images: ";
    rosidl_generator_traits::value_to_yaml(msg.numb_images, out);
    out << "\n";
  }

  // member: counter_error
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "counter_error: ";
    rosidl_generator_traits::value_to_yaml(msg.counter_error, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const CrossValidation & msg, bool use_flow_style = false)
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
  const pm_vision_interfaces::msg::CrossValidation & msg,
  std::ostream & out, size_t indentation = 0)
{
  pm_vision_interfaces::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use pm_vision_interfaces::msg::to_yaml() instead")]]
inline std::string to_yaml(const pm_vision_interfaces::msg::CrossValidation & msg)
{
  return pm_vision_interfaces::msg::to_yaml(msg);
}

template<>
inline const char * data_type<pm_vision_interfaces::msg::CrossValidation>()
{
  return "pm_vision_interfaces::msg::CrossValidation";
}

template<>
inline const char * name<pm_vision_interfaces::msg::CrossValidation>()
{
  return "pm_vision_interfaces/msg/CrossValidation";
}

template<>
struct has_fixed_size<pm_vision_interfaces::msg::CrossValidation>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<pm_vision_interfaces::msg::CrossValidation>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<pm_vision_interfaces::msg::CrossValidation>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // PM_VISION_INTERFACES__MSG__DETAIL__CROSS_VALIDATION__TRAITS_HPP_

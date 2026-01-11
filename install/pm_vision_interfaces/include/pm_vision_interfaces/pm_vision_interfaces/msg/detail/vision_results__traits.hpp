// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from pm_vision_interfaces:msg/VisionResults.idl
// generated code does not contain a copyright notice

#ifndef PM_VISION_INTERFACES__MSG__DETAIL__VISION_RESULTS__TRAITS_HPP_
#define PM_VISION_INTERFACES__MSG__DETAIL__VISION_RESULTS__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "pm_vision_interfaces/msg/detail/vision_results__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'points'
#include "pm_vision_interfaces/msg/detail/vision_point__traits.hpp"
// Member 'lines'
#include "pm_vision_interfaces/msg/detail/vision_line__traits.hpp"
// Member 'areas'
#include "pm_vision_interfaces/msg/detail/vision_area__traits.hpp"
// Member 'circles'
#include "pm_vision_interfaces/msg/detail/vision_circle__traits.hpp"
// Member 'image_sharpness'
#include "pm_vision_interfaces/msg/detail/image_sharpness__traits.hpp"

namespace pm_vision_interfaces
{

namespace msg
{

inline void to_flow_style_yaml(
  const VisionResults & msg,
  std::ostream & out)
{
  out << "{";
  // member: points
  {
    if (msg.points.size() == 0) {
      out << "points: []";
    } else {
      out << "points: [";
      size_t pending_items = msg.points.size();
      for (auto item : msg.points) {
        to_flow_style_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: lines
  {
    if (msg.lines.size() == 0) {
      out << "lines: []";
    } else {
      out << "lines: [";
      size_t pending_items = msg.lines.size();
      for (auto item : msg.lines) {
        to_flow_style_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: areas
  {
    if (msg.areas.size() == 0) {
      out << "areas: []";
    } else {
      out << "areas: [";
      size_t pending_items = msg.areas.size();
      for (auto item : msg.areas) {
        to_flow_style_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: circles
  {
    if (msg.circles.size() == 0) {
      out << "circles: []";
    } else {
      out << "circles: [";
      size_t pending_items = msg.circles.size();
      for (auto item : msg.circles) {
        to_flow_style_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: image_sharpness
  {
    out << "image_sharpness: ";
    to_flow_style_yaml(msg.image_sharpness, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const VisionResults & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: points
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.points.size() == 0) {
      out << "points: []\n";
    } else {
      out << "points:\n";
      for (auto item : msg.points) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "-\n";
        to_block_style_yaml(item, out, indentation + 2);
      }
    }
  }

  // member: lines
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.lines.size() == 0) {
      out << "lines: []\n";
    } else {
      out << "lines:\n";
      for (auto item : msg.lines) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "-\n";
        to_block_style_yaml(item, out, indentation + 2);
      }
    }
  }

  // member: areas
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.areas.size() == 0) {
      out << "areas: []\n";
    } else {
      out << "areas:\n";
      for (auto item : msg.areas) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "-\n";
        to_block_style_yaml(item, out, indentation + 2);
      }
    }
  }

  // member: circles
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.circles.size() == 0) {
      out << "circles: []\n";
    } else {
      out << "circles:\n";
      for (auto item : msg.circles) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "-\n";
        to_block_style_yaml(item, out, indentation + 2);
      }
    }
  }

  // member: image_sharpness
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "image_sharpness:\n";
    to_block_style_yaml(msg.image_sharpness, out, indentation + 2);
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const VisionResults & msg, bool use_flow_style = false)
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
  const pm_vision_interfaces::msg::VisionResults & msg,
  std::ostream & out, size_t indentation = 0)
{
  pm_vision_interfaces::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use pm_vision_interfaces::msg::to_yaml() instead")]]
inline std::string to_yaml(const pm_vision_interfaces::msg::VisionResults & msg)
{
  return pm_vision_interfaces::msg::to_yaml(msg);
}

template<>
inline const char * data_type<pm_vision_interfaces::msg::VisionResults>()
{
  return "pm_vision_interfaces::msg::VisionResults";
}

template<>
inline const char * name<pm_vision_interfaces::msg::VisionResults>()
{
  return "pm_vision_interfaces/msg/VisionResults";
}

template<>
struct has_fixed_size<pm_vision_interfaces::msg::VisionResults>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<pm_vision_interfaces::msg::VisionResults>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<pm_vision_interfaces::msg::VisionResults>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // PM_VISION_INTERFACES__MSG__DETAIL__VISION_RESULTS__TRAITS_HPP_

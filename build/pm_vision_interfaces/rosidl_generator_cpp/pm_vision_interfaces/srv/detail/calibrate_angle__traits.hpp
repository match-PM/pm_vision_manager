// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from pm_vision_interfaces:srv/CalibrateAngle.idl
// generated code does not contain a copyright notice

#ifndef PM_VISION_INTERFACES__SRV__DETAIL__CALIBRATE_ANGLE__TRAITS_HPP_
#define PM_VISION_INTERFACES__SRV__DETAIL__CALIBRATE_ANGLE__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "pm_vision_interfaces/srv/detail/calibrate_angle__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace pm_vision_interfaces
{

namespace srv
{

inline void to_flow_style_yaml(
  const CalibrateAngle_Request & msg,
  std::ostream & out)
{
  out << "{";
  // member: angle_diff
  {
    out << "angle_diff: ";
    rosidl_generator_traits::value_to_yaml(msg.angle_diff, out);
    out << ", ";
  }

  // member: camera_config_file_name
  {
    out << "camera_config_file_name: ";
    rosidl_generator_traits::value_to_yaml(msg.camera_config_file_name, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const CalibrateAngle_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: angle_diff
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "angle_diff: ";
    rosidl_generator_traits::value_to_yaml(msg.angle_diff, out);
    out << "\n";
  }

  // member: camera_config_file_name
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "camera_config_file_name: ";
    rosidl_generator_traits::value_to_yaml(msg.camera_config_file_name, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const CalibrateAngle_Request & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace srv

}  // namespace pm_vision_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use pm_vision_interfaces::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const pm_vision_interfaces::srv::CalibrateAngle_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  pm_vision_interfaces::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use pm_vision_interfaces::srv::to_yaml() instead")]]
inline std::string to_yaml(const pm_vision_interfaces::srv::CalibrateAngle_Request & msg)
{
  return pm_vision_interfaces::srv::to_yaml(msg);
}

template<>
inline const char * data_type<pm_vision_interfaces::srv::CalibrateAngle_Request>()
{
  return "pm_vision_interfaces::srv::CalibrateAngle_Request";
}

template<>
inline const char * name<pm_vision_interfaces::srv::CalibrateAngle_Request>()
{
  return "pm_vision_interfaces/srv/CalibrateAngle_Request";
}

template<>
struct has_fixed_size<pm_vision_interfaces::srv::CalibrateAngle_Request>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<pm_vision_interfaces::srv::CalibrateAngle_Request>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<pm_vision_interfaces::srv::CalibrateAngle_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace pm_vision_interfaces
{

namespace srv
{

inline void to_flow_style_yaml(
  const CalibrateAngle_Response & msg,
  std::ostream & out)
{
  out << "{";
  // member: success
  {
    out << "success: ";
    rosidl_generator_traits::value_to_yaml(msg.success, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const CalibrateAngle_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: success
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "success: ";
    rosidl_generator_traits::value_to_yaml(msg.success, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const CalibrateAngle_Response & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace srv

}  // namespace pm_vision_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use pm_vision_interfaces::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const pm_vision_interfaces::srv::CalibrateAngle_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  pm_vision_interfaces::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use pm_vision_interfaces::srv::to_yaml() instead")]]
inline std::string to_yaml(const pm_vision_interfaces::srv::CalibrateAngle_Response & msg)
{
  return pm_vision_interfaces::srv::to_yaml(msg);
}

template<>
inline const char * data_type<pm_vision_interfaces::srv::CalibrateAngle_Response>()
{
  return "pm_vision_interfaces::srv::CalibrateAngle_Response";
}

template<>
inline const char * name<pm_vision_interfaces::srv::CalibrateAngle_Response>()
{
  return "pm_vision_interfaces/srv/CalibrateAngle_Response";
}

template<>
struct has_fixed_size<pm_vision_interfaces::srv::CalibrateAngle_Response>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<pm_vision_interfaces::srv::CalibrateAngle_Response>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<pm_vision_interfaces::srv::CalibrateAngle_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<pm_vision_interfaces::srv::CalibrateAngle>()
{
  return "pm_vision_interfaces::srv::CalibrateAngle";
}

template<>
inline const char * name<pm_vision_interfaces::srv::CalibrateAngle>()
{
  return "pm_vision_interfaces/srv/CalibrateAngle";
}

template<>
struct has_fixed_size<pm_vision_interfaces::srv::CalibrateAngle>
  : std::integral_constant<
    bool,
    has_fixed_size<pm_vision_interfaces::srv::CalibrateAngle_Request>::value &&
    has_fixed_size<pm_vision_interfaces::srv::CalibrateAngle_Response>::value
  >
{
};

template<>
struct has_bounded_size<pm_vision_interfaces::srv::CalibrateAngle>
  : std::integral_constant<
    bool,
    has_bounded_size<pm_vision_interfaces::srv::CalibrateAngle_Request>::value &&
    has_bounded_size<pm_vision_interfaces::srv::CalibrateAngle_Response>::value
  >
{
};

template<>
struct is_service<pm_vision_interfaces::srv::CalibrateAngle>
  : std::true_type
{
};

template<>
struct is_service_request<pm_vision_interfaces::srv::CalibrateAngle_Request>
  : std::true_type
{
};

template<>
struct is_service_response<pm_vision_interfaces::srv::CalibrateAngle_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

#endif  // PM_VISION_INTERFACES__SRV__DETAIL__CALIBRATE_ANGLE__TRAITS_HPP_

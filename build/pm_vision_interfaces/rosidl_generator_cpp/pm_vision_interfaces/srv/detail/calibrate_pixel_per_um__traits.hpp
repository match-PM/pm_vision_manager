// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from pm_vision_interfaces:srv/CalibratePixelPerUm.idl
// generated code does not contain a copyright notice

#ifndef PM_VISION_INTERFACES__SRV__DETAIL__CALIBRATE_PIXEL_PER_UM__TRAITS_HPP_
#define PM_VISION_INTERFACES__SRV__DETAIL__CALIBRATE_PIXEL_PER_UM__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "pm_vision_interfaces/srv/detail/calibrate_pixel_per_um__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace pm_vision_interfaces
{

namespace srv
{

inline void to_flow_style_yaml(
  const CalibratePixelPerUm_Request & msg,
  std::ostream & out)
{
  out << "{";
  // member: multiplicator
  {
    out << "multiplicator: ";
    rosidl_generator_traits::value_to_yaml(msg.multiplicator, out);
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
  const CalibratePixelPerUm_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: multiplicator
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "multiplicator: ";
    rosidl_generator_traits::value_to_yaml(msg.multiplicator, out);
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

inline std::string to_yaml(const CalibratePixelPerUm_Request & msg, bool use_flow_style = false)
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
  const pm_vision_interfaces::srv::CalibratePixelPerUm_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  pm_vision_interfaces::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use pm_vision_interfaces::srv::to_yaml() instead")]]
inline std::string to_yaml(const pm_vision_interfaces::srv::CalibratePixelPerUm_Request & msg)
{
  return pm_vision_interfaces::srv::to_yaml(msg);
}

template<>
inline const char * data_type<pm_vision_interfaces::srv::CalibratePixelPerUm_Request>()
{
  return "pm_vision_interfaces::srv::CalibratePixelPerUm_Request";
}

template<>
inline const char * name<pm_vision_interfaces::srv::CalibratePixelPerUm_Request>()
{
  return "pm_vision_interfaces/srv/CalibratePixelPerUm_Request";
}

template<>
struct has_fixed_size<pm_vision_interfaces::srv::CalibratePixelPerUm_Request>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<pm_vision_interfaces::srv::CalibratePixelPerUm_Request>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<pm_vision_interfaces::srv::CalibratePixelPerUm_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace pm_vision_interfaces
{

namespace srv
{

inline void to_flow_style_yaml(
  const CalibratePixelPerUm_Response & msg,
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
  const CalibratePixelPerUm_Response & msg,
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

inline std::string to_yaml(const CalibratePixelPerUm_Response & msg, bool use_flow_style = false)
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
  const pm_vision_interfaces::srv::CalibratePixelPerUm_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  pm_vision_interfaces::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use pm_vision_interfaces::srv::to_yaml() instead")]]
inline std::string to_yaml(const pm_vision_interfaces::srv::CalibratePixelPerUm_Response & msg)
{
  return pm_vision_interfaces::srv::to_yaml(msg);
}

template<>
inline const char * data_type<pm_vision_interfaces::srv::CalibratePixelPerUm_Response>()
{
  return "pm_vision_interfaces::srv::CalibratePixelPerUm_Response";
}

template<>
inline const char * name<pm_vision_interfaces::srv::CalibratePixelPerUm_Response>()
{
  return "pm_vision_interfaces/srv/CalibratePixelPerUm_Response";
}

template<>
struct has_fixed_size<pm_vision_interfaces::srv::CalibratePixelPerUm_Response>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<pm_vision_interfaces::srv::CalibratePixelPerUm_Response>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<pm_vision_interfaces::srv::CalibratePixelPerUm_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<pm_vision_interfaces::srv::CalibratePixelPerUm>()
{
  return "pm_vision_interfaces::srv::CalibratePixelPerUm";
}

template<>
inline const char * name<pm_vision_interfaces::srv::CalibratePixelPerUm>()
{
  return "pm_vision_interfaces/srv/CalibratePixelPerUm";
}

template<>
struct has_fixed_size<pm_vision_interfaces::srv::CalibratePixelPerUm>
  : std::integral_constant<
    bool,
    has_fixed_size<pm_vision_interfaces::srv::CalibratePixelPerUm_Request>::value &&
    has_fixed_size<pm_vision_interfaces::srv::CalibratePixelPerUm_Response>::value
  >
{
};

template<>
struct has_bounded_size<pm_vision_interfaces::srv::CalibratePixelPerUm>
  : std::integral_constant<
    bool,
    has_bounded_size<pm_vision_interfaces::srv::CalibratePixelPerUm_Request>::value &&
    has_bounded_size<pm_vision_interfaces::srv::CalibratePixelPerUm_Response>::value
  >
{
};

template<>
struct is_service<pm_vision_interfaces::srv::CalibratePixelPerUm>
  : std::true_type
{
};

template<>
struct is_service_request<pm_vision_interfaces::srv::CalibratePixelPerUm_Request>
  : std::true_type
{
};

template<>
struct is_service_response<pm_vision_interfaces::srv::CalibratePixelPerUm_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

#endif  // PM_VISION_INTERFACES__SRV__DETAIL__CALIBRATE_PIXEL_PER_UM__TRAITS_HPP_

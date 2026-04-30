// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from pm_vision_interfaces:srv/ExecuteVision.idl
// generated code does not contain a copyright notice

#ifndef PM_VISION_INTERFACES__SRV__DETAIL__EXECUTE_VISION__TRAITS_HPP_
#define PM_VISION_INTERFACES__SRV__DETAIL__EXECUTE_VISION__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "pm_vision_interfaces/srv/detail/execute_vision__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace pm_vision_interfaces
{

namespace srv
{

inline void to_flow_style_yaml(
  const ExecuteVision_Request & msg,
  std::ostream & out)
{
  out << "{";
  // member: process_filename
  {
    out << "process_filename: ";
    rosidl_generator_traits::value_to_yaml(msg.process_filename, out);
    out << ", ";
  }

  // member: camera_config_filename
  {
    out << "camera_config_filename: ";
    rosidl_generator_traits::value_to_yaml(msg.camera_config_filename, out);
    out << ", ";
  }

  // member: process_uid
  {
    out << "process_uid: ";
    rosidl_generator_traits::value_to_yaml(msg.process_uid, out);
    out << ", ";
  }

  // member: image_display_time
  {
    out << "image_display_time: ";
    rosidl_generator_traits::value_to_yaml(msg.image_display_time, out);
    out << ", ";
  }

  // member: run_cross_validation
  {
    out << "run_cross_validation: ";
    rosidl_generator_traits::value_to_yaml(msg.run_cross_validation, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const ExecuteVision_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: process_filename
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "process_filename: ";
    rosidl_generator_traits::value_to_yaml(msg.process_filename, out);
    out << "\n";
  }

  // member: camera_config_filename
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "camera_config_filename: ";
    rosidl_generator_traits::value_to_yaml(msg.camera_config_filename, out);
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

  // member: image_display_time
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "image_display_time: ";
    rosidl_generator_traits::value_to_yaml(msg.image_display_time, out);
    out << "\n";
  }

  // member: run_cross_validation
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "run_cross_validation: ";
    rosidl_generator_traits::value_to_yaml(msg.run_cross_validation, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const ExecuteVision_Request & msg, bool use_flow_style = false)
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
  const pm_vision_interfaces::srv::ExecuteVision_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  pm_vision_interfaces::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use pm_vision_interfaces::srv::to_yaml() instead")]]
inline std::string to_yaml(const pm_vision_interfaces::srv::ExecuteVision_Request & msg)
{
  return pm_vision_interfaces::srv::to_yaml(msg);
}

template<>
inline const char * data_type<pm_vision_interfaces::srv::ExecuteVision_Request>()
{
  return "pm_vision_interfaces::srv::ExecuteVision_Request";
}

template<>
inline const char * name<pm_vision_interfaces::srv::ExecuteVision_Request>()
{
  return "pm_vision_interfaces/srv/ExecuteVision_Request";
}

template<>
struct has_fixed_size<pm_vision_interfaces::srv::ExecuteVision_Request>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<pm_vision_interfaces::srv::ExecuteVision_Request>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<pm_vision_interfaces::srv::ExecuteVision_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

// Include directives for member types
// Member 'vision_response'
#include "pm_vision_interfaces/msg/detail/vision_response__traits.hpp"

namespace pm_vision_interfaces
{

namespace srv
{

inline void to_flow_style_yaml(
  const ExecuteVision_Response & msg,
  std::ostream & out)
{
  out << "{";
  // member: success
  {
    out << "success: ";
    rosidl_generator_traits::value_to_yaml(msg.success, out);
    out << ", ";
  }

  // member: results_path
  {
    out << "results_path: ";
    rosidl_generator_traits::value_to_yaml(msg.results_path, out);
    out << ", ";
  }

  // member: vision_response
  {
    out << "vision_response: ";
    to_flow_style_yaml(msg.vision_response, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const ExecuteVision_Response & msg,
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

  // member: results_path
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "results_path: ";
    rosidl_generator_traits::value_to_yaml(msg.results_path, out);
    out << "\n";
  }

  // member: vision_response
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "vision_response:\n";
    to_block_style_yaml(msg.vision_response, out, indentation + 2);
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const ExecuteVision_Response & msg, bool use_flow_style = false)
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
  const pm_vision_interfaces::srv::ExecuteVision_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  pm_vision_interfaces::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use pm_vision_interfaces::srv::to_yaml() instead")]]
inline std::string to_yaml(const pm_vision_interfaces::srv::ExecuteVision_Response & msg)
{
  return pm_vision_interfaces::srv::to_yaml(msg);
}

template<>
inline const char * data_type<pm_vision_interfaces::srv::ExecuteVision_Response>()
{
  return "pm_vision_interfaces::srv::ExecuteVision_Response";
}

template<>
inline const char * name<pm_vision_interfaces::srv::ExecuteVision_Response>()
{
  return "pm_vision_interfaces/srv/ExecuteVision_Response";
}

template<>
struct has_fixed_size<pm_vision_interfaces::srv::ExecuteVision_Response>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<pm_vision_interfaces::srv::ExecuteVision_Response>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<pm_vision_interfaces::srv::ExecuteVision_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<pm_vision_interfaces::srv::ExecuteVision>()
{
  return "pm_vision_interfaces::srv::ExecuteVision";
}

template<>
inline const char * name<pm_vision_interfaces::srv::ExecuteVision>()
{
  return "pm_vision_interfaces/srv/ExecuteVision";
}

template<>
struct has_fixed_size<pm_vision_interfaces::srv::ExecuteVision>
  : std::integral_constant<
    bool,
    has_fixed_size<pm_vision_interfaces::srv::ExecuteVision_Request>::value &&
    has_fixed_size<pm_vision_interfaces::srv::ExecuteVision_Response>::value
  >
{
};

template<>
struct has_bounded_size<pm_vision_interfaces::srv::ExecuteVision>
  : std::integral_constant<
    bool,
    has_bounded_size<pm_vision_interfaces::srv::ExecuteVision_Request>::value &&
    has_bounded_size<pm_vision_interfaces::srv::ExecuteVision_Response>::value
  >
{
};

template<>
struct is_service<pm_vision_interfaces::srv::ExecuteVision>
  : std::true_type
{
};

template<>
struct is_service_request<pm_vision_interfaces::srv::ExecuteVision_Request>
  : std::true_type
{
};

template<>
struct is_service_response<pm_vision_interfaces::srv::ExecuteVision_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

#endif  // PM_VISION_INTERFACES__SRV__DETAIL__EXECUTE_VISION__TRAITS_HPP_

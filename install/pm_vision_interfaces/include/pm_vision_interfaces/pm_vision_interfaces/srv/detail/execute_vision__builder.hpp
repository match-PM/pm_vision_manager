// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from pm_vision_interfaces:srv/ExecuteVision.idl
// generated code does not contain a copyright notice

#ifndef PM_VISION_INTERFACES__SRV__DETAIL__EXECUTE_VISION__BUILDER_HPP_
#define PM_VISION_INTERFACES__SRV__DETAIL__EXECUTE_VISION__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "pm_vision_interfaces/srv/detail/execute_vision__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace pm_vision_interfaces
{

namespace srv
{

namespace builder
{

class Init_ExecuteVision_Request_run_cross_validation
{
public:
  explicit Init_ExecuteVision_Request_run_cross_validation(::pm_vision_interfaces::srv::ExecuteVision_Request & msg)
  : msg_(msg)
  {}
  ::pm_vision_interfaces::srv::ExecuteVision_Request run_cross_validation(::pm_vision_interfaces::srv::ExecuteVision_Request::_run_cross_validation_type arg)
  {
    msg_.run_cross_validation = std::move(arg);
    return std::move(msg_);
  }

private:
  ::pm_vision_interfaces::srv::ExecuteVision_Request msg_;
};

class Init_ExecuteVision_Request_image_display_time
{
public:
  explicit Init_ExecuteVision_Request_image_display_time(::pm_vision_interfaces::srv::ExecuteVision_Request & msg)
  : msg_(msg)
  {}
  Init_ExecuteVision_Request_run_cross_validation image_display_time(::pm_vision_interfaces::srv::ExecuteVision_Request::_image_display_time_type arg)
  {
    msg_.image_display_time = std::move(arg);
    return Init_ExecuteVision_Request_run_cross_validation(msg_);
  }

private:
  ::pm_vision_interfaces::srv::ExecuteVision_Request msg_;
};

class Init_ExecuteVision_Request_process_uid
{
public:
  explicit Init_ExecuteVision_Request_process_uid(::pm_vision_interfaces::srv::ExecuteVision_Request & msg)
  : msg_(msg)
  {}
  Init_ExecuteVision_Request_image_display_time process_uid(::pm_vision_interfaces::srv::ExecuteVision_Request::_process_uid_type arg)
  {
    msg_.process_uid = std::move(arg);
    return Init_ExecuteVision_Request_image_display_time(msg_);
  }

private:
  ::pm_vision_interfaces::srv::ExecuteVision_Request msg_;
};

class Init_ExecuteVision_Request_camera_config_filename
{
public:
  explicit Init_ExecuteVision_Request_camera_config_filename(::pm_vision_interfaces::srv::ExecuteVision_Request & msg)
  : msg_(msg)
  {}
  Init_ExecuteVision_Request_process_uid camera_config_filename(::pm_vision_interfaces::srv::ExecuteVision_Request::_camera_config_filename_type arg)
  {
    msg_.camera_config_filename = std::move(arg);
    return Init_ExecuteVision_Request_process_uid(msg_);
  }

private:
  ::pm_vision_interfaces::srv::ExecuteVision_Request msg_;
};

class Init_ExecuteVision_Request_process_filename
{
public:
  Init_ExecuteVision_Request_process_filename()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_ExecuteVision_Request_camera_config_filename process_filename(::pm_vision_interfaces::srv::ExecuteVision_Request::_process_filename_type arg)
  {
    msg_.process_filename = std::move(arg);
    return Init_ExecuteVision_Request_camera_config_filename(msg_);
  }

private:
  ::pm_vision_interfaces::srv::ExecuteVision_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::pm_vision_interfaces::srv::ExecuteVision_Request>()
{
  return pm_vision_interfaces::srv::builder::Init_ExecuteVision_Request_process_filename();
}

}  // namespace pm_vision_interfaces


namespace pm_vision_interfaces
{

namespace srv
{

namespace builder
{

class Init_ExecuteVision_Response_vision_response
{
public:
  explicit Init_ExecuteVision_Response_vision_response(::pm_vision_interfaces::srv::ExecuteVision_Response & msg)
  : msg_(msg)
  {}
  ::pm_vision_interfaces::srv::ExecuteVision_Response vision_response(::pm_vision_interfaces::srv::ExecuteVision_Response::_vision_response_type arg)
  {
    msg_.vision_response = std::move(arg);
    return std::move(msg_);
  }

private:
  ::pm_vision_interfaces::srv::ExecuteVision_Response msg_;
};

class Init_ExecuteVision_Response_results_path
{
public:
  explicit Init_ExecuteVision_Response_results_path(::pm_vision_interfaces::srv::ExecuteVision_Response & msg)
  : msg_(msg)
  {}
  Init_ExecuteVision_Response_vision_response results_path(::pm_vision_interfaces::srv::ExecuteVision_Response::_results_path_type arg)
  {
    msg_.results_path = std::move(arg);
    return Init_ExecuteVision_Response_vision_response(msg_);
  }

private:
  ::pm_vision_interfaces::srv::ExecuteVision_Response msg_;
};

class Init_ExecuteVision_Response_success
{
public:
  Init_ExecuteVision_Response_success()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_ExecuteVision_Response_results_path success(::pm_vision_interfaces::srv::ExecuteVision_Response::_success_type arg)
  {
    msg_.success = std::move(arg);
    return Init_ExecuteVision_Response_results_path(msg_);
  }

private:
  ::pm_vision_interfaces::srv::ExecuteVision_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::pm_vision_interfaces::srv::ExecuteVision_Response>()
{
  return pm_vision_interfaces::srv::builder::Init_ExecuteVision_Response_success();
}

}  // namespace pm_vision_interfaces

#endif  // PM_VISION_INTERFACES__SRV__DETAIL__EXECUTE_VISION__BUILDER_HPP_

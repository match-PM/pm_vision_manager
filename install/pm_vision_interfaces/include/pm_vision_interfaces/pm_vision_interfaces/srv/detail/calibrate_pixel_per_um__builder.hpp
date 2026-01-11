// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from pm_vision_interfaces:srv/CalibratePixelPerUm.idl
// generated code does not contain a copyright notice

#ifndef PM_VISION_INTERFACES__SRV__DETAIL__CALIBRATE_PIXEL_PER_UM__BUILDER_HPP_
#define PM_VISION_INTERFACES__SRV__DETAIL__CALIBRATE_PIXEL_PER_UM__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "pm_vision_interfaces/srv/detail/calibrate_pixel_per_um__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace pm_vision_interfaces
{

namespace srv
{

namespace builder
{

class Init_CalibratePixelPerUm_Request_camera_config_file_name
{
public:
  explicit Init_CalibratePixelPerUm_Request_camera_config_file_name(::pm_vision_interfaces::srv::CalibratePixelPerUm_Request & msg)
  : msg_(msg)
  {}
  ::pm_vision_interfaces::srv::CalibratePixelPerUm_Request camera_config_file_name(::pm_vision_interfaces::srv::CalibratePixelPerUm_Request::_camera_config_file_name_type arg)
  {
    msg_.camera_config_file_name = std::move(arg);
    return std::move(msg_);
  }

private:
  ::pm_vision_interfaces::srv::CalibratePixelPerUm_Request msg_;
};

class Init_CalibratePixelPerUm_Request_multiplicator
{
public:
  Init_CalibratePixelPerUm_Request_multiplicator()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_CalibratePixelPerUm_Request_camera_config_file_name multiplicator(::pm_vision_interfaces::srv::CalibratePixelPerUm_Request::_multiplicator_type arg)
  {
    msg_.multiplicator = std::move(arg);
    return Init_CalibratePixelPerUm_Request_camera_config_file_name(msg_);
  }

private:
  ::pm_vision_interfaces::srv::CalibratePixelPerUm_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::pm_vision_interfaces::srv::CalibratePixelPerUm_Request>()
{
  return pm_vision_interfaces::srv::builder::Init_CalibratePixelPerUm_Request_multiplicator();
}

}  // namespace pm_vision_interfaces


namespace pm_vision_interfaces
{

namespace srv
{

namespace builder
{

class Init_CalibratePixelPerUm_Response_success
{
public:
  Init_CalibratePixelPerUm_Response_success()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::pm_vision_interfaces::srv::CalibratePixelPerUm_Response success(::pm_vision_interfaces::srv::CalibratePixelPerUm_Response::_success_type arg)
  {
    msg_.success = std::move(arg);
    return std::move(msg_);
  }

private:
  ::pm_vision_interfaces::srv::CalibratePixelPerUm_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::pm_vision_interfaces::srv::CalibratePixelPerUm_Response>()
{
  return pm_vision_interfaces::srv::builder::Init_CalibratePixelPerUm_Response_success();
}

}  // namespace pm_vision_interfaces

#endif  // PM_VISION_INTERFACES__SRV__DETAIL__CALIBRATE_PIXEL_PER_UM__BUILDER_HPP_

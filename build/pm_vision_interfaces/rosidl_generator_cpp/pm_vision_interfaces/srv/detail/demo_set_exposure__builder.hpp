// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from pm_vision_interfaces:srv/DemoSetExposure.idl
// generated code does not contain a copyright notice

#ifndef PM_VISION_INTERFACES__SRV__DETAIL__DEMO_SET_EXPOSURE__BUILDER_HPP_
#define PM_VISION_INTERFACES__SRV__DETAIL__DEMO_SET_EXPOSURE__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "pm_vision_interfaces/srv/detail/demo_set_exposure__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace pm_vision_interfaces
{

namespace srv
{

namespace builder
{

class Init_DemoSetExposure_Request_target_value
{
public:
  Init_DemoSetExposure_Request_target_value()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::pm_vision_interfaces::srv::DemoSetExposure_Request target_value(::pm_vision_interfaces::srv::DemoSetExposure_Request::_target_value_type arg)
  {
    msg_.target_value = std::move(arg);
    return std::move(msg_);
  }

private:
  ::pm_vision_interfaces::srv::DemoSetExposure_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::pm_vision_interfaces::srv::DemoSetExposure_Request>()
{
  return pm_vision_interfaces::srv::builder::Init_DemoSetExposure_Request_target_value();
}

}  // namespace pm_vision_interfaces


namespace pm_vision_interfaces
{

namespace srv
{

namespace builder
{

class Init_DemoSetExposure_Response_success
{
public:
  Init_DemoSetExposure_Response_success()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::pm_vision_interfaces::srv::DemoSetExposure_Response success(::pm_vision_interfaces::srv::DemoSetExposure_Response::_success_type arg)
  {
    msg_.success = std::move(arg);
    return std::move(msg_);
  }

private:
  ::pm_vision_interfaces::srv::DemoSetExposure_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::pm_vision_interfaces::srv::DemoSetExposure_Response>()
{
  return pm_vision_interfaces::srv::builder::Init_DemoSetExposure_Response_success();
}

}  // namespace pm_vision_interfaces

#endif  // PM_VISION_INTERFACES__SRV__DETAIL__DEMO_SET_EXPOSURE__BUILDER_HPP_

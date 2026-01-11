// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from pm_vision_interfaces:msg/VisionResponse.idl
// generated code does not contain a copyright notice

#ifndef PM_VISION_INTERFACES__MSG__DETAIL__VISION_RESPONSE__BUILDER_HPP_
#define PM_VISION_INTERFACES__MSG__DETAIL__VISION_RESPONSE__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "pm_vision_interfaces/msg/detail/vision_response__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace pm_vision_interfaces
{

namespace msg
{

namespace builder
{

class Init_VisionResponse_results
{
public:
  explicit Init_VisionResponse_results(::pm_vision_interfaces::msg::VisionResponse & msg)
  : msg_(msg)
  {}
  ::pm_vision_interfaces::msg::VisionResponse results(::pm_vision_interfaces::msg::VisionResponse::_results_type arg)
  {
    msg_.results = std::move(arg);
    return std::move(msg_);
  }

private:
  ::pm_vision_interfaces::msg::VisionResponse msg_;
};

class Init_VisionResponse_cross_validation
{
public:
  explicit Init_VisionResponse_cross_validation(::pm_vision_interfaces::msg::VisionResponse & msg)
  : msg_(msg)
  {}
  Init_VisionResponse_results cross_validation(::pm_vision_interfaces::msg::VisionResponse::_cross_validation_type arg)
  {
    msg_.cross_validation = std::move(arg);
    return Init_VisionResponse_results(msg_);
  }

private:
  ::pm_vision_interfaces::msg::VisionResponse msg_;
};

class Init_VisionResponse_exec_timestamp
{
public:
  explicit Init_VisionResponse_exec_timestamp(::pm_vision_interfaces::msg::VisionResponse & msg)
  : msg_(msg)
  {}
  Init_VisionResponse_cross_validation exec_timestamp(::pm_vision_interfaces::msg::VisionResponse::_exec_timestamp_type arg)
  {
    msg_.exec_timestamp = std::move(arg);
    return Init_VisionResponse_cross_validation(msg_);
  }

private:
  ::pm_vision_interfaces::msg::VisionResponse msg_;
};

class Init_VisionResponse_process_uid
{
public:
  explicit Init_VisionResponse_process_uid(::pm_vision_interfaces::msg::VisionResponse & msg)
  : msg_(msg)
  {}
  Init_VisionResponse_exec_timestamp process_uid(::pm_vision_interfaces::msg::VisionResponse::_process_uid_type arg)
  {
    msg_.process_uid = std::move(arg);
    return Init_VisionResponse_exec_timestamp(msg_);
  }

private:
  ::pm_vision_interfaces::msg::VisionResponse msg_;
};

class Init_VisionResponse_process_name
{
public:
  explicit Init_VisionResponse_process_name(::pm_vision_interfaces::msg::VisionResponse & msg)
  : msg_(msg)
  {}
  Init_VisionResponse_process_uid process_name(::pm_vision_interfaces::msg::VisionResponse::_process_name_type arg)
  {
    msg_.process_name = std::move(arg);
    return Init_VisionResponse_process_uid(msg_);
  }

private:
  ::pm_vision_interfaces::msg::VisionResponse msg_;
};

class Init_VisionResponse_vision_ok
{
public:
  Init_VisionResponse_vision_ok()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_VisionResponse_process_name vision_ok(::pm_vision_interfaces::msg::VisionResponse::_vision_ok_type arg)
  {
    msg_.vision_ok = std::move(arg);
    return Init_VisionResponse_process_name(msg_);
  }

private:
  ::pm_vision_interfaces::msg::VisionResponse msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::pm_vision_interfaces::msg::VisionResponse>()
{
  return pm_vision_interfaces::msg::builder::Init_VisionResponse_vision_ok();
}

}  // namespace pm_vision_interfaces

#endif  // PM_VISION_INTERFACES__MSG__DETAIL__VISION_RESPONSE__BUILDER_HPP_

// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from pm_vision_interfaces:msg/VisionPoint.idl
// generated code does not contain a copyright notice

#ifndef PM_VISION_INTERFACES__MSG__DETAIL__VISION_POINT__BUILDER_HPP_
#define PM_VISION_INTERFACES__MSG__DETAIL__VISION_POINT__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "pm_vision_interfaces/msg/detail/vision_point__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace pm_vision_interfaces
{

namespace msg
{

namespace builder
{

class Init_VisionPoint_axis_suffix_2
{
public:
  explicit Init_VisionPoint_axis_suffix_2(::pm_vision_interfaces::msg::VisionPoint & msg)
  : msg_(msg)
  {}
  ::pm_vision_interfaces::msg::VisionPoint axis_suffix_2(::pm_vision_interfaces::msg::VisionPoint::_axis_suffix_2_type arg)
  {
    msg_.axis_suffix_2 = std::move(arg);
    return std::move(msg_);
  }

private:
  ::pm_vision_interfaces::msg::VisionPoint msg_;
};

class Init_VisionPoint_axis_suffix_1
{
public:
  explicit Init_VisionPoint_axis_suffix_1(::pm_vision_interfaces::msg::VisionPoint & msg)
  : msg_(msg)
  {}
  Init_VisionPoint_axis_suffix_2 axis_suffix_1(::pm_vision_interfaces::msg::VisionPoint::_axis_suffix_1_type arg)
  {
    msg_.axis_suffix_1 = std::move(arg);
    return Init_VisionPoint_axis_suffix_2(msg_);
  }

private:
  ::pm_vision_interfaces::msg::VisionPoint msg_;
};

class Init_VisionPoint_axis_value_2
{
public:
  explicit Init_VisionPoint_axis_value_2(::pm_vision_interfaces::msg::VisionPoint & msg)
  : msg_(msg)
  {}
  Init_VisionPoint_axis_suffix_1 axis_value_2(::pm_vision_interfaces::msg::VisionPoint::_axis_value_2_type arg)
  {
    msg_.axis_value_2 = std::move(arg);
    return Init_VisionPoint_axis_suffix_1(msg_);
  }

private:
  ::pm_vision_interfaces::msg::VisionPoint msg_;
};

class Init_VisionPoint_axis_value_1
{
public:
  Init_VisionPoint_axis_value_1()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_VisionPoint_axis_value_2 axis_value_1(::pm_vision_interfaces::msg::VisionPoint::_axis_value_1_type arg)
  {
    msg_.axis_value_1 = std::move(arg);
    return Init_VisionPoint_axis_value_2(msg_);
  }

private:
  ::pm_vision_interfaces::msg::VisionPoint msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::pm_vision_interfaces::msg::VisionPoint>()
{
  return pm_vision_interfaces::msg::builder::Init_VisionPoint_axis_value_1();
}

}  // namespace pm_vision_interfaces

#endif  // PM_VISION_INTERFACES__MSG__DETAIL__VISION_POINT__BUILDER_HPP_

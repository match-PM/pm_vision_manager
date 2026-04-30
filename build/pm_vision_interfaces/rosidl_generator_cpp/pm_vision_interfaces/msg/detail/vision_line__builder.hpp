// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from pm_vision_interfaces:msg/VisionLine.idl
// generated code does not contain a copyright notice

#ifndef PM_VISION_INTERFACES__MSG__DETAIL__VISION_LINE__BUILDER_HPP_
#define PM_VISION_INTERFACES__MSG__DETAIL__VISION_LINE__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "pm_vision_interfaces/msg/detail/vision_line__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace pm_vision_interfaces
{

namespace msg
{

namespace builder
{

class Init_VisionLine_length
{
public:
  explicit Init_VisionLine_length(::pm_vision_interfaces::msg::VisionLine & msg)
  : msg_(msg)
  {}
  ::pm_vision_interfaces::msg::VisionLine length(::pm_vision_interfaces::msg::VisionLine::_length_type arg)
  {
    msg_.length = std::move(arg);
    return std::move(msg_);
  }

private:
  ::pm_vision_interfaces::msg::VisionLine msg_;
};

class Init_VisionLine_angle
{
public:
  explicit Init_VisionLine_angle(::pm_vision_interfaces::msg::VisionLine & msg)
  : msg_(msg)
  {}
  Init_VisionLine_length angle(::pm_vision_interfaces::msg::VisionLine::_angle_type arg)
  {
    msg_.angle = std::move(arg);
    return Init_VisionLine_length(msg_);
  }

private:
  ::pm_vision_interfaces::msg::VisionLine msg_;
};

class Init_VisionLine_point_mid
{
public:
  explicit Init_VisionLine_point_mid(::pm_vision_interfaces::msg::VisionLine & msg)
  : msg_(msg)
  {}
  Init_VisionLine_angle point_mid(::pm_vision_interfaces::msg::VisionLine::_point_mid_type arg)
  {
    msg_.point_mid = std::move(arg);
    return Init_VisionLine_angle(msg_);
  }

private:
  ::pm_vision_interfaces::msg::VisionLine msg_;
};

class Init_VisionLine_point_2
{
public:
  explicit Init_VisionLine_point_2(::pm_vision_interfaces::msg::VisionLine & msg)
  : msg_(msg)
  {}
  Init_VisionLine_point_mid point_2(::pm_vision_interfaces::msg::VisionLine::_point_2_type arg)
  {
    msg_.point_2 = std::move(arg);
    return Init_VisionLine_point_mid(msg_);
  }

private:
  ::pm_vision_interfaces::msg::VisionLine msg_;
};

class Init_VisionLine_point_1
{
public:
  Init_VisionLine_point_1()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_VisionLine_point_2 point_1(::pm_vision_interfaces::msg::VisionLine::_point_1_type arg)
  {
    msg_.point_1 = std::move(arg);
    return Init_VisionLine_point_2(msg_);
  }

private:
  ::pm_vision_interfaces::msg::VisionLine msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::pm_vision_interfaces::msg::VisionLine>()
{
  return pm_vision_interfaces::msg::builder::Init_VisionLine_point_1();
}

}  // namespace pm_vision_interfaces

#endif  // PM_VISION_INTERFACES__MSG__DETAIL__VISION_LINE__BUILDER_HPP_

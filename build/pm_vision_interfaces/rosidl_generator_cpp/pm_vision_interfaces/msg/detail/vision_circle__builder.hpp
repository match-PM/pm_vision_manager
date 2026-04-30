// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from pm_vision_interfaces:msg/VisionCircle.idl
// generated code does not contain a copyright notice

#ifndef PM_VISION_INTERFACES__MSG__DETAIL__VISION_CIRCLE__BUILDER_HPP_
#define PM_VISION_INTERFACES__MSG__DETAIL__VISION_CIRCLE__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "pm_vision_interfaces/msg/detail/vision_circle__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace pm_vision_interfaces
{

namespace msg
{

namespace builder
{

class Init_VisionCircle_radius
{
public:
  explicit Init_VisionCircle_radius(::pm_vision_interfaces::msg::VisionCircle & msg)
  : msg_(msg)
  {}
  ::pm_vision_interfaces::msg::VisionCircle radius(::pm_vision_interfaces::msg::VisionCircle::_radius_type arg)
  {
    msg_.radius = std::move(arg);
    return std::move(msg_);
  }

private:
  ::pm_vision_interfaces::msg::VisionCircle msg_;
};

class Init_VisionCircle_center_point
{
public:
  Init_VisionCircle_center_point()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_VisionCircle_radius center_point(::pm_vision_interfaces::msg::VisionCircle::_center_point_type arg)
  {
    msg_.center_point = std::move(arg);
    return Init_VisionCircle_radius(msg_);
  }

private:
  ::pm_vision_interfaces::msg::VisionCircle msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::pm_vision_interfaces::msg::VisionCircle>()
{
  return pm_vision_interfaces::msg::builder::Init_VisionCircle_center_point();
}

}  // namespace pm_vision_interfaces

#endif  // PM_VISION_INTERFACES__MSG__DETAIL__VISION_CIRCLE__BUILDER_HPP_

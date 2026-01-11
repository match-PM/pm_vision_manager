// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from pm_vision_interfaces:msg/VisionResults.idl
// generated code does not contain a copyright notice

#ifndef PM_VISION_INTERFACES__MSG__DETAIL__VISION_RESULTS__BUILDER_HPP_
#define PM_VISION_INTERFACES__MSG__DETAIL__VISION_RESULTS__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "pm_vision_interfaces/msg/detail/vision_results__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace pm_vision_interfaces
{

namespace msg
{

namespace builder
{

class Init_VisionResults_image_sharpness
{
public:
  explicit Init_VisionResults_image_sharpness(::pm_vision_interfaces::msg::VisionResults & msg)
  : msg_(msg)
  {}
  ::pm_vision_interfaces::msg::VisionResults image_sharpness(::pm_vision_interfaces::msg::VisionResults::_image_sharpness_type arg)
  {
    msg_.image_sharpness = std::move(arg);
    return std::move(msg_);
  }

private:
  ::pm_vision_interfaces::msg::VisionResults msg_;
};

class Init_VisionResults_circles
{
public:
  explicit Init_VisionResults_circles(::pm_vision_interfaces::msg::VisionResults & msg)
  : msg_(msg)
  {}
  Init_VisionResults_image_sharpness circles(::pm_vision_interfaces::msg::VisionResults::_circles_type arg)
  {
    msg_.circles = std::move(arg);
    return Init_VisionResults_image_sharpness(msg_);
  }

private:
  ::pm_vision_interfaces::msg::VisionResults msg_;
};

class Init_VisionResults_areas
{
public:
  explicit Init_VisionResults_areas(::pm_vision_interfaces::msg::VisionResults & msg)
  : msg_(msg)
  {}
  Init_VisionResults_circles areas(::pm_vision_interfaces::msg::VisionResults::_areas_type arg)
  {
    msg_.areas = std::move(arg);
    return Init_VisionResults_circles(msg_);
  }

private:
  ::pm_vision_interfaces::msg::VisionResults msg_;
};

class Init_VisionResults_lines
{
public:
  explicit Init_VisionResults_lines(::pm_vision_interfaces::msg::VisionResults & msg)
  : msg_(msg)
  {}
  Init_VisionResults_areas lines(::pm_vision_interfaces::msg::VisionResults::_lines_type arg)
  {
    msg_.lines = std::move(arg);
    return Init_VisionResults_areas(msg_);
  }

private:
  ::pm_vision_interfaces::msg::VisionResults msg_;
};

class Init_VisionResults_points
{
public:
  Init_VisionResults_points()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_VisionResults_lines points(::pm_vision_interfaces::msg::VisionResults::_points_type arg)
  {
    msg_.points = std::move(arg);
    return Init_VisionResults_lines(msg_);
  }

private:
  ::pm_vision_interfaces::msg::VisionResults msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::pm_vision_interfaces::msg::VisionResults>()
{
  return pm_vision_interfaces::msg::builder::Init_VisionResults_points();
}

}  // namespace pm_vision_interfaces

#endif  // PM_VISION_INTERFACES__MSG__DETAIL__VISION_RESULTS__BUILDER_HPP_

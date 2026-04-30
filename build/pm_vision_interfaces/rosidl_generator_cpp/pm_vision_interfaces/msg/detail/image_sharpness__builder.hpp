// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from pm_vision_interfaces:msg/ImageSharpness.idl
// generated code does not contain a copyright notice

#ifndef PM_VISION_INTERFACES__MSG__DETAIL__IMAGE_SHARPNESS__BUILDER_HPP_
#define PM_VISION_INTERFACES__MSG__DETAIL__IMAGE_SHARPNESS__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "pm_vision_interfaces/msg/detail/image_sharpness__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace pm_vision_interfaces
{

namespace msg
{

namespace builder
{

class Init_ImageSharpness_sharpness_value
{
public:
  Init_ImageSharpness_sharpness_value()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::pm_vision_interfaces::msg::ImageSharpness sharpness_value(::pm_vision_interfaces::msg::ImageSharpness::_sharpness_value_type arg)
  {
    msg_.sharpness_value = std::move(arg);
    return std::move(msg_);
  }

private:
  ::pm_vision_interfaces::msg::ImageSharpness msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::pm_vision_interfaces::msg::ImageSharpness>()
{
  return pm_vision_interfaces::msg::builder::Init_ImageSharpness_sharpness_value();
}

}  // namespace pm_vision_interfaces

#endif  // PM_VISION_INTERFACES__MSG__DETAIL__IMAGE_SHARPNESS__BUILDER_HPP_

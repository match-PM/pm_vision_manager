// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from pm_vision_interfaces:msg/CrossValidation.idl
// generated code does not contain a copyright notice

#ifndef PM_VISION_INTERFACES__MSG__DETAIL__CROSS_VALIDATION__BUILDER_HPP_
#define PM_VISION_INTERFACES__MSG__DETAIL__CROSS_VALIDATION__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "pm_vision_interfaces/msg/detail/cross_validation__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace pm_vision_interfaces
{

namespace msg
{

namespace builder
{

class Init_CrossValidation_counter_error
{
public:
  explicit Init_CrossValidation_counter_error(::pm_vision_interfaces::msg::CrossValidation & msg)
  : msg_(msg)
  {}
  ::pm_vision_interfaces::msg::CrossValidation counter_error(::pm_vision_interfaces::msg::CrossValidation::_counter_error_type arg)
  {
    msg_.counter_error = std::move(arg);
    return std::move(msg_);
  }

private:
  ::pm_vision_interfaces::msg::CrossValidation msg_;
};

class Init_CrossValidation_numb_images
{
public:
  explicit Init_CrossValidation_numb_images(::pm_vision_interfaces::msg::CrossValidation & msg)
  : msg_(msg)
  {}
  Init_CrossValidation_counter_error numb_images(::pm_vision_interfaces::msg::CrossValidation::_numb_images_type arg)
  {
    msg_.numb_images = std::move(arg);
    return Init_CrossValidation_counter_error(msg_);
  }

private:
  ::pm_vision_interfaces::msg::CrossValidation msg_;
};

class Init_CrossValidation_failed_images
{
public:
  explicit Init_CrossValidation_failed_images(::pm_vision_interfaces::msg::CrossValidation & msg)
  : msg_(msg)
  {}
  Init_CrossValidation_numb_images failed_images(::pm_vision_interfaces::msg::CrossValidation::_failed_images_type arg)
  {
    msg_.failed_images = std::move(arg);
    return Init_CrossValidation_numb_images(msg_);
  }

private:
  ::pm_vision_interfaces::msg::CrossValidation msg_;
};

class Init_CrossValidation_vision_ok
{
public:
  explicit Init_CrossValidation_vision_ok(::pm_vision_interfaces::msg::CrossValidation & msg)
  : msg_(msg)
  {}
  Init_CrossValidation_failed_images vision_ok(::pm_vision_interfaces::msg::CrossValidation::_vision_ok_type arg)
  {
    msg_.vision_ok = std::move(arg);
    return Init_CrossValidation_failed_images(msg_);
  }

private:
  ::pm_vision_interfaces::msg::CrossValidation msg_;
};

class Init_CrossValidation_image_source_name
{
public:
  Init_CrossValidation_image_source_name()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_CrossValidation_vision_ok image_source_name(::pm_vision_interfaces::msg::CrossValidation::_image_source_name_type arg)
  {
    msg_.image_source_name = std::move(arg);
    return Init_CrossValidation_vision_ok(msg_);
  }

private:
  ::pm_vision_interfaces::msg::CrossValidation msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::pm_vision_interfaces::msg::CrossValidation>()
{
  return pm_vision_interfaces::msg::builder::Init_CrossValidation_image_source_name();
}

}  // namespace pm_vision_interfaces

#endif  // PM_VISION_INTERFACES__MSG__DETAIL__CROSS_VALIDATION__BUILDER_HPP_

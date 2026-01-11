// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from pm_vision_interfaces:msg/ImageSharpness.idl
// generated code does not contain a copyright notice

#ifndef PM_VISION_INTERFACES__MSG__DETAIL__IMAGE_SHARPNESS__STRUCT_HPP_
#define PM_VISION_INTERFACES__MSG__DETAIL__IMAGE_SHARPNESS__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__pm_vision_interfaces__msg__ImageSharpness __attribute__((deprecated))
#else
# define DEPRECATED__pm_vision_interfaces__msg__ImageSharpness __declspec(deprecated)
#endif

namespace pm_vision_interfaces
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct ImageSharpness_
{
  using Type = ImageSharpness_<ContainerAllocator>;

  explicit ImageSharpness_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->sharpness_value = 0.0;
    }
  }

  explicit ImageSharpness_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->sharpness_value = 0.0;
    }
  }

  // field types and members
  using _sharpness_value_type =
    double;
  _sharpness_value_type sharpness_value;

  // setters for named parameter idiom
  Type & set__sharpness_value(
    const double & _arg)
  {
    this->sharpness_value = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    pm_vision_interfaces::msg::ImageSharpness_<ContainerAllocator> *;
  using ConstRawPtr =
    const pm_vision_interfaces::msg::ImageSharpness_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<pm_vision_interfaces::msg::ImageSharpness_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<pm_vision_interfaces::msg::ImageSharpness_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      pm_vision_interfaces::msg::ImageSharpness_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<pm_vision_interfaces::msg::ImageSharpness_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      pm_vision_interfaces::msg::ImageSharpness_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<pm_vision_interfaces::msg::ImageSharpness_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<pm_vision_interfaces::msg::ImageSharpness_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<pm_vision_interfaces::msg::ImageSharpness_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__pm_vision_interfaces__msg__ImageSharpness
    std::shared_ptr<pm_vision_interfaces::msg::ImageSharpness_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__pm_vision_interfaces__msg__ImageSharpness
    std::shared_ptr<pm_vision_interfaces::msg::ImageSharpness_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const ImageSharpness_ & other) const
  {
    if (this->sharpness_value != other.sharpness_value) {
      return false;
    }
    return true;
  }
  bool operator!=(const ImageSharpness_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct ImageSharpness_

// alias to use template instance with default allocator
using ImageSharpness =
  pm_vision_interfaces::msg::ImageSharpness_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace pm_vision_interfaces

#endif  // PM_VISION_INTERFACES__MSG__DETAIL__IMAGE_SHARPNESS__STRUCT_HPP_

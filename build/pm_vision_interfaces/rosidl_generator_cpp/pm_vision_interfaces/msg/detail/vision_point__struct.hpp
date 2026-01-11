// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from pm_vision_interfaces:msg/VisionPoint.idl
// generated code does not contain a copyright notice

#ifndef PM_VISION_INTERFACES__MSG__DETAIL__VISION_POINT__STRUCT_HPP_
#define PM_VISION_INTERFACES__MSG__DETAIL__VISION_POINT__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__pm_vision_interfaces__msg__VisionPoint __attribute__((deprecated))
#else
# define DEPRECATED__pm_vision_interfaces__msg__VisionPoint __declspec(deprecated)
#endif

namespace pm_vision_interfaces
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct VisionPoint_
{
  using Type = VisionPoint_<ContainerAllocator>;

  explicit VisionPoint_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->axis_value_1 = 0.0f;
      this->axis_value_2 = 0.0f;
      this->axis_suffix_1 = "";
      this->axis_suffix_2 = "";
    }
  }

  explicit VisionPoint_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : axis_suffix_1(_alloc),
    axis_suffix_2(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->axis_value_1 = 0.0f;
      this->axis_value_2 = 0.0f;
      this->axis_suffix_1 = "";
      this->axis_suffix_2 = "";
    }
  }

  // field types and members
  using _axis_value_1_type =
    float;
  _axis_value_1_type axis_value_1;
  using _axis_value_2_type =
    float;
  _axis_value_2_type axis_value_2;
  using _axis_suffix_1_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _axis_suffix_1_type axis_suffix_1;
  using _axis_suffix_2_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _axis_suffix_2_type axis_suffix_2;

  // setters for named parameter idiom
  Type & set__axis_value_1(
    const float & _arg)
  {
    this->axis_value_1 = _arg;
    return *this;
  }
  Type & set__axis_value_2(
    const float & _arg)
  {
    this->axis_value_2 = _arg;
    return *this;
  }
  Type & set__axis_suffix_1(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->axis_suffix_1 = _arg;
    return *this;
  }
  Type & set__axis_suffix_2(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->axis_suffix_2 = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    pm_vision_interfaces::msg::VisionPoint_<ContainerAllocator> *;
  using ConstRawPtr =
    const pm_vision_interfaces::msg::VisionPoint_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<pm_vision_interfaces::msg::VisionPoint_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<pm_vision_interfaces::msg::VisionPoint_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      pm_vision_interfaces::msg::VisionPoint_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<pm_vision_interfaces::msg::VisionPoint_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      pm_vision_interfaces::msg::VisionPoint_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<pm_vision_interfaces::msg::VisionPoint_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<pm_vision_interfaces::msg::VisionPoint_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<pm_vision_interfaces::msg::VisionPoint_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__pm_vision_interfaces__msg__VisionPoint
    std::shared_ptr<pm_vision_interfaces::msg::VisionPoint_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__pm_vision_interfaces__msg__VisionPoint
    std::shared_ptr<pm_vision_interfaces::msg::VisionPoint_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const VisionPoint_ & other) const
  {
    if (this->axis_value_1 != other.axis_value_1) {
      return false;
    }
    if (this->axis_value_2 != other.axis_value_2) {
      return false;
    }
    if (this->axis_suffix_1 != other.axis_suffix_1) {
      return false;
    }
    if (this->axis_suffix_2 != other.axis_suffix_2) {
      return false;
    }
    return true;
  }
  bool operator!=(const VisionPoint_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct VisionPoint_

// alias to use template instance with default allocator
using VisionPoint =
  pm_vision_interfaces::msg::VisionPoint_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace pm_vision_interfaces

#endif  // PM_VISION_INTERFACES__MSG__DETAIL__VISION_POINT__STRUCT_HPP_

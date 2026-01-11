// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from pm_vision_interfaces:msg/VisionLine.idl
// generated code does not contain a copyright notice

#ifndef PM_VISION_INTERFACES__MSG__DETAIL__VISION_LINE__STRUCT_HPP_
#define PM_VISION_INTERFACES__MSG__DETAIL__VISION_LINE__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


// Include directives for member types
// Member 'point_1'
// Member 'point_2'
// Member 'point_mid'
#include "pm_vision_interfaces/msg/detail/vision_point__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__pm_vision_interfaces__msg__VisionLine __attribute__((deprecated))
#else
# define DEPRECATED__pm_vision_interfaces__msg__VisionLine __declspec(deprecated)
#endif

namespace pm_vision_interfaces
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct VisionLine_
{
  using Type = VisionLine_<ContainerAllocator>;

  explicit VisionLine_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : point_1(_init),
    point_2(_init),
    point_mid(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->angle = 0.0f;
      this->length = 0.0f;
    }
  }

  explicit VisionLine_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : point_1(_alloc, _init),
    point_2(_alloc, _init),
    point_mid(_alloc, _init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->angle = 0.0f;
      this->length = 0.0f;
    }
  }

  // field types and members
  using _point_1_type =
    pm_vision_interfaces::msg::VisionPoint_<ContainerAllocator>;
  _point_1_type point_1;
  using _point_2_type =
    pm_vision_interfaces::msg::VisionPoint_<ContainerAllocator>;
  _point_2_type point_2;
  using _point_mid_type =
    pm_vision_interfaces::msg::VisionPoint_<ContainerAllocator>;
  _point_mid_type point_mid;
  using _angle_type =
    float;
  _angle_type angle;
  using _length_type =
    float;
  _length_type length;

  // setters for named parameter idiom
  Type & set__point_1(
    const pm_vision_interfaces::msg::VisionPoint_<ContainerAllocator> & _arg)
  {
    this->point_1 = _arg;
    return *this;
  }
  Type & set__point_2(
    const pm_vision_interfaces::msg::VisionPoint_<ContainerAllocator> & _arg)
  {
    this->point_2 = _arg;
    return *this;
  }
  Type & set__point_mid(
    const pm_vision_interfaces::msg::VisionPoint_<ContainerAllocator> & _arg)
  {
    this->point_mid = _arg;
    return *this;
  }
  Type & set__angle(
    const float & _arg)
  {
    this->angle = _arg;
    return *this;
  }
  Type & set__length(
    const float & _arg)
  {
    this->length = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    pm_vision_interfaces::msg::VisionLine_<ContainerAllocator> *;
  using ConstRawPtr =
    const pm_vision_interfaces::msg::VisionLine_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<pm_vision_interfaces::msg::VisionLine_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<pm_vision_interfaces::msg::VisionLine_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      pm_vision_interfaces::msg::VisionLine_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<pm_vision_interfaces::msg::VisionLine_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      pm_vision_interfaces::msg::VisionLine_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<pm_vision_interfaces::msg::VisionLine_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<pm_vision_interfaces::msg::VisionLine_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<pm_vision_interfaces::msg::VisionLine_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__pm_vision_interfaces__msg__VisionLine
    std::shared_ptr<pm_vision_interfaces::msg::VisionLine_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__pm_vision_interfaces__msg__VisionLine
    std::shared_ptr<pm_vision_interfaces::msg::VisionLine_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const VisionLine_ & other) const
  {
    if (this->point_1 != other.point_1) {
      return false;
    }
    if (this->point_2 != other.point_2) {
      return false;
    }
    if (this->point_mid != other.point_mid) {
      return false;
    }
    if (this->angle != other.angle) {
      return false;
    }
    if (this->length != other.length) {
      return false;
    }
    return true;
  }
  bool operator!=(const VisionLine_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct VisionLine_

// alias to use template instance with default allocator
using VisionLine =
  pm_vision_interfaces::msg::VisionLine_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace pm_vision_interfaces

#endif  // PM_VISION_INTERFACES__MSG__DETAIL__VISION_LINE__STRUCT_HPP_

// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from pm_vision_interfaces:msg/VisionCircle.idl
// generated code does not contain a copyright notice

#ifndef PM_VISION_INTERFACES__MSG__DETAIL__VISION_CIRCLE__STRUCT_HPP_
#define PM_VISION_INTERFACES__MSG__DETAIL__VISION_CIRCLE__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


// Include directives for member types
// Member 'center_point'
#include "pm_vision_interfaces/msg/detail/vision_point__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__pm_vision_interfaces__msg__VisionCircle __attribute__((deprecated))
#else
# define DEPRECATED__pm_vision_interfaces__msg__VisionCircle __declspec(deprecated)
#endif

namespace pm_vision_interfaces
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct VisionCircle_
{
  using Type = VisionCircle_<ContainerAllocator>;

  explicit VisionCircle_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : center_point(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->radius = 0.0;
    }
  }

  explicit VisionCircle_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : center_point(_alloc, _init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->radius = 0.0;
    }
  }

  // field types and members
  using _center_point_type =
    pm_vision_interfaces::msg::VisionPoint_<ContainerAllocator>;
  _center_point_type center_point;
  using _radius_type =
    double;
  _radius_type radius;

  // setters for named parameter idiom
  Type & set__center_point(
    const pm_vision_interfaces::msg::VisionPoint_<ContainerAllocator> & _arg)
  {
    this->center_point = _arg;
    return *this;
  }
  Type & set__radius(
    const double & _arg)
  {
    this->radius = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    pm_vision_interfaces::msg::VisionCircle_<ContainerAllocator> *;
  using ConstRawPtr =
    const pm_vision_interfaces::msg::VisionCircle_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<pm_vision_interfaces::msg::VisionCircle_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<pm_vision_interfaces::msg::VisionCircle_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      pm_vision_interfaces::msg::VisionCircle_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<pm_vision_interfaces::msg::VisionCircle_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      pm_vision_interfaces::msg::VisionCircle_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<pm_vision_interfaces::msg::VisionCircle_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<pm_vision_interfaces::msg::VisionCircle_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<pm_vision_interfaces::msg::VisionCircle_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__pm_vision_interfaces__msg__VisionCircle
    std::shared_ptr<pm_vision_interfaces::msg::VisionCircle_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__pm_vision_interfaces__msg__VisionCircle
    std::shared_ptr<pm_vision_interfaces::msg::VisionCircle_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const VisionCircle_ & other) const
  {
    if (this->center_point != other.center_point) {
      return false;
    }
    if (this->radius != other.radius) {
      return false;
    }
    return true;
  }
  bool operator!=(const VisionCircle_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct VisionCircle_

// alias to use template instance with default allocator
using VisionCircle =
  pm_vision_interfaces::msg::VisionCircle_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace pm_vision_interfaces

#endif  // PM_VISION_INTERFACES__MSG__DETAIL__VISION_CIRCLE__STRUCT_HPP_

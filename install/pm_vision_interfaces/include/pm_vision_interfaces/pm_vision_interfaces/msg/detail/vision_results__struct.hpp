// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from pm_vision_interfaces:msg/VisionResults.idl
// generated code does not contain a copyright notice

#ifndef PM_VISION_INTERFACES__MSG__DETAIL__VISION_RESULTS__STRUCT_HPP_
#define PM_VISION_INTERFACES__MSG__DETAIL__VISION_RESULTS__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


// Include directives for member types
// Member 'points'
#include "pm_vision_interfaces/msg/detail/vision_point__struct.hpp"
// Member 'lines'
#include "pm_vision_interfaces/msg/detail/vision_line__struct.hpp"
// Member 'areas'
#include "pm_vision_interfaces/msg/detail/vision_area__struct.hpp"
// Member 'circles'
#include "pm_vision_interfaces/msg/detail/vision_circle__struct.hpp"
// Member 'image_sharpness'
#include "pm_vision_interfaces/msg/detail/image_sharpness__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__pm_vision_interfaces__msg__VisionResults __attribute__((deprecated))
#else
# define DEPRECATED__pm_vision_interfaces__msg__VisionResults __declspec(deprecated)
#endif

namespace pm_vision_interfaces
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct VisionResults_
{
  using Type = VisionResults_<ContainerAllocator>;

  explicit VisionResults_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : image_sharpness(_init)
  {
    (void)_init;
  }

  explicit VisionResults_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : image_sharpness(_alloc, _init)
  {
    (void)_init;
  }

  // field types and members
  using _points_type =
    std::vector<pm_vision_interfaces::msg::VisionPoint_<ContainerAllocator>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<pm_vision_interfaces::msg::VisionPoint_<ContainerAllocator>>>;
  _points_type points;
  using _lines_type =
    std::vector<pm_vision_interfaces::msg::VisionLine_<ContainerAllocator>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<pm_vision_interfaces::msg::VisionLine_<ContainerAllocator>>>;
  _lines_type lines;
  using _areas_type =
    std::vector<pm_vision_interfaces::msg::VisionArea_<ContainerAllocator>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<pm_vision_interfaces::msg::VisionArea_<ContainerAllocator>>>;
  _areas_type areas;
  using _circles_type =
    std::vector<pm_vision_interfaces::msg::VisionCircle_<ContainerAllocator>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<pm_vision_interfaces::msg::VisionCircle_<ContainerAllocator>>>;
  _circles_type circles;
  using _image_sharpness_type =
    pm_vision_interfaces::msg::ImageSharpness_<ContainerAllocator>;
  _image_sharpness_type image_sharpness;

  // setters for named parameter idiom
  Type & set__points(
    const std::vector<pm_vision_interfaces::msg::VisionPoint_<ContainerAllocator>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<pm_vision_interfaces::msg::VisionPoint_<ContainerAllocator>>> & _arg)
  {
    this->points = _arg;
    return *this;
  }
  Type & set__lines(
    const std::vector<pm_vision_interfaces::msg::VisionLine_<ContainerAllocator>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<pm_vision_interfaces::msg::VisionLine_<ContainerAllocator>>> & _arg)
  {
    this->lines = _arg;
    return *this;
  }
  Type & set__areas(
    const std::vector<pm_vision_interfaces::msg::VisionArea_<ContainerAllocator>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<pm_vision_interfaces::msg::VisionArea_<ContainerAllocator>>> & _arg)
  {
    this->areas = _arg;
    return *this;
  }
  Type & set__circles(
    const std::vector<pm_vision_interfaces::msg::VisionCircle_<ContainerAllocator>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<pm_vision_interfaces::msg::VisionCircle_<ContainerAllocator>>> & _arg)
  {
    this->circles = _arg;
    return *this;
  }
  Type & set__image_sharpness(
    const pm_vision_interfaces::msg::ImageSharpness_<ContainerAllocator> & _arg)
  {
    this->image_sharpness = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    pm_vision_interfaces::msg::VisionResults_<ContainerAllocator> *;
  using ConstRawPtr =
    const pm_vision_interfaces::msg::VisionResults_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<pm_vision_interfaces::msg::VisionResults_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<pm_vision_interfaces::msg::VisionResults_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      pm_vision_interfaces::msg::VisionResults_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<pm_vision_interfaces::msg::VisionResults_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      pm_vision_interfaces::msg::VisionResults_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<pm_vision_interfaces::msg::VisionResults_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<pm_vision_interfaces::msg::VisionResults_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<pm_vision_interfaces::msg::VisionResults_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__pm_vision_interfaces__msg__VisionResults
    std::shared_ptr<pm_vision_interfaces::msg::VisionResults_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__pm_vision_interfaces__msg__VisionResults
    std::shared_ptr<pm_vision_interfaces::msg::VisionResults_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const VisionResults_ & other) const
  {
    if (this->points != other.points) {
      return false;
    }
    if (this->lines != other.lines) {
      return false;
    }
    if (this->areas != other.areas) {
      return false;
    }
    if (this->circles != other.circles) {
      return false;
    }
    if (this->image_sharpness != other.image_sharpness) {
      return false;
    }
    return true;
  }
  bool operator!=(const VisionResults_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct VisionResults_

// alias to use template instance with default allocator
using VisionResults =
  pm_vision_interfaces::msg::VisionResults_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace pm_vision_interfaces

#endif  // PM_VISION_INTERFACES__MSG__DETAIL__VISION_RESULTS__STRUCT_HPP_

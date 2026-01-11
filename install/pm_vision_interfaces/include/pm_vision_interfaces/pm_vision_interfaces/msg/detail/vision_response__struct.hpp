// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from pm_vision_interfaces:msg/VisionResponse.idl
// generated code does not contain a copyright notice

#ifndef PM_VISION_INTERFACES__MSG__DETAIL__VISION_RESPONSE__STRUCT_HPP_
#define PM_VISION_INTERFACES__MSG__DETAIL__VISION_RESPONSE__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


// Include directives for member types
// Member 'cross_validation'
#include "pm_vision_interfaces/msg/detail/cross_validation__struct.hpp"
// Member 'results'
#include "pm_vision_interfaces/msg/detail/vision_results__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__pm_vision_interfaces__msg__VisionResponse __attribute__((deprecated))
#else
# define DEPRECATED__pm_vision_interfaces__msg__VisionResponse __declspec(deprecated)
#endif

namespace pm_vision_interfaces
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct VisionResponse_
{
  using Type = VisionResponse_<ContainerAllocator>;

  explicit VisionResponse_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : cross_validation(_init),
    results(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->vision_ok = false;
      this->process_name = "";
      this->process_uid = "";
      this->exec_timestamp = "";
    }
  }

  explicit VisionResponse_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : process_name(_alloc),
    process_uid(_alloc),
    exec_timestamp(_alloc),
    cross_validation(_alloc, _init),
    results(_alloc, _init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->vision_ok = false;
      this->process_name = "";
      this->process_uid = "";
      this->exec_timestamp = "";
    }
  }

  // field types and members
  using _vision_ok_type =
    bool;
  _vision_ok_type vision_ok;
  using _process_name_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _process_name_type process_name;
  using _process_uid_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _process_uid_type process_uid;
  using _exec_timestamp_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _exec_timestamp_type exec_timestamp;
  using _cross_validation_type =
    pm_vision_interfaces::msg::CrossValidation_<ContainerAllocator>;
  _cross_validation_type cross_validation;
  using _results_type =
    pm_vision_interfaces::msg::VisionResults_<ContainerAllocator>;
  _results_type results;

  // setters for named parameter idiom
  Type & set__vision_ok(
    const bool & _arg)
  {
    this->vision_ok = _arg;
    return *this;
  }
  Type & set__process_name(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->process_name = _arg;
    return *this;
  }
  Type & set__process_uid(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->process_uid = _arg;
    return *this;
  }
  Type & set__exec_timestamp(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->exec_timestamp = _arg;
    return *this;
  }
  Type & set__cross_validation(
    const pm_vision_interfaces::msg::CrossValidation_<ContainerAllocator> & _arg)
  {
    this->cross_validation = _arg;
    return *this;
  }
  Type & set__results(
    const pm_vision_interfaces::msg::VisionResults_<ContainerAllocator> & _arg)
  {
    this->results = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    pm_vision_interfaces::msg::VisionResponse_<ContainerAllocator> *;
  using ConstRawPtr =
    const pm_vision_interfaces::msg::VisionResponse_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<pm_vision_interfaces::msg::VisionResponse_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<pm_vision_interfaces::msg::VisionResponse_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      pm_vision_interfaces::msg::VisionResponse_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<pm_vision_interfaces::msg::VisionResponse_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      pm_vision_interfaces::msg::VisionResponse_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<pm_vision_interfaces::msg::VisionResponse_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<pm_vision_interfaces::msg::VisionResponse_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<pm_vision_interfaces::msg::VisionResponse_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__pm_vision_interfaces__msg__VisionResponse
    std::shared_ptr<pm_vision_interfaces::msg::VisionResponse_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__pm_vision_interfaces__msg__VisionResponse
    std::shared_ptr<pm_vision_interfaces::msg::VisionResponse_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const VisionResponse_ & other) const
  {
    if (this->vision_ok != other.vision_ok) {
      return false;
    }
    if (this->process_name != other.process_name) {
      return false;
    }
    if (this->process_uid != other.process_uid) {
      return false;
    }
    if (this->exec_timestamp != other.exec_timestamp) {
      return false;
    }
    if (this->cross_validation != other.cross_validation) {
      return false;
    }
    if (this->results != other.results) {
      return false;
    }
    return true;
  }
  bool operator!=(const VisionResponse_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct VisionResponse_

// alias to use template instance with default allocator
using VisionResponse =
  pm_vision_interfaces::msg::VisionResponse_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace pm_vision_interfaces

#endif  // PM_VISION_INTERFACES__MSG__DETAIL__VISION_RESPONSE__STRUCT_HPP_

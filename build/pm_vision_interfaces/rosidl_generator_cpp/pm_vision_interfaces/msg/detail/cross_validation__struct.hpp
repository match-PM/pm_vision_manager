// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from pm_vision_interfaces:msg/CrossValidation.idl
// generated code does not contain a copyright notice

#ifndef PM_VISION_INTERFACES__MSG__DETAIL__CROSS_VALIDATION__STRUCT_HPP_
#define PM_VISION_INTERFACES__MSG__DETAIL__CROSS_VALIDATION__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__pm_vision_interfaces__msg__CrossValidation __attribute__((deprecated))
#else
# define DEPRECATED__pm_vision_interfaces__msg__CrossValidation __declspec(deprecated)
#endif

namespace pm_vision_interfaces
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct CrossValidation_
{
  using Type = CrossValidation_<ContainerAllocator>;

  explicit CrossValidation_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->image_source_name = "";
      this->vision_ok = false;
      this->numb_images = 0l;
      this->counter_error = 0l;
    }
  }

  explicit CrossValidation_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : image_source_name(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->image_source_name = "";
      this->vision_ok = false;
      this->numb_images = 0l;
      this->counter_error = 0l;
    }
  }

  // field types and members
  using _image_source_name_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _image_source_name_type image_source_name;
  using _vision_ok_type =
    bool;
  _vision_ok_type vision_ok;
  using _failed_images_type =
    std::vector<std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>>>;
  _failed_images_type failed_images;
  using _numb_images_type =
    int32_t;
  _numb_images_type numb_images;
  using _counter_error_type =
    int32_t;
  _counter_error_type counter_error;

  // setters for named parameter idiom
  Type & set__image_source_name(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->image_source_name = _arg;
    return *this;
  }
  Type & set__vision_ok(
    const bool & _arg)
  {
    this->vision_ok = _arg;
    return *this;
  }
  Type & set__failed_images(
    const std::vector<std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>>> & _arg)
  {
    this->failed_images = _arg;
    return *this;
  }
  Type & set__numb_images(
    const int32_t & _arg)
  {
    this->numb_images = _arg;
    return *this;
  }
  Type & set__counter_error(
    const int32_t & _arg)
  {
    this->counter_error = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    pm_vision_interfaces::msg::CrossValidation_<ContainerAllocator> *;
  using ConstRawPtr =
    const pm_vision_interfaces::msg::CrossValidation_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<pm_vision_interfaces::msg::CrossValidation_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<pm_vision_interfaces::msg::CrossValidation_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      pm_vision_interfaces::msg::CrossValidation_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<pm_vision_interfaces::msg::CrossValidation_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      pm_vision_interfaces::msg::CrossValidation_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<pm_vision_interfaces::msg::CrossValidation_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<pm_vision_interfaces::msg::CrossValidation_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<pm_vision_interfaces::msg::CrossValidation_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__pm_vision_interfaces__msg__CrossValidation
    std::shared_ptr<pm_vision_interfaces::msg::CrossValidation_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__pm_vision_interfaces__msg__CrossValidation
    std::shared_ptr<pm_vision_interfaces::msg::CrossValidation_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const CrossValidation_ & other) const
  {
    if (this->image_source_name != other.image_source_name) {
      return false;
    }
    if (this->vision_ok != other.vision_ok) {
      return false;
    }
    if (this->failed_images != other.failed_images) {
      return false;
    }
    if (this->numb_images != other.numb_images) {
      return false;
    }
    if (this->counter_error != other.counter_error) {
      return false;
    }
    return true;
  }
  bool operator!=(const CrossValidation_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct CrossValidation_

// alias to use template instance with default allocator
using CrossValidation =
  pm_vision_interfaces::msg::CrossValidation_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace pm_vision_interfaces

#endif  // PM_VISION_INTERFACES__MSG__DETAIL__CROSS_VALIDATION__STRUCT_HPP_

// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from pm_vision_interfaces:srv/DemoSetExposure.idl
// generated code does not contain a copyright notice

#ifndef PM_VISION_INTERFACES__SRV__DETAIL__DEMO_SET_EXPOSURE__STRUCT_HPP_
#define PM_VISION_INTERFACES__SRV__DETAIL__DEMO_SET_EXPOSURE__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__pm_vision_interfaces__srv__DemoSetExposure_Request __attribute__((deprecated))
#else
# define DEPRECATED__pm_vision_interfaces__srv__DemoSetExposure_Request __declspec(deprecated)
#endif

namespace pm_vision_interfaces
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct DemoSetExposure_Request_
{
  using Type = DemoSetExposure_Request_<ContainerAllocator>;

  explicit DemoSetExposure_Request_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->target_value = 0.0;
    }
  }

  explicit DemoSetExposure_Request_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->target_value = 0.0;
    }
  }

  // field types and members
  using _target_value_type =
    double;
  _target_value_type target_value;

  // setters for named parameter idiom
  Type & set__target_value(
    const double & _arg)
  {
    this->target_value = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    pm_vision_interfaces::srv::DemoSetExposure_Request_<ContainerAllocator> *;
  using ConstRawPtr =
    const pm_vision_interfaces::srv::DemoSetExposure_Request_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<pm_vision_interfaces::srv::DemoSetExposure_Request_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<pm_vision_interfaces::srv::DemoSetExposure_Request_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      pm_vision_interfaces::srv::DemoSetExposure_Request_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<pm_vision_interfaces::srv::DemoSetExposure_Request_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      pm_vision_interfaces::srv::DemoSetExposure_Request_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<pm_vision_interfaces::srv::DemoSetExposure_Request_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<pm_vision_interfaces::srv::DemoSetExposure_Request_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<pm_vision_interfaces::srv::DemoSetExposure_Request_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__pm_vision_interfaces__srv__DemoSetExposure_Request
    std::shared_ptr<pm_vision_interfaces::srv::DemoSetExposure_Request_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__pm_vision_interfaces__srv__DemoSetExposure_Request
    std::shared_ptr<pm_vision_interfaces::srv::DemoSetExposure_Request_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const DemoSetExposure_Request_ & other) const
  {
    if (this->target_value != other.target_value) {
      return false;
    }
    return true;
  }
  bool operator!=(const DemoSetExposure_Request_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct DemoSetExposure_Request_

// alias to use template instance with default allocator
using DemoSetExposure_Request =
  pm_vision_interfaces::srv::DemoSetExposure_Request_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace pm_vision_interfaces


#ifndef _WIN32
# define DEPRECATED__pm_vision_interfaces__srv__DemoSetExposure_Response __attribute__((deprecated))
#else
# define DEPRECATED__pm_vision_interfaces__srv__DemoSetExposure_Response __declspec(deprecated)
#endif

namespace pm_vision_interfaces
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct DemoSetExposure_Response_
{
  using Type = DemoSetExposure_Response_<ContainerAllocator>;

  explicit DemoSetExposure_Response_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->success = false;
    }
  }

  explicit DemoSetExposure_Response_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->success = false;
    }
  }

  // field types and members
  using _success_type =
    bool;
  _success_type success;

  // setters for named parameter idiom
  Type & set__success(
    const bool & _arg)
  {
    this->success = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    pm_vision_interfaces::srv::DemoSetExposure_Response_<ContainerAllocator> *;
  using ConstRawPtr =
    const pm_vision_interfaces::srv::DemoSetExposure_Response_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<pm_vision_interfaces::srv::DemoSetExposure_Response_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<pm_vision_interfaces::srv::DemoSetExposure_Response_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      pm_vision_interfaces::srv::DemoSetExposure_Response_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<pm_vision_interfaces::srv::DemoSetExposure_Response_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      pm_vision_interfaces::srv::DemoSetExposure_Response_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<pm_vision_interfaces::srv::DemoSetExposure_Response_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<pm_vision_interfaces::srv::DemoSetExposure_Response_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<pm_vision_interfaces::srv::DemoSetExposure_Response_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__pm_vision_interfaces__srv__DemoSetExposure_Response
    std::shared_ptr<pm_vision_interfaces::srv::DemoSetExposure_Response_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__pm_vision_interfaces__srv__DemoSetExposure_Response
    std::shared_ptr<pm_vision_interfaces::srv::DemoSetExposure_Response_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const DemoSetExposure_Response_ & other) const
  {
    if (this->success != other.success) {
      return false;
    }
    return true;
  }
  bool operator!=(const DemoSetExposure_Response_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct DemoSetExposure_Response_

// alias to use template instance with default allocator
using DemoSetExposure_Response =
  pm_vision_interfaces::srv::DemoSetExposure_Response_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace pm_vision_interfaces

namespace pm_vision_interfaces
{

namespace srv
{

struct DemoSetExposure
{
  using Request = pm_vision_interfaces::srv::DemoSetExposure_Request;
  using Response = pm_vision_interfaces::srv::DemoSetExposure_Response;
};

}  // namespace srv

}  // namespace pm_vision_interfaces

#endif  // PM_VISION_INTERFACES__SRV__DETAIL__DEMO_SET_EXPOSURE__STRUCT_HPP_

// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from pm_vision_interfaces:srv/CalibratePixelPerUm.idl
// generated code does not contain a copyright notice

#ifndef PM_VISION_INTERFACES__SRV__DETAIL__CALIBRATE_PIXEL_PER_UM__STRUCT_HPP_
#define PM_VISION_INTERFACES__SRV__DETAIL__CALIBRATE_PIXEL_PER_UM__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__pm_vision_interfaces__srv__CalibratePixelPerUm_Request __attribute__((deprecated))
#else
# define DEPRECATED__pm_vision_interfaces__srv__CalibratePixelPerUm_Request __declspec(deprecated)
#endif

namespace pm_vision_interfaces
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct CalibratePixelPerUm_Request_
{
  using Type = CalibratePixelPerUm_Request_<ContainerAllocator>;

  explicit CalibratePixelPerUm_Request_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->multiplicator = 0.0;
      this->camera_config_file_name = "";
    }
  }

  explicit CalibratePixelPerUm_Request_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : camera_config_file_name(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->multiplicator = 0.0;
      this->camera_config_file_name = "";
    }
  }

  // field types and members
  using _multiplicator_type =
    double;
  _multiplicator_type multiplicator;
  using _camera_config_file_name_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _camera_config_file_name_type camera_config_file_name;

  // setters for named parameter idiom
  Type & set__multiplicator(
    const double & _arg)
  {
    this->multiplicator = _arg;
    return *this;
  }
  Type & set__camera_config_file_name(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->camera_config_file_name = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    pm_vision_interfaces::srv::CalibratePixelPerUm_Request_<ContainerAllocator> *;
  using ConstRawPtr =
    const pm_vision_interfaces::srv::CalibratePixelPerUm_Request_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<pm_vision_interfaces::srv::CalibratePixelPerUm_Request_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<pm_vision_interfaces::srv::CalibratePixelPerUm_Request_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      pm_vision_interfaces::srv::CalibratePixelPerUm_Request_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<pm_vision_interfaces::srv::CalibratePixelPerUm_Request_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      pm_vision_interfaces::srv::CalibratePixelPerUm_Request_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<pm_vision_interfaces::srv::CalibratePixelPerUm_Request_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<pm_vision_interfaces::srv::CalibratePixelPerUm_Request_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<pm_vision_interfaces::srv::CalibratePixelPerUm_Request_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__pm_vision_interfaces__srv__CalibratePixelPerUm_Request
    std::shared_ptr<pm_vision_interfaces::srv::CalibratePixelPerUm_Request_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__pm_vision_interfaces__srv__CalibratePixelPerUm_Request
    std::shared_ptr<pm_vision_interfaces::srv::CalibratePixelPerUm_Request_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const CalibratePixelPerUm_Request_ & other) const
  {
    if (this->multiplicator != other.multiplicator) {
      return false;
    }
    if (this->camera_config_file_name != other.camera_config_file_name) {
      return false;
    }
    return true;
  }
  bool operator!=(const CalibratePixelPerUm_Request_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct CalibratePixelPerUm_Request_

// alias to use template instance with default allocator
using CalibratePixelPerUm_Request =
  pm_vision_interfaces::srv::CalibratePixelPerUm_Request_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace pm_vision_interfaces


#ifndef _WIN32
# define DEPRECATED__pm_vision_interfaces__srv__CalibratePixelPerUm_Response __attribute__((deprecated))
#else
# define DEPRECATED__pm_vision_interfaces__srv__CalibratePixelPerUm_Response __declspec(deprecated)
#endif

namespace pm_vision_interfaces
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct CalibratePixelPerUm_Response_
{
  using Type = CalibratePixelPerUm_Response_<ContainerAllocator>;

  explicit CalibratePixelPerUm_Response_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->success = false;
    }
  }

  explicit CalibratePixelPerUm_Response_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
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
    pm_vision_interfaces::srv::CalibratePixelPerUm_Response_<ContainerAllocator> *;
  using ConstRawPtr =
    const pm_vision_interfaces::srv::CalibratePixelPerUm_Response_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<pm_vision_interfaces::srv::CalibratePixelPerUm_Response_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<pm_vision_interfaces::srv::CalibratePixelPerUm_Response_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      pm_vision_interfaces::srv::CalibratePixelPerUm_Response_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<pm_vision_interfaces::srv::CalibratePixelPerUm_Response_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      pm_vision_interfaces::srv::CalibratePixelPerUm_Response_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<pm_vision_interfaces::srv::CalibratePixelPerUm_Response_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<pm_vision_interfaces::srv::CalibratePixelPerUm_Response_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<pm_vision_interfaces::srv::CalibratePixelPerUm_Response_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__pm_vision_interfaces__srv__CalibratePixelPerUm_Response
    std::shared_ptr<pm_vision_interfaces::srv::CalibratePixelPerUm_Response_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__pm_vision_interfaces__srv__CalibratePixelPerUm_Response
    std::shared_ptr<pm_vision_interfaces::srv::CalibratePixelPerUm_Response_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const CalibratePixelPerUm_Response_ & other) const
  {
    if (this->success != other.success) {
      return false;
    }
    return true;
  }
  bool operator!=(const CalibratePixelPerUm_Response_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct CalibratePixelPerUm_Response_

// alias to use template instance with default allocator
using CalibratePixelPerUm_Response =
  pm_vision_interfaces::srv::CalibratePixelPerUm_Response_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace pm_vision_interfaces

namespace pm_vision_interfaces
{

namespace srv
{

struct CalibratePixelPerUm
{
  using Request = pm_vision_interfaces::srv::CalibratePixelPerUm_Request;
  using Response = pm_vision_interfaces::srv::CalibratePixelPerUm_Response;
};

}  // namespace srv

}  // namespace pm_vision_interfaces

#endif  // PM_VISION_INTERFACES__SRV__DETAIL__CALIBRATE_PIXEL_PER_UM__STRUCT_HPP_

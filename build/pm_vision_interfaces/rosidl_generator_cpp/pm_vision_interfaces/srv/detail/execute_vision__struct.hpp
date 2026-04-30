// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from pm_vision_interfaces:srv/ExecuteVision.idl
// generated code does not contain a copyright notice

#ifndef PM_VISION_INTERFACES__SRV__DETAIL__EXECUTE_VISION__STRUCT_HPP_
#define PM_VISION_INTERFACES__SRV__DETAIL__EXECUTE_VISION__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__pm_vision_interfaces__srv__ExecuteVision_Request __attribute__((deprecated))
#else
# define DEPRECATED__pm_vision_interfaces__srv__ExecuteVision_Request __declspec(deprecated)
#endif

namespace pm_vision_interfaces
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct ExecuteVision_Request_
{
  using Type = ExecuteVision_Request_<ContainerAllocator>;

  explicit ExecuteVision_Request_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->process_filename = "";
      this->camera_config_filename = "";
      this->process_uid = "";
      this->image_display_time = 0ll;
      this->run_cross_validation = false;
    }
  }

  explicit ExecuteVision_Request_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : process_filename(_alloc),
    camera_config_filename(_alloc),
    process_uid(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->process_filename = "";
      this->camera_config_filename = "";
      this->process_uid = "";
      this->image_display_time = 0ll;
      this->run_cross_validation = false;
    }
  }

  // field types and members
  using _process_filename_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _process_filename_type process_filename;
  using _camera_config_filename_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _camera_config_filename_type camera_config_filename;
  using _process_uid_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _process_uid_type process_uid;
  using _image_display_time_type =
    int64_t;
  _image_display_time_type image_display_time;
  using _run_cross_validation_type =
    bool;
  _run_cross_validation_type run_cross_validation;

  // setters for named parameter idiom
  Type & set__process_filename(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->process_filename = _arg;
    return *this;
  }
  Type & set__camera_config_filename(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->camera_config_filename = _arg;
    return *this;
  }
  Type & set__process_uid(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->process_uid = _arg;
    return *this;
  }
  Type & set__image_display_time(
    const int64_t & _arg)
  {
    this->image_display_time = _arg;
    return *this;
  }
  Type & set__run_cross_validation(
    const bool & _arg)
  {
    this->run_cross_validation = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    pm_vision_interfaces::srv::ExecuteVision_Request_<ContainerAllocator> *;
  using ConstRawPtr =
    const pm_vision_interfaces::srv::ExecuteVision_Request_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<pm_vision_interfaces::srv::ExecuteVision_Request_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<pm_vision_interfaces::srv::ExecuteVision_Request_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      pm_vision_interfaces::srv::ExecuteVision_Request_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<pm_vision_interfaces::srv::ExecuteVision_Request_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      pm_vision_interfaces::srv::ExecuteVision_Request_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<pm_vision_interfaces::srv::ExecuteVision_Request_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<pm_vision_interfaces::srv::ExecuteVision_Request_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<pm_vision_interfaces::srv::ExecuteVision_Request_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__pm_vision_interfaces__srv__ExecuteVision_Request
    std::shared_ptr<pm_vision_interfaces::srv::ExecuteVision_Request_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__pm_vision_interfaces__srv__ExecuteVision_Request
    std::shared_ptr<pm_vision_interfaces::srv::ExecuteVision_Request_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const ExecuteVision_Request_ & other) const
  {
    if (this->process_filename != other.process_filename) {
      return false;
    }
    if (this->camera_config_filename != other.camera_config_filename) {
      return false;
    }
    if (this->process_uid != other.process_uid) {
      return false;
    }
    if (this->image_display_time != other.image_display_time) {
      return false;
    }
    if (this->run_cross_validation != other.run_cross_validation) {
      return false;
    }
    return true;
  }
  bool operator!=(const ExecuteVision_Request_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct ExecuteVision_Request_

// alias to use template instance with default allocator
using ExecuteVision_Request =
  pm_vision_interfaces::srv::ExecuteVision_Request_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace pm_vision_interfaces


// Include directives for member types
// Member 'vision_response'
#include "pm_vision_interfaces/msg/detail/vision_response__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__pm_vision_interfaces__srv__ExecuteVision_Response __attribute__((deprecated))
#else
# define DEPRECATED__pm_vision_interfaces__srv__ExecuteVision_Response __declspec(deprecated)
#endif

namespace pm_vision_interfaces
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct ExecuteVision_Response_
{
  using Type = ExecuteVision_Response_<ContainerAllocator>;

  explicit ExecuteVision_Response_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : vision_response(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->success = false;
      this->results_path = "";
    }
  }

  explicit ExecuteVision_Response_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : results_path(_alloc),
    vision_response(_alloc, _init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->success = false;
      this->results_path = "";
    }
  }

  // field types and members
  using _success_type =
    bool;
  _success_type success;
  using _results_path_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _results_path_type results_path;
  using _vision_response_type =
    pm_vision_interfaces::msg::VisionResponse_<ContainerAllocator>;
  _vision_response_type vision_response;

  // setters for named parameter idiom
  Type & set__success(
    const bool & _arg)
  {
    this->success = _arg;
    return *this;
  }
  Type & set__results_path(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->results_path = _arg;
    return *this;
  }
  Type & set__vision_response(
    const pm_vision_interfaces::msg::VisionResponse_<ContainerAllocator> & _arg)
  {
    this->vision_response = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    pm_vision_interfaces::srv::ExecuteVision_Response_<ContainerAllocator> *;
  using ConstRawPtr =
    const pm_vision_interfaces::srv::ExecuteVision_Response_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<pm_vision_interfaces::srv::ExecuteVision_Response_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<pm_vision_interfaces::srv::ExecuteVision_Response_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      pm_vision_interfaces::srv::ExecuteVision_Response_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<pm_vision_interfaces::srv::ExecuteVision_Response_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      pm_vision_interfaces::srv::ExecuteVision_Response_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<pm_vision_interfaces::srv::ExecuteVision_Response_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<pm_vision_interfaces::srv::ExecuteVision_Response_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<pm_vision_interfaces::srv::ExecuteVision_Response_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__pm_vision_interfaces__srv__ExecuteVision_Response
    std::shared_ptr<pm_vision_interfaces::srv::ExecuteVision_Response_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__pm_vision_interfaces__srv__ExecuteVision_Response
    std::shared_ptr<pm_vision_interfaces::srv::ExecuteVision_Response_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const ExecuteVision_Response_ & other) const
  {
    if (this->success != other.success) {
      return false;
    }
    if (this->results_path != other.results_path) {
      return false;
    }
    if (this->vision_response != other.vision_response) {
      return false;
    }
    return true;
  }
  bool operator!=(const ExecuteVision_Response_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct ExecuteVision_Response_

// alias to use template instance with default allocator
using ExecuteVision_Response =
  pm_vision_interfaces::srv::ExecuteVision_Response_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace pm_vision_interfaces

namespace pm_vision_interfaces
{

namespace srv
{

struct ExecuteVision
{
  using Request = pm_vision_interfaces::srv::ExecuteVision_Request;
  using Response = pm_vision_interfaces::srv::ExecuteVision_Response;
};

}  // namespace srv

}  // namespace pm_vision_interfaces

#endif  // PM_VISION_INTERFACES__SRV__DETAIL__EXECUTE_VISION__STRUCT_HPP_

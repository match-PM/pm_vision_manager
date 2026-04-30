// generated from rosidl_typesupport_introspection_cpp/resource/idl__type_support.cpp.em
// with input from pm_vision_interfaces:msg/VisionArea.idl
// generated code does not contain a copyright notice

#include "array"
#include "cstddef"
#include "string"
#include "vector"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_interface/macros.h"
#include "pm_vision_interfaces/msg/detail/vision_area__struct.hpp"
#include "rosidl_typesupport_introspection_cpp/field_types.hpp"
#include "rosidl_typesupport_introspection_cpp/identifier.hpp"
#include "rosidl_typesupport_introspection_cpp/message_introspection.hpp"
#include "rosidl_typesupport_introspection_cpp/message_type_support_decl.hpp"
#include "rosidl_typesupport_introspection_cpp/visibility_control.h"

namespace pm_vision_interfaces
{

namespace msg
{

namespace rosidl_typesupport_introspection_cpp
{

void VisionArea_init_function(
  void * message_memory, rosidl_runtime_cpp::MessageInitialization _init)
{
  new (message_memory) pm_vision_interfaces::msg::VisionArea(_init);
}

void VisionArea_fini_function(void * message_memory)
{
  auto typed_message = static_cast<pm_vision_interfaces::msg::VisionArea *>(message_memory);
  typed_message->~VisionArea();
}

static const ::rosidl_typesupport_introspection_cpp::MessageMember VisionArea_message_member_array[1] = {
  {
    "structure_needs_at_least_one_member",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_UINT8,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(pm_vision_interfaces::msg::VisionArea, structure_needs_at_least_one_member),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  }
};

static const ::rosidl_typesupport_introspection_cpp::MessageMembers VisionArea_message_members = {
  "pm_vision_interfaces::msg",  // message namespace
  "VisionArea",  // message name
  1,  // number of fields
  sizeof(pm_vision_interfaces::msg::VisionArea),
  VisionArea_message_member_array,  // message members
  VisionArea_init_function,  // function to initialize message memory (memory has to be allocated)
  VisionArea_fini_function  // function to terminate message instance (will not free memory)
};

static const rosidl_message_type_support_t VisionArea_message_type_support_handle = {
  ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  &VisionArea_message_members,
  get_message_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_introspection_cpp

}  // namespace msg

}  // namespace pm_vision_interfaces


namespace rosidl_typesupport_introspection_cpp
{

template<>
ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<pm_vision_interfaces::msg::VisionArea>()
{
  return &::pm_vision_interfaces::msg::rosidl_typesupport_introspection_cpp::VisionArea_message_type_support_handle;
}

}  // namespace rosidl_typesupport_introspection_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, pm_vision_interfaces, msg, VisionArea)() {
  return &::pm_vision_interfaces::msg::rosidl_typesupport_introspection_cpp::VisionArea_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif

// generated from rosidl_typesupport_introspection_cpp/resource/idl__type_support.cpp.em
// with input from pm_vision_interfaces:msg/VisionResults.idl
// generated code does not contain a copyright notice

#include "array"
#include "cstddef"
#include "string"
#include "vector"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_interface/macros.h"
#include "pm_vision_interfaces/msg/detail/vision_results__struct.hpp"
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

void VisionResults_init_function(
  void * message_memory, rosidl_runtime_cpp::MessageInitialization _init)
{
  new (message_memory) pm_vision_interfaces::msg::VisionResults(_init);
}

void VisionResults_fini_function(void * message_memory)
{
  auto typed_message = static_cast<pm_vision_interfaces::msg::VisionResults *>(message_memory);
  typed_message->~VisionResults();
}

size_t size_function__VisionResults__points(const void * untyped_member)
{
  const auto * member = reinterpret_cast<const std::vector<pm_vision_interfaces::msg::VisionPoint> *>(untyped_member);
  return member->size();
}

const void * get_const_function__VisionResults__points(const void * untyped_member, size_t index)
{
  const auto & member =
    *reinterpret_cast<const std::vector<pm_vision_interfaces::msg::VisionPoint> *>(untyped_member);
  return &member[index];
}

void * get_function__VisionResults__points(void * untyped_member, size_t index)
{
  auto & member =
    *reinterpret_cast<std::vector<pm_vision_interfaces::msg::VisionPoint> *>(untyped_member);
  return &member[index];
}

void fetch_function__VisionResults__points(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const auto & item = *reinterpret_cast<const pm_vision_interfaces::msg::VisionPoint *>(
    get_const_function__VisionResults__points(untyped_member, index));
  auto & value = *reinterpret_cast<pm_vision_interfaces::msg::VisionPoint *>(untyped_value);
  value = item;
}

void assign_function__VisionResults__points(
  void * untyped_member, size_t index, const void * untyped_value)
{
  auto & item = *reinterpret_cast<pm_vision_interfaces::msg::VisionPoint *>(
    get_function__VisionResults__points(untyped_member, index));
  const auto & value = *reinterpret_cast<const pm_vision_interfaces::msg::VisionPoint *>(untyped_value);
  item = value;
}

void resize_function__VisionResults__points(void * untyped_member, size_t size)
{
  auto * member =
    reinterpret_cast<std::vector<pm_vision_interfaces::msg::VisionPoint> *>(untyped_member);
  member->resize(size);
}

size_t size_function__VisionResults__lines(const void * untyped_member)
{
  const auto * member = reinterpret_cast<const std::vector<pm_vision_interfaces::msg::VisionLine> *>(untyped_member);
  return member->size();
}

const void * get_const_function__VisionResults__lines(const void * untyped_member, size_t index)
{
  const auto & member =
    *reinterpret_cast<const std::vector<pm_vision_interfaces::msg::VisionLine> *>(untyped_member);
  return &member[index];
}

void * get_function__VisionResults__lines(void * untyped_member, size_t index)
{
  auto & member =
    *reinterpret_cast<std::vector<pm_vision_interfaces::msg::VisionLine> *>(untyped_member);
  return &member[index];
}

void fetch_function__VisionResults__lines(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const auto & item = *reinterpret_cast<const pm_vision_interfaces::msg::VisionLine *>(
    get_const_function__VisionResults__lines(untyped_member, index));
  auto & value = *reinterpret_cast<pm_vision_interfaces::msg::VisionLine *>(untyped_value);
  value = item;
}

void assign_function__VisionResults__lines(
  void * untyped_member, size_t index, const void * untyped_value)
{
  auto & item = *reinterpret_cast<pm_vision_interfaces::msg::VisionLine *>(
    get_function__VisionResults__lines(untyped_member, index));
  const auto & value = *reinterpret_cast<const pm_vision_interfaces::msg::VisionLine *>(untyped_value);
  item = value;
}

void resize_function__VisionResults__lines(void * untyped_member, size_t size)
{
  auto * member =
    reinterpret_cast<std::vector<pm_vision_interfaces::msg::VisionLine> *>(untyped_member);
  member->resize(size);
}

size_t size_function__VisionResults__areas(const void * untyped_member)
{
  const auto * member = reinterpret_cast<const std::vector<pm_vision_interfaces::msg::VisionArea> *>(untyped_member);
  return member->size();
}

const void * get_const_function__VisionResults__areas(const void * untyped_member, size_t index)
{
  const auto & member =
    *reinterpret_cast<const std::vector<pm_vision_interfaces::msg::VisionArea> *>(untyped_member);
  return &member[index];
}

void * get_function__VisionResults__areas(void * untyped_member, size_t index)
{
  auto & member =
    *reinterpret_cast<std::vector<pm_vision_interfaces::msg::VisionArea> *>(untyped_member);
  return &member[index];
}

void fetch_function__VisionResults__areas(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const auto & item = *reinterpret_cast<const pm_vision_interfaces::msg::VisionArea *>(
    get_const_function__VisionResults__areas(untyped_member, index));
  auto & value = *reinterpret_cast<pm_vision_interfaces::msg::VisionArea *>(untyped_value);
  value = item;
}

void assign_function__VisionResults__areas(
  void * untyped_member, size_t index, const void * untyped_value)
{
  auto & item = *reinterpret_cast<pm_vision_interfaces::msg::VisionArea *>(
    get_function__VisionResults__areas(untyped_member, index));
  const auto & value = *reinterpret_cast<const pm_vision_interfaces::msg::VisionArea *>(untyped_value);
  item = value;
}

void resize_function__VisionResults__areas(void * untyped_member, size_t size)
{
  auto * member =
    reinterpret_cast<std::vector<pm_vision_interfaces::msg::VisionArea> *>(untyped_member);
  member->resize(size);
}

size_t size_function__VisionResults__circles(const void * untyped_member)
{
  const auto * member = reinterpret_cast<const std::vector<pm_vision_interfaces::msg::VisionCircle> *>(untyped_member);
  return member->size();
}

const void * get_const_function__VisionResults__circles(const void * untyped_member, size_t index)
{
  const auto & member =
    *reinterpret_cast<const std::vector<pm_vision_interfaces::msg::VisionCircle> *>(untyped_member);
  return &member[index];
}

void * get_function__VisionResults__circles(void * untyped_member, size_t index)
{
  auto & member =
    *reinterpret_cast<std::vector<pm_vision_interfaces::msg::VisionCircle> *>(untyped_member);
  return &member[index];
}

void fetch_function__VisionResults__circles(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const auto & item = *reinterpret_cast<const pm_vision_interfaces::msg::VisionCircle *>(
    get_const_function__VisionResults__circles(untyped_member, index));
  auto & value = *reinterpret_cast<pm_vision_interfaces::msg::VisionCircle *>(untyped_value);
  value = item;
}

void assign_function__VisionResults__circles(
  void * untyped_member, size_t index, const void * untyped_value)
{
  auto & item = *reinterpret_cast<pm_vision_interfaces::msg::VisionCircle *>(
    get_function__VisionResults__circles(untyped_member, index));
  const auto & value = *reinterpret_cast<const pm_vision_interfaces::msg::VisionCircle *>(untyped_value);
  item = value;
}

void resize_function__VisionResults__circles(void * untyped_member, size_t size)
{
  auto * member =
    reinterpret_cast<std::vector<pm_vision_interfaces::msg::VisionCircle> *>(untyped_member);
  member->resize(size);
}

static const ::rosidl_typesupport_introspection_cpp::MessageMember VisionResults_message_member_array[5] = {
  {
    "points",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    ::rosidl_typesupport_introspection_cpp::get_message_type_support_handle<pm_vision_interfaces::msg::VisionPoint>(),  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(pm_vision_interfaces::msg::VisionResults, points),  // bytes offset in struct
    nullptr,  // default value
    size_function__VisionResults__points,  // size() function pointer
    get_const_function__VisionResults__points,  // get_const(index) function pointer
    get_function__VisionResults__points,  // get(index) function pointer
    fetch_function__VisionResults__points,  // fetch(index, &value) function pointer
    assign_function__VisionResults__points,  // assign(index, value) function pointer
    resize_function__VisionResults__points  // resize(index) function pointer
  },
  {
    "lines",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    ::rosidl_typesupport_introspection_cpp::get_message_type_support_handle<pm_vision_interfaces::msg::VisionLine>(),  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(pm_vision_interfaces::msg::VisionResults, lines),  // bytes offset in struct
    nullptr,  // default value
    size_function__VisionResults__lines,  // size() function pointer
    get_const_function__VisionResults__lines,  // get_const(index) function pointer
    get_function__VisionResults__lines,  // get(index) function pointer
    fetch_function__VisionResults__lines,  // fetch(index, &value) function pointer
    assign_function__VisionResults__lines,  // assign(index, value) function pointer
    resize_function__VisionResults__lines  // resize(index) function pointer
  },
  {
    "areas",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    ::rosidl_typesupport_introspection_cpp::get_message_type_support_handle<pm_vision_interfaces::msg::VisionArea>(),  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(pm_vision_interfaces::msg::VisionResults, areas),  // bytes offset in struct
    nullptr,  // default value
    size_function__VisionResults__areas,  // size() function pointer
    get_const_function__VisionResults__areas,  // get_const(index) function pointer
    get_function__VisionResults__areas,  // get(index) function pointer
    fetch_function__VisionResults__areas,  // fetch(index, &value) function pointer
    assign_function__VisionResults__areas,  // assign(index, value) function pointer
    resize_function__VisionResults__areas  // resize(index) function pointer
  },
  {
    "circles",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    ::rosidl_typesupport_introspection_cpp::get_message_type_support_handle<pm_vision_interfaces::msg::VisionCircle>(),  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(pm_vision_interfaces::msg::VisionResults, circles),  // bytes offset in struct
    nullptr,  // default value
    size_function__VisionResults__circles,  // size() function pointer
    get_const_function__VisionResults__circles,  // get_const(index) function pointer
    get_function__VisionResults__circles,  // get(index) function pointer
    fetch_function__VisionResults__circles,  // fetch(index, &value) function pointer
    assign_function__VisionResults__circles,  // assign(index, value) function pointer
    resize_function__VisionResults__circles  // resize(index) function pointer
  },
  {
    "image_sharpness",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    ::rosidl_typesupport_introspection_cpp::get_message_type_support_handle<pm_vision_interfaces::msg::ImageSharpness>(),  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(pm_vision_interfaces::msg::VisionResults, image_sharpness),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  }
};

static const ::rosidl_typesupport_introspection_cpp::MessageMembers VisionResults_message_members = {
  "pm_vision_interfaces::msg",  // message namespace
  "VisionResults",  // message name
  5,  // number of fields
  sizeof(pm_vision_interfaces::msg::VisionResults),
  VisionResults_message_member_array,  // message members
  VisionResults_init_function,  // function to initialize message memory (memory has to be allocated)
  VisionResults_fini_function  // function to terminate message instance (will not free memory)
};

static const rosidl_message_type_support_t VisionResults_message_type_support_handle = {
  ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  &VisionResults_message_members,
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
get_message_type_support_handle<pm_vision_interfaces::msg::VisionResults>()
{
  return &::pm_vision_interfaces::msg::rosidl_typesupport_introspection_cpp::VisionResults_message_type_support_handle;
}

}  // namespace rosidl_typesupport_introspection_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, pm_vision_interfaces, msg, VisionResults)() {
  return &::pm_vision_interfaces::msg::rosidl_typesupport_introspection_cpp::VisionResults_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif

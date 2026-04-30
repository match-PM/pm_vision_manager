// generated from rosidl_typesupport_cpp/resource/idl__type_support.cpp.em
// with input from pm_vision_interfaces:msg/VisionPoint.idl
// generated code does not contain a copyright notice

#include "cstddef"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "pm_vision_interfaces/msg/detail/vision_point__struct.hpp"
#include "rosidl_typesupport_cpp/identifier.hpp"
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_c/type_support_map.h"
#include "rosidl_typesupport_cpp/message_type_support_dispatch.hpp"
#include "rosidl_typesupport_cpp/visibility_control.h"
#include "rosidl_typesupport_interface/macros.h"

namespace pm_vision_interfaces
{

namespace msg
{

namespace rosidl_typesupport_cpp
{

typedef struct _VisionPoint_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _VisionPoint_type_support_ids_t;

static const _VisionPoint_type_support_ids_t _VisionPoint_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _VisionPoint_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _VisionPoint_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _VisionPoint_type_support_symbol_names_t _VisionPoint_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, pm_vision_interfaces, msg, VisionPoint)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, pm_vision_interfaces, msg, VisionPoint)),
  }
};

typedef struct _VisionPoint_type_support_data_t
{
  void * data[2];
} _VisionPoint_type_support_data_t;

static _VisionPoint_type_support_data_t _VisionPoint_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _VisionPoint_message_typesupport_map = {
  2,
  "pm_vision_interfaces",
  &_VisionPoint_message_typesupport_ids.typesupport_identifier[0],
  &_VisionPoint_message_typesupport_symbol_names.symbol_name[0],
  &_VisionPoint_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t VisionPoint_message_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_VisionPoint_message_typesupport_map),
  ::rosidl_typesupport_cpp::get_message_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace msg

}  // namespace pm_vision_interfaces

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<pm_vision_interfaces::msg::VisionPoint>()
{
  return &::pm_vision_interfaces::msg::rosidl_typesupport_cpp::VisionPoint_message_type_support_handle;
}

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_cpp, pm_vision_interfaces, msg, VisionPoint)() {
  return get_message_type_support_handle<pm_vision_interfaces::msg::VisionPoint>();
}

#ifdef __cplusplus
}
#endif
}  // namespace rosidl_typesupport_cpp

// generated from rosidl_typesupport_c/resource/idl__type_support.cpp.em
// with input from pm_vision_interfaces:msg/VisionLine.idl
// generated code does not contain a copyright notice

#include "cstddef"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "pm_vision_interfaces/msg/detail/vision_line__struct.h"
#include "pm_vision_interfaces/msg/detail/vision_line__type_support.h"
#include "rosidl_typesupport_c/identifier.h"
#include "rosidl_typesupport_c/message_type_support_dispatch.h"
#include "rosidl_typesupport_c/type_support_map.h"
#include "rosidl_typesupport_c/visibility_control.h"
#include "rosidl_typesupport_interface/macros.h"

namespace pm_vision_interfaces
{

namespace msg
{

namespace rosidl_typesupport_c
{

typedef struct _VisionLine_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _VisionLine_type_support_ids_t;

static const _VisionLine_type_support_ids_t _VisionLine_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
  }
};

typedef struct _VisionLine_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _VisionLine_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _VisionLine_type_support_symbol_names_t _VisionLine_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, pm_vision_interfaces, msg, VisionLine)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, pm_vision_interfaces, msg, VisionLine)),
  }
};

typedef struct _VisionLine_type_support_data_t
{
  void * data[2];
} _VisionLine_type_support_data_t;

static _VisionLine_type_support_data_t _VisionLine_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _VisionLine_message_typesupport_map = {
  2,
  "pm_vision_interfaces",
  &_VisionLine_message_typesupport_ids.typesupport_identifier[0],
  &_VisionLine_message_typesupport_symbol_names.symbol_name[0],
  &_VisionLine_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t VisionLine_message_type_support_handle = {
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_VisionLine_message_typesupport_map),
  rosidl_typesupport_c__get_message_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_c

}  // namespace msg

}  // namespace pm_vision_interfaces

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_c, pm_vision_interfaces, msg, VisionLine)() {
  return &::pm_vision_interfaces::msg::rosidl_typesupport_c::VisionLine_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif

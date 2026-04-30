// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from pm_vision_interfaces:srv/CalibrateAngle.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "pm_vision_interfaces/srv/detail/calibrate_angle__rosidl_typesupport_introspection_c.h"
#include "pm_vision_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "pm_vision_interfaces/srv/detail/calibrate_angle__functions.h"
#include "pm_vision_interfaces/srv/detail/calibrate_angle__struct.h"


// Include directives for member types
// Member `camera_config_file_name`
#include "rosidl_runtime_c/string_functions.h"

#ifdef __cplusplus
extern "C"
{
#endif

void pm_vision_interfaces__srv__CalibrateAngle_Request__rosidl_typesupport_introspection_c__CalibrateAngle_Request_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  pm_vision_interfaces__srv__CalibrateAngle_Request__init(message_memory);
}

void pm_vision_interfaces__srv__CalibrateAngle_Request__rosidl_typesupport_introspection_c__CalibrateAngle_Request_fini_function(void * message_memory)
{
  pm_vision_interfaces__srv__CalibrateAngle_Request__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember pm_vision_interfaces__srv__CalibrateAngle_Request__rosidl_typesupport_introspection_c__CalibrateAngle_Request_message_member_array[2] = {
  {
    "angle_diff",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(pm_vision_interfaces__srv__CalibrateAngle_Request, angle_diff),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "camera_config_file_name",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(pm_vision_interfaces__srv__CalibrateAngle_Request, camera_config_file_name),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers pm_vision_interfaces__srv__CalibrateAngle_Request__rosidl_typesupport_introspection_c__CalibrateAngle_Request_message_members = {
  "pm_vision_interfaces__srv",  // message namespace
  "CalibrateAngle_Request",  // message name
  2,  // number of fields
  sizeof(pm_vision_interfaces__srv__CalibrateAngle_Request),
  pm_vision_interfaces__srv__CalibrateAngle_Request__rosidl_typesupport_introspection_c__CalibrateAngle_Request_message_member_array,  // message members
  pm_vision_interfaces__srv__CalibrateAngle_Request__rosidl_typesupport_introspection_c__CalibrateAngle_Request_init_function,  // function to initialize message memory (memory has to be allocated)
  pm_vision_interfaces__srv__CalibrateAngle_Request__rosidl_typesupport_introspection_c__CalibrateAngle_Request_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t pm_vision_interfaces__srv__CalibrateAngle_Request__rosidl_typesupport_introspection_c__CalibrateAngle_Request_message_type_support_handle = {
  0,
  &pm_vision_interfaces__srv__CalibrateAngle_Request__rosidl_typesupport_introspection_c__CalibrateAngle_Request_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_pm_vision_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, pm_vision_interfaces, srv, CalibrateAngle_Request)() {
  if (!pm_vision_interfaces__srv__CalibrateAngle_Request__rosidl_typesupport_introspection_c__CalibrateAngle_Request_message_type_support_handle.typesupport_identifier) {
    pm_vision_interfaces__srv__CalibrateAngle_Request__rosidl_typesupport_introspection_c__CalibrateAngle_Request_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &pm_vision_interfaces__srv__CalibrateAngle_Request__rosidl_typesupport_introspection_c__CalibrateAngle_Request_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

// already included above
// #include <stddef.h>
// already included above
// #include "pm_vision_interfaces/srv/detail/calibrate_angle__rosidl_typesupport_introspection_c.h"
// already included above
// #include "pm_vision_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "rosidl_typesupport_introspection_c/field_types.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
// already included above
// #include "rosidl_typesupport_introspection_c/message_introspection.h"
// already included above
// #include "pm_vision_interfaces/srv/detail/calibrate_angle__functions.h"
// already included above
// #include "pm_vision_interfaces/srv/detail/calibrate_angle__struct.h"


#ifdef __cplusplus
extern "C"
{
#endif

void pm_vision_interfaces__srv__CalibrateAngle_Response__rosidl_typesupport_introspection_c__CalibrateAngle_Response_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  pm_vision_interfaces__srv__CalibrateAngle_Response__init(message_memory);
}

void pm_vision_interfaces__srv__CalibrateAngle_Response__rosidl_typesupport_introspection_c__CalibrateAngle_Response_fini_function(void * message_memory)
{
  pm_vision_interfaces__srv__CalibrateAngle_Response__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember pm_vision_interfaces__srv__CalibrateAngle_Response__rosidl_typesupport_introspection_c__CalibrateAngle_Response_message_member_array[1] = {
  {
    "success",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_BOOLEAN,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(pm_vision_interfaces__srv__CalibrateAngle_Response, success),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers pm_vision_interfaces__srv__CalibrateAngle_Response__rosidl_typesupport_introspection_c__CalibrateAngle_Response_message_members = {
  "pm_vision_interfaces__srv",  // message namespace
  "CalibrateAngle_Response",  // message name
  1,  // number of fields
  sizeof(pm_vision_interfaces__srv__CalibrateAngle_Response),
  pm_vision_interfaces__srv__CalibrateAngle_Response__rosidl_typesupport_introspection_c__CalibrateAngle_Response_message_member_array,  // message members
  pm_vision_interfaces__srv__CalibrateAngle_Response__rosidl_typesupport_introspection_c__CalibrateAngle_Response_init_function,  // function to initialize message memory (memory has to be allocated)
  pm_vision_interfaces__srv__CalibrateAngle_Response__rosidl_typesupport_introspection_c__CalibrateAngle_Response_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t pm_vision_interfaces__srv__CalibrateAngle_Response__rosidl_typesupport_introspection_c__CalibrateAngle_Response_message_type_support_handle = {
  0,
  &pm_vision_interfaces__srv__CalibrateAngle_Response__rosidl_typesupport_introspection_c__CalibrateAngle_Response_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_pm_vision_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, pm_vision_interfaces, srv, CalibrateAngle_Response)() {
  if (!pm_vision_interfaces__srv__CalibrateAngle_Response__rosidl_typesupport_introspection_c__CalibrateAngle_Response_message_type_support_handle.typesupport_identifier) {
    pm_vision_interfaces__srv__CalibrateAngle_Response__rosidl_typesupport_introspection_c__CalibrateAngle_Response_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &pm_vision_interfaces__srv__CalibrateAngle_Response__rosidl_typesupport_introspection_c__CalibrateAngle_Response_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

#include "rosidl_runtime_c/service_type_support_struct.h"
// already included above
// #include "pm_vision_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "pm_vision_interfaces/srv/detail/calibrate_angle__rosidl_typesupport_introspection_c.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/service_introspection.h"

// this is intentionally not const to allow initialization later to prevent an initialization race
static rosidl_typesupport_introspection_c__ServiceMembers pm_vision_interfaces__srv__detail__calibrate_angle__rosidl_typesupport_introspection_c__CalibrateAngle_service_members = {
  "pm_vision_interfaces__srv",  // service namespace
  "CalibrateAngle",  // service name
  // these two fields are initialized below on the first access
  NULL,  // request message
  // pm_vision_interfaces__srv__detail__calibrate_angle__rosidl_typesupport_introspection_c__CalibrateAngle_Request_message_type_support_handle,
  NULL  // response message
  // pm_vision_interfaces__srv__detail__calibrate_angle__rosidl_typesupport_introspection_c__CalibrateAngle_Response_message_type_support_handle
};

static rosidl_service_type_support_t pm_vision_interfaces__srv__detail__calibrate_angle__rosidl_typesupport_introspection_c__CalibrateAngle_service_type_support_handle = {
  0,
  &pm_vision_interfaces__srv__detail__calibrate_angle__rosidl_typesupport_introspection_c__CalibrateAngle_service_members,
  get_service_typesupport_handle_function,
};

// Forward declaration of request/response type support functions
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, pm_vision_interfaces, srv, CalibrateAngle_Request)();

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, pm_vision_interfaces, srv, CalibrateAngle_Response)();

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_pm_vision_interfaces
const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_introspection_c, pm_vision_interfaces, srv, CalibrateAngle)() {
  if (!pm_vision_interfaces__srv__detail__calibrate_angle__rosidl_typesupport_introspection_c__CalibrateAngle_service_type_support_handle.typesupport_identifier) {
    pm_vision_interfaces__srv__detail__calibrate_angle__rosidl_typesupport_introspection_c__CalibrateAngle_service_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  rosidl_typesupport_introspection_c__ServiceMembers * service_members =
    (rosidl_typesupport_introspection_c__ServiceMembers *)pm_vision_interfaces__srv__detail__calibrate_angle__rosidl_typesupport_introspection_c__CalibrateAngle_service_type_support_handle.data;

  if (!service_members->request_members_) {
    service_members->request_members_ =
      (const rosidl_typesupport_introspection_c__MessageMembers *)
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, pm_vision_interfaces, srv, CalibrateAngle_Request)()->data;
  }
  if (!service_members->response_members_) {
    service_members->response_members_ =
      (const rosidl_typesupport_introspection_c__MessageMembers *)
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, pm_vision_interfaces, srv, CalibrateAngle_Response)()->data;
  }

  return &pm_vision_interfaces__srv__detail__calibrate_angle__rosidl_typesupport_introspection_c__CalibrateAngle_service_type_support_handle;
}

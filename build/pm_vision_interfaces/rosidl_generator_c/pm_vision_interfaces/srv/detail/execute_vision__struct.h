// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from pm_vision_interfaces:srv/ExecuteVision.idl
// generated code does not contain a copyright notice

#ifndef PM_VISION_INTERFACES__SRV__DETAIL__EXECUTE_VISION__STRUCT_H_
#define PM_VISION_INTERFACES__SRV__DETAIL__EXECUTE_VISION__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'process_filename'
// Member 'camera_config_filename'
// Member 'process_uid'
#include "rosidl_runtime_c/string.h"

/// Struct defined in srv/ExecuteVision in the package pm_vision_interfaces.
typedef struct pm_vision_interfaces__srv__ExecuteVision_Request
{
  rosidl_runtime_c__String process_filename;
  rosidl_runtime_c__String camera_config_filename;
  rosidl_runtime_c__String process_uid;
  int64_t image_display_time;
  bool run_cross_validation;
} pm_vision_interfaces__srv__ExecuteVision_Request;

// Struct for a sequence of pm_vision_interfaces__srv__ExecuteVision_Request.
typedef struct pm_vision_interfaces__srv__ExecuteVision_Request__Sequence
{
  pm_vision_interfaces__srv__ExecuteVision_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} pm_vision_interfaces__srv__ExecuteVision_Request__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'results_path'
// already included above
// #include "rosidl_runtime_c/string.h"
// Member 'vision_response'
#include "pm_vision_interfaces/msg/detail/vision_response__struct.h"

/// Struct defined in srv/ExecuteVision in the package pm_vision_interfaces.
typedef struct pm_vision_interfaces__srv__ExecuteVision_Response
{
  bool success;
  rosidl_runtime_c__String results_path;
  pm_vision_interfaces__msg__VisionResponse vision_response;
} pm_vision_interfaces__srv__ExecuteVision_Response;

// Struct for a sequence of pm_vision_interfaces__srv__ExecuteVision_Response.
typedef struct pm_vision_interfaces__srv__ExecuteVision_Response__Sequence
{
  pm_vision_interfaces__srv__ExecuteVision_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} pm_vision_interfaces__srv__ExecuteVision_Response__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // PM_VISION_INTERFACES__SRV__DETAIL__EXECUTE_VISION__STRUCT_H_

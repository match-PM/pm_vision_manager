// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from pm_vision_interfaces:srv/CalibrateAngle.idl
// generated code does not contain a copyright notice

#ifndef PM_VISION_INTERFACES__SRV__DETAIL__CALIBRATE_ANGLE__STRUCT_H_
#define PM_VISION_INTERFACES__SRV__DETAIL__CALIBRATE_ANGLE__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'camera_config_file_name'
#include "rosidl_runtime_c/string.h"

/// Struct defined in srv/CalibrateAngle in the package pm_vision_interfaces.
typedef struct pm_vision_interfaces__srv__CalibrateAngle_Request
{
  double angle_diff;
  rosidl_runtime_c__String camera_config_file_name;
} pm_vision_interfaces__srv__CalibrateAngle_Request;

// Struct for a sequence of pm_vision_interfaces__srv__CalibrateAngle_Request.
typedef struct pm_vision_interfaces__srv__CalibrateAngle_Request__Sequence
{
  pm_vision_interfaces__srv__CalibrateAngle_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} pm_vision_interfaces__srv__CalibrateAngle_Request__Sequence;


// Constants defined in the message

/// Struct defined in srv/CalibrateAngle in the package pm_vision_interfaces.
typedef struct pm_vision_interfaces__srv__CalibrateAngle_Response
{
  bool success;
} pm_vision_interfaces__srv__CalibrateAngle_Response;

// Struct for a sequence of pm_vision_interfaces__srv__CalibrateAngle_Response.
typedef struct pm_vision_interfaces__srv__CalibrateAngle_Response__Sequence
{
  pm_vision_interfaces__srv__CalibrateAngle_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} pm_vision_interfaces__srv__CalibrateAngle_Response__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // PM_VISION_INTERFACES__SRV__DETAIL__CALIBRATE_ANGLE__STRUCT_H_

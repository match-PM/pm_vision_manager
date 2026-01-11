// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from pm_vision_interfaces:msg/VisionPoint.idl
// generated code does not contain a copyright notice

#ifndef PM_VISION_INTERFACES__MSG__DETAIL__VISION_POINT__STRUCT_H_
#define PM_VISION_INTERFACES__MSG__DETAIL__VISION_POINT__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'axis_suffix_1'
// Member 'axis_suffix_2'
#include "rosidl_runtime_c/string.h"

/// Struct defined in msg/VisionPoint in the package pm_vision_interfaces.
typedef struct pm_vision_interfaces__msg__VisionPoint
{
  float axis_value_1;
  float axis_value_2;
  rosidl_runtime_c__String axis_suffix_1;
  rosidl_runtime_c__String axis_suffix_2;
} pm_vision_interfaces__msg__VisionPoint;

// Struct for a sequence of pm_vision_interfaces__msg__VisionPoint.
typedef struct pm_vision_interfaces__msg__VisionPoint__Sequence
{
  pm_vision_interfaces__msg__VisionPoint * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} pm_vision_interfaces__msg__VisionPoint__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // PM_VISION_INTERFACES__MSG__DETAIL__VISION_POINT__STRUCT_H_

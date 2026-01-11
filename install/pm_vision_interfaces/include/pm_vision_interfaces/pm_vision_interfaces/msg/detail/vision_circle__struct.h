// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from pm_vision_interfaces:msg/VisionCircle.idl
// generated code does not contain a copyright notice

#ifndef PM_VISION_INTERFACES__MSG__DETAIL__VISION_CIRCLE__STRUCT_H_
#define PM_VISION_INTERFACES__MSG__DETAIL__VISION_CIRCLE__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'center_point'
#include "pm_vision_interfaces/msg/detail/vision_point__struct.h"

/// Struct defined in msg/VisionCircle in the package pm_vision_interfaces.
typedef struct pm_vision_interfaces__msg__VisionCircle
{
  pm_vision_interfaces__msg__VisionPoint center_point;
  double radius;
} pm_vision_interfaces__msg__VisionCircle;

// Struct for a sequence of pm_vision_interfaces__msg__VisionCircle.
typedef struct pm_vision_interfaces__msg__VisionCircle__Sequence
{
  pm_vision_interfaces__msg__VisionCircle * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} pm_vision_interfaces__msg__VisionCircle__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // PM_VISION_INTERFACES__MSG__DETAIL__VISION_CIRCLE__STRUCT_H_

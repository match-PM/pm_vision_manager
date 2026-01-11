// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from pm_vision_interfaces:msg/VisionLine.idl
// generated code does not contain a copyright notice

#ifndef PM_VISION_INTERFACES__MSG__DETAIL__VISION_LINE__STRUCT_H_
#define PM_VISION_INTERFACES__MSG__DETAIL__VISION_LINE__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'point_1'
// Member 'point_2'
// Member 'point_mid'
#include "pm_vision_interfaces/msg/detail/vision_point__struct.h"

/// Struct defined in msg/VisionLine in the package pm_vision_interfaces.
typedef struct pm_vision_interfaces__msg__VisionLine
{
  pm_vision_interfaces__msg__VisionPoint point_1;
  pm_vision_interfaces__msg__VisionPoint point_2;
  pm_vision_interfaces__msg__VisionPoint point_mid;
  float angle;
  float length;
} pm_vision_interfaces__msg__VisionLine;

// Struct for a sequence of pm_vision_interfaces__msg__VisionLine.
typedef struct pm_vision_interfaces__msg__VisionLine__Sequence
{
  pm_vision_interfaces__msg__VisionLine * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} pm_vision_interfaces__msg__VisionLine__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // PM_VISION_INTERFACES__MSG__DETAIL__VISION_LINE__STRUCT_H_

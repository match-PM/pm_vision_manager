// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from pm_vision_interfaces:msg/VisionResults.idl
// generated code does not contain a copyright notice

#ifndef PM_VISION_INTERFACES__MSG__DETAIL__VISION_RESULTS__STRUCT_H_
#define PM_VISION_INTERFACES__MSG__DETAIL__VISION_RESULTS__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'points'
#include "pm_vision_interfaces/msg/detail/vision_point__struct.h"
// Member 'lines'
#include "pm_vision_interfaces/msg/detail/vision_line__struct.h"
// Member 'areas'
#include "pm_vision_interfaces/msg/detail/vision_area__struct.h"
// Member 'circles'
#include "pm_vision_interfaces/msg/detail/vision_circle__struct.h"
// Member 'image_sharpness'
#include "pm_vision_interfaces/msg/detail/image_sharpness__struct.h"

/// Struct defined in msg/VisionResults in the package pm_vision_interfaces.
typedef struct pm_vision_interfaces__msg__VisionResults
{
  pm_vision_interfaces__msg__VisionPoint__Sequence points;
  pm_vision_interfaces__msg__VisionLine__Sequence lines;
  pm_vision_interfaces__msg__VisionArea__Sequence areas;
  pm_vision_interfaces__msg__VisionCircle__Sequence circles;
  pm_vision_interfaces__msg__ImageSharpness image_sharpness;
} pm_vision_interfaces__msg__VisionResults;

// Struct for a sequence of pm_vision_interfaces__msg__VisionResults.
typedef struct pm_vision_interfaces__msg__VisionResults__Sequence
{
  pm_vision_interfaces__msg__VisionResults * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} pm_vision_interfaces__msg__VisionResults__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // PM_VISION_INTERFACES__MSG__DETAIL__VISION_RESULTS__STRUCT_H_

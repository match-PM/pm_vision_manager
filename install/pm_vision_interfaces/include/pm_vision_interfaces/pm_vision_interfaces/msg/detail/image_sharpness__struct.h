// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from pm_vision_interfaces:msg/ImageSharpness.idl
// generated code does not contain a copyright notice

#ifndef PM_VISION_INTERFACES__MSG__DETAIL__IMAGE_SHARPNESS__STRUCT_H_
#define PM_VISION_INTERFACES__MSG__DETAIL__IMAGE_SHARPNESS__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in msg/ImageSharpness in the package pm_vision_interfaces.
typedef struct pm_vision_interfaces__msg__ImageSharpness
{
  double sharpness_value;
} pm_vision_interfaces__msg__ImageSharpness;

// Struct for a sequence of pm_vision_interfaces__msg__ImageSharpness.
typedef struct pm_vision_interfaces__msg__ImageSharpness__Sequence
{
  pm_vision_interfaces__msg__ImageSharpness * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} pm_vision_interfaces__msg__ImageSharpness__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // PM_VISION_INTERFACES__MSG__DETAIL__IMAGE_SHARPNESS__STRUCT_H_

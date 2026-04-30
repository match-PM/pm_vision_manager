// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from pm_vision_interfaces:msg/CrossValidation.idl
// generated code does not contain a copyright notice

#ifndef PM_VISION_INTERFACES__MSG__DETAIL__CROSS_VALIDATION__STRUCT_H_
#define PM_VISION_INTERFACES__MSG__DETAIL__CROSS_VALIDATION__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'image_source_name'
// Member 'failed_images'
#include "rosidl_runtime_c/string.h"

/// Struct defined in msg/CrossValidation in the package pm_vision_interfaces.
typedef struct pm_vision_interfaces__msg__CrossValidation
{
  rosidl_runtime_c__String image_source_name;
  bool vision_ok;
  rosidl_runtime_c__String__Sequence failed_images;
  int32_t numb_images;
  int32_t counter_error;
} pm_vision_interfaces__msg__CrossValidation;

// Struct for a sequence of pm_vision_interfaces__msg__CrossValidation.
typedef struct pm_vision_interfaces__msg__CrossValidation__Sequence
{
  pm_vision_interfaces__msg__CrossValidation * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} pm_vision_interfaces__msg__CrossValidation__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // PM_VISION_INTERFACES__MSG__DETAIL__CROSS_VALIDATION__STRUCT_H_

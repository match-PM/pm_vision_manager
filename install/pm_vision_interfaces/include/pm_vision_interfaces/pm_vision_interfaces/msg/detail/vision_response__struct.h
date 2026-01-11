// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from pm_vision_interfaces:msg/VisionResponse.idl
// generated code does not contain a copyright notice

#ifndef PM_VISION_INTERFACES__MSG__DETAIL__VISION_RESPONSE__STRUCT_H_
#define PM_VISION_INTERFACES__MSG__DETAIL__VISION_RESPONSE__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'process_name'
// Member 'process_uid'
// Member 'exec_timestamp'
#include "rosidl_runtime_c/string.h"
// Member 'cross_validation'
#include "pm_vision_interfaces/msg/detail/cross_validation__struct.h"
// Member 'results'
#include "pm_vision_interfaces/msg/detail/vision_results__struct.h"

/// Struct defined in msg/VisionResponse in the package pm_vision_interfaces.
typedef struct pm_vision_interfaces__msg__VisionResponse
{
  bool vision_ok;
  rosidl_runtime_c__String process_name;
  rosidl_runtime_c__String process_uid;
  rosidl_runtime_c__String exec_timestamp;
  pm_vision_interfaces__msg__CrossValidation cross_validation;
  pm_vision_interfaces__msg__VisionResults results;
} pm_vision_interfaces__msg__VisionResponse;

// Struct for a sequence of pm_vision_interfaces__msg__VisionResponse.
typedef struct pm_vision_interfaces__msg__VisionResponse__Sequence
{
  pm_vision_interfaces__msg__VisionResponse * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} pm_vision_interfaces__msg__VisionResponse__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // PM_VISION_INTERFACES__MSG__DETAIL__VISION_RESPONSE__STRUCT_H_

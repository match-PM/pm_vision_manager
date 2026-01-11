// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from pm_vision_interfaces:msg/VisionArea.idl
// generated code does not contain a copyright notice

#ifndef PM_VISION_INTERFACES__MSG__DETAIL__VISION_AREA__STRUCT_H_
#define PM_VISION_INTERFACES__MSG__DETAIL__VISION_AREA__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in msg/VisionArea in the package pm_vision_interfaces.
typedef struct pm_vision_interfaces__msg__VisionArea
{
  uint8_t structure_needs_at_least_one_member;
} pm_vision_interfaces__msg__VisionArea;

// Struct for a sequence of pm_vision_interfaces__msg__VisionArea.
typedef struct pm_vision_interfaces__msg__VisionArea__Sequence
{
  pm_vision_interfaces__msg__VisionArea * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} pm_vision_interfaces__msg__VisionArea__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // PM_VISION_INTERFACES__MSG__DETAIL__VISION_AREA__STRUCT_H_

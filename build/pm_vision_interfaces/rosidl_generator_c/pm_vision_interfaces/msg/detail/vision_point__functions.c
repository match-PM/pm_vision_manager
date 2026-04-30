// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from pm_vision_interfaces:msg/VisionPoint.idl
// generated code does not contain a copyright notice
#include "pm_vision_interfaces/msg/detail/vision_point__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `axis_suffix_1`
// Member `axis_suffix_2`
#include "rosidl_runtime_c/string_functions.h"

bool
pm_vision_interfaces__msg__VisionPoint__init(pm_vision_interfaces__msg__VisionPoint * msg)
{
  if (!msg) {
    return false;
  }
  // axis_value_1
  // axis_value_2
  // axis_suffix_1
  if (!rosidl_runtime_c__String__init(&msg->axis_suffix_1)) {
    pm_vision_interfaces__msg__VisionPoint__fini(msg);
    return false;
  }
  // axis_suffix_2
  if (!rosidl_runtime_c__String__init(&msg->axis_suffix_2)) {
    pm_vision_interfaces__msg__VisionPoint__fini(msg);
    return false;
  }
  return true;
}

void
pm_vision_interfaces__msg__VisionPoint__fini(pm_vision_interfaces__msg__VisionPoint * msg)
{
  if (!msg) {
    return;
  }
  // axis_value_1
  // axis_value_2
  // axis_suffix_1
  rosidl_runtime_c__String__fini(&msg->axis_suffix_1);
  // axis_suffix_2
  rosidl_runtime_c__String__fini(&msg->axis_suffix_2);
}

bool
pm_vision_interfaces__msg__VisionPoint__are_equal(const pm_vision_interfaces__msg__VisionPoint * lhs, const pm_vision_interfaces__msg__VisionPoint * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // axis_value_1
  if (lhs->axis_value_1 != rhs->axis_value_1) {
    return false;
  }
  // axis_value_2
  if (lhs->axis_value_2 != rhs->axis_value_2) {
    return false;
  }
  // axis_suffix_1
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->axis_suffix_1), &(rhs->axis_suffix_1)))
  {
    return false;
  }
  // axis_suffix_2
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->axis_suffix_2), &(rhs->axis_suffix_2)))
  {
    return false;
  }
  return true;
}

bool
pm_vision_interfaces__msg__VisionPoint__copy(
  const pm_vision_interfaces__msg__VisionPoint * input,
  pm_vision_interfaces__msg__VisionPoint * output)
{
  if (!input || !output) {
    return false;
  }
  // axis_value_1
  output->axis_value_1 = input->axis_value_1;
  // axis_value_2
  output->axis_value_2 = input->axis_value_2;
  // axis_suffix_1
  if (!rosidl_runtime_c__String__copy(
      &(input->axis_suffix_1), &(output->axis_suffix_1)))
  {
    return false;
  }
  // axis_suffix_2
  if (!rosidl_runtime_c__String__copy(
      &(input->axis_suffix_2), &(output->axis_suffix_2)))
  {
    return false;
  }
  return true;
}

pm_vision_interfaces__msg__VisionPoint *
pm_vision_interfaces__msg__VisionPoint__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  pm_vision_interfaces__msg__VisionPoint * msg = (pm_vision_interfaces__msg__VisionPoint *)allocator.allocate(sizeof(pm_vision_interfaces__msg__VisionPoint), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(pm_vision_interfaces__msg__VisionPoint));
  bool success = pm_vision_interfaces__msg__VisionPoint__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
pm_vision_interfaces__msg__VisionPoint__destroy(pm_vision_interfaces__msg__VisionPoint * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    pm_vision_interfaces__msg__VisionPoint__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
pm_vision_interfaces__msg__VisionPoint__Sequence__init(pm_vision_interfaces__msg__VisionPoint__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  pm_vision_interfaces__msg__VisionPoint * data = NULL;

  if (size) {
    data = (pm_vision_interfaces__msg__VisionPoint *)allocator.zero_allocate(size, sizeof(pm_vision_interfaces__msg__VisionPoint), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = pm_vision_interfaces__msg__VisionPoint__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        pm_vision_interfaces__msg__VisionPoint__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
pm_vision_interfaces__msg__VisionPoint__Sequence__fini(pm_vision_interfaces__msg__VisionPoint__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      pm_vision_interfaces__msg__VisionPoint__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

pm_vision_interfaces__msg__VisionPoint__Sequence *
pm_vision_interfaces__msg__VisionPoint__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  pm_vision_interfaces__msg__VisionPoint__Sequence * array = (pm_vision_interfaces__msg__VisionPoint__Sequence *)allocator.allocate(sizeof(pm_vision_interfaces__msg__VisionPoint__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = pm_vision_interfaces__msg__VisionPoint__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
pm_vision_interfaces__msg__VisionPoint__Sequence__destroy(pm_vision_interfaces__msg__VisionPoint__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    pm_vision_interfaces__msg__VisionPoint__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
pm_vision_interfaces__msg__VisionPoint__Sequence__are_equal(const pm_vision_interfaces__msg__VisionPoint__Sequence * lhs, const pm_vision_interfaces__msg__VisionPoint__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!pm_vision_interfaces__msg__VisionPoint__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
pm_vision_interfaces__msg__VisionPoint__Sequence__copy(
  const pm_vision_interfaces__msg__VisionPoint__Sequence * input,
  pm_vision_interfaces__msg__VisionPoint__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(pm_vision_interfaces__msg__VisionPoint);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    pm_vision_interfaces__msg__VisionPoint * data =
      (pm_vision_interfaces__msg__VisionPoint *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!pm_vision_interfaces__msg__VisionPoint__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          pm_vision_interfaces__msg__VisionPoint__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!pm_vision_interfaces__msg__VisionPoint__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}

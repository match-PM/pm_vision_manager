// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from pm_vision_interfaces:msg/VisionResults.idl
// generated code does not contain a copyright notice
#include "pm_vision_interfaces/msg/detail/vision_results__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `points`
#include "pm_vision_interfaces/msg/detail/vision_point__functions.h"
// Member `lines`
#include "pm_vision_interfaces/msg/detail/vision_line__functions.h"
// Member `areas`
#include "pm_vision_interfaces/msg/detail/vision_area__functions.h"
// Member `circles`
#include "pm_vision_interfaces/msg/detail/vision_circle__functions.h"
// Member `image_sharpness`
#include "pm_vision_interfaces/msg/detail/image_sharpness__functions.h"

bool
pm_vision_interfaces__msg__VisionResults__init(pm_vision_interfaces__msg__VisionResults * msg)
{
  if (!msg) {
    return false;
  }
  // points
  if (!pm_vision_interfaces__msg__VisionPoint__Sequence__init(&msg->points, 0)) {
    pm_vision_interfaces__msg__VisionResults__fini(msg);
    return false;
  }
  // lines
  if (!pm_vision_interfaces__msg__VisionLine__Sequence__init(&msg->lines, 0)) {
    pm_vision_interfaces__msg__VisionResults__fini(msg);
    return false;
  }
  // areas
  if (!pm_vision_interfaces__msg__VisionArea__Sequence__init(&msg->areas, 0)) {
    pm_vision_interfaces__msg__VisionResults__fini(msg);
    return false;
  }
  // circles
  if (!pm_vision_interfaces__msg__VisionCircle__Sequence__init(&msg->circles, 0)) {
    pm_vision_interfaces__msg__VisionResults__fini(msg);
    return false;
  }
  // image_sharpness
  if (!pm_vision_interfaces__msg__ImageSharpness__init(&msg->image_sharpness)) {
    pm_vision_interfaces__msg__VisionResults__fini(msg);
    return false;
  }
  return true;
}

void
pm_vision_interfaces__msg__VisionResults__fini(pm_vision_interfaces__msg__VisionResults * msg)
{
  if (!msg) {
    return;
  }
  // points
  pm_vision_interfaces__msg__VisionPoint__Sequence__fini(&msg->points);
  // lines
  pm_vision_interfaces__msg__VisionLine__Sequence__fini(&msg->lines);
  // areas
  pm_vision_interfaces__msg__VisionArea__Sequence__fini(&msg->areas);
  // circles
  pm_vision_interfaces__msg__VisionCircle__Sequence__fini(&msg->circles);
  // image_sharpness
  pm_vision_interfaces__msg__ImageSharpness__fini(&msg->image_sharpness);
}

bool
pm_vision_interfaces__msg__VisionResults__are_equal(const pm_vision_interfaces__msg__VisionResults * lhs, const pm_vision_interfaces__msg__VisionResults * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // points
  if (!pm_vision_interfaces__msg__VisionPoint__Sequence__are_equal(
      &(lhs->points), &(rhs->points)))
  {
    return false;
  }
  // lines
  if (!pm_vision_interfaces__msg__VisionLine__Sequence__are_equal(
      &(lhs->lines), &(rhs->lines)))
  {
    return false;
  }
  // areas
  if (!pm_vision_interfaces__msg__VisionArea__Sequence__are_equal(
      &(lhs->areas), &(rhs->areas)))
  {
    return false;
  }
  // circles
  if (!pm_vision_interfaces__msg__VisionCircle__Sequence__are_equal(
      &(lhs->circles), &(rhs->circles)))
  {
    return false;
  }
  // image_sharpness
  if (!pm_vision_interfaces__msg__ImageSharpness__are_equal(
      &(lhs->image_sharpness), &(rhs->image_sharpness)))
  {
    return false;
  }
  return true;
}

bool
pm_vision_interfaces__msg__VisionResults__copy(
  const pm_vision_interfaces__msg__VisionResults * input,
  pm_vision_interfaces__msg__VisionResults * output)
{
  if (!input || !output) {
    return false;
  }
  // points
  if (!pm_vision_interfaces__msg__VisionPoint__Sequence__copy(
      &(input->points), &(output->points)))
  {
    return false;
  }
  // lines
  if (!pm_vision_interfaces__msg__VisionLine__Sequence__copy(
      &(input->lines), &(output->lines)))
  {
    return false;
  }
  // areas
  if (!pm_vision_interfaces__msg__VisionArea__Sequence__copy(
      &(input->areas), &(output->areas)))
  {
    return false;
  }
  // circles
  if (!pm_vision_interfaces__msg__VisionCircle__Sequence__copy(
      &(input->circles), &(output->circles)))
  {
    return false;
  }
  // image_sharpness
  if (!pm_vision_interfaces__msg__ImageSharpness__copy(
      &(input->image_sharpness), &(output->image_sharpness)))
  {
    return false;
  }
  return true;
}

pm_vision_interfaces__msg__VisionResults *
pm_vision_interfaces__msg__VisionResults__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  pm_vision_interfaces__msg__VisionResults * msg = (pm_vision_interfaces__msg__VisionResults *)allocator.allocate(sizeof(pm_vision_interfaces__msg__VisionResults), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(pm_vision_interfaces__msg__VisionResults));
  bool success = pm_vision_interfaces__msg__VisionResults__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
pm_vision_interfaces__msg__VisionResults__destroy(pm_vision_interfaces__msg__VisionResults * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    pm_vision_interfaces__msg__VisionResults__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
pm_vision_interfaces__msg__VisionResults__Sequence__init(pm_vision_interfaces__msg__VisionResults__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  pm_vision_interfaces__msg__VisionResults * data = NULL;

  if (size) {
    data = (pm_vision_interfaces__msg__VisionResults *)allocator.zero_allocate(size, sizeof(pm_vision_interfaces__msg__VisionResults), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = pm_vision_interfaces__msg__VisionResults__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        pm_vision_interfaces__msg__VisionResults__fini(&data[i - 1]);
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
pm_vision_interfaces__msg__VisionResults__Sequence__fini(pm_vision_interfaces__msg__VisionResults__Sequence * array)
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
      pm_vision_interfaces__msg__VisionResults__fini(&array->data[i]);
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

pm_vision_interfaces__msg__VisionResults__Sequence *
pm_vision_interfaces__msg__VisionResults__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  pm_vision_interfaces__msg__VisionResults__Sequence * array = (pm_vision_interfaces__msg__VisionResults__Sequence *)allocator.allocate(sizeof(pm_vision_interfaces__msg__VisionResults__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = pm_vision_interfaces__msg__VisionResults__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
pm_vision_interfaces__msg__VisionResults__Sequence__destroy(pm_vision_interfaces__msg__VisionResults__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    pm_vision_interfaces__msg__VisionResults__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
pm_vision_interfaces__msg__VisionResults__Sequence__are_equal(const pm_vision_interfaces__msg__VisionResults__Sequence * lhs, const pm_vision_interfaces__msg__VisionResults__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!pm_vision_interfaces__msg__VisionResults__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
pm_vision_interfaces__msg__VisionResults__Sequence__copy(
  const pm_vision_interfaces__msg__VisionResults__Sequence * input,
  pm_vision_interfaces__msg__VisionResults__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(pm_vision_interfaces__msg__VisionResults);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    pm_vision_interfaces__msg__VisionResults * data =
      (pm_vision_interfaces__msg__VisionResults *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!pm_vision_interfaces__msg__VisionResults__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          pm_vision_interfaces__msg__VisionResults__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!pm_vision_interfaces__msg__VisionResults__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}

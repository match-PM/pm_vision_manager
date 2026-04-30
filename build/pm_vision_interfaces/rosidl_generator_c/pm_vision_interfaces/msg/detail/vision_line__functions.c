// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from pm_vision_interfaces:msg/VisionLine.idl
// generated code does not contain a copyright notice
#include "pm_vision_interfaces/msg/detail/vision_line__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `point_1`
// Member `point_2`
// Member `point_mid`
#include "pm_vision_interfaces/msg/detail/vision_point__functions.h"

bool
pm_vision_interfaces__msg__VisionLine__init(pm_vision_interfaces__msg__VisionLine * msg)
{
  if (!msg) {
    return false;
  }
  // point_1
  if (!pm_vision_interfaces__msg__VisionPoint__init(&msg->point_1)) {
    pm_vision_interfaces__msg__VisionLine__fini(msg);
    return false;
  }
  // point_2
  if (!pm_vision_interfaces__msg__VisionPoint__init(&msg->point_2)) {
    pm_vision_interfaces__msg__VisionLine__fini(msg);
    return false;
  }
  // point_mid
  if (!pm_vision_interfaces__msg__VisionPoint__init(&msg->point_mid)) {
    pm_vision_interfaces__msg__VisionLine__fini(msg);
    return false;
  }
  // angle
  // length
  return true;
}

void
pm_vision_interfaces__msg__VisionLine__fini(pm_vision_interfaces__msg__VisionLine * msg)
{
  if (!msg) {
    return;
  }
  // point_1
  pm_vision_interfaces__msg__VisionPoint__fini(&msg->point_1);
  // point_2
  pm_vision_interfaces__msg__VisionPoint__fini(&msg->point_2);
  // point_mid
  pm_vision_interfaces__msg__VisionPoint__fini(&msg->point_mid);
  // angle
  // length
}

bool
pm_vision_interfaces__msg__VisionLine__are_equal(const pm_vision_interfaces__msg__VisionLine * lhs, const pm_vision_interfaces__msg__VisionLine * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // point_1
  if (!pm_vision_interfaces__msg__VisionPoint__are_equal(
      &(lhs->point_1), &(rhs->point_1)))
  {
    return false;
  }
  // point_2
  if (!pm_vision_interfaces__msg__VisionPoint__are_equal(
      &(lhs->point_2), &(rhs->point_2)))
  {
    return false;
  }
  // point_mid
  if (!pm_vision_interfaces__msg__VisionPoint__are_equal(
      &(lhs->point_mid), &(rhs->point_mid)))
  {
    return false;
  }
  // angle
  if (lhs->angle != rhs->angle) {
    return false;
  }
  // length
  if (lhs->length != rhs->length) {
    return false;
  }
  return true;
}

bool
pm_vision_interfaces__msg__VisionLine__copy(
  const pm_vision_interfaces__msg__VisionLine * input,
  pm_vision_interfaces__msg__VisionLine * output)
{
  if (!input || !output) {
    return false;
  }
  // point_1
  if (!pm_vision_interfaces__msg__VisionPoint__copy(
      &(input->point_1), &(output->point_1)))
  {
    return false;
  }
  // point_2
  if (!pm_vision_interfaces__msg__VisionPoint__copy(
      &(input->point_2), &(output->point_2)))
  {
    return false;
  }
  // point_mid
  if (!pm_vision_interfaces__msg__VisionPoint__copy(
      &(input->point_mid), &(output->point_mid)))
  {
    return false;
  }
  // angle
  output->angle = input->angle;
  // length
  output->length = input->length;
  return true;
}

pm_vision_interfaces__msg__VisionLine *
pm_vision_interfaces__msg__VisionLine__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  pm_vision_interfaces__msg__VisionLine * msg = (pm_vision_interfaces__msg__VisionLine *)allocator.allocate(sizeof(pm_vision_interfaces__msg__VisionLine), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(pm_vision_interfaces__msg__VisionLine));
  bool success = pm_vision_interfaces__msg__VisionLine__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
pm_vision_interfaces__msg__VisionLine__destroy(pm_vision_interfaces__msg__VisionLine * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    pm_vision_interfaces__msg__VisionLine__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
pm_vision_interfaces__msg__VisionLine__Sequence__init(pm_vision_interfaces__msg__VisionLine__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  pm_vision_interfaces__msg__VisionLine * data = NULL;

  if (size) {
    data = (pm_vision_interfaces__msg__VisionLine *)allocator.zero_allocate(size, sizeof(pm_vision_interfaces__msg__VisionLine), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = pm_vision_interfaces__msg__VisionLine__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        pm_vision_interfaces__msg__VisionLine__fini(&data[i - 1]);
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
pm_vision_interfaces__msg__VisionLine__Sequence__fini(pm_vision_interfaces__msg__VisionLine__Sequence * array)
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
      pm_vision_interfaces__msg__VisionLine__fini(&array->data[i]);
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

pm_vision_interfaces__msg__VisionLine__Sequence *
pm_vision_interfaces__msg__VisionLine__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  pm_vision_interfaces__msg__VisionLine__Sequence * array = (pm_vision_interfaces__msg__VisionLine__Sequence *)allocator.allocate(sizeof(pm_vision_interfaces__msg__VisionLine__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = pm_vision_interfaces__msg__VisionLine__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
pm_vision_interfaces__msg__VisionLine__Sequence__destroy(pm_vision_interfaces__msg__VisionLine__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    pm_vision_interfaces__msg__VisionLine__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
pm_vision_interfaces__msg__VisionLine__Sequence__are_equal(const pm_vision_interfaces__msg__VisionLine__Sequence * lhs, const pm_vision_interfaces__msg__VisionLine__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!pm_vision_interfaces__msg__VisionLine__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
pm_vision_interfaces__msg__VisionLine__Sequence__copy(
  const pm_vision_interfaces__msg__VisionLine__Sequence * input,
  pm_vision_interfaces__msg__VisionLine__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(pm_vision_interfaces__msg__VisionLine);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    pm_vision_interfaces__msg__VisionLine * data =
      (pm_vision_interfaces__msg__VisionLine *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!pm_vision_interfaces__msg__VisionLine__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          pm_vision_interfaces__msg__VisionLine__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!pm_vision_interfaces__msg__VisionLine__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}

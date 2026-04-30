// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from pm_vision_interfaces:msg/VisionResponse.idl
// generated code does not contain a copyright notice
#include "pm_vision_interfaces/msg/detail/vision_response__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `process_name`
// Member `process_uid`
// Member `exec_timestamp`
#include "rosidl_runtime_c/string_functions.h"
// Member `cross_validation`
#include "pm_vision_interfaces/msg/detail/cross_validation__functions.h"
// Member `results`
#include "pm_vision_interfaces/msg/detail/vision_results__functions.h"

bool
pm_vision_interfaces__msg__VisionResponse__init(pm_vision_interfaces__msg__VisionResponse * msg)
{
  if (!msg) {
    return false;
  }
  // vision_ok
  // process_name
  if (!rosidl_runtime_c__String__init(&msg->process_name)) {
    pm_vision_interfaces__msg__VisionResponse__fini(msg);
    return false;
  }
  // process_uid
  if (!rosidl_runtime_c__String__init(&msg->process_uid)) {
    pm_vision_interfaces__msg__VisionResponse__fini(msg);
    return false;
  }
  // exec_timestamp
  if (!rosidl_runtime_c__String__init(&msg->exec_timestamp)) {
    pm_vision_interfaces__msg__VisionResponse__fini(msg);
    return false;
  }
  // cross_validation
  if (!pm_vision_interfaces__msg__CrossValidation__init(&msg->cross_validation)) {
    pm_vision_interfaces__msg__VisionResponse__fini(msg);
    return false;
  }
  // results
  if (!pm_vision_interfaces__msg__VisionResults__init(&msg->results)) {
    pm_vision_interfaces__msg__VisionResponse__fini(msg);
    return false;
  }
  return true;
}

void
pm_vision_interfaces__msg__VisionResponse__fini(pm_vision_interfaces__msg__VisionResponse * msg)
{
  if (!msg) {
    return;
  }
  // vision_ok
  // process_name
  rosidl_runtime_c__String__fini(&msg->process_name);
  // process_uid
  rosidl_runtime_c__String__fini(&msg->process_uid);
  // exec_timestamp
  rosidl_runtime_c__String__fini(&msg->exec_timestamp);
  // cross_validation
  pm_vision_interfaces__msg__CrossValidation__fini(&msg->cross_validation);
  // results
  pm_vision_interfaces__msg__VisionResults__fini(&msg->results);
}

bool
pm_vision_interfaces__msg__VisionResponse__are_equal(const pm_vision_interfaces__msg__VisionResponse * lhs, const pm_vision_interfaces__msg__VisionResponse * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // vision_ok
  if (lhs->vision_ok != rhs->vision_ok) {
    return false;
  }
  // process_name
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->process_name), &(rhs->process_name)))
  {
    return false;
  }
  // process_uid
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->process_uid), &(rhs->process_uid)))
  {
    return false;
  }
  // exec_timestamp
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->exec_timestamp), &(rhs->exec_timestamp)))
  {
    return false;
  }
  // cross_validation
  if (!pm_vision_interfaces__msg__CrossValidation__are_equal(
      &(lhs->cross_validation), &(rhs->cross_validation)))
  {
    return false;
  }
  // results
  if (!pm_vision_interfaces__msg__VisionResults__are_equal(
      &(lhs->results), &(rhs->results)))
  {
    return false;
  }
  return true;
}

bool
pm_vision_interfaces__msg__VisionResponse__copy(
  const pm_vision_interfaces__msg__VisionResponse * input,
  pm_vision_interfaces__msg__VisionResponse * output)
{
  if (!input || !output) {
    return false;
  }
  // vision_ok
  output->vision_ok = input->vision_ok;
  // process_name
  if (!rosidl_runtime_c__String__copy(
      &(input->process_name), &(output->process_name)))
  {
    return false;
  }
  // process_uid
  if (!rosidl_runtime_c__String__copy(
      &(input->process_uid), &(output->process_uid)))
  {
    return false;
  }
  // exec_timestamp
  if (!rosidl_runtime_c__String__copy(
      &(input->exec_timestamp), &(output->exec_timestamp)))
  {
    return false;
  }
  // cross_validation
  if (!pm_vision_interfaces__msg__CrossValidation__copy(
      &(input->cross_validation), &(output->cross_validation)))
  {
    return false;
  }
  // results
  if (!pm_vision_interfaces__msg__VisionResults__copy(
      &(input->results), &(output->results)))
  {
    return false;
  }
  return true;
}

pm_vision_interfaces__msg__VisionResponse *
pm_vision_interfaces__msg__VisionResponse__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  pm_vision_interfaces__msg__VisionResponse * msg = (pm_vision_interfaces__msg__VisionResponse *)allocator.allocate(sizeof(pm_vision_interfaces__msg__VisionResponse), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(pm_vision_interfaces__msg__VisionResponse));
  bool success = pm_vision_interfaces__msg__VisionResponse__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
pm_vision_interfaces__msg__VisionResponse__destroy(pm_vision_interfaces__msg__VisionResponse * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    pm_vision_interfaces__msg__VisionResponse__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
pm_vision_interfaces__msg__VisionResponse__Sequence__init(pm_vision_interfaces__msg__VisionResponse__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  pm_vision_interfaces__msg__VisionResponse * data = NULL;

  if (size) {
    data = (pm_vision_interfaces__msg__VisionResponse *)allocator.zero_allocate(size, sizeof(pm_vision_interfaces__msg__VisionResponse), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = pm_vision_interfaces__msg__VisionResponse__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        pm_vision_interfaces__msg__VisionResponse__fini(&data[i - 1]);
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
pm_vision_interfaces__msg__VisionResponse__Sequence__fini(pm_vision_interfaces__msg__VisionResponse__Sequence * array)
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
      pm_vision_interfaces__msg__VisionResponse__fini(&array->data[i]);
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

pm_vision_interfaces__msg__VisionResponse__Sequence *
pm_vision_interfaces__msg__VisionResponse__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  pm_vision_interfaces__msg__VisionResponse__Sequence * array = (pm_vision_interfaces__msg__VisionResponse__Sequence *)allocator.allocate(sizeof(pm_vision_interfaces__msg__VisionResponse__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = pm_vision_interfaces__msg__VisionResponse__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
pm_vision_interfaces__msg__VisionResponse__Sequence__destroy(pm_vision_interfaces__msg__VisionResponse__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    pm_vision_interfaces__msg__VisionResponse__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
pm_vision_interfaces__msg__VisionResponse__Sequence__are_equal(const pm_vision_interfaces__msg__VisionResponse__Sequence * lhs, const pm_vision_interfaces__msg__VisionResponse__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!pm_vision_interfaces__msg__VisionResponse__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
pm_vision_interfaces__msg__VisionResponse__Sequence__copy(
  const pm_vision_interfaces__msg__VisionResponse__Sequence * input,
  pm_vision_interfaces__msg__VisionResponse__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(pm_vision_interfaces__msg__VisionResponse);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    pm_vision_interfaces__msg__VisionResponse * data =
      (pm_vision_interfaces__msg__VisionResponse *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!pm_vision_interfaces__msg__VisionResponse__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          pm_vision_interfaces__msg__VisionResponse__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!pm_vision_interfaces__msg__VisionResponse__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}

// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from pm_vision_interfaces:msg/CrossValidation.idl
// generated code does not contain a copyright notice
#include "pm_vision_interfaces/msg/detail/cross_validation__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `image_source_name`
// Member `failed_images`
#include "rosidl_runtime_c/string_functions.h"

bool
pm_vision_interfaces__msg__CrossValidation__init(pm_vision_interfaces__msg__CrossValidation * msg)
{
  if (!msg) {
    return false;
  }
  // image_source_name
  if (!rosidl_runtime_c__String__init(&msg->image_source_name)) {
    pm_vision_interfaces__msg__CrossValidation__fini(msg);
    return false;
  }
  // vision_ok
  // failed_images
  if (!rosidl_runtime_c__String__Sequence__init(&msg->failed_images, 0)) {
    pm_vision_interfaces__msg__CrossValidation__fini(msg);
    return false;
  }
  // numb_images
  // counter_error
  return true;
}

void
pm_vision_interfaces__msg__CrossValidation__fini(pm_vision_interfaces__msg__CrossValidation * msg)
{
  if (!msg) {
    return;
  }
  // image_source_name
  rosidl_runtime_c__String__fini(&msg->image_source_name);
  // vision_ok
  // failed_images
  rosidl_runtime_c__String__Sequence__fini(&msg->failed_images);
  // numb_images
  // counter_error
}

bool
pm_vision_interfaces__msg__CrossValidation__are_equal(const pm_vision_interfaces__msg__CrossValidation * lhs, const pm_vision_interfaces__msg__CrossValidation * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // image_source_name
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->image_source_name), &(rhs->image_source_name)))
  {
    return false;
  }
  // vision_ok
  if (lhs->vision_ok != rhs->vision_ok) {
    return false;
  }
  // failed_images
  if (!rosidl_runtime_c__String__Sequence__are_equal(
      &(lhs->failed_images), &(rhs->failed_images)))
  {
    return false;
  }
  // numb_images
  if (lhs->numb_images != rhs->numb_images) {
    return false;
  }
  // counter_error
  if (lhs->counter_error != rhs->counter_error) {
    return false;
  }
  return true;
}

bool
pm_vision_interfaces__msg__CrossValidation__copy(
  const pm_vision_interfaces__msg__CrossValidation * input,
  pm_vision_interfaces__msg__CrossValidation * output)
{
  if (!input || !output) {
    return false;
  }
  // image_source_name
  if (!rosidl_runtime_c__String__copy(
      &(input->image_source_name), &(output->image_source_name)))
  {
    return false;
  }
  // vision_ok
  output->vision_ok = input->vision_ok;
  // failed_images
  if (!rosidl_runtime_c__String__Sequence__copy(
      &(input->failed_images), &(output->failed_images)))
  {
    return false;
  }
  // numb_images
  output->numb_images = input->numb_images;
  // counter_error
  output->counter_error = input->counter_error;
  return true;
}

pm_vision_interfaces__msg__CrossValidation *
pm_vision_interfaces__msg__CrossValidation__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  pm_vision_interfaces__msg__CrossValidation * msg = (pm_vision_interfaces__msg__CrossValidation *)allocator.allocate(sizeof(pm_vision_interfaces__msg__CrossValidation), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(pm_vision_interfaces__msg__CrossValidation));
  bool success = pm_vision_interfaces__msg__CrossValidation__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
pm_vision_interfaces__msg__CrossValidation__destroy(pm_vision_interfaces__msg__CrossValidation * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    pm_vision_interfaces__msg__CrossValidation__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
pm_vision_interfaces__msg__CrossValidation__Sequence__init(pm_vision_interfaces__msg__CrossValidation__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  pm_vision_interfaces__msg__CrossValidation * data = NULL;

  if (size) {
    data = (pm_vision_interfaces__msg__CrossValidation *)allocator.zero_allocate(size, sizeof(pm_vision_interfaces__msg__CrossValidation), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = pm_vision_interfaces__msg__CrossValidation__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        pm_vision_interfaces__msg__CrossValidation__fini(&data[i - 1]);
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
pm_vision_interfaces__msg__CrossValidation__Sequence__fini(pm_vision_interfaces__msg__CrossValidation__Sequence * array)
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
      pm_vision_interfaces__msg__CrossValidation__fini(&array->data[i]);
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

pm_vision_interfaces__msg__CrossValidation__Sequence *
pm_vision_interfaces__msg__CrossValidation__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  pm_vision_interfaces__msg__CrossValidation__Sequence * array = (pm_vision_interfaces__msg__CrossValidation__Sequence *)allocator.allocate(sizeof(pm_vision_interfaces__msg__CrossValidation__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = pm_vision_interfaces__msg__CrossValidation__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
pm_vision_interfaces__msg__CrossValidation__Sequence__destroy(pm_vision_interfaces__msg__CrossValidation__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    pm_vision_interfaces__msg__CrossValidation__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
pm_vision_interfaces__msg__CrossValidation__Sequence__are_equal(const pm_vision_interfaces__msg__CrossValidation__Sequence * lhs, const pm_vision_interfaces__msg__CrossValidation__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!pm_vision_interfaces__msg__CrossValidation__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
pm_vision_interfaces__msg__CrossValidation__Sequence__copy(
  const pm_vision_interfaces__msg__CrossValidation__Sequence * input,
  pm_vision_interfaces__msg__CrossValidation__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(pm_vision_interfaces__msg__CrossValidation);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    pm_vision_interfaces__msg__CrossValidation * data =
      (pm_vision_interfaces__msg__CrossValidation *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!pm_vision_interfaces__msg__CrossValidation__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          pm_vision_interfaces__msg__CrossValidation__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!pm_vision_interfaces__msg__CrossValidation__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}

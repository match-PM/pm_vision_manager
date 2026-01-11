// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from pm_vision_interfaces:srv/CalibratePixelPerUm.idl
// generated code does not contain a copyright notice
#include "pm_vision_interfaces/srv/detail/calibrate_pixel_per_um__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"

// Include directives for member types
// Member `camera_config_file_name`
#include "rosidl_runtime_c/string_functions.h"

bool
pm_vision_interfaces__srv__CalibratePixelPerUm_Request__init(pm_vision_interfaces__srv__CalibratePixelPerUm_Request * msg)
{
  if (!msg) {
    return false;
  }
  // multiplicator
  // camera_config_file_name
  if (!rosidl_runtime_c__String__init(&msg->camera_config_file_name)) {
    pm_vision_interfaces__srv__CalibratePixelPerUm_Request__fini(msg);
    return false;
  }
  return true;
}

void
pm_vision_interfaces__srv__CalibratePixelPerUm_Request__fini(pm_vision_interfaces__srv__CalibratePixelPerUm_Request * msg)
{
  if (!msg) {
    return;
  }
  // multiplicator
  // camera_config_file_name
  rosidl_runtime_c__String__fini(&msg->camera_config_file_name);
}

bool
pm_vision_interfaces__srv__CalibratePixelPerUm_Request__are_equal(const pm_vision_interfaces__srv__CalibratePixelPerUm_Request * lhs, const pm_vision_interfaces__srv__CalibratePixelPerUm_Request * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // multiplicator
  if (lhs->multiplicator != rhs->multiplicator) {
    return false;
  }
  // camera_config_file_name
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->camera_config_file_name), &(rhs->camera_config_file_name)))
  {
    return false;
  }
  return true;
}

bool
pm_vision_interfaces__srv__CalibratePixelPerUm_Request__copy(
  const pm_vision_interfaces__srv__CalibratePixelPerUm_Request * input,
  pm_vision_interfaces__srv__CalibratePixelPerUm_Request * output)
{
  if (!input || !output) {
    return false;
  }
  // multiplicator
  output->multiplicator = input->multiplicator;
  // camera_config_file_name
  if (!rosidl_runtime_c__String__copy(
      &(input->camera_config_file_name), &(output->camera_config_file_name)))
  {
    return false;
  }
  return true;
}

pm_vision_interfaces__srv__CalibratePixelPerUm_Request *
pm_vision_interfaces__srv__CalibratePixelPerUm_Request__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  pm_vision_interfaces__srv__CalibratePixelPerUm_Request * msg = (pm_vision_interfaces__srv__CalibratePixelPerUm_Request *)allocator.allocate(sizeof(pm_vision_interfaces__srv__CalibratePixelPerUm_Request), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(pm_vision_interfaces__srv__CalibratePixelPerUm_Request));
  bool success = pm_vision_interfaces__srv__CalibratePixelPerUm_Request__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
pm_vision_interfaces__srv__CalibratePixelPerUm_Request__destroy(pm_vision_interfaces__srv__CalibratePixelPerUm_Request * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    pm_vision_interfaces__srv__CalibratePixelPerUm_Request__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
pm_vision_interfaces__srv__CalibratePixelPerUm_Request__Sequence__init(pm_vision_interfaces__srv__CalibratePixelPerUm_Request__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  pm_vision_interfaces__srv__CalibratePixelPerUm_Request * data = NULL;

  if (size) {
    data = (pm_vision_interfaces__srv__CalibratePixelPerUm_Request *)allocator.zero_allocate(size, sizeof(pm_vision_interfaces__srv__CalibratePixelPerUm_Request), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = pm_vision_interfaces__srv__CalibratePixelPerUm_Request__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        pm_vision_interfaces__srv__CalibratePixelPerUm_Request__fini(&data[i - 1]);
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
pm_vision_interfaces__srv__CalibratePixelPerUm_Request__Sequence__fini(pm_vision_interfaces__srv__CalibratePixelPerUm_Request__Sequence * array)
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
      pm_vision_interfaces__srv__CalibratePixelPerUm_Request__fini(&array->data[i]);
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

pm_vision_interfaces__srv__CalibratePixelPerUm_Request__Sequence *
pm_vision_interfaces__srv__CalibratePixelPerUm_Request__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  pm_vision_interfaces__srv__CalibratePixelPerUm_Request__Sequence * array = (pm_vision_interfaces__srv__CalibratePixelPerUm_Request__Sequence *)allocator.allocate(sizeof(pm_vision_interfaces__srv__CalibratePixelPerUm_Request__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = pm_vision_interfaces__srv__CalibratePixelPerUm_Request__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
pm_vision_interfaces__srv__CalibratePixelPerUm_Request__Sequence__destroy(pm_vision_interfaces__srv__CalibratePixelPerUm_Request__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    pm_vision_interfaces__srv__CalibratePixelPerUm_Request__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
pm_vision_interfaces__srv__CalibratePixelPerUm_Request__Sequence__are_equal(const pm_vision_interfaces__srv__CalibratePixelPerUm_Request__Sequence * lhs, const pm_vision_interfaces__srv__CalibratePixelPerUm_Request__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!pm_vision_interfaces__srv__CalibratePixelPerUm_Request__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
pm_vision_interfaces__srv__CalibratePixelPerUm_Request__Sequence__copy(
  const pm_vision_interfaces__srv__CalibratePixelPerUm_Request__Sequence * input,
  pm_vision_interfaces__srv__CalibratePixelPerUm_Request__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(pm_vision_interfaces__srv__CalibratePixelPerUm_Request);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    pm_vision_interfaces__srv__CalibratePixelPerUm_Request * data =
      (pm_vision_interfaces__srv__CalibratePixelPerUm_Request *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!pm_vision_interfaces__srv__CalibratePixelPerUm_Request__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          pm_vision_interfaces__srv__CalibratePixelPerUm_Request__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!pm_vision_interfaces__srv__CalibratePixelPerUm_Request__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


bool
pm_vision_interfaces__srv__CalibratePixelPerUm_Response__init(pm_vision_interfaces__srv__CalibratePixelPerUm_Response * msg)
{
  if (!msg) {
    return false;
  }
  // success
  return true;
}

void
pm_vision_interfaces__srv__CalibratePixelPerUm_Response__fini(pm_vision_interfaces__srv__CalibratePixelPerUm_Response * msg)
{
  if (!msg) {
    return;
  }
  // success
}

bool
pm_vision_interfaces__srv__CalibratePixelPerUm_Response__are_equal(const pm_vision_interfaces__srv__CalibratePixelPerUm_Response * lhs, const pm_vision_interfaces__srv__CalibratePixelPerUm_Response * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // success
  if (lhs->success != rhs->success) {
    return false;
  }
  return true;
}

bool
pm_vision_interfaces__srv__CalibratePixelPerUm_Response__copy(
  const pm_vision_interfaces__srv__CalibratePixelPerUm_Response * input,
  pm_vision_interfaces__srv__CalibratePixelPerUm_Response * output)
{
  if (!input || !output) {
    return false;
  }
  // success
  output->success = input->success;
  return true;
}

pm_vision_interfaces__srv__CalibratePixelPerUm_Response *
pm_vision_interfaces__srv__CalibratePixelPerUm_Response__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  pm_vision_interfaces__srv__CalibratePixelPerUm_Response * msg = (pm_vision_interfaces__srv__CalibratePixelPerUm_Response *)allocator.allocate(sizeof(pm_vision_interfaces__srv__CalibratePixelPerUm_Response), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(pm_vision_interfaces__srv__CalibratePixelPerUm_Response));
  bool success = pm_vision_interfaces__srv__CalibratePixelPerUm_Response__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
pm_vision_interfaces__srv__CalibratePixelPerUm_Response__destroy(pm_vision_interfaces__srv__CalibratePixelPerUm_Response * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    pm_vision_interfaces__srv__CalibratePixelPerUm_Response__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
pm_vision_interfaces__srv__CalibratePixelPerUm_Response__Sequence__init(pm_vision_interfaces__srv__CalibratePixelPerUm_Response__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  pm_vision_interfaces__srv__CalibratePixelPerUm_Response * data = NULL;

  if (size) {
    data = (pm_vision_interfaces__srv__CalibratePixelPerUm_Response *)allocator.zero_allocate(size, sizeof(pm_vision_interfaces__srv__CalibratePixelPerUm_Response), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = pm_vision_interfaces__srv__CalibratePixelPerUm_Response__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        pm_vision_interfaces__srv__CalibratePixelPerUm_Response__fini(&data[i - 1]);
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
pm_vision_interfaces__srv__CalibratePixelPerUm_Response__Sequence__fini(pm_vision_interfaces__srv__CalibratePixelPerUm_Response__Sequence * array)
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
      pm_vision_interfaces__srv__CalibratePixelPerUm_Response__fini(&array->data[i]);
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

pm_vision_interfaces__srv__CalibratePixelPerUm_Response__Sequence *
pm_vision_interfaces__srv__CalibratePixelPerUm_Response__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  pm_vision_interfaces__srv__CalibratePixelPerUm_Response__Sequence * array = (pm_vision_interfaces__srv__CalibratePixelPerUm_Response__Sequence *)allocator.allocate(sizeof(pm_vision_interfaces__srv__CalibratePixelPerUm_Response__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = pm_vision_interfaces__srv__CalibratePixelPerUm_Response__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
pm_vision_interfaces__srv__CalibratePixelPerUm_Response__Sequence__destroy(pm_vision_interfaces__srv__CalibratePixelPerUm_Response__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    pm_vision_interfaces__srv__CalibratePixelPerUm_Response__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
pm_vision_interfaces__srv__CalibratePixelPerUm_Response__Sequence__are_equal(const pm_vision_interfaces__srv__CalibratePixelPerUm_Response__Sequence * lhs, const pm_vision_interfaces__srv__CalibratePixelPerUm_Response__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!pm_vision_interfaces__srv__CalibratePixelPerUm_Response__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
pm_vision_interfaces__srv__CalibratePixelPerUm_Response__Sequence__copy(
  const pm_vision_interfaces__srv__CalibratePixelPerUm_Response__Sequence * input,
  pm_vision_interfaces__srv__CalibratePixelPerUm_Response__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(pm_vision_interfaces__srv__CalibratePixelPerUm_Response);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    pm_vision_interfaces__srv__CalibratePixelPerUm_Response * data =
      (pm_vision_interfaces__srv__CalibratePixelPerUm_Response *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!pm_vision_interfaces__srv__CalibratePixelPerUm_Response__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          pm_vision_interfaces__srv__CalibratePixelPerUm_Response__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!pm_vision_interfaces__srv__CalibratePixelPerUm_Response__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}

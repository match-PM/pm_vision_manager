// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from pm_vision_interfaces:srv/ExecuteVision.idl
// generated code does not contain a copyright notice
#include "pm_vision_interfaces/srv/detail/execute_vision__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"

// Include directives for member types
// Member `process_filename`
// Member `camera_config_filename`
// Member `process_uid`
#include "rosidl_runtime_c/string_functions.h"

bool
pm_vision_interfaces__srv__ExecuteVision_Request__init(pm_vision_interfaces__srv__ExecuteVision_Request * msg)
{
  if (!msg) {
    return false;
  }
  // process_filename
  if (!rosidl_runtime_c__String__init(&msg->process_filename)) {
    pm_vision_interfaces__srv__ExecuteVision_Request__fini(msg);
    return false;
  }
  // camera_config_filename
  if (!rosidl_runtime_c__String__init(&msg->camera_config_filename)) {
    pm_vision_interfaces__srv__ExecuteVision_Request__fini(msg);
    return false;
  }
  // process_uid
  if (!rosidl_runtime_c__String__init(&msg->process_uid)) {
    pm_vision_interfaces__srv__ExecuteVision_Request__fini(msg);
    return false;
  }
  // image_display_time
  // run_cross_validation
  return true;
}

void
pm_vision_interfaces__srv__ExecuteVision_Request__fini(pm_vision_interfaces__srv__ExecuteVision_Request * msg)
{
  if (!msg) {
    return;
  }
  // process_filename
  rosidl_runtime_c__String__fini(&msg->process_filename);
  // camera_config_filename
  rosidl_runtime_c__String__fini(&msg->camera_config_filename);
  // process_uid
  rosidl_runtime_c__String__fini(&msg->process_uid);
  // image_display_time
  // run_cross_validation
}

bool
pm_vision_interfaces__srv__ExecuteVision_Request__are_equal(const pm_vision_interfaces__srv__ExecuteVision_Request * lhs, const pm_vision_interfaces__srv__ExecuteVision_Request * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // process_filename
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->process_filename), &(rhs->process_filename)))
  {
    return false;
  }
  // camera_config_filename
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->camera_config_filename), &(rhs->camera_config_filename)))
  {
    return false;
  }
  // process_uid
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->process_uid), &(rhs->process_uid)))
  {
    return false;
  }
  // image_display_time
  if (lhs->image_display_time != rhs->image_display_time) {
    return false;
  }
  // run_cross_validation
  if (lhs->run_cross_validation != rhs->run_cross_validation) {
    return false;
  }
  return true;
}

bool
pm_vision_interfaces__srv__ExecuteVision_Request__copy(
  const pm_vision_interfaces__srv__ExecuteVision_Request * input,
  pm_vision_interfaces__srv__ExecuteVision_Request * output)
{
  if (!input || !output) {
    return false;
  }
  // process_filename
  if (!rosidl_runtime_c__String__copy(
      &(input->process_filename), &(output->process_filename)))
  {
    return false;
  }
  // camera_config_filename
  if (!rosidl_runtime_c__String__copy(
      &(input->camera_config_filename), &(output->camera_config_filename)))
  {
    return false;
  }
  // process_uid
  if (!rosidl_runtime_c__String__copy(
      &(input->process_uid), &(output->process_uid)))
  {
    return false;
  }
  // image_display_time
  output->image_display_time = input->image_display_time;
  // run_cross_validation
  output->run_cross_validation = input->run_cross_validation;
  return true;
}

pm_vision_interfaces__srv__ExecuteVision_Request *
pm_vision_interfaces__srv__ExecuteVision_Request__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  pm_vision_interfaces__srv__ExecuteVision_Request * msg = (pm_vision_interfaces__srv__ExecuteVision_Request *)allocator.allocate(sizeof(pm_vision_interfaces__srv__ExecuteVision_Request), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(pm_vision_interfaces__srv__ExecuteVision_Request));
  bool success = pm_vision_interfaces__srv__ExecuteVision_Request__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
pm_vision_interfaces__srv__ExecuteVision_Request__destroy(pm_vision_interfaces__srv__ExecuteVision_Request * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    pm_vision_interfaces__srv__ExecuteVision_Request__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
pm_vision_interfaces__srv__ExecuteVision_Request__Sequence__init(pm_vision_interfaces__srv__ExecuteVision_Request__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  pm_vision_interfaces__srv__ExecuteVision_Request * data = NULL;

  if (size) {
    data = (pm_vision_interfaces__srv__ExecuteVision_Request *)allocator.zero_allocate(size, sizeof(pm_vision_interfaces__srv__ExecuteVision_Request), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = pm_vision_interfaces__srv__ExecuteVision_Request__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        pm_vision_interfaces__srv__ExecuteVision_Request__fini(&data[i - 1]);
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
pm_vision_interfaces__srv__ExecuteVision_Request__Sequence__fini(pm_vision_interfaces__srv__ExecuteVision_Request__Sequence * array)
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
      pm_vision_interfaces__srv__ExecuteVision_Request__fini(&array->data[i]);
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

pm_vision_interfaces__srv__ExecuteVision_Request__Sequence *
pm_vision_interfaces__srv__ExecuteVision_Request__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  pm_vision_interfaces__srv__ExecuteVision_Request__Sequence * array = (pm_vision_interfaces__srv__ExecuteVision_Request__Sequence *)allocator.allocate(sizeof(pm_vision_interfaces__srv__ExecuteVision_Request__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = pm_vision_interfaces__srv__ExecuteVision_Request__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
pm_vision_interfaces__srv__ExecuteVision_Request__Sequence__destroy(pm_vision_interfaces__srv__ExecuteVision_Request__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    pm_vision_interfaces__srv__ExecuteVision_Request__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
pm_vision_interfaces__srv__ExecuteVision_Request__Sequence__are_equal(const pm_vision_interfaces__srv__ExecuteVision_Request__Sequence * lhs, const pm_vision_interfaces__srv__ExecuteVision_Request__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!pm_vision_interfaces__srv__ExecuteVision_Request__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
pm_vision_interfaces__srv__ExecuteVision_Request__Sequence__copy(
  const pm_vision_interfaces__srv__ExecuteVision_Request__Sequence * input,
  pm_vision_interfaces__srv__ExecuteVision_Request__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(pm_vision_interfaces__srv__ExecuteVision_Request);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    pm_vision_interfaces__srv__ExecuteVision_Request * data =
      (pm_vision_interfaces__srv__ExecuteVision_Request *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!pm_vision_interfaces__srv__ExecuteVision_Request__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          pm_vision_interfaces__srv__ExecuteVision_Request__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!pm_vision_interfaces__srv__ExecuteVision_Request__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


// Include directives for member types
// Member `results_path`
// already included above
// #include "rosidl_runtime_c/string_functions.h"
// Member `vision_response`
#include "pm_vision_interfaces/msg/detail/vision_response__functions.h"

bool
pm_vision_interfaces__srv__ExecuteVision_Response__init(pm_vision_interfaces__srv__ExecuteVision_Response * msg)
{
  if (!msg) {
    return false;
  }
  // success
  // results_path
  if (!rosidl_runtime_c__String__init(&msg->results_path)) {
    pm_vision_interfaces__srv__ExecuteVision_Response__fini(msg);
    return false;
  }
  // vision_response
  if (!pm_vision_interfaces__msg__VisionResponse__init(&msg->vision_response)) {
    pm_vision_interfaces__srv__ExecuteVision_Response__fini(msg);
    return false;
  }
  return true;
}

void
pm_vision_interfaces__srv__ExecuteVision_Response__fini(pm_vision_interfaces__srv__ExecuteVision_Response * msg)
{
  if (!msg) {
    return;
  }
  // success
  // results_path
  rosidl_runtime_c__String__fini(&msg->results_path);
  // vision_response
  pm_vision_interfaces__msg__VisionResponse__fini(&msg->vision_response);
}

bool
pm_vision_interfaces__srv__ExecuteVision_Response__are_equal(const pm_vision_interfaces__srv__ExecuteVision_Response * lhs, const pm_vision_interfaces__srv__ExecuteVision_Response * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // success
  if (lhs->success != rhs->success) {
    return false;
  }
  // results_path
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->results_path), &(rhs->results_path)))
  {
    return false;
  }
  // vision_response
  if (!pm_vision_interfaces__msg__VisionResponse__are_equal(
      &(lhs->vision_response), &(rhs->vision_response)))
  {
    return false;
  }
  return true;
}

bool
pm_vision_interfaces__srv__ExecuteVision_Response__copy(
  const pm_vision_interfaces__srv__ExecuteVision_Response * input,
  pm_vision_interfaces__srv__ExecuteVision_Response * output)
{
  if (!input || !output) {
    return false;
  }
  // success
  output->success = input->success;
  // results_path
  if (!rosidl_runtime_c__String__copy(
      &(input->results_path), &(output->results_path)))
  {
    return false;
  }
  // vision_response
  if (!pm_vision_interfaces__msg__VisionResponse__copy(
      &(input->vision_response), &(output->vision_response)))
  {
    return false;
  }
  return true;
}

pm_vision_interfaces__srv__ExecuteVision_Response *
pm_vision_interfaces__srv__ExecuteVision_Response__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  pm_vision_interfaces__srv__ExecuteVision_Response * msg = (pm_vision_interfaces__srv__ExecuteVision_Response *)allocator.allocate(sizeof(pm_vision_interfaces__srv__ExecuteVision_Response), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(pm_vision_interfaces__srv__ExecuteVision_Response));
  bool success = pm_vision_interfaces__srv__ExecuteVision_Response__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
pm_vision_interfaces__srv__ExecuteVision_Response__destroy(pm_vision_interfaces__srv__ExecuteVision_Response * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    pm_vision_interfaces__srv__ExecuteVision_Response__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
pm_vision_interfaces__srv__ExecuteVision_Response__Sequence__init(pm_vision_interfaces__srv__ExecuteVision_Response__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  pm_vision_interfaces__srv__ExecuteVision_Response * data = NULL;

  if (size) {
    data = (pm_vision_interfaces__srv__ExecuteVision_Response *)allocator.zero_allocate(size, sizeof(pm_vision_interfaces__srv__ExecuteVision_Response), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = pm_vision_interfaces__srv__ExecuteVision_Response__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        pm_vision_interfaces__srv__ExecuteVision_Response__fini(&data[i - 1]);
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
pm_vision_interfaces__srv__ExecuteVision_Response__Sequence__fini(pm_vision_interfaces__srv__ExecuteVision_Response__Sequence * array)
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
      pm_vision_interfaces__srv__ExecuteVision_Response__fini(&array->data[i]);
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

pm_vision_interfaces__srv__ExecuteVision_Response__Sequence *
pm_vision_interfaces__srv__ExecuteVision_Response__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  pm_vision_interfaces__srv__ExecuteVision_Response__Sequence * array = (pm_vision_interfaces__srv__ExecuteVision_Response__Sequence *)allocator.allocate(sizeof(pm_vision_interfaces__srv__ExecuteVision_Response__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = pm_vision_interfaces__srv__ExecuteVision_Response__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
pm_vision_interfaces__srv__ExecuteVision_Response__Sequence__destroy(pm_vision_interfaces__srv__ExecuteVision_Response__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    pm_vision_interfaces__srv__ExecuteVision_Response__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
pm_vision_interfaces__srv__ExecuteVision_Response__Sequence__are_equal(const pm_vision_interfaces__srv__ExecuteVision_Response__Sequence * lhs, const pm_vision_interfaces__srv__ExecuteVision_Response__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!pm_vision_interfaces__srv__ExecuteVision_Response__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
pm_vision_interfaces__srv__ExecuteVision_Response__Sequence__copy(
  const pm_vision_interfaces__srv__ExecuteVision_Response__Sequence * input,
  pm_vision_interfaces__srv__ExecuteVision_Response__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(pm_vision_interfaces__srv__ExecuteVision_Response);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    pm_vision_interfaces__srv__ExecuteVision_Response * data =
      (pm_vision_interfaces__srv__ExecuteVision_Response *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!pm_vision_interfaces__srv__ExecuteVision_Response__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          pm_vision_interfaces__srv__ExecuteVision_Response__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!pm_vision_interfaces__srv__ExecuteVision_Response__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}

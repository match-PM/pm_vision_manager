// generated from rosidl_generator_c/resource/idl__functions.h.em
// with input from pm_vision_interfaces:msg/VisionLine.idl
// generated code does not contain a copyright notice

#ifndef PM_VISION_INTERFACES__MSG__DETAIL__VISION_LINE__FUNCTIONS_H_
#define PM_VISION_INTERFACES__MSG__DETAIL__VISION_LINE__FUNCTIONS_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stdlib.h>

#include "rosidl_runtime_c/visibility_control.h"
#include "pm_vision_interfaces/msg/rosidl_generator_c__visibility_control.h"

#include "pm_vision_interfaces/msg/detail/vision_line__struct.h"

/// Initialize msg/VisionLine message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * pm_vision_interfaces__msg__VisionLine
 * )) before or use
 * pm_vision_interfaces__msg__VisionLine__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_pm_vision_interfaces
bool
pm_vision_interfaces__msg__VisionLine__init(pm_vision_interfaces__msg__VisionLine * msg);

/// Finalize msg/VisionLine message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_pm_vision_interfaces
void
pm_vision_interfaces__msg__VisionLine__fini(pm_vision_interfaces__msg__VisionLine * msg);

/// Create msg/VisionLine message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * pm_vision_interfaces__msg__VisionLine__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_pm_vision_interfaces
pm_vision_interfaces__msg__VisionLine *
pm_vision_interfaces__msg__VisionLine__create();

/// Destroy msg/VisionLine message.
/**
 * It calls
 * pm_vision_interfaces__msg__VisionLine__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_pm_vision_interfaces
void
pm_vision_interfaces__msg__VisionLine__destroy(pm_vision_interfaces__msg__VisionLine * msg);

/// Check for msg/VisionLine message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_pm_vision_interfaces
bool
pm_vision_interfaces__msg__VisionLine__are_equal(const pm_vision_interfaces__msg__VisionLine * lhs, const pm_vision_interfaces__msg__VisionLine * rhs);

/// Copy a msg/VisionLine message.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source message pointer.
 * \param[out] output The target message pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer is null
 *   or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_pm_vision_interfaces
bool
pm_vision_interfaces__msg__VisionLine__copy(
  const pm_vision_interfaces__msg__VisionLine * input,
  pm_vision_interfaces__msg__VisionLine * output);

/// Initialize array of msg/VisionLine messages.
/**
 * It allocates the memory for the number of elements and calls
 * pm_vision_interfaces__msg__VisionLine__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_pm_vision_interfaces
bool
pm_vision_interfaces__msg__VisionLine__Sequence__init(pm_vision_interfaces__msg__VisionLine__Sequence * array, size_t size);

/// Finalize array of msg/VisionLine messages.
/**
 * It calls
 * pm_vision_interfaces__msg__VisionLine__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_pm_vision_interfaces
void
pm_vision_interfaces__msg__VisionLine__Sequence__fini(pm_vision_interfaces__msg__VisionLine__Sequence * array);

/// Create array of msg/VisionLine messages.
/**
 * It allocates the memory for the array and calls
 * pm_vision_interfaces__msg__VisionLine__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_pm_vision_interfaces
pm_vision_interfaces__msg__VisionLine__Sequence *
pm_vision_interfaces__msg__VisionLine__Sequence__create(size_t size);

/// Destroy array of msg/VisionLine messages.
/**
 * It calls
 * pm_vision_interfaces__msg__VisionLine__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_pm_vision_interfaces
void
pm_vision_interfaces__msg__VisionLine__Sequence__destroy(pm_vision_interfaces__msg__VisionLine__Sequence * array);

/// Check for msg/VisionLine message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_pm_vision_interfaces
bool
pm_vision_interfaces__msg__VisionLine__Sequence__are_equal(const pm_vision_interfaces__msg__VisionLine__Sequence * lhs, const pm_vision_interfaces__msg__VisionLine__Sequence * rhs);

/// Copy an array of msg/VisionLine messages.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source array pointer.
 * \param[out] output The target array pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer
 *   is null or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_pm_vision_interfaces
bool
pm_vision_interfaces__msg__VisionLine__Sequence__copy(
  const pm_vision_interfaces__msg__VisionLine__Sequence * input,
  pm_vision_interfaces__msg__VisionLine__Sequence * output);

#ifdef __cplusplus
}
#endif

#endif  // PM_VISION_INTERFACES__MSG__DETAIL__VISION_LINE__FUNCTIONS_H_

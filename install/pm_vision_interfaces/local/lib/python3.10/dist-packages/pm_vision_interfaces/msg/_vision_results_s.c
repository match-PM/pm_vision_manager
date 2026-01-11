// generated from rosidl_generator_py/resource/_idl_support.c.em
// with input from pm_vision_interfaces:msg/VisionResults.idl
// generated code does not contain a copyright notice
#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION
#include <Python.h>
#include <stdbool.h>
#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-function"
#endif
#include "numpy/ndarrayobject.h"
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif
#include "rosidl_runtime_c/visibility_control.h"
#include "pm_vision_interfaces/msg/detail/vision_results__struct.h"
#include "pm_vision_interfaces/msg/detail/vision_results__functions.h"

#include "rosidl_runtime_c/primitives_sequence.h"
#include "rosidl_runtime_c/primitives_sequence_functions.h"

// Nested array functions includes
#include "pm_vision_interfaces/msg/detail/vision_area__functions.h"
#include "pm_vision_interfaces/msg/detail/vision_circle__functions.h"
#include "pm_vision_interfaces/msg/detail/vision_line__functions.h"
#include "pm_vision_interfaces/msg/detail/vision_point__functions.h"
// end nested array functions include
bool pm_vision_interfaces__msg__vision_point__convert_from_py(PyObject * _pymsg, void * _ros_message);
PyObject * pm_vision_interfaces__msg__vision_point__convert_to_py(void * raw_ros_message);
bool pm_vision_interfaces__msg__vision_line__convert_from_py(PyObject * _pymsg, void * _ros_message);
PyObject * pm_vision_interfaces__msg__vision_line__convert_to_py(void * raw_ros_message);
bool pm_vision_interfaces__msg__vision_area__convert_from_py(PyObject * _pymsg, void * _ros_message);
PyObject * pm_vision_interfaces__msg__vision_area__convert_to_py(void * raw_ros_message);
bool pm_vision_interfaces__msg__vision_circle__convert_from_py(PyObject * _pymsg, void * _ros_message);
PyObject * pm_vision_interfaces__msg__vision_circle__convert_to_py(void * raw_ros_message);
bool pm_vision_interfaces__msg__image_sharpness__convert_from_py(PyObject * _pymsg, void * _ros_message);
PyObject * pm_vision_interfaces__msg__image_sharpness__convert_to_py(void * raw_ros_message);

ROSIDL_GENERATOR_C_EXPORT
bool pm_vision_interfaces__msg__vision_results__convert_from_py(PyObject * _pymsg, void * _ros_message)
{
  // check that the passed message is of the expected Python class
  {
    char full_classname_dest[55];
    {
      char * class_name = NULL;
      char * module_name = NULL;
      {
        PyObject * class_attr = PyObject_GetAttrString(_pymsg, "__class__");
        if (class_attr) {
          PyObject * name_attr = PyObject_GetAttrString(class_attr, "__name__");
          if (name_attr) {
            class_name = (char *)PyUnicode_1BYTE_DATA(name_attr);
            Py_DECREF(name_attr);
          }
          PyObject * module_attr = PyObject_GetAttrString(class_attr, "__module__");
          if (module_attr) {
            module_name = (char *)PyUnicode_1BYTE_DATA(module_attr);
            Py_DECREF(module_attr);
          }
          Py_DECREF(class_attr);
        }
      }
      if (!class_name || !module_name) {
        return false;
      }
      snprintf(full_classname_dest, sizeof(full_classname_dest), "%s.%s", module_name, class_name);
    }
    assert(strncmp("pm_vision_interfaces.msg._vision_results.VisionResults", full_classname_dest, 54) == 0);
  }
  pm_vision_interfaces__msg__VisionResults * ros_message = _ros_message;
  {  // points
    PyObject * field = PyObject_GetAttrString(_pymsg, "points");
    if (!field) {
      return false;
    }
    PyObject * seq_field = PySequence_Fast(field, "expected a sequence in 'points'");
    if (!seq_field) {
      Py_DECREF(field);
      return false;
    }
    Py_ssize_t size = PySequence_Size(field);
    if (-1 == size) {
      Py_DECREF(seq_field);
      Py_DECREF(field);
      return false;
    }
    if (!pm_vision_interfaces__msg__VisionPoint__Sequence__init(&(ros_message->points), size)) {
      PyErr_SetString(PyExc_RuntimeError, "unable to create pm_vision_interfaces__msg__VisionPoint__Sequence ros_message");
      Py_DECREF(seq_field);
      Py_DECREF(field);
      return false;
    }
    pm_vision_interfaces__msg__VisionPoint * dest = ros_message->points.data;
    for (Py_ssize_t i = 0; i < size; ++i) {
      if (!pm_vision_interfaces__msg__vision_point__convert_from_py(PySequence_Fast_GET_ITEM(seq_field, i), &dest[i])) {
        Py_DECREF(seq_field);
        Py_DECREF(field);
        return false;
      }
    }
    Py_DECREF(seq_field);
    Py_DECREF(field);
  }
  {  // lines
    PyObject * field = PyObject_GetAttrString(_pymsg, "lines");
    if (!field) {
      return false;
    }
    PyObject * seq_field = PySequence_Fast(field, "expected a sequence in 'lines'");
    if (!seq_field) {
      Py_DECREF(field);
      return false;
    }
    Py_ssize_t size = PySequence_Size(field);
    if (-1 == size) {
      Py_DECREF(seq_field);
      Py_DECREF(field);
      return false;
    }
    if (!pm_vision_interfaces__msg__VisionLine__Sequence__init(&(ros_message->lines), size)) {
      PyErr_SetString(PyExc_RuntimeError, "unable to create pm_vision_interfaces__msg__VisionLine__Sequence ros_message");
      Py_DECREF(seq_field);
      Py_DECREF(field);
      return false;
    }
    pm_vision_interfaces__msg__VisionLine * dest = ros_message->lines.data;
    for (Py_ssize_t i = 0; i < size; ++i) {
      if (!pm_vision_interfaces__msg__vision_line__convert_from_py(PySequence_Fast_GET_ITEM(seq_field, i), &dest[i])) {
        Py_DECREF(seq_field);
        Py_DECREF(field);
        return false;
      }
    }
    Py_DECREF(seq_field);
    Py_DECREF(field);
  }
  {  // areas
    PyObject * field = PyObject_GetAttrString(_pymsg, "areas");
    if (!field) {
      return false;
    }
    PyObject * seq_field = PySequence_Fast(field, "expected a sequence in 'areas'");
    if (!seq_field) {
      Py_DECREF(field);
      return false;
    }
    Py_ssize_t size = PySequence_Size(field);
    if (-1 == size) {
      Py_DECREF(seq_field);
      Py_DECREF(field);
      return false;
    }
    if (!pm_vision_interfaces__msg__VisionArea__Sequence__init(&(ros_message->areas), size)) {
      PyErr_SetString(PyExc_RuntimeError, "unable to create pm_vision_interfaces__msg__VisionArea__Sequence ros_message");
      Py_DECREF(seq_field);
      Py_DECREF(field);
      return false;
    }
    pm_vision_interfaces__msg__VisionArea * dest = ros_message->areas.data;
    for (Py_ssize_t i = 0; i < size; ++i) {
      if (!pm_vision_interfaces__msg__vision_area__convert_from_py(PySequence_Fast_GET_ITEM(seq_field, i), &dest[i])) {
        Py_DECREF(seq_field);
        Py_DECREF(field);
        return false;
      }
    }
    Py_DECREF(seq_field);
    Py_DECREF(field);
  }
  {  // circles
    PyObject * field = PyObject_GetAttrString(_pymsg, "circles");
    if (!field) {
      return false;
    }
    PyObject * seq_field = PySequence_Fast(field, "expected a sequence in 'circles'");
    if (!seq_field) {
      Py_DECREF(field);
      return false;
    }
    Py_ssize_t size = PySequence_Size(field);
    if (-1 == size) {
      Py_DECREF(seq_field);
      Py_DECREF(field);
      return false;
    }
    if (!pm_vision_interfaces__msg__VisionCircle__Sequence__init(&(ros_message->circles), size)) {
      PyErr_SetString(PyExc_RuntimeError, "unable to create pm_vision_interfaces__msg__VisionCircle__Sequence ros_message");
      Py_DECREF(seq_field);
      Py_DECREF(field);
      return false;
    }
    pm_vision_interfaces__msg__VisionCircle * dest = ros_message->circles.data;
    for (Py_ssize_t i = 0; i < size; ++i) {
      if (!pm_vision_interfaces__msg__vision_circle__convert_from_py(PySequence_Fast_GET_ITEM(seq_field, i), &dest[i])) {
        Py_DECREF(seq_field);
        Py_DECREF(field);
        return false;
      }
    }
    Py_DECREF(seq_field);
    Py_DECREF(field);
  }
  {  // image_sharpness
    PyObject * field = PyObject_GetAttrString(_pymsg, "image_sharpness");
    if (!field) {
      return false;
    }
    if (!pm_vision_interfaces__msg__image_sharpness__convert_from_py(field, &ros_message->image_sharpness)) {
      Py_DECREF(field);
      return false;
    }
    Py_DECREF(field);
  }

  return true;
}

ROSIDL_GENERATOR_C_EXPORT
PyObject * pm_vision_interfaces__msg__vision_results__convert_to_py(void * raw_ros_message)
{
  /* NOTE(esteve): Call constructor of VisionResults */
  PyObject * _pymessage = NULL;
  {
    PyObject * pymessage_module = PyImport_ImportModule("pm_vision_interfaces.msg._vision_results");
    assert(pymessage_module);
    PyObject * pymessage_class = PyObject_GetAttrString(pymessage_module, "VisionResults");
    assert(pymessage_class);
    Py_DECREF(pymessage_module);
    _pymessage = PyObject_CallObject(pymessage_class, NULL);
    Py_DECREF(pymessage_class);
    if (!_pymessage) {
      return NULL;
    }
  }
  pm_vision_interfaces__msg__VisionResults * ros_message = (pm_vision_interfaces__msg__VisionResults *)raw_ros_message;
  {  // points
    PyObject * field = NULL;
    size_t size = ros_message->points.size;
    field = PyList_New(size);
    if (!field) {
      return NULL;
    }
    pm_vision_interfaces__msg__VisionPoint * item;
    for (size_t i = 0; i < size; ++i) {
      item = &(ros_message->points.data[i]);
      PyObject * pyitem = pm_vision_interfaces__msg__vision_point__convert_to_py(item);
      if (!pyitem) {
        Py_DECREF(field);
        return NULL;
      }
      int rc = PyList_SetItem(field, i, pyitem);
      (void)rc;
      assert(rc == 0);
    }
    assert(PySequence_Check(field));
    {
      int rc = PyObject_SetAttrString(_pymessage, "points", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // lines
    PyObject * field = NULL;
    size_t size = ros_message->lines.size;
    field = PyList_New(size);
    if (!field) {
      return NULL;
    }
    pm_vision_interfaces__msg__VisionLine * item;
    for (size_t i = 0; i < size; ++i) {
      item = &(ros_message->lines.data[i]);
      PyObject * pyitem = pm_vision_interfaces__msg__vision_line__convert_to_py(item);
      if (!pyitem) {
        Py_DECREF(field);
        return NULL;
      }
      int rc = PyList_SetItem(field, i, pyitem);
      (void)rc;
      assert(rc == 0);
    }
    assert(PySequence_Check(field));
    {
      int rc = PyObject_SetAttrString(_pymessage, "lines", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // areas
    PyObject * field = NULL;
    size_t size = ros_message->areas.size;
    field = PyList_New(size);
    if (!field) {
      return NULL;
    }
    pm_vision_interfaces__msg__VisionArea * item;
    for (size_t i = 0; i < size; ++i) {
      item = &(ros_message->areas.data[i]);
      PyObject * pyitem = pm_vision_interfaces__msg__vision_area__convert_to_py(item);
      if (!pyitem) {
        Py_DECREF(field);
        return NULL;
      }
      int rc = PyList_SetItem(field, i, pyitem);
      (void)rc;
      assert(rc == 0);
    }
    assert(PySequence_Check(field));
    {
      int rc = PyObject_SetAttrString(_pymessage, "areas", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // circles
    PyObject * field = NULL;
    size_t size = ros_message->circles.size;
    field = PyList_New(size);
    if (!field) {
      return NULL;
    }
    pm_vision_interfaces__msg__VisionCircle * item;
    for (size_t i = 0; i < size; ++i) {
      item = &(ros_message->circles.data[i]);
      PyObject * pyitem = pm_vision_interfaces__msg__vision_circle__convert_to_py(item);
      if (!pyitem) {
        Py_DECREF(field);
        return NULL;
      }
      int rc = PyList_SetItem(field, i, pyitem);
      (void)rc;
      assert(rc == 0);
    }
    assert(PySequence_Check(field));
    {
      int rc = PyObject_SetAttrString(_pymessage, "circles", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // image_sharpness
    PyObject * field = NULL;
    field = pm_vision_interfaces__msg__image_sharpness__convert_to_py(&ros_message->image_sharpness);
    if (!field) {
      return NULL;
    }
    {
      int rc = PyObject_SetAttrString(_pymessage, "image_sharpness", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }

  // ownership of _pymessage is transferred to the caller
  return _pymessage;
}

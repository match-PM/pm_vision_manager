// generated from rosidl_generator_py/resource/_idl_support.c.em
// with input from pm_vision_interfaces:msg/VisionResponse.idl
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
#include "pm_vision_interfaces/msg/detail/vision_response__struct.h"
#include "pm_vision_interfaces/msg/detail/vision_response__functions.h"

#include "rosidl_runtime_c/string.h"
#include "rosidl_runtime_c/string_functions.h"

bool pm_vision_interfaces__msg__cross_validation__convert_from_py(PyObject * _pymsg, void * _ros_message);
PyObject * pm_vision_interfaces__msg__cross_validation__convert_to_py(void * raw_ros_message);
bool pm_vision_interfaces__msg__vision_results__convert_from_py(PyObject * _pymsg, void * _ros_message);
PyObject * pm_vision_interfaces__msg__vision_results__convert_to_py(void * raw_ros_message);

ROSIDL_GENERATOR_C_EXPORT
bool pm_vision_interfaces__msg__vision_response__convert_from_py(PyObject * _pymsg, void * _ros_message)
{
  // check that the passed message is of the expected Python class
  {
    char full_classname_dest[57];
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
    assert(strncmp("pm_vision_interfaces.msg._vision_response.VisionResponse", full_classname_dest, 56) == 0);
  }
  pm_vision_interfaces__msg__VisionResponse * ros_message = _ros_message;
  {  // vision_ok
    PyObject * field = PyObject_GetAttrString(_pymsg, "vision_ok");
    if (!field) {
      return false;
    }
    assert(PyBool_Check(field));
    ros_message->vision_ok = (Py_True == field);
    Py_DECREF(field);
  }
  {  // process_name
    PyObject * field = PyObject_GetAttrString(_pymsg, "process_name");
    if (!field) {
      return false;
    }
    assert(PyUnicode_Check(field));
    PyObject * encoded_field = PyUnicode_AsUTF8String(field);
    if (!encoded_field) {
      Py_DECREF(field);
      return false;
    }
    rosidl_runtime_c__String__assign(&ros_message->process_name, PyBytes_AS_STRING(encoded_field));
    Py_DECREF(encoded_field);
    Py_DECREF(field);
  }
  {  // process_uid
    PyObject * field = PyObject_GetAttrString(_pymsg, "process_uid");
    if (!field) {
      return false;
    }
    assert(PyUnicode_Check(field));
    PyObject * encoded_field = PyUnicode_AsUTF8String(field);
    if (!encoded_field) {
      Py_DECREF(field);
      return false;
    }
    rosidl_runtime_c__String__assign(&ros_message->process_uid, PyBytes_AS_STRING(encoded_field));
    Py_DECREF(encoded_field);
    Py_DECREF(field);
  }
  {  // exec_timestamp
    PyObject * field = PyObject_GetAttrString(_pymsg, "exec_timestamp");
    if (!field) {
      return false;
    }
    assert(PyUnicode_Check(field));
    PyObject * encoded_field = PyUnicode_AsUTF8String(field);
    if (!encoded_field) {
      Py_DECREF(field);
      return false;
    }
    rosidl_runtime_c__String__assign(&ros_message->exec_timestamp, PyBytes_AS_STRING(encoded_field));
    Py_DECREF(encoded_field);
    Py_DECREF(field);
  }
  {  // cross_validation
    PyObject * field = PyObject_GetAttrString(_pymsg, "cross_validation");
    if (!field) {
      return false;
    }
    if (!pm_vision_interfaces__msg__cross_validation__convert_from_py(field, &ros_message->cross_validation)) {
      Py_DECREF(field);
      return false;
    }
    Py_DECREF(field);
  }
  {  // results
    PyObject * field = PyObject_GetAttrString(_pymsg, "results");
    if (!field) {
      return false;
    }
    if (!pm_vision_interfaces__msg__vision_results__convert_from_py(field, &ros_message->results)) {
      Py_DECREF(field);
      return false;
    }
    Py_DECREF(field);
  }

  return true;
}

ROSIDL_GENERATOR_C_EXPORT
PyObject * pm_vision_interfaces__msg__vision_response__convert_to_py(void * raw_ros_message)
{
  /* NOTE(esteve): Call constructor of VisionResponse */
  PyObject * _pymessage = NULL;
  {
    PyObject * pymessage_module = PyImport_ImportModule("pm_vision_interfaces.msg._vision_response");
    assert(pymessage_module);
    PyObject * pymessage_class = PyObject_GetAttrString(pymessage_module, "VisionResponse");
    assert(pymessage_class);
    Py_DECREF(pymessage_module);
    _pymessage = PyObject_CallObject(pymessage_class, NULL);
    Py_DECREF(pymessage_class);
    if (!_pymessage) {
      return NULL;
    }
  }
  pm_vision_interfaces__msg__VisionResponse * ros_message = (pm_vision_interfaces__msg__VisionResponse *)raw_ros_message;
  {  // vision_ok
    PyObject * field = NULL;
    field = PyBool_FromLong(ros_message->vision_ok ? 1 : 0);
    {
      int rc = PyObject_SetAttrString(_pymessage, "vision_ok", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // process_name
    PyObject * field = NULL;
    field = PyUnicode_DecodeUTF8(
      ros_message->process_name.data,
      strlen(ros_message->process_name.data),
      "replace");
    if (!field) {
      return NULL;
    }
    {
      int rc = PyObject_SetAttrString(_pymessage, "process_name", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // process_uid
    PyObject * field = NULL;
    field = PyUnicode_DecodeUTF8(
      ros_message->process_uid.data,
      strlen(ros_message->process_uid.data),
      "replace");
    if (!field) {
      return NULL;
    }
    {
      int rc = PyObject_SetAttrString(_pymessage, "process_uid", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // exec_timestamp
    PyObject * field = NULL;
    field = PyUnicode_DecodeUTF8(
      ros_message->exec_timestamp.data,
      strlen(ros_message->exec_timestamp.data),
      "replace");
    if (!field) {
      return NULL;
    }
    {
      int rc = PyObject_SetAttrString(_pymessage, "exec_timestamp", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // cross_validation
    PyObject * field = NULL;
    field = pm_vision_interfaces__msg__cross_validation__convert_to_py(&ros_message->cross_validation);
    if (!field) {
      return NULL;
    }
    {
      int rc = PyObject_SetAttrString(_pymessage, "cross_validation", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // results
    PyObject * field = NULL;
    field = pm_vision_interfaces__msg__vision_results__convert_to_py(&ros_message->results);
    if (!field) {
      return NULL;
    }
    {
      int rc = PyObject_SetAttrString(_pymessage, "results", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }

  // ownership of _pymessage is transferred to the caller
  return _pymessage;
}

// generated from rosidl_generator_py/resource/_idl_support.c.em
// with input from pm_vision_interfaces:srv/ExecuteVision.idl
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
#include "pm_vision_interfaces/srv/detail/execute_vision__struct.h"
#include "pm_vision_interfaces/srv/detail/execute_vision__functions.h"

#include "rosidl_runtime_c/string.h"
#include "rosidl_runtime_c/string_functions.h"


ROSIDL_GENERATOR_C_EXPORT
bool pm_vision_interfaces__srv__execute_vision__request__convert_from_py(PyObject * _pymsg, void * _ros_message)
{
  // check that the passed message is of the expected Python class
  {
    char full_classname_dest[63];
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
    assert(strncmp("pm_vision_interfaces.srv._execute_vision.ExecuteVision_Request", full_classname_dest, 62) == 0);
  }
  pm_vision_interfaces__srv__ExecuteVision_Request * ros_message = _ros_message;
  {  // process_filename
    PyObject * field = PyObject_GetAttrString(_pymsg, "process_filename");
    if (!field) {
      return false;
    }
    assert(PyUnicode_Check(field));
    PyObject * encoded_field = PyUnicode_AsUTF8String(field);
    if (!encoded_field) {
      Py_DECREF(field);
      return false;
    }
    rosidl_runtime_c__String__assign(&ros_message->process_filename, PyBytes_AS_STRING(encoded_field));
    Py_DECREF(encoded_field);
    Py_DECREF(field);
  }
  {  // camera_config_filename
    PyObject * field = PyObject_GetAttrString(_pymsg, "camera_config_filename");
    if (!field) {
      return false;
    }
    assert(PyUnicode_Check(field));
    PyObject * encoded_field = PyUnicode_AsUTF8String(field);
    if (!encoded_field) {
      Py_DECREF(field);
      return false;
    }
    rosidl_runtime_c__String__assign(&ros_message->camera_config_filename, PyBytes_AS_STRING(encoded_field));
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
  {  // image_display_time
    PyObject * field = PyObject_GetAttrString(_pymsg, "image_display_time");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->image_display_time = PyLong_AsLongLong(field);
    Py_DECREF(field);
  }
  {  // run_cross_validation
    PyObject * field = PyObject_GetAttrString(_pymsg, "run_cross_validation");
    if (!field) {
      return false;
    }
    assert(PyBool_Check(field));
    ros_message->run_cross_validation = (Py_True == field);
    Py_DECREF(field);
  }

  return true;
}

ROSIDL_GENERATOR_C_EXPORT
PyObject * pm_vision_interfaces__srv__execute_vision__request__convert_to_py(void * raw_ros_message)
{
  /* NOTE(esteve): Call constructor of ExecuteVision_Request */
  PyObject * _pymessage = NULL;
  {
    PyObject * pymessage_module = PyImport_ImportModule("pm_vision_interfaces.srv._execute_vision");
    assert(pymessage_module);
    PyObject * pymessage_class = PyObject_GetAttrString(pymessage_module, "ExecuteVision_Request");
    assert(pymessage_class);
    Py_DECREF(pymessage_module);
    _pymessage = PyObject_CallObject(pymessage_class, NULL);
    Py_DECREF(pymessage_class);
    if (!_pymessage) {
      return NULL;
    }
  }
  pm_vision_interfaces__srv__ExecuteVision_Request * ros_message = (pm_vision_interfaces__srv__ExecuteVision_Request *)raw_ros_message;
  {  // process_filename
    PyObject * field = NULL;
    field = PyUnicode_DecodeUTF8(
      ros_message->process_filename.data,
      strlen(ros_message->process_filename.data),
      "replace");
    if (!field) {
      return NULL;
    }
    {
      int rc = PyObject_SetAttrString(_pymessage, "process_filename", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // camera_config_filename
    PyObject * field = NULL;
    field = PyUnicode_DecodeUTF8(
      ros_message->camera_config_filename.data,
      strlen(ros_message->camera_config_filename.data),
      "replace");
    if (!field) {
      return NULL;
    }
    {
      int rc = PyObject_SetAttrString(_pymessage, "camera_config_filename", field);
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
  {  // image_display_time
    PyObject * field = NULL;
    field = PyLong_FromLongLong(ros_message->image_display_time);
    {
      int rc = PyObject_SetAttrString(_pymessage, "image_display_time", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // run_cross_validation
    PyObject * field = NULL;
    field = PyBool_FromLong(ros_message->run_cross_validation ? 1 : 0);
    {
      int rc = PyObject_SetAttrString(_pymessage, "run_cross_validation", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }

  // ownership of _pymessage is transferred to the caller
  return _pymessage;
}

#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION
// already included above
// #include <Python.h>
// already included above
// #include <stdbool.h>
// already included above
// #include "numpy/ndarrayobject.h"
// already included above
// #include "rosidl_runtime_c/visibility_control.h"
// already included above
// #include "pm_vision_interfaces/srv/detail/execute_vision__struct.h"
// already included above
// #include "pm_vision_interfaces/srv/detail/execute_vision__functions.h"

// already included above
// #include "rosidl_runtime_c/string.h"
// already included above
// #include "rosidl_runtime_c/string_functions.h"

bool pm_vision_interfaces__msg__vision_response__convert_from_py(PyObject * _pymsg, void * _ros_message);
PyObject * pm_vision_interfaces__msg__vision_response__convert_to_py(void * raw_ros_message);

ROSIDL_GENERATOR_C_EXPORT
bool pm_vision_interfaces__srv__execute_vision__response__convert_from_py(PyObject * _pymsg, void * _ros_message)
{
  // check that the passed message is of the expected Python class
  {
    char full_classname_dest[64];
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
    assert(strncmp("pm_vision_interfaces.srv._execute_vision.ExecuteVision_Response", full_classname_dest, 63) == 0);
  }
  pm_vision_interfaces__srv__ExecuteVision_Response * ros_message = _ros_message;
  {  // success
    PyObject * field = PyObject_GetAttrString(_pymsg, "success");
    if (!field) {
      return false;
    }
    assert(PyBool_Check(field));
    ros_message->success = (Py_True == field);
    Py_DECREF(field);
  }
  {  // results_path
    PyObject * field = PyObject_GetAttrString(_pymsg, "results_path");
    if (!field) {
      return false;
    }
    assert(PyUnicode_Check(field));
    PyObject * encoded_field = PyUnicode_AsUTF8String(field);
    if (!encoded_field) {
      Py_DECREF(field);
      return false;
    }
    rosidl_runtime_c__String__assign(&ros_message->results_path, PyBytes_AS_STRING(encoded_field));
    Py_DECREF(encoded_field);
    Py_DECREF(field);
  }
  {  // vision_response
    PyObject * field = PyObject_GetAttrString(_pymsg, "vision_response");
    if (!field) {
      return false;
    }
    if (!pm_vision_interfaces__msg__vision_response__convert_from_py(field, &ros_message->vision_response)) {
      Py_DECREF(field);
      return false;
    }
    Py_DECREF(field);
  }

  return true;
}

ROSIDL_GENERATOR_C_EXPORT
PyObject * pm_vision_interfaces__srv__execute_vision__response__convert_to_py(void * raw_ros_message)
{
  /* NOTE(esteve): Call constructor of ExecuteVision_Response */
  PyObject * _pymessage = NULL;
  {
    PyObject * pymessage_module = PyImport_ImportModule("pm_vision_interfaces.srv._execute_vision");
    assert(pymessage_module);
    PyObject * pymessage_class = PyObject_GetAttrString(pymessage_module, "ExecuteVision_Response");
    assert(pymessage_class);
    Py_DECREF(pymessage_module);
    _pymessage = PyObject_CallObject(pymessage_class, NULL);
    Py_DECREF(pymessage_class);
    if (!_pymessage) {
      return NULL;
    }
  }
  pm_vision_interfaces__srv__ExecuteVision_Response * ros_message = (pm_vision_interfaces__srv__ExecuteVision_Response *)raw_ros_message;
  {  // success
    PyObject * field = NULL;
    field = PyBool_FromLong(ros_message->success ? 1 : 0);
    {
      int rc = PyObject_SetAttrString(_pymessage, "success", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // results_path
    PyObject * field = NULL;
    field = PyUnicode_DecodeUTF8(
      ros_message->results_path.data,
      strlen(ros_message->results_path.data),
      "replace");
    if (!field) {
      return NULL;
    }
    {
      int rc = PyObject_SetAttrString(_pymessage, "results_path", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // vision_response
    PyObject * field = NULL;
    field = pm_vision_interfaces__msg__vision_response__convert_to_py(&ros_message->vision_response);
    if (!field) {
      return NULL;
    }
    {
      int rc = PyObject_SetAttrString(_pymessage, "vision_response", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }

  // ownership of _pymessage is transferred to the caller
  return _pymessage;
}

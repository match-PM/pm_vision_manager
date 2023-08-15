# PM Vision Assistant
ROS2 Vision-Assistant to intuitivly build reusable vision-pipelines based on openCV functions.
## 1. Description
The pm vision assistant is designed to intuitivly build reusable vision-pipelines based on openCV functions. It's basic idea is that the vision assistant manager runs different vision functions (mostly based on openCV) defined in an processfile.json successively to extract specific features from an image. In order to do so, the vision manager offers some basic services, which with vision pipleines can be executed (ExecuteVision) or interactivly build (StartVisionAssistant). While a vision assistant service is running a processed (and the original) image you subscribed to will be displayed while you can modify the vision pipeline in the processfile.json on the fly. It also has an feature to crossvalidate images from a data base with the loaded vision_process.json. 

There are some important config files to operate the vision manager:
* `vision_assistant_path_config.yaml`: This file specifies where to find the config, vision processes, camera configurations and the image data base. The path configuration file is transfered to '/home/USER/ros2_ws/install/pm_vision_manager/share' when building the package. 

* `vision_assistant_config.yaml`: This config file configures how the vision assistant services will operate (parameters can be changed while the service is runing). In order to change the behavoir of the assistants during runtime that file can be changed.

* `camera_config.yaml`: This file specifies the parameters for the connected camera (e.a. webcam). Some of the input and (all) output parameter of the vision functions are specified in microns (calculated by the definitions in camera_config) and refered to the camera cooridnate system. 

Currently the assistant is designed for camera setups with telecentric lenses only! It is currently intended to be used in precision assembly tasks for fast vision pipeline deployment.

### Overview
* `config`: Contains the vision_assistant_path_config.yaml, the vision_assistant_config.yaml and the demo webcam_config.yaml.
* `pm_vision_manager`: Contain the node file for the vision assistant, the python classes for the assistant and an webcam image publisher
* `vision_functions`: Description of all the vision functions supported by the vision assistant - do be done!
* `vision_db`: Default database for demonstration  
* `vision_processes`: Default folder for processes with a process_demo.json

## 2. Installation 
* To run the vision assistant, the installation of ROS2 (tested on Humble) is mandatory! Despite that no other installation is needed.
* Start by changing directory to your workspace!
* Clone package
```
git clone https://github.com/match-PM/pm_vision.git
```
* Go into pm_vision/config/vision_assistant_path_config.yaml and change:
```
process_library_path
```
```
vision_database_path
```
```
camera_config_path
```
```
vision_assistant_config
```
The pathes you insert in this config file specify where the vision assitant looks for the assistant configuration, processes and camera configs and where to save images. You can specify any path here. Make sure the assistant finds the respective files in that locations. The vision_assistant_path_config.yaml should not be removed! The File is added to .gitignore to prevent file changes when pulling from origin.
* Build your workspace:
```
colcon build 
```

## 3. Getting Started
If you leave (modify accordingly) the default file pathes in the '/config/vision_assistant_path_config.yaml', the vision assistant will launch with the process_demo.json. Images will be saved in vision_db/process_demo. By default it will load the camera parameter from config/webcam_config.yaml. By default it will subscribe to the topic 'video_frames'.

### To launch the node
```
ros2 launch pm_vision_manager pm_vision.launch.py
```
### Start the webcam publisher (a webcam needs to be connected) to publish topic 'video_frames'
```
ros2 run pm_vision vision_webcam_publisher
```
## 4. Services
The pm_vision_manager offers three services:
```
ExecuteVision
```
* `process_filename`: Filename/Path of the process file (json)
* `camera_config_filename`: Filename/Path of the camera config file (yaml)
* `process_uid`: (Random) ID of the process (should be random and not yet in use)
* `db_cross_val_only`: run vision only in crossvalidation on database 
* `image_display_time`: time the image will be displayed after vision finished
* `cross_validate_in_execution`: tbd
------------------------
* `success`: returns true if the vision function on the last image exited without error
* `results_dict`: string containing the vision results dictionary
* `results_path`: path of the process results json
```
StartVisionAssistant
```
* `process_filename`: Filename/Path of the process file (json)
* `camera_config_filename`: Filename/Path of the camera config file (yaml)
* `process_uid`: (Random) ID of the process (should be random and not yet in use)
* `db_cross_val_only`: run vision only in crossvalidation on database 
* `open_process_file`: if set to true, the process - json will be opened in vscode
------------------------
(service return generally not relevant for the usage in assistant mode)
* `success`: returns true if the vision function on the last image exited without error
* `results_dict`: string containing the vision results dictionary
* `results_path`: path of the process results json
```
StopVisionAssistant
```
* `process_uid`: ID of the vision assistant process to be closed 
------------------------
* `success`: returns true if the respective vision assistant could be closed; else returns false
## 5. To Do's
* Conditions
* Function yaml descriptions
* cleaner code


* GUI to build vision pipelines in json and to configure the vision asssistant.

## 5. External documentation
[ROS 2 - Humble - Documentation and Tutorial](https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debians.html)

VS CODE gnome-terminal Issue
unset GTK_PATH



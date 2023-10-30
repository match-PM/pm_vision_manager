# PM Vision Assistant
ROS2 Vision-Assistant to intuitivly build reusable vision-pipelines based on openCV functions.
## 1. Description and Concept of the pm vision manager
The pm vision assistant (pm_vision_manager) is designed to intuitivly build reusable vision-pipelines based on openCV (and other python and custom) functions. It's basic idea is that the vision assistant manager runs vision functions (mostly based on openCV) defined in an processfile.json successively on an initial image to extract specific features. In order to do so, the vision manager offers some simple services, with which vision pipleines can be executed (ExecuteVision) or interactivly build (StartVisionAssistant). While a vision assistant service is running, a processed (and the original) image you subscribed to will be displayed while you can modify the vision pipeline in the processfile.json on the fly. It also has a feature to crossvalidate images from a database with the loaded vision_process.json.

In precision assembly processes the usage of camera vision and image processing is prerequisite. In order to create, execute and manage image pipelines for precision assembly task this package has been created. The pm vision manager operates using vision pipelines that are defined in a json file format. By defining camera specifications (with its resprecitve topic on which the camera is publishing) the pm vision manager can execute these process file on any camera image. Based on this concept, the user can define custom vision pipelines in json format with no python coding needed. To assist with the task, there is also an app for creating process.json files. Using the service of the pm vision manager to start a vision assistant, the operator can view changes on the process.json in realtime an thus rapidly build up new vision pipelines when teaching in a new assembly process. Additionally a cross validation among a image database can be run, to check how changes on a process.json would have affect past assembly parts. 

Currently the assistant is designed for camera setups with telecentric lenses only! It is currently intended to be used in precision assembly tasks for fast vision pipeline deployment.

## 2. Package Overview
* `config`: Contains the vision_assistant_path_config.yaml, the vision_assistant_config.yaml and the demo webcam_config.yaml.
* `pm_vision_manager`: Contains the node file for the pm_vision_manager, the python classes for the assistant and a webcam image publisher
* `vision_functions`: Description of all the vision functions supported by the vision assistant! These files are used by the vision_assistant_app.
* `vision_db` (not mandatory to run the node): Default demo database  
* `vision_processes` (not mandatory to run the node): Default demo folder for processes with a process_demo.json

## 3. Configuring the pm_vision_manager

Go into pm_vision-manager/config/vision_assistant_path_config.yaml and change:

* `process_library_path`: This path specifies where the pm_vision_manager looks for process files (root folder of the process libary). You can specify any path here. To change it to default, correct the path in the vision_assistant_path_config.yaml.
* `vision_database_path`: This path specifies where the pm_vision_manager will save images, when executing visions (root folder of images). Images will be saved in a folder being named after the process id (name of the process). To change it to default, correct the path in the vision_assistant_path_config.yaml.
* `function_libary_path`: This path specifies where to find the vision functions libarys. The vision functons libary consists of multple yaml-files that descripe the functionality and the input parameter of a vision function. The vision functions libary is used by the vision app, to build process_files. Correct the path according to the one in the vision_assistant_path_config.yaml!
* `camera_config_path`: This path specifies where to find all the definitions for available cameras (root folder of the camera libary). You can specify any path here. To change it to default, correct the path in the vision_assistant_path_config.yaml.
* `vision_assistant_config`: This path specifies where the pm_vision manager looks for the vision_assistant_config. Correct the path according to the one in the vision_assistant_path_config.yaml! In the vision_assistant_config file, the image output format of the pm_vision_manager can be specified. 

Further explanations:
* `vision_assistant_path_config.yaml`: This file specifies where to find the config, vision processes, camera configurations and the image data base. The path configuration file is transfered to '/home/USER/ros2_ws/install/pm_vision_manager/share' when building the package. 

* `camera_config.yaml`: The camera_config.yamls specifie the parameters for the connected camera (e.a. webcam). Some of the input and (all) output parameter of the vision functions are specified in microns (calculated by the definitions in camera_config) and refered to the camera cooridnate system.
* 
## 4. Getting Started
To launch the pm vision manager execute
```
ros2 launch pm_vision_manager pm_vision.launch.py
```
To start a demo image publisher, start the webcam publisher (a webcam needs to be connected) to publish topic 'video_frames'
```
ros2 run pm_vision_manager vision_webcam_publisher
```
## 5. Services
After launching the pm_vision_manager, three services will be available:
```
ExecuteVision
```
Running this service call, the pm_vision_manager will subsribe to the topic specified in the camera_config_file. It will then execute the vision pipeline defined in the process_filname.json. There are also some other inputs to the service call, that specify how the call will behave:

* `process_filename` (str): Filename or relative path to the process_libary of the process file (json)
* `camera_config_filename` (str): Filename or relative path to the camera config file (yaml)
* `process_uid` (str): ID of the process (should be random and/or not yet in use)
* `db_cross_val_only` (bool): If this is set to true, the pm_vision_manager will execute the process pipeline on images in the database only (database_path/process_name/). In this case, every image in the database is evalued once. Then the service call returns. Information from the camera_config_file are still relevant, as they specify technical details of the camera.  
* `image_display_time` (int): Time the image will be displayed after vision finished
* `run_cross_validation`: If this is set to true, the vision pipeline will additionally be executed on images in the database (database_path/process_name/). Results of the cross_validation will be saved in  (database_path/process_name/Results/).
------------------------
* `success` (bool): returns true if the vision pipeline exited with no error (on the subscribed image). In case of "db_cross_val_only" the success value refers to the last image evaluated from the database. 
* `results_dict` (str): String of the vision results dictionary
* `results_path` (str): Path of the process results json
```
StartVisionAssistant
```
* `process_filename` (str): Filename/Path of the process file (json)
* `camera_config_filename` (str): Filename/Path of the camera config file (yaml)
* `process_uid` (str): (Random) ID of the process (should be random and not yet in use)
* `db_cross_val_only` (bool): If this is set to true, the pm_vision_manager will execute the process pipeline on images in the database only (database_path/process_name/). If "show_image_on_error" or "step_through_images" are not set to true, the user will get no image.
* `run_cross_validation`(bool): If this is set to true, the vision pipeline will additionally be executed on images in the database (database_path/process_name/). Results of the cross_validation will be saved in  (database_path/process_name/Results/).
* `show_image_on_error` (bool): This is only relevant if "run_cross_validation == True". If true, the user can use the space key to show images on which the vision pipeline failed.
* `step_through_images` (bool): This is only relevant if "run_cross_validation == True". If true, the user can use the space key to cycle through the image database.
* `open_process_file` (bool): If set to true, the process.json will be opened in vscode (this will be replaced by a startup of the app.py in the future)
------------------------
(service return generally not relevant for the usage in assistant mode)
* `success`: returns true if the vision function on the last image exited without error
* `results_dict`: string containing the vision results dictionary
* `results_path`: path of the process results json
```
StopVisionAssistant
```
* `process_uid` (str): ID of the vision assistant process to be closed 
------------------------
* `success`: returns true if the respective vision assistant could be closed; else returns false

## 5. To Do's
* Conditions
* Function yaml descriptions

## 6. How to add new vision functions to the pm vision manager
TBD

VS CODE gnome-terminal Issue
unset GTK_PATH



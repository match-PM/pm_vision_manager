# PM Vision Assistant
ROS2 Vision-Assistant to intuitivly build reusable vision-pipelines based on openCV and other python functions.
## 1. Description
The pm vision assistant (pm_vision_manager) is designed to intuitivly build reusable vision-pipelines based on openCV (and other python and custom) functions. It's basic idea is that the vision assistant manager runs vision functions (mostly based on openCV) defined in an processfile.json successively on an initial image to extract specific features. In order to do so, the vision manager offers some basic services, with which vision pipleines can be executed (ExecuteVision) or interactivly build (StartVisionAssistant). While a vision assistant service is running, a processed (and the original) image you subscribed to will be displayed while you can modify the vision pipeline in the processfile.json on the fly. It also has an feature to crossvalidate images from a database with the loaded vision_process.json. 

## 2. Repository overview
This repository contains the following packages:
* `pm_vision_manager`: ROS2 package that conatins the pm_vision_manager node and all of its python code.
* `pm_vision_interfaces`: Contains the message and service descriptions for the pm_vision_manager
* `vision_assistant_app`: Contains a python app, which can be used to build vision pipelines for the pm_vision_manager.

For further information read the README.me within the packages.

## 3. Installation 
* To run the vision assistant, the installation of ROS2 (tested on Humble) is mandatory!
* Start the installation by opening a terminal and chaneging the directory to your workspace!
* Clone package
```
git clone https://github.com/match-PM/pm_vision_manager.git
```
* Install mandatory python packages:
```
pip3 install keyboard
```
```
pip3 install PyQt6
```
* Go into the pm_vision_manager folder in your workspace and configure the node as described in the pm_vision_manager/pm_vision_manager/README.me

## Notes
VS CODE gnome-terminal Issue
unset GTK_PATH

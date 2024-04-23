import os
import yaml
from ament_index_python.packages import get_package_share_directory

def check_for_valid_path_config(logger=None)->bool:
    package_share_directory = get_package_share_directory("pm_vision_manager")
    path_config_path = f"{package_share_directory}/vision_assistant_path_config.yaml"
    try:
        with open(path_config_path, "r") as file:
            FileData = yaml.safe_load(file)

        config = FileData["vision_assistant_path_config"]
        process_library_path = config["process_library_path"]
        camera_config_path = config["camera_config_path"]
        vision_database_path = config["vision_database_path"]
        if os.path.exists(process_library_path) and os.path.exists(camera_config_path) and os.path.exists(vision_database_path):
            return True
        else:
            if logger is not None:
                logger.error("Path config file is not valid!")
            return False
    except KeyError as e:
        if logger is not None:
            logger.error(f"Error in path config file: {str(e)}")
        return False
    except FileNotFoundError as e:
        if logger is not None:
            logger.error(f"Error opening path config file: {str(e)}")


def set_process_library_path(process_libary_path:str,logger=None):
    _set_path_config_value(process_libary_path, "process_library_path", logger)

def set_function_library_path(function_libary_path:str,logger=None):
    _set_path_config_value(function_libary_path, "function_libary_path", logger)

def set_vision_database_path(vision_database_path:str,logger=None):
    _set_path_config_value(vision_database_path, "vision_database_path", logger)

def set_camera_config_path(camera_config_path:str,logger=None):
    _set_path_config_value(camera_config_path, "camera_config_path", logger)

def _set_path_config_value(value:str, key:str, logger=None):
    package_share_directory = get_package_share_directory("pm_vision_manager")
    path_config_path = f"{package_share_directory}/vision_assistant_path_config.yaml"
    try:
        with open(path_config_path, "r") as file:
            FileData = yaml.safe_load(file)

        FileData["vision_assistant_path_config"][key] = value

        with open(path_config_path, "w") as file:
            yaml.safe_dump(FileData, file)

        logger.info(f"{key} set to: {value}")

    except KeyError as e:
        if logger is not None:
            logger.error(f"Error in path config file: {str(e)}")

    except FileNotFoundError as e:
        if logger is not None:
            logger.error(f"Error opening path config file: {str(e)}")

def check_for_valid_inputs(process_file_name:str, camera_file_name:str, logger = None)->bool:
    
    if process_file_name is None or camera_file_name is None:
        return False
    
    package_share_directory = get_package_share_directory("pm_vision_manager")
    path_config_path = f"{package_share_directory}/vision_assistant_path_config.yaml"
    try:
        with open(path_config_path, "r") as file:
            FileData = yaml.safe_load(file)

        config = FileData["vision_assistant_path_config"]
        process_library_path = config["process_library_path"]
        camera_config_path = config["camera_config_path"]
        process_file_path = process_library_path + process_file_name
        camera_file_path = camera_config_path + camera_file_name
        if os.path.exists(process_file_path) and os.path.exists(camera_file_path):
            return True
        else:
            return False
    except KeyError as e:
        if logger is not None:  
            logger.error(f"Error in path config file: {str(e)}")
        return False
    except FileNotFoundError as e:
        if logger is not None:
            logger.error(f"Error opening path config file: {str(e)}")
        return False
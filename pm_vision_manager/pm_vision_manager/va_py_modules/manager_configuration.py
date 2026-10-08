import os
import yaml
from threading import Thread
from ament_index_python.packages import get_package_share_directory

# Paths that have to be reachable for the vision manager to work
REQUIRED_PATH_KEYS = ["process_library_path", "camera_config_path", "vision_database_path"]

# Max time to wait for a filesystem check. Paths on an unreachable network share (e.g. CIFS mount)
# can otherwise block os.path.exists for a very long time.
PATH_CHECK_TIMEOUT_SEC = 2.0

def path_exists_with_timeout(path:str, timeout:float = PATH_CHECK_TIMEOUT_SEC, logger=None)->bool:
    """
    Check if a path exists without blocking longer than 'timeout' seconds.
    Returns False if the check does not finish in time (e.g. network share not reachable).
    """
    if not path:
        return False

    result = {"exists": False}

    def _check():
        result["exists"] = os.path.exists(path)

    # Daemon thread, so a hanging check does not block the shutdown of the program
    check_thread = Thread(target=_check, daemon=True)
    check_thread.start()
    check_thread.join(timeout)

    if check_thread.is_alive():
        if logger is not None:
            logger.error(f"Path '{path}' not reachable within {timeout}s (network share unavailable?)")
        return False

    return result["exists"]

def get_invalid_path_config_keys(logger=None)->list:
    """
    Returns the keys of the required paths that are missing or not reachable.
    """
    package_share_directory = get_package_share_directory("pm_vision_manager")
    path_config_path = f"{package_share_directory}/vision_assistant_path_config.yaml"
    try:
        with open(path_config_path, "r") as file:
            FileData = yaml.safe_load(file)
        config = FileData["vision_assistant_path_config"]
    except (KeyError, TypeError) as e:
        if logger is not None:
            logger.error(f"Error in path config file: {str(e)}")
        return list(REQUIRED_PATH_KEYS)
    except FileNotFoundError as e:
        if logger is not None:
            logger.error(f"Error opening path config file: {str(e)}")
        return list(REQUIRED_PATH_KEYS)

    invalid_keys = []
    for key in REQUIRED_PATH_KEYS:
        path = config.get(key)
        if not path_exists_with_timeout(path, logger=logger):
            if logger is not None:
                logger.error(f"Path config '{key}' is not valid: '{path}'")
            invalid_keys.append(key)

    return invalid_keys

def get_path_config(logger=None)->dict:
    """
    Returns the current path config as dict (empty dict if the config file can not be read).
    """
    package_share_directory = get_package_share_directory("pm_vision_manager")
    path_config_path = f"{package_share_directory}/vision_assistant_path_config.yaml"
    try:
        with open(path_config_path, "r") as file:
            FileData = yaml.safe_load(file)
        return dict(FileData["vision_assistant_path_config"])
    except (KeyError, TypeError, FileNotFoundError) as e:
        if logger is not None:
            logger.error(f"Error reading path config file: {str(e)}")
        return {}

def check_for_valid_path_config(logger=None)->bool:
    invalid_keys = get_invalid_path_config_keys(logger)
    if invalid_keys and logger is not None:
        logger.error("Path config file is not valid!")
    return len(invalid_keys) == 0


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
        if path_exists_with_timeout(process_file_path, logger=logger) and path_exists_with_timeout(camera_file_path, logger=logger):
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
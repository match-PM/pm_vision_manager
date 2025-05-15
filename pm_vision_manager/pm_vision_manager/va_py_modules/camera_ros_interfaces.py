
from rclpy.node import Node
from rosidl_runtime_py.convert import message_to_ordereddict, get_message_slot_types
from rosidl_runtime_py.utilities import get_service #, get_interface, get_message
import time

class CameraExposureTimeError(Exception):
    def __init__(self, message="Camera exposure time service is not available!"):
        self.message = message
        super().__init__(self.message)

class CameraSetCoaxLightError(Exception):
    def __init__(self, message="Camera set coax light service is not available!"):
        self.message = message
        super().__init__(self.message)

def percentage_to_value(percentage, min_value, max_value):
    # Ensure that the percentage is within the valid range (0% to 100%)
    percentage = max(0, min(percentage, 100))
    
    # Convert the percentage to the original value
    value = (percentage / 100) * (max_value - min_value) + min_value
    
    return value


class CameraExposureTimeInterface:
    def __init__(self, node:Node):
        self.available = False
        self.node = node
        self.srv_client_exposure_time = None
        self.srv_type_exposure_time = None
        self.min_val_exposure_time = None
        self.max_val_exposure_time = None

    def init(self, config:dict):
        # Instanciating Exposure Time interface from yaml
        if config == {}:
            self.node.get_logger().warn("Camera exposure_time not defined!")
            return

        try:
            self.srv_client_exposure_time = config["srv_client_name"]
            self.srv_type_exposure_time = config["srv_type"]
            self.min_val_exposure_time = config["min_val"]
            self.max_val_exposure_time = config["max_val"]
            self.camera_exposure_time_set_value = 0

            service_metaclass = get_service(self.srv_type_exposure_time)

            self.client_exposure_time = self.node.create_client(service_metaclass, self.srv_client_exposure_time)

            if not self.client_exposure_time.wait_for_service(timeout_sec=1.0):
                self.node.get_logger().warn("Exposure time client not online!")
                raise CameraExposureTimeError

            self.available = True

        except KeyError as e:
            self.node.get_logger().warn(f"Error in camera exposure_time config or not defined!")

        except ValueError as e:
            self.node.get_logger().warn(f"Service interface '{self.srv_type_exposure_time}' not installed!")

        except CameraExposureTimeError as e:
            self.node.get_logger().warn(str(e))
        
        except Exception as e:
            self.node.get_logger().error(str(type(e).__name__))
            self.node.get_logger().error(str(e))

        finally:
            if not self.available:
                self.node.get_logger().warn("Camera exposure time interface not available!")
            else:
                self.node.get_logger().info("Camera exposure time interface is available!")

    def set_camera_exposure_time(self, exposure_value_percent)->bool:
        if self.available:
            # Convert the percentage to a actual exposue time value
            exposure_time = percentage_to_value(exposure_value_percent,
                                    self.min_val_exposure_time,
                                    self.max_val_exposure_time)
            
            # Only if is an valid value (This should normaly be the case, but I the config is wrong it might not)
            if (exposure_time <= self.max_val_exposure_time) and (
                exposure_time >= self.min_val_exposure_time):
                
                if self.camera_exposure_time_set_value != exposure_value_percent:
                    service_request = get_service(self.srv_type_exposure_time).Request()
                    value_key = None
                    for _key, _value in service_request.get_fields_and_field_types().items():
                        if _value == 'double' or _value == 'float':
                            value_key = _key
                    if value_key is None:
                        self.node.get_logger().error(f"No field of type 'double' found in service request of type '{self.srv_type_exposure_time}'.")
                        return False
                    setattr(service_request, value_key, exposure_time)
                    if not self.client_exposure_time.wait_for_service(timeout_sec=1.0):
                        self.node.get_logger().error("Camera exposure service not available!")
                    response = self.client_exposure_time.call(service_request)

                    self.camera_exposure_time_set_value = exposure_value_percent
                    self.node.get_logger().info(f"Camera exposure time set to '{exposure_time}'!")
                    time.sleep(1)
                    # This needs to be set so that in 'Execute Vision' the callback gets another image with the new exposure time
                    return True
            
            else:
                self.node.get_logger().error("Camera exposure time not set! Invalid bounds!")
                return False
        else:
            self.node.get_logger().warn("Camera exposure time not available!")
            return False

class CameraSetCoaxLightBoolInterface:
    def __init__(self, node:Node):
        self.available = False
        self.node = node
        self.srv_client__set_coax_light = None
        self.srv_type_set_coax_light = None
        self.coax_light_state = None

    def init(self, config:dict):
        if config == {}:
            self.node.get_logger().warn(f"Camera set_coax_light_bool not defined!")
            return

        # Instanciating Exposure Time interface from yaml
        try:
            self.client_set_coax_light = config["srv_client_name"]
            self.srv_type_set_coax_light = config["srv_type"]

            service_metaclass = get_service(self.srv_type_set_coax_light)

            self.client_set_coax_light = self.node.create_client(service_metaclass, self.client_set_coax_light)

            if not self.client_set_coax_light.wait_for_service(timeout_sec=1.0):
                self.node.get_logger().warn("Set coax light bool client not online!")
                raise CameraExposureTimeError

            self.available = True

        except KeyError as e:
            self.node.get_logger().warn(f"Error in camera set_coax_light_bool config or not defined!")

        except ValueError as e:
            self.node.get_logger().warn(f"Service interface '{self.srv_type_set_coax_light}' not installed!")

        except CameraSetCoaxLightError as e:
            self.node.get_logger().warn(str(e))
        
        except Exception as e:
            self.node.get_logger().error(str(type(e).__name__))
            self.node.get_logger().error(str(e))

        finally:
            if not self.available:
                self.node.get_logger().warn("Camera set coax light bool interface not available!")
            else:
                self.node.get_logger().info("Camera set coax light bool interface is available!")

    def set_coax_light(self, set_value)->bool:
        if self.available:
                
            if self.coax_light_state != set_value:
                service_request = get_service(self.srv_type_set_coax_light).Request()
                value_key = None
                for _key, _value in service_request.get_fields_and_field_types().items():
                    self.node.get_logger().error(f"{_value}")
                    self.node.get_logger().error(f"{_key}")
                    self.node.get_logger().error(f"")
                    if _value == 'boolean':
                        value_key = _key
                if value_key is None:
                    self.node.get_logger().error(f"No field of type 'bool' found in service request of type '{self.srv_type_set_coax_light}'.")
                    return False
                setattr(service_request, value_key, set_value)
                if not self.client_set_coax_light.wait_for_service(timeout_sec=1.0):
                    self.node.get_logger().error("Camera set coax light service not available!")
                response = self.client_set_coax_light.call(service_request)

                self.coax_light_state = set_value
                self.node.get_logger().info(f"Camera coax light state set to '{set_value}'!")
                time.sleep(2)
                return True
            return False
        
        else:
            self.node.get_logger().warn("Camera exposure time not available!")
            return False
        


class CameraSetCoaxLightInterface:
    def __init__(self, node:Node):
        self.available = False
        self.node = node
        self.srv_client = None
        self.srv_type = None
        self.min_val = None
        self.max_val = None

    def init(self, config:dict):
        # Instanciating Exposure Time interface from yaml
        if config == {}:
            self.node.get_logger().warn(f"Camera set_coax_light_int not defined!")
            return
        
        try:
            self.srv_client = config["srv_client_name"]
            self.srv_type = config["srv_type"]
            self.min_val = config["min_val"]
            self.max_val = config["max_val"]
            self.set_value = 0

            service_metaclass = get_service(self.srv_type)
            self.client = self.node.create_client(service_metaclass, self.srv_client)

            if not self.client.wait_for_service(timeout_sec=1.0):
                self.node.get_logger().warn("Camera set coax light client not online!")
                raise CameraSetCoaxLightError

            self.available = True

        except KeyError as e:
            self.node.get_logger().warn(f"Error in camera set coax config or not defined!")

        except ValueError as e:
            self.node.get_logger().warn(f"Service interface '{self.srv_type}' not installed!")

        except CameraSetCoaxLightError as e:
            self.node.get_logger().warn(str(e))
        
        except Exception as e:
            self.node.get_logger().error(str(type(e).__name__))
            self.node.get_logger().error(str(e))

        finally:
            if not self.available:
                self.node.get_logger().warn("Camera set coax interface not available!")
            else:
                self.node.get_logger().info("Camera set coax interface is available!")

    def set_coax_light(self, value_percent: int)->bool:
        if self.available:
            # Convert the percentage to a actual exposue time value
            value = percentage_to_value(value_percent,
                                    self.min_val,
                                    self.max_val)
            
            # Only if is an valid value (This should normaly be the case, but I the config is wrong it might not)
            if (value <= self.max_val) and (
                value >= self.min_val):

                if int(self.set_value) != int(value):
                    service_request = get_service(self.srv_type).Request()
                    value_key = None
                    value_type = None
                    for _key, _value in service_request.get_fields_and_field_types().items():
                        self.node.get_logger().debug(f"{_key}")
                        self.node.get_logger().debug(f"{_value}")
                        self.node.get_logger().debug(f"")

                        if _value == 'integer' or _value == 'int' or _value == 'double' or _value == 'float'or _value == 'uint8':
                            value_key = _key
                            value_type = _value
                    if value_key is None:
                        self.node.get_logger().error(f"No field of type 'integer'/'int'/'double'/'float' found in service request of type '{self.srv_type}'.")
                        return False
                    
                    if value_type == 'integer' or value_type == 'int' or value_type == 'uint8':
                        value = int(value)
                    
                    setattr(service_request, value_key, value)

                    if not self.client.wait_for_service(timeout_sec=1.0):
                        self.node.get_logger().error("Camera set coax light service not available!")

                    self.node.get_logger().error(f"{str(service_request)}")
                    response = self.client.call(service_request)

                    self.set_value = value

                    self.node.get_logger().info(f"Camera set coax light to '{value}'!")
                    # This needs to be set so that in 'Execute Vision' the callback gets another image with the new exposure time
                    time.sleep(1)
                    return True
                return False
                                        
            else:
                self.node.get_logger().error("Camera coax light value not set! Invalid bounds!")
                return False
    
        else:
            self.node.get_logger().warn("Camera set coax light int not available!")
            return False
        
class CameraRingLightInterface:
    def __init__(self, node:Node):
        self.available = False
        self.node = node
        self.srv_client = None
        self.srv_type = None

    def init(self, config:dict):
        # Instanciating Exposure Time interface from yaml
        if config == {}:
            self.node.get_logger().warn(f"Camera ring light interface not defined!")
            return
        
        try:
            self.srv_client = config["srv_client_name"]
            self.srv_type = config["srv_type"]
            self.set_value_bools = []
            self.set_value_rgb = []
            
            service_metaclass = get_service(self.srv_type)

            self.client = self.node.create_client(service_metaclass, self.srv_client)

            if not self.client.wait_for_service(timeout_sec=1.0):
                self.node.get_logger().warn("Camera set coax light client not online!")
                raise CameraSetCoaxLightError

            self.available = True

        except KeyError as e:
            self.node.get_logger().warn(f"Error in camera ring light config or not defined!")

        except ValueError as e:
            self.node.get_logger().warn(f"Service interface '{self.srv_type}' not installed!")

        except CameraSetCoaxLightError as e:
            self.node.get_logger().warn(str(e))
        
        except Exception as e:
            self.node.get_logger().error(str(type(e).__name__))
            self.node.get_logger().error(str(e))

        finally:
            if not self.available:
                self.node.get_logger().warn("Camera set ring light interface not available!")
            else:
                self.node.get_logger().info("Camera set ring light interface is available!")

    def set_ring_light(self, bool_list: list[bool], rgb_list:list[float]):
        if self.available:
            
            if self.set_value_bools != bool_list or self.set_value_rgb != rgb_list:

                service_request = get_service(self.srv_type).Request()
                #value_key = None
                #value_type = None
                # for _key, _value in service_request.get_fields_and_field_types().items():
                #     self.node.get_logger().debug(f"{_key}")
                #     self.node.get_logger().debug(f"{_value}")
                #     self.node.get_logger().debug(f"")

                #     if _value == 'integer' or _value == 'int' or _value == 'double' or _value == 'float'or _value == 'uint8':
                #         value_key = _key
                #         value_type = _value
                # if value_key is None:
                #     self.node.get_logger().error(f"No field of type 'integer'/'int'/'double'/'float' found in service request of type '{self.srv_type}'.")
                #     return False
                
                # if value_type == 'integer' or value_type == 'int' or value_type == 'uint8':
                #     value = int(value)
                
                setattr(service_request, 'turn_on', bool_list)
                setattr(service_request,'rgb',rgb_list)

                if not self.client.wait_for_service(timeout_sec=1.0):
                    self.node.get_logger().error("Camera ring service not available!")

                self.node.get_logger().error(f"{str(service_request)}")
                response = self.client.call(service_request)

                self.set_value_bools = bool_list
                self.set_value_rgb = rgb_list

                self.node.get_logger().info(f"Camera ring light set to '{bool_list}' with intensity of {rgb_list}!")
                # This needs to be set so that in 'Execute Vision' the callback gets another image with the new exposure time
                time.sleep(1)
                return True
            return False
        else:
            self.node.get_logger().warn("Camera ring light int not available!")
            return False

class CameraRosInterfaces:
    def __init__(self,node:Node):
        self.node = node
        self.exposure_time_interface = CameraExposureTimeInterface(self.node)
        self.set_coax_light_bool_interface = CameraSetCoaxLightBoolInterface(self.node)
        self.set_coax_light_interface = CameraSetCoaxLightInterface(self.node)
        self.set_ring_light_interfaces = CameraRingLightInterface(self.node)

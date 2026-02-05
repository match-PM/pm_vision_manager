#from rclpy.logging import logger
import numpy as np
import cv2 # OpenCV library
from math import pi
import math
from copy import copy, deepcopy
from typing import Union

from geometry_msgs.msg import Point


import pm_vision_manager.va_py_modules.vision_utils as vu
import pm_vision_interfaces.msg as pvimsg 

class ImageNotGrayScaleError(Exception):
    def __init__(self, message="Processing image is not gray scale. Convert to gray scale before calling this function!"):
        self.message = message
        super().__init__(self.message)

class ImageNotBinaryError(Exception):
    def __init__(self, message="Processing image is not binary. Convert to binary before calling this function!"):
        self.message = message
        super().__init__(self.message)

class ImageProcessingHandler:

    MODE_EXECUTE = 0
    MODE_LOOP = 1
    MODE_CROSSVAL = 2
    MODE_IMAGE_LOOP = 3
    
    def __init__(self, logger = None):
        self._initial_image: np.ndarray = None
        self._processing_image: np.ndarray = None
        self._display_frame: np.ndarray = None
        self._final_image: np.ndarray = None
        self._processed_image_overlay: np.ndarray = None
        self.frame_visual_elements = None
        self.frame_buffer = []
        self.logger = logger
        self.visionOK = True

        self._vision_results_dict = {}
        self._vision_results_list = []

        self._debug_log_list = []

        self._quality_scores_dict = {}

        self.process_db_path = None

        self.pixelsize = None
        self.magnification = None
        self.camera_axis_1 = None
        self.camera_axis_2 = None
        self.camera_axis_1_angle = None
        self.camera_axis_2_angle = None
        self.pixelPROum = None
        self.umPROpixel = None
        self.cross_val_running = False
        self.save_in_cross_val = False
        self.show_input_and_output_image = True
        self.exposure_time_interface_available = False
        self.current_image_name = ""
        self.screen_height = 1080
        text_scale = 5 # scale of written text in the images
        line_scale = 2 # scale of lines in the images
        self.vision_routine_done = False

        # Init for camera clients
        self.client_exposure_time = None
        self.srv_client_exposure_time = None
        self.srv_type_exposure_time = None
        self.min_val_exposure_time = None
        self.max_val_exposure_time = None
        self.exposure_time_interface_available = False
        self.camera_exposure_time_set_value = None
        # object that contains all vision results
        self._vision_response = pvimsg.VisionResponse()
        self._mode = self.MODE_EXECUTE
    
    
    def set_mode(self, mode:int):
        """
        Set the mode of the image processing handler.
        """
        if mode == self.MODE_EXECUTE:
            self._mode = self.MODE_EXECUTE
        elif mode == self.MODE_LOOP:
            self._mode = self.MODE_LOOP
        else:
            self._mode = self.MODE_EXECUTE

    def get_mode(self)->int:
        """
        Get the mode of the image processing handler.
        """
        return self._mode    
    
    def set_camera_parameter(self, pixelsize: float, 
                             magnification: float, 
                             camera_axis_1:str, 
                             camera_axis_2:str, 
                             camera_axis_1_angle:float, 
                             camera_axis_2_angle:str):
        
        self.pixelsize = pixelsize
        self.magnification = magnification
        self.camera_axis_1 = camera_axis_1
        self.camera_axis_2 = camera_axis_2
        self.camera_axis_1_angle = camera_axis_1_angle
        self.camera_axis_2_angle = camera_axis_2_angle
        self.ROI_CS_CV_top_left_x = None
        self.ROI_CS_CV_top_left_y = None
        self.ROI_CS_CV_bottom_right_x = None
        self.ROI_CS_CV_bottom_right_y = None

    def set_image_output_config(self, screen_heigt:int, show_input_and_output_image: bool):
        self.screen_height = screen_heigt
        self.show_input_and_output_image = show_input_and_output_image

    def set_initial_image(self, image):
        self._initial_image = np.copy(image)

    def get_initial_image(self):
        # returns a copy of the initial image
        return deepcopy(self._initial_image)

    def get_processing_image(self):
        """
        Returns a copy of the current processing image.
        """
        return np.copy(self._processing_image)
    
    def init_begin(self):
        if (self.pixelsize is None or 
            self.magnification is None or 
            self.camera_axis_1 is None or 
            self.camera_axis_2 is None or 
            self.camera_axis_1_angle is None or 
            self.camera_axis_2_angle is None):
            raise AttributeError("Camera parameter not initialized. Call set_camera_parameter before!")
        
        self.pixelPROum = self.magnification / self.pixelsize
        self.umPROpixel = self.pixelsize / self.magnification
        
        self._processing_image = deepcopy(self._initial_image)
        self._display_frame = deepcopy(self._processing_image)
        self.frame_visual_elements = np.zeros((self._initial_image.shape[0], self._initial_image.shape[1], 3), dtype = np.uint8)

        self.img_width  = self._initial_image.shape[1] # width of the image in pixel
        self.img_height = self._initial_image.shape[0]  # height of the image in pixel
        self.fov_width  = self.umPROpixel*self.img_width 
        self.fov_height = self.umPROpixel*self.img_height
        self.roi_used:bool =  False
        self.set_vision_ok(True)
        
        self.frame_buffer.clear()

        # clear vision results
        self._vision_results_list.clear()       # delete this in the future
        self.clear_vision_results()

    def init_results(self):
        # Add border to vision elements based on `get_vision_ok()`
        color = (0, 255, 0) if self.get_vision_ok() else (0, 0, 255)
        cv2.rectangle(self.frame_visual_elements, (0, 0), 
                    (self.frame_visual_elements.shape[1], self.frame_visual_elements.shape[0]), 
                    color, 3)
        
        show_vision_elements_in_output_image = True

        # Overlay vision elements on display frame
        self._display_frame = self.create_vision_element_overlay(self._display_frame, 
                                                                self.frame_visual_elements, 
                                                                self.logger)

        self._processed_image_overlay = deepcopy(self._display_frame)

        self._vision_results_dict["vision_results"] = self._vision_results_list
        
        initial_image = self.get_initial_image()

        # Handle `_initial_image` grayscale case
        if len(initial_image) < 3:
            initial_image = cv2.cvtColor(initial_image, cv2.COLOR_GRAY2BGR)


        # Ensure `_display_frame` is initialized
        if self._display_frame is None:
            self._display_frame = initial_image.copy()
            return

        # Ensure `_display_frame` is also 3-channel BGR
        if len(self._display_frame.shape) < 3:
            self._display_frame = cv2.cvtColor(self._display_frame, cv2.COLOR_GRAY2BGR)

        # Ensure same width before vconcat
        if initial_image.shape[1] != self._display_frame.shape[1]:
            self.logger.warning("Resizing images to match width.")

        # Ensure same data type
        if initial_image.dtype != self._display_frame.dtype:
            self._display_frame = self._display_frame.astype(initial_image.dtype)

        if show_vision_elements_in_output_image:
            initial_image = self.create_vision_element_overlay(initial_image, 
                                                                self.frame_visual_elements, 
                                                                self.logger)
        # Concatenate safely
        if self.show_input_and_output_image:
            self._display_frame = cv2.vconcat([initial_image, self._display_frame])

        self._final_image = deepcopy(self._display_frame)
        
        # Sort results if there are any
        self._sort_results()
            # resize display frame
            #self._display_frame=vu.image_resize(self._display_frame, height = (self.screen_height-100))

    def get_results(self)->dict:
        return self._vision_results_dict
    
    def get_display_image(self):
        return deepcopy(self._display_frame)
    
    def get_processed_image_overlay(self):
        return  self._processed_image_overlay

    def is_process_image_grayscale(self)->bool:
        # Check the number of color channels
        if len(self._processing_image.shape) == 2 or (len(self._processing_image.shape) == 3 and self._processing_image.shape[2] == 1):
            return True  # Grayscale image
        else:
            return False  # Color image
        #elif len(self._processing_image.shape) == 3 and self._processing_image.shape[2] == 3:

    def is_process_image_binary(self) -> bool:
        image = self._processing_image

        # 1. Check if image is single-channel (2D)
        if image.ndim != 2:
            print("Image is not single-channel")
            return False

        # 2. Check if dtype is uint8
        if image.dtype != np.uint8:
            print("Image is not uint8")
            return False

        # 3. Get unique values
        unique_values = np.unique(image)
        print("Unique values:", unique_values)

        # 4. Accept if it's either {0}, {255}, or {0, 255}
        binary_values = {0, 255}
        if set(unique_values).issubset(binary_values):
            return True

        return False

        
    def set_cross_val_running(self, bool_value:bool):
        self.cross_val_running = bool_value

    def set_processing_image(self, processing_image:np.ndarray):
        self._processing_image = np.copy(processing_image)
        #self.frame_buffer.append(self._processing_image)
        self._display_frame=self.adaptImagewithROI(self._display_frame, np.copy(self._processing_image))

    def set_camera_exposure_time(self, value)->bool:
        """
        This function should be overwritten from in the vision assistant_class
        """
        pass

    def set_camera_coax_light_bool(self, set_state)->bool:
        """
        This function should be overwritten from in the vision assistant_class
        """
        pass
    
    def set_camera_coax_light(self, value)->bool:
        """
        This function should be overwritten from in the vision assistant_class
        """
        pass

    def set_ring_light(self, bool_list, rgb_list)->bool:
        """
        This function should be overwritten from in the vision assistant_class
        """
        pass
    
    def disable_all_lights(self)->bool:
        """
        This function should be overwritten from in the vision assistant_class
        """
        self.set_camera_coax_light_bool(False)
                
        self.set_ring_light([False, False, False, False],
                            [0, 0, 0])
        
        self.set_camera_coax_light(0)
        return True

    def get_visual_elements_canvas(self):
        if self.roi_used:
            canvas = self.frame_visual_elements[self.ROI_CS_CV_top_left_y:self.ROI_CS_CV_bottom_right_y, self.ROI_CS_CV_top_left_x:self.ROI_CS_CV_bottom_right_x]
            return canvas
        else:
            return np.copy(self.frame_visual_elements)
            
    def apply_visual_elements_canvas(self, canvas):
        if self.roi_used:
            self.frame_visual_elements = self.adaptImagewithROI(self.frame_visual_elements, canvas)
        else:
            self.frame_visual_elements = canvas

    def adaptImagewithROI(self, disp_frame, prcs_frame):

        if len(prcs_frame.shape) == 2 or (len(prcs_frame.shape) == 3 and prcs_frame.shape[2] == 1):
            prcs_frame = cv2.cvtColor(prcs_frame, cv2.COLOR_GRAY2BGR)

        if len(disp_frame.shape) == 2 or (len(disp_frame.shape) == 3 and disp_frame.shape[2] == 1):
            disp_frame = cv2.cvtColor(disp_frame, cv2.COLOR_GRAY2BGR)

        if self.roi_used:
            x_offset = self.ROI_CS_CV_top_left_x
            y_offset = self.ROI_CS_CV_top_left_y
            disp_frame[
                y_offset : y_offset + prcs_frame.shape[0],
                x_offset : x_offset + prcs_frame.shape[1],
            ] = prcs_frame
        else:
            disp_frame = prcs_frame
        return disp_frame
    
    def set_vision_ok(self, bool_value: bool)->None:
        self.visionOK = bool_value

    def get_vision_ok(self)->bool:
        return self.visionOK
    
    def get_final_image(self):
        """
        Returns the final image of the vision process.
        This image is not deleted when a new run starts.
        """
        return np.copy(self._final_image)
    
    def set_roi_settings(self, top_left_x:int, top_left_y:int, bottom_right_x:int, bottom_right_y:int):
        self.ROI_CS_CV_top_left_x = top_left_x
        self.ROI_CS_CV_top_left_y = top_left_y
        self.ROI_CS_CV_bottom_right_x = bottom_right_x
        self.ROI_CS_CV_bottom_right_y = bottom_right_y
        self.roi_used = True

    def set_image_metatdata(self, process_db_path:str, current_image_name:str):
        self.current_image_name = current_image_name
        self.process_db_path = process_db_path

    def set_process_db_path(self, process_db_path:str):
        self.process_db_path = process_db_path

    def CS_Conv_ROI_Pix_TO_Img_Pix(self, x_roi, y_roi):
        """
        This method converts coordinates that may be from an roi image to the coordinate system of the initial image.
        Origin of the cs is the top left corner.
        """
        if self.roi_used:
            x_img = self.ROI_CS_CV_top_left_x + x_roi
            y_img = self.ROI_CS_CV_top_left_y + y_roi
        else:
            x_img = x_roi
            y_img = y_roi
        return x_img, y_img
    
    def CS_Camera_TO_Image(self, x_val_c, y_val_c):
        """
        This method converts coordinates given in the camera coordinate system to coordinates defined in a image coordinate system in um.
        Origin of the image cs is the center of the image.
        ROI is not considered in this method.
        """
        if self.camera_axis_2_angle == "++":
            y_val_c = -y_val_c
        x_val_i = x_val_c * math.cos(
            2 * pi - vu.degrees_to_rads(self.camera_axis_1_angle)
        ) + y_val_c * math.sin(2 * pi - vu.degrees_to_rads(self.camera_axis_1_angle))
        y_val_i = -x_val_c * math.sin(
            2 * pi - vu.degrees_to_rads(self.camera_axis_1_angle)
        ) + y_val_c * math.cos(2 * pi - vu.degrees_to_rads(self.camera_axis_1_angle))
        return x_val_i, y_val_i

    def CS_Image_TO_Camera(self, x_val_i, y_val_i):
        """
        This method converts image coordinates in um in camera coordinates (which may be rotated to the image cooridnates system).
        Origin of the image cs is the center of the image.
        ROI is not considered in this method.
        """
        x_val_c = x_val_i * math.cos(vu.degrees_to_rads(self.camera_axis_1_angle)) + y_val_i * math.sin(vu.degrees_to_rads(self.camera_axis_1_angle))
        y_val_c = -x_val_i * math.sin(vu.degrees_to_rads(self.camera_axis_1_angle)) + y_val_i * math.cos(vu.degrees_to_rads(self.camera_axis_1_angle))
        if self.camera_axis_2_angle == "++":
            y_val_c = -y_val_c

        if self.camera_axis_2_angle == "-":

            if self.logger:
                self.logger.error("Using '-' for camera angle setting is deprecated. Use '++' instead!")
            
        return x_val_c, y_val_c
    
    def CS_Image_TO_Pixel(self, x_val_i, y_val_i):
        """
        This method converts coordinates given in um to coordinates in pixel.
        """
        # x_val_pix = int(round(self.pixelPROum * x_val_i))
        # y_val_pix = int(round(self.pixelPROum * y_val_i))
        x_val_pix = self.pixelPROum * x_val_i
        y_val_pix = self.pixelPROum * y_val_i
        return x_val_pix, y_val_pix

    def CS_Pixel_TO_Image(self, x_val_pix, y_val_pix):
        """
        This method convers coordinates given in pixel to coordinates in um.
        """
        x_val_i = x_val_pix * self.umPROpixel
        y_val_i = y_val_pix * self.umPROpixel
        return x_val_i, y_val_i

    def CS_CV_TO_camera_with_ROI(self, x_value:int, y_value:int):
        """
        Converts the image coordinates (origin top left) given (x and y value) to camera coordinate values.
        This is the method you should use when calculating camera coordinates. 
        """
        x_tl, y_tl = self.CS_Conv_ROI_Pix_TO_Img_Pix(x_value, y_value)

        x_center_pix, y_center_pix = self.CS_Conv_Pixel_Top_Left_TO_Center(self.img_width, self.img_height, x_tl, y_tl)

        x_center_image_um, y_center_image_um = self.CS_Pixel_TO_Image(x_center_pix, y_center_pix)

        x_cs_camera, y_cs_camera = self.CS_Image_TO_Camera(x_center_image_um, y_center_image_um)

        if self.logger:
            self.logger.debug(f"x_tl: {x_tl}, y_tl_ {y_tl}")
            self.logger.debug(f"x_center_pix: {x_center_pix}, y_center_pix {y_center_pix}")
            self.logger.debug(f"x_center_image_um: {x_center_image_um}, y_center_image_um {y_center_image_um}")
            self.logger.debug(f"x_cs_camera: {x_cs_camera}, y_cs_camera {y_cs_camera}")


        return x_cs_camera, y_cs_camera

    def get_quality_scores(self):
        return self._quality_scores_dict

    def set_quality_scores(self, function_name:str, quality_dict:dict):
        self._quality_scores_dict[function_name] = quality_dict

    def append_to_results(self, result:dict):
        self._vision_results_list.append(result)

    def append_vision_process_debug(self, log_str: str):
        self._debug_log_list.append(log_str)

    def get_vision_process_debug(self)->list:
        return self._debug_log_list

    def clear_vision_process_debug(self):
        self._debug_log_list = []

    def clear_vision_results(self):
        self._vision_response = pvimsg.VisionResponse()

    def get_vision_response(self)->pvimsg.VisionResponse:
        return self._vision_response
    
    def append_vision_obj_to_results(self, vision_obj: Union[pvimsg.VisionPoint, 
                                                             pvimsg.VisionCircle, 
                                                             pvimsg.VisionArea, 
                                                             pvimsg.VisionLine]):   
        """
        This method appends a vision object to the vision results.
        
        """
        if isinstance(vision_obj, pvimsg.VisionPoint):
            self._vision_response.results.points.append(vision_obj)
        elif isinstance(vision_obj, pvimsg.VisionCircle):
            self._vision_response.results.circles.append(vision_obj)
        elif isinstance(vision_obj, pvimsg.VisionArea):
            self._vision_response.results.areas.append(vision_obj)
        elif isinstance(vision_obj, pvimsg.VisionLine):
            self._vision_response.results.lines.append(vision_obj)
        else:
            raise ValueError("Vision object type not supported!")

    def new_vision_point_result(self)->pvimsg.VisionPoint:
        return pvimsg.VisionPoint()
    
    def new_vision_circle_result(self)->pvimsg.VisionCircle:
        return pvimsg.VisionCircle()
    
    def new_vision_area_result(self)->pvimsg.VisionArea:
        return pvimsg.VisionArea()
    
    def new_vision_line_result(self)->pvimsg.VisionLine:
        return pvimsg.VisionLine()
    
    def set_image_sharpness(self, sharpness_value: float):
        self._vision_response.results.image_sharpness.sharpness_value = sharpness_value
    
    def _sort_results(self):
        """
        This method sorts the vision results based on the type of the vision object.
        """
        #self._vision_response.results.points.sort(key=lambda x: x.axis_value_1)
        # Sort the circles according to their potential field value
        
        self._sort_result_circles()
        self._sort_result_points()

    def _sort_result_circles(self):
        if len(self._vision_response.results.circles) == 0:
            return
        
        potential_values = self._create_potential_field(self._vision_response.results.circles)
        # Create a list of tuples (circle, potential_value)
        circles_with_potential = list(zip(self._vision_response.results.circles, potential_values))
        # Sort the list by potential_value
        circles_with_potential.sort(key=lambda x: x[1])
        # Unzip the sorted list back into two lists
        sorted_circles, sorted_potentials = zip(*circles_with_potential)
        # Update the vision response with sorted circles
        self._vision_response.results.circles = list(sorted_circles)
        
    def _sort_result_points(self):
        if len(self._vision_response.results.points) == 0:
            return
        potential_values = self._create_potential_field(self._vision_response.results.points)
        # Create a list of tuples (point, potential_value)
        points_with_potential = list(zip(self._vision_response.results.points, potential_values))
        # Sort the list by potential_value
        points_with_potential.sort(key=lambda x: x[1])
        # Unzip the sorted list back into two lists
        sorted_points, sorted_potentials = zip(*points_with_potential)
        # Update the vision response with sorted points
        self._vision_response.results.points = list(sorted_points)
        
        
    def _create_potential_field(self, list_of_elements: Union[list[pvimsg.VisionPoint], 
                                                              list[pvimsg.VisionCircle], 
                                                              ])->list:
        """
        This method creates a potential field based on the given elements.
        The potential field is a list of floats.
        """
        list_of_points:list[Point] = []
        if not isinstance(list_of_elements, list):
            raise TypeError("list_of_elements must be a list of VisionPoint or VisionCircle objects.")
        
        if len(list_of_elements) == 0:
            return []
        
        if isinstance(list_of_elements[0], pvimsg.VisionPoint):
            for elem in list_of_elements:
                elem: pvimsg.VisionPoint
                point = Point()
                point.x = elem.axis_value_1 + (self.fov_width+self.fov_height)
                point.y = elem.axis_value_2 + (self.fov_width+self.fov_height)
                list_of_points.append(point)
        
        if isinstance(list_of_elements[0], pvimsg.VisionCircle):
            for elem2 in list_of_elements:
                elem2: pvimsg.VisionCircle
                point = Point()
                point.x = elem2.center_point.axis_value_1 + (self.fov_width+self.fov_height)
                point.y = elem2.center_point.axis_value_2 + (self.fov_width+self.fov_height)
                list_of_points.append(point)
        
        potential = self._create_potential_for_points(list_of_points)
        return potential
    
    def _create_potential_for_points(self, points: list[Point]) -> list[float]:
        
        if len(points) == 0:
            return []
        
        potential = []
        distances = []
        angles = []

        for point in points:
            dist = math.sqrt(point.x**2 + point.y**2)
            angle = math.atan2(point.y, point.x)
            distances.append(dist)
            angles.append(angle)

        distances = np.array(distances)
        angles = np.array(angles)

        # Normalize
        normalized_distances = distances / np.max(distances) if np.max(distances) > 0 else distances
        normalized_angles = (angles + math.pi) / math.tau  # Normalize to [0, 1]

        for dist, angle in zip(normalized_distances, angles):
            pot = 0.5 * (dist + angle) * (dist + angle + 1) + angle
            potential.append(pot)

        return potential
    
    @staticmethod
    def create_vision_element_overlay(displ_frame, vis_elem_frame, logger = None):
        # Add visual elements to the display frame
        if len(displ_frame.shape) < 3:
            displ_frame = cv2.cvtColor(displ_frame, cv2.COLOR_GRAY2BGR)
        if displ_frame.shape[:2] != vis_elem_frame.shape[:2]:
            logger.debug("The visual elements frame has not the same size as the display frame!")
            logger.debug("Visual elements frame shape: " + str(vis_elem_frame.shape))
            logger.debug("Display frame shape: " + str(displ_frame.shape))

        # Now create a mask of logo and create its inverse mask also
        mask_frame = cv2.cvtColor(vis_elem_frame, cv2.COLOR_BGR2GRAY)
        _, mask = cv2.threshold(mask_frame, 10, 255, cv2.THRESH_BINARY)
        mask_inv = cv2.bitwise_not(mask)
        # Now black-out the area of logo in ROI
        img1_bg = cv2.bitwise_and(displ_frame, displ_frame, mask=mask_inv)
        # Take only region of logo from logo image.
        img2_fg = cv2.bitwise_and(vis_elem_frame, vis_elem_frame, mask=mask)
        # Put logo in ROI and modify the main image
        _displ_frame = np.copy(cv2.add(img1_bg, img2_fg))
        return _displ_frame
    
    @staticmethod
    def CS_Conv_Pixel_Top_Left_TO_Center(img_width, img_height, x_tl, y_tl):
        """
        Converts image coordinates given in top left origin to center origin. 
        """
        # x_center = int(round(x_tl - img_width / 2))
        # y_center = int(round(img_height / 2 - y_tl))
        x_center = x_tl - img_width / 2.0
        y_center = img_height / 2.0 - y_tl
        return x_center, y_center
    
    @staticmethod
    def CS_Conv_Pixel_Center_TO_Top_Left(img_width, img_height, x_center, y_center):
        """
        Converts image coordinates given in center origin to top left origin. 
        """
        x_tl = int(round(img_width / 2) + x_center)
        y_tl = int(round(img_height / 2) - y_center)
        # x_tl = (img_width / 2.0) + x_center
        # y_tl = (img_height / 2.0) - y_center
        return x_tl, y_tl

# def plot_grid_heatmap(grid, potential, rows, cols):
#     import matplotlib.pyplot as plt
#     # Convert flat potential list to 2D array for heatmap
#     potential_grid = np.array(potential).reshape((rows, cols))

#     plt.imshow(potential_grid, origin='lower', cmap='viridis', interpolation='nearest')
#     plt.colorbar(label='Potential')
#     plt.xlabel('X Coordinate')
#     plt.ylabel('Y Coordinate')
#     plt.title('Grid Potential Heat Map')
#     plt.show()

if __name__ == "__main__":
   pass

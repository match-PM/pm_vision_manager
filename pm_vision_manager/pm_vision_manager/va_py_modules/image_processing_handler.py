#from rclpy.logging import logger
import numpy as np
import cv2 # OpenCV library
from math import pi
import math
from copy import copy, deepcopy
from typing import Union

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
    def __init__(self, logger = None):
        self._initial_image: np.ndarray = None
        self._processing_image: np.ndarray = None
        self._display_frame: np.ndarray = None
        self._final_image: np.ndarray = None
        self.frame_visual_elements = None
        self.frame_buffer = []
        self.logger = logger
        self.visionOK = True

        self._vision_results_dict = {}
        self._vision_results_list = []
        
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
        return self._initial_image

    def get_processing_image(self):
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

        self.img_width  = self._initial_image.shape[1]
        self.img_height = self._initial_image.shape[0]
        self.fov_width  = self.umPROpixel*self.img_width 
        self.fov_height = self.umPROpixel*self.img_height
        self.roi_used:bool =  False
        self.set_vision_ok(True)
        
        self.frame_buffer.clear()

        # clear vision results
        self._vision_results_list.clear()       # delete this in the future
        self.clear_vision_results()

    def init_results(self):
        # add bool boarder to vision elements
        if not self.get_vision_ok():
            cv2.rectangle(self.frame_visual_elements,(0,0),(self.frame_visual_elements.shape[1],self.frame_visual_elements.shape[0]),(0,0,255),3)
        else:
            cv2.rectangle(self.frame_visual_elements,(0,0),(self.frame_visual_elements.shape[1],self.frame_visual_elements.shape[0]),(0,255,0),3)
        
        # lay vision elements over display frame
        self._display_frame = self.create_vision_element_overlay(self._display_frame,self.frame_visual_elements,self.logger)
        self._vision_results_dict["vision_results"] = self._vision_results_list

        if len(self._initial_image.shape)<3:
            _initial_image = cv2.cvtColor(self._initial_image,cv2.COLOR_GRAY2BGR)
        else:
            _initial_image = self._initial_image

        if self.show_input_and_output_image:
            self._display_frame = cv2.vconcat([_initial_image, self._display_frame])

        self._final_image = self.get_display_image()
        # resize display frame
        #self._display_frame=vu.image_resize(self._display_frame, height = (self.screen_height-100))

    def get_results(self)->dict:
        return self._vision_results_dict
    
    def get_display_image(self):
        return deepcopy(self._display_frame)
    
    def is_process_image_grayscale(self)->bool:
        # Check the number of color channels
        if len(self._processing_image.shape) == 2 or (len(self._processing_image.shape) == 3 and self._processing_image.shape[2] == 1):
            return True  # Grayscale image
        else:
            return False  # Color image
        #elif len(self._processing_image.shape) == 3 and self._processing_image.shape[2] == 3:

    def is_process_image_binary(self)->bool:
        unique_values = np.unique(self._processing_image)
        print(unique_values)
        if len(unique_values) <= 2:
            return True  # Binary image
        else:
            return False
        
    def set_cross_val_running(self, bool_value:bool):
        self.cross_val_running = bool_value

    def set_processing_image(self, processing_image:np.ndarray):
        self._processing_image = np.copy(processing_image)
        #self.frame_buffer.append(self._processing_image)
        self._display_frame=self.adaptImagewithROI(self._display_frame, np.copy(self._processing_image))

    def set_camera_exposure_time(self, value):
        """
        This function should be overwritten from in the vision assistant_class
        """
        pass
    
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
        if self.camera_axis_2_angle == "-":
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
        x_val_c = x_val_i * math.cos(
            vu.degrees_to_rads(self.camera_axis_1_angle)
        ) + y_val_i * math.sin(vu.degrees_to_rads(self.camera_axis_1_angle))
        y_val_c = -x_val_i * math.sin(
            vu.degrees_to_rads(self.camera_axis_1_angle)
        ) + y_val_i * math.cos(vu.degrees_to_rads(self.camera_axis_1_angle))
        if self.camera_axis_2_angle == "-":
            y_val_c = -y_val_c
        return x_val_c, y_val_c
    
    def CS_Image_TO_Pixel(self, x_val_i, y_val_i):
        """
        This method converts coordinates given in um to coordinates in pixel.
        """
        x_val_pix = int(round(self.pixelPROum * x_val_i))
        y_val_pix = int(round(self.pixelPROum * y_val_i))
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
        x_center_pix, y_center_pix = self.CS_Conv_Pixel_Top_Left_TO_Center(
            self.img_width, self.img_height, x_tl, y_tl
        )
        x_center_image_um, y_center_image_um = self.CS_Pixel_TO_Image(x_center_pix, y_center_pix)

        x_cs_camera, y_cs_camera = self.CS_Image_TO_Camera(x_center_image_um, y_center_image_um)

        return x_cs_camera, y_cs_camera
    
    def append_to_results(self, result:dict):
        self._vision_results_list.append(result)

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
        x_center = int(round(x_tl - img_width / 2))
        y_center = int(round(img_height / 2 - y_tl))
        return x_center, y_center
    
    @staticmethod
    def CS_Conv_Pixel_Center_TO_Top_Left(img_width, img_height, x_center, y_center):
        """
        Converts image coordinates given in center origin to top left origin. 
        """
        x_tl = int(round(img_width / 2) + x_center)
        y_tl = int(round(img_height / 2) - y_center)
        return x_tl, y_tl
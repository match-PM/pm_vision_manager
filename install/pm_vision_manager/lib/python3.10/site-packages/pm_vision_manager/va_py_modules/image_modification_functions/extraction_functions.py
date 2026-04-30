import cv2
import numpy as np
# import logger RRecu
from rclpy.impl.rcutils_logger import RcutilsLogger
from pm_vision_manager.va_py_modules.image_processing_handler import ImageProcessingHandler, ImageNotBinaryError, ImageNotGrayScaleError


def extract_color_areas(image_processing_handler: ImageProcessingHandler, 
                        lower_hue, 
                        lower_saturation, 
                        lower_value, 
                        upper_hue, 
                        upper_saturation, 
                        upper_value,
                        logger:RcutilsLogger = None)->bool:
    
    if image_processing_handler.is_process_image_binary():
        raise ImageNotBinaryError(message="Image is binary. Color extraction is not possible. Make sure the image is not binary.")
    
    if image_processing_handler.is_process_image_grayscale():
        raise ImageNotGrayScaleError(message="Image is grayscale. Color extraction is not possible. Make sure the image is not grayscale.")

    # Define lower and upper bounds for color
    lower_bound = np.array([lower_hue, lower_saturation, lower_value], dtype=np.uint8)
    upper_bound = np.array([upper_hue, upper_saturation, upper_value], dtype=np.uint8)

    # Validate inputs
    if not isinstance(lower_bound, (list, np.ndarray)) or not isinstance(upper_bound, (list, np.ndarray)):
        raise ValueError("Lower and upper bounds must be lists or numpy arrays.")
    if len(lower_bound) != 3 or len(upper_bound) != 3:
        raise ValueError("Bounds must have exactly three elements (HSV values).")
    
    # Get the image

    image = image_processing_handler.get_processing_image()     # this is a copy
    
    # Convert to HSV color space
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # Create a mask for the specified color regions
    mask = cv2.inRange(hsv, lower_bound, upper_bound)
    
    # Apply the mask to extract the color regions
    color_regions = cv2.bitwise_and(image, image, mask=mask)
    
    image_processing_handler.set_processing_image(color_regions)

    return True

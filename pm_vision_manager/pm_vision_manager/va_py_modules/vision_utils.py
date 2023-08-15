import cv2
import subprocess
from math import pi
import numpy as np

def get_screen_resolution():
   output = subprocess.Popen('xrandr | grep "\*" | cut -d " " -f4', shell=True, stdout=subprocess.PIPE).communicate()[0]
   resolution = output.split()[0].split(b'x')
   return {'width':resolution[0],'height':resolution[1]}

def degrees_to_rads(deg):
  return (deg * pi) / 180.0

def rads_to_degrees(rad):
  return (180.0*rad)/pi

def rotate_image(image, angle):
  image_center = tuple(np.array(image.shape[1::-1]) / 2)
  rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
  result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
  return result

def image_resize(image, width=None, height = None, inter = cv2.INTER_AREA):
  dim = None
  (h,w)=image.shape[:2]

  if width is None and height is None:
    return image
  if width is None:
    r=height/float (h)
    dim = (int(w*r),height)
  else:
    r=width/float(w)
    dim=(width,int(h*r)) 
  resized = cv2.resize(image, dim ,interpolation=inter)
  return resized

if __name__ == '__main__':
  pass

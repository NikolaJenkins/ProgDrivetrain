from cscore import CameraServer as cs
import ntcore
import cv2
import json
import numpy as np
import time

def main():
   cs.enableLogging()
   camera = CameracsServer.startAutomaticCapture()
   width, height = 160, 120
   camera.setResolution(width, height)
   sink = cs.getVideo()
   while True:
      time, input_img = cvSink.grabFrame(input_img)
      hsv_img = cv2.cvtColor(input_img, cv2.COLOR_BGR2HSV)
      binary_img = cv2.inRange(hsv_img, (min_hue, min_sat, min_val), (max_hue, max_sat, max_val))
      if time == 0: # There is an error
         continue
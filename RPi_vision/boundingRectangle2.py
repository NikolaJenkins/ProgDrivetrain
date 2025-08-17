from cscore import CameraServer
import ntcore
import cv2
import json
import numpy as np
import time

IS_TABLE_HOST = True

# camera settings
X_RESOLUTION = 320
Y_RESOLUTION = 240
FRAME_RATE = 30
LINE_COLOR = (0, 255, 0)

# object detection requirements
MIN_CONTOUR_AREA = 200
CONTOUR_RECT_THRESHOLD = 0.8

# finds largest image within image with certain color
def find_largest_object(hsv_image: np.ndarray, min_threshold: np.array, max_threshold: np.array) -> np.ndarray:
    mask = cv2.inRange(hsv_image, min_threshold, max_threshold)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        return max(contours, key = cv2.contourArea)
    
# checks if contour is shaped like object
def contour_is_coral(contour: np.ndarray) -> bool:
    if cv2.contourArea(contour) < MIN_CONTOUR_AREA:
        # print('too small contour area')
        return False
    
    # gets smallest convex polygon that fits around contour
    contour_hull = cv2.convexHull(contour)
    # gets smallest rectangle that fits around contour
    rectangle = cv2.minAreaRect(contour_hull)
    width = rectangle[1][0]
    height = rectangle[1][1]
    area = width * height
    # print('contour match') if cv2.contourArea(contour_hull) / area > CONTOUR_RECT_THRESHOLD else print ('no contour match')
    return cv2.contourArea(contour_hull) / area > CONTOUR_RECT_THRESHOLD

def main():
    # connect to server
    nt_instance = ntcore.NetworkTableInstance.getDefault()

    # host or client?
    if IS_TABLE_HOST:
        nt_instance.startServer()
    else:
        nt_instance.setServerTeam(3636)
        nt_instance.startClient4("visionPi")

    # vision table
    vision_nt = nt_instance.getTable('Vision')
    vision_nt.putNumber('min hue', 0.0)
    vision_nt.putNumber('min sat', 0.0)
    vision_nt.putNumber('min val', 0.0)
    vision_nt.putNumber('max hue', 180.0)
    vision_nt.putNumber('max sat', 255.0)
    vision_nt.putNumber('max val', 255.0)

    # set up camera
    CameraServer.startAutomaticCapture()
    CameraServer.enableLogging()
    cv_sink = CameraServer.getVideo()
    output_stream = CameraServer.putVideo('Vision', X_RESOLUTION, Y_RESOLUTION)

    img = np.zeros(shape=(X_RESOLUTION, Y_RESOLUTION, 3), dtype=np.uint8)

    while True:
        # convert from bgr to hsv
        time, img = cv_sink.grabFrame(img)
        frame_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # adjust thresholds
        min_hue = vision_nt.getNumber('min hue', 0.0)
        min_sat = vision_nt.getNumber('min sat', 0.0)
        min_val = vision_nt.getNumber('min val', 0.0)
        max_hue = vision_nt.getNumber('max hue', 0.0)
        max_sat = vision_nt.getNumber('max sat', 0.0)
        max_val = vision_nt.getNumber('max val', 0.0)
        min_color_threshold = np.array([min_hue, min_sat, min_val])
        max_color_threshold = np.array([max_hue, max_sat, max_val])

        # find contour
        contour = find_largest_object(frame_hsv, min_color_threshold, max_color_threshold)

        # draw rectangle on stream
        if contour is not None and contour_is_coral(contour):
            rect = cv2.minAreaRect(contour)
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            cv2.drawContours(img, [box], -1, LINE_COLOR, 2) 

        output_stream.putFrame(img)

main()
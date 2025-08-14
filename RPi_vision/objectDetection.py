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
MIN_COLOR_THRESHOLD = np.array([3, 80, 80])
MAX_COLOR_THRESHOLD = np.array([6, 255, 255])
MIN_CONTOUR_AREA = 400
CONTOUR_RECT_THRESHOLD = 0.9

# finds largest image within image with certain color
def find_largest_object(hsv_image: np.ndarray) -> np.ndarray:
    mask = cv2.inRange(hsv_image, MIN_COLOR_THRESHOLD, MAX_COLOR_THRESHOLD)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        return max(contours, key = cv2.contourArea)
    
# checks if contour is shaped like object
def contour_is_coral(contour: np.ndarray) -> bool:
    if cv2.contourArea(contour) < MIN_CONTOUR_AREA:
        return False
    
    # gets smallest convex polygon that fits around contour
    contour_hull = cv2.convexHull(contour)
    # gets smallest rectangle that fits around contour
    rectangle = cv2.minAreaRect(contour_hull)
    width = rectangle[1][0]
    height = rectangle[1][1]
    area = width * height
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
        contour = find_largest_object(frame_hsv)

        # draw rectangle on stream
        if contour is not None and contour_is_coral(contour):
            rect = cv2.minAreaRect(contour)
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            cv2.drawContours(frame_hsv, [box], LINE_COLOR, 2)

        output_stream.putFrame(frame_hsv)

main()
import robotpy_apriltag
import wpimath
from cscore import CameraServer
import ntcore
import numpy as np
import cv2

# camera settings
xResolution = 640
yResolution = 480
frameRate = 30
lineColor = (0, 255, 0)

# host - raspberry pi? roborio?
isTableHost = False

# start up NetworkTables as a server
ntInstance = ntcore.NetworkTableInstance.getDefault()
if isTableHost:
    ntInstance.startServer()
else:
    ntInstance.setServerTeam(3636)
    ntInstance.startClient("visionPi")

# Start USB camera capture via CameraServer
camera = CameraServer.startAutomaticCapture()

# Enable logging so we see some output to the terminal
CameraServer.enableLogging()

# set resolution and framerate
camera.setResolution(xResolution, yResolution)
camera.setFPS(frameRate)
cvSink = CameraServer.getVideo()

# open up an output stream to put modified video into
outputStream = CameraServer.putVideo("Vision", xResolution, yResolution)

# create the AprilTagDetector
aprilTagDetector = robotpy_apriltag.AprilTagDetector()
aprilTagDetector.addFamily("tag16h5", 3)

# create mats
rgbMat = np.zeros(shape = (xResolution, yResolution, 3), dtype = np.uint8)
grayMat = np.zeros(shape = (xResolution, yResolution), dtype = np.uint8)

while True:
    # grab rgb mat
    time, rgbMat = cvSink.grabFrame(rgbMat)

    # convert rgb mat to grayscale
    grayMat = cv2.cvtColor(rgbMat, cv2.COLOR_RGB2GRAY) 

    # run the AprilTagDetector
    detections = aprilTagDetector.detect(grayMat)

    for detection in detections:
        for i in range(4):
            j = (i + 1) % 4
            pt1 = (int(detection.getCorner(i).x), int(detection.getCorner(i).y))
            pt2 = (int(detection.getCorner(j).x), int(detection.getCorner(j).y))
            rgbMat = cv2.line(rgbMat, pt1, pt2, lineColor, 2)

    # upload frame to network tables
    outputStream.putFrame(rgbMat)
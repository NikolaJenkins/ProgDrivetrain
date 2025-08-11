import robotpy_apriltag
import wpimath
from cscore import CameraServer
import ntcore
import numpy as np
import cv2

# camera settings
xResolution = 320
yResolution = 240
frameRate = 30
lineColor = (0, 255, 0)

# host - raspberry pi? roborio?
isTableHost = True

# start up NetworkTables as a server
ntInstance = ntcore.NetworkTableInstance.getDefault()
if isTableHost:
    ntInstance.startServer()
else:
    ntInstance.setServerTeam(3636)
    ntInstance.startClient4("visionPi")

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

# create the PoseEstimator configuration
poseEstimatorConfig = robotpy_apriltag.AprilTagPoseEstimator.Config(
    0.1651,             #tag size in meters
    269.72,  #Fx: x focal length in mm
    269.04,  #Fy: y focal length in mm
    175.09,  #Cx: x focal center (based on 320x240 resolution)
    110.03, #Cy: y focal center (based on 320x240 resolution)
)
# create the PoseEstimator
poseEstimator = robotpy_apriltag.AprilTagPoseEstimator(poseEstimatorConfig)

# create network table for apriltag values
aprilTagNT = ntInstance.getTable('April Tag')

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

    if detections != []:
        # compute the transform from the Camera to the Tag
        cameraToTag = poseEstimator.estimate(detections[0])
        tagId = detections[0].getId()
        aprilTagNT.putBoolean('April Tag Detected', True)
    else:  
        # no tags found, so just store an empty transform
        cameraToTag = wpimath.geometry.Transform3d()
        tagId = 0
        aprilTagNT.putBoolean('April Tag Detected', False)
    aprilTagNT.putNumber('Tag ID', tagId)
    aprilTagNT.putNumber('TagX', cameraToTag.translation.x)
    aprilTagNT.putNumber('TagY', cameraToTag.translation.y)
    aprilTagNT.putNumber('TagZ', cameraToTag.translation.z)


    # upload frame to network tables
    outputStream.putFrame(rgbMat)
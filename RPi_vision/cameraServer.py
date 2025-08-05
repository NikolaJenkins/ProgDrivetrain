from cscore import CameraServer
import ntcore
import numpy
import cv2

# camera settings
xResolution = 640
yResolution = 480
frameRate = 30

# make green crosshairs
crosshairColor = (0, 255, 0)
crosshairSize = 20

# start up NetworkTables as a server
ntInstance = ntcore.NetworkTableInstance.getDefault()
ntInstance.startServer()

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

# create a color mat (image), sized xRes x yRes x 3 array
mat = numpy.zeros(shape=(xResolution, yResolution, 3), dtype=numpy.uint8)

# loop forever so program doesn't stop
while True:
   time, mat = cvSink.grabFrame(mat)
   point1 = (int(xResolution / 2 - crosshairSize), int(yResolution / 2))
   point2 = (int(xResolution / 2 + crosshairSize), int(yResolution / 2))
   mat = cv2.line(mat, point1, point2, crosshairColor, 2)
   point1 = (int(xResolution / 2), int(yResolution / 2 + crosshairSize))
   point2 = (int(xResolution / 2), int(yResolution / 2 - crosshairSize))
   mat = cv2.line(mat, point1, point2, crosshairColor, 2)
   outputStream.putFrame(mat)

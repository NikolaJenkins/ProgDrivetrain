from cscore import CameraServer
import ntcore
import numpy
import cv2

# camera settings
xResolution = 640
yResolution = 480
frameRate = 30

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
   outputStream.putFrame(mat)
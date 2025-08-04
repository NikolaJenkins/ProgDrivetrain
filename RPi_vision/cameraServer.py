from cscore import CameraServer
import ntcore


# start up NetworkTables as a server
ntInstance = ntcore.NetworkTableInstance.getDefault()
ntInstance.startServer()


# Start USB camera capture via CameraServer
camera = CameraServer.startAutomaticCapture()


# Enable logging so we see some output to the terminal
CameraServer.enableLogging()


# loop forever so program doesn't stop
while True:
    pass
from cscore import CameraServer
import ntcore

ntInstance = ntcore.NetworkTableInstance.getDefault()
ntInstance.setServerTeam(3636)

camera = CameraServer.startAutomaticCapture()
CameraServer.enableLogging()

while True:
    pass
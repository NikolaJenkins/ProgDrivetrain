from cscore import CameraServer
from imutils.video import WebcamVideoStream
import imutils
from networktables import NetworkTable
import time

# nt.NetworkTables.initialize(server = 'roborio-3636-frc.local')
# table = nt.NetworkTables.getTable('data table')
# x = table.getDoubleTopic('x').subscribe(0.0)
NetworkTable.setTeam(3636)
NetworkTable.setClientMode()
NetworkTable.initialize()
vp = NetworkTable.getTable("Stream")


camera = CameraServer.startAutomaticCapture()
CameraServer.enableLogging()

while True:
    x += 1
    vp.putNumber('X', x)
    time.sleep(1)
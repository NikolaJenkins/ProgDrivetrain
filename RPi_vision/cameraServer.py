from cscore import CameraServer
from networktables import NetworkTables as nt
import time

nt.NetworkTables.initialize(server = 'roborio-3636-frc.local')
table = nt.NetworkTables.getTable('data table')
x = table.getDoubleTopic('x').subscribe(0.0)

camera = CameraServer.startAutomaticCapture()
CameraServer.enableLogging()

while True:
    x += 1
    table.putNumber('X', x)
    time.sleep(1)
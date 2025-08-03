from cscore import CameraServer
from networktables import NetworkTables as nt

nt.initialize(server = 'roborio-3636-frc.local')
table = nt.getTable('data table')
x = table.getDoubleTopic('x').subscribe(0.0)

camera = CameraServer.startAutomaticCapture()
CameraServer.enableLogging()

while True:
    x += 1
    table.set(x)
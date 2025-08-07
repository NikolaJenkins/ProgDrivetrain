from cscore import CameraServer
import ntcore
import cv2
import json
import numpy as np
import time
def main():
    is_table_host = True

    with open('/boot/frc.json') as f:
        config = json.load(f)
    camera = config['cameras'][0]
    width = camera['width']
    height = camera['height']
    nt_instance = ntcore.NetworkTableInstance.getDefault()

    if is_table_host:
        nt_instance.startServer()
    else:
        nt_instance.setServerTeam(3636)
        nt_instance.startClient4("visionPi")

    CameraServer.startAutomaticCapture()
    CameraServer.enableLogging()
    cv_sink = CameraServer.getVideo()
    output_stream = CameraServer.putVideo('Processed', width, height)
    vision_nt = nt_instance.getTable('Vision')
    img = np.zeros(shape=(240, 320, 3), dtype=np.uint8)

    while True:
        time, input_image = cv_sink.grabFrame(img)
        output_stream.putFrame(img)

main()
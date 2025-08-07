from cscore import CameraServer
import ntcore
import cv2
import json
import numpy as np
import time

def main():
    camera_config()
    network_tables(True)
    video_stream()
    vision_table()
    periodic()

def camera_config():
    with open('/boot/frc.json') as f:
        config = json.load(f)
    camera = config['cameras'][0]
    width = camera['width']
    height = camera['height']

def network_tables(is_table_host):
    nt_instance = ntcore.NetworkTableInstance.getDefault()
    if is_table_host:
        nt_instance.startServer()
    else:
        nt_instance.setServerTeam(3636)
        nt_instance.startClient4("visionPi")

def video_stream():
    CameraServer.startAutomaticCapture()
    input_stream = CameraServer.getVideo()
    output_stream = CameraServer.putVideo('Processed', width, height)

def vision_table():
    vision_nt = nt_instance.getTable('Vision')
    img = np.zeros(shape=(240, 320, 3), dtype=np.uint8)

def periodic():
    time.sleep(0.5)
    while True:
        time, input_image = input_stream.getFrame(img)
    output_stream.putFrame(output_image)

main()
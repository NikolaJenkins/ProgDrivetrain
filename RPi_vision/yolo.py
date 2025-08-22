from cscore import CameraServer
import ntcore
import cv2
from ultralytics import YOLO
import numpy as np

IS_TABLE_HOST = True

# camera settings
X_RESOLUTION = 320
Y_RESOLUTION = 240
FRAME_RATE = 30
LINE_COLOR = (0, 255, 0)

# load yolo model
yolo = YOLO('yolov8s.pt')

def get_colors(cls_num):
    base_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
    increments = [(1, -2, 1), (-2, 1, -1), (1, -1, 2)]
    color_index = cls_num % len(base_colors)
    color = [base_colors[color_index][i] + increments[color_index][i] * (cls_num // len(base_colors)) % 256 for i in range(3)]
    return tuple(color)

def main():
    # connect to server
    nt_instance = ntcore.NetworkTableInstance.getDefault()

    # host or client?
    if IS_TABLE_HOST:
        nt_instance.startServer()
    else:
        nt_instance.setServerTeam(3636)
        nt_instance.startClient4("visionPi")
    
    # vision table
    vision_nt = nt_instance.getTable("Vision")

    # set up camera
    CameraServer.startAutomaticCapture()
    CameraServer.enableLogging()
    cv_sink = CameraServer.getVideo()
    output_stream = CameraServer.putVideo("Vision", X_RESOLUTION, Y_RESOLUTION)

    # mat
    img = np.zeros(shape = (X_RESOLUTION, Y_RESOLUTION, 3), dtype = np.uint8)

    while True:
        time, img = cv_sink.grabFrame(img)
        if not img:
            continue
        results = yolo.track(img, stream = True)

        # get class names
        for result in results:
            classes_names = result.names

            #iterate over each box
            for box in result.boxes:
                if box.conf[0] > 0.4:
                    # get coordinates
                    [x1, y1, x2, y2] = box.xyxy[0]

                    # convert to int
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

                    # get class
                    cls = int(box.cls[0])

                    # get class name
                    class_name = classes_names[cls]

                    # get respective color
                    color = get_colors(cls)

                    # draw the rectangle
                    cv2.rectangle(img, (x1, y1), (x2, y2), LINE_COLOR, 2)

                    # put class name and confidence on frame
                    cv2.putText(img, f'{class_name} {box.conf[0]: .2f}', cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

        output_stream.putFrame(img)

main()
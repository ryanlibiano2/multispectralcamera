import time
import numpy as np
import sys
import nanocamera

import cv2

class ndvi:
    GSTREAMER_PIPELINE = 'nvarguscamerasrc sensor_mode=0 ! video/x-raw(memory:NVMM), width=3280, height=2464, format=(string)NV12, framerate=20/1 ! nvvidconv flip-method=0 ! video/x-raw, width=600, height=480, format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! appsink'
    video_capture = cv2.VideoCapture(GSTREAER_PIPELINE, cv2.CAP_GSTREAMER)
    #video_capture = nano.Camera(flip=0, width=1280, height=800, fps=30)
    if video_capture.isOpened() is not True:
        print 'Cannot open camera. Exiting.'
        quit()
    def run():
        while True:
            image = video_capture.read()
            b, g, r = cv2.split(image)
            bottom = (r.astype(float) + b.astype(float))
            bottom[bottom == 0] = 0.01
            ndvi = (r.astype(float) - b) / bottom
            ndvi = contrast_stretch(ndvi)
            ndvi = ndvi.astype(np.uint8)
            label(b, 'Blue')
            label(g, 'Green')
            label(r, 'NIR')
            label(ndvi, 'NDVI')
            combined = disp_multiple(b, g, r, ndvi)
            cv2.imshow('ndvi', combined)
            cv2.waitKey(7) % 0x100

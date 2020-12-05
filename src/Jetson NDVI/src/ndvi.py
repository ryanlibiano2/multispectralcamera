import time
import numpy as np
import sys
import nanocamera

import cv2

class ndvi:
    #def gstreamer_pipeline(capture_width=1280, capture_height=720, display_width=1280, display_height=720, framerate=30, flip_method=0):
        #return("nvarguscamerasrc ! ""video/x-raw(memory:NVMM), ""width=(int)%d, height=(int)%d, ""format=(string)NV12, framerate=(fraction)%d/1 ! " "nvvidconv flip-method=%d ! " "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! " "videoconvert ! " "video/x-raw, format=(string)BGR ! appsink" % (capture_width, capture_height, framerate, flip_method, display_width, display_height))
    #GSTREAMER_PIPELINE = 'nvarguscamerasrc sensor_mode=0 ! video/x-raw(memory:NVMM), width=3280, height=2464, format=(string)NV12, framerate=20/1 ! nvvidconv flip-method=0 ! video/x-raw, width=600, height=480, format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! appsink'
    #cap = cv2.VideoCapture(GSTREAMER_PIPELINE, cv2.CAP_GSTREAMER)
    #cap = nano.Camera(flip=0, width=1280, height=800, fps=30
    stream = 'nvarguscamerasrc ! video/x-raw(memory:NVMM), width=%d, height=%d, format=(string)NV12, framerate=(fraction)%d/1 !nvvidconv flip-method=%d ! nvvidconv ! video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! videoconvert ! appsink' % (1280, 720, 30,0, 640, 480)
    def run():
        while True:
            cap = cv2.VideoCapture(stream, cv2.CAP_GSTREAMER)
            window_handle = cv2.namedWindow("ndvi", cv2.WINDOW_AUTOSIZE)
            while cv2.getWindowProperty("ndvi", 0) >= 0:
                ret_val, image = cap.read()
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
                cv2.imshow('ndvi', combined)
                cv2.waitKey(30) % 0xFF

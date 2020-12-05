import cv2
import nanocamera as nano
import serial
import os
import adafruit_gps
import busio
import board
import Jetson.GPIO as GPIO

class camera:
    camera = nano.Camera(flip=0, width=2000, height=2000, fps=21)
    file = '~/Desktop/ndvi/'
    but_pin = 18
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(but_pin, GPIO.IN)


    if camera.isReady() is not True:
        print('failed to take picture, exiting')
    def snapshot():
        while True:
            if GPIO.wait_for_edge(but_pin, GPIO.FALLING)
                image = camera.read()
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
                cv2.imwrite("ndvi.POS:{},{},{}/Date:{},{},{}/Time:{},{},{}".format(gps.latitude, gps.longitude, gps.altitude_m, gps.timestamp_utc.tm_mon, gps.timestamp_utc.tm_mday, gps.timestamp_utc.tm_year,  gps.timestamp_utc.tm_hour,  gps.timestamp_utc.tm_min, gps.timestamp_utc.tm_sec) + ".png", ndvi)
                

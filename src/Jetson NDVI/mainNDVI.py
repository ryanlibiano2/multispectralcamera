import board
import serial
import adafruit_gps
import cv2
import numpy as np
import time
import busio
from gpsinitialize import gps
from ndvi import ndvi
import multiprocessing import Process

gps.initialize
time.sleep(5)
print('ready to go')
time.sleep(5)
if True:
    p1 = Process(target = display)
    p1.start()
    p2 = Process(target = run )
    p2.start()
    p1.join()
    p2.join()
    

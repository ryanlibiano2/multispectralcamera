import board
import serial
import adafruit_gps
import cv2 as cv
import numpy as np
import time
import busio

#set a gps instance for initialization and live video
uart = serial.Serial("/dev/ttyUSB0", baudrate = 9600, timeout = 3000)
gps = adafruit_gps.GPS(uart)
GSTREAMER_PIPELINE = 'nvarguscamerasrc sensor_mode=0 ! video/x-raw(memory:NVMM), width=3280, height=2464, format=(string)NV12, framerate=20/1 ! nvvidconv flip-method=0 ! video/x-raw, width=600, height=480, format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! appsink'
but_pin = 18
GPIO.setmode(GPIO.BOARD)
GPIO.setup(but_pin, GPIO.IN)

#define a gps intitialize ffunction
def initialize():
    gps.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")
    gps.send_command(b"PMTK220,1000")
    gps.update()
        if not gps.has_fix()
        print("gps finding fix...")
        continue
    print("+" * 40)
    print('Fix timestamp: {}/{}/{} {:02}:{:02}:{:02}'.format(gps.timestamp_utc.tm_mon, gps.timestamp_utc.tm_mday, gps.timestamp_utc.tm_year,  gps.timestamp_utc.tm_hour,  gps.timestamp_utc.tm_min, gps.timestamp_utc.tm_sec))
    print('Latitude: {} degrees'.format(gps.latitude))
    print('Longitude: {} degrees'.format(gps.longitude))
    print('Fix quality: {}'.format(gps.fix_quality))
    print('# satellites: {}'.format(gps.satellites))
    if gps.satellites is not None:
        print("# satellites: {}".format(gps.satellites))
    if gps.altitude_m is not None:
        print("Altitude: {} meters".format(gps.altitude_m))
    if gps.speed_knots is not None:
        print("Speed: {} knots".format(gps.speed_knots))
    if gps.track_angle_deg is not None:
        print("Track angle: {} degrees".format(gps.track_angle_deg))
    if gps.horizontal_dilution is not None:
        print("Horizontal dilution: {}".format(gps.horizontal_dilution))
    if gps.height_geoid is not None:
        print("Height geo ID: {} meters".format(gps.height_geoid))
    print("+" * 40)
#define a gps display function
def display():
    last_print = time.monotonic()
    while True:
        gps.update()
        current = time.monotonic()
        if current - last_print >= 1.0:
            last_print
            if not gps.has_fix:
                print("lost fix, re-acquiring")
                continue
            print("+" *40)
            print('Fix timestamp: {}/{}/{} {:02}:{:02}:{:02}'.format(gps.timestamp_utc.tm_mon, gps.timestamp_utc.tm_mday, gps.timestamp_utc.tm_year,  gps.timestamp_utc.tm_hour,  gps.timestamp_utc.tm_min, gps.timestamp_utc.tm_sec))
            print('Latitude: {} degrees'.format(gps.latitude))
            print('Longitude: {} degrees'.format(gps.longitude))
            print('Fix quality: {}'.format(gps.fix_quality))
            print('# satellites: {}'.format(gps.satellites))
            print('Altitude: {} meters'.format(gps.altitude_m))
# define camera run function
def run():
    cap = cv2.VideoCapture(GSTREAMER_PIPELINE, cv2.CAP_GSTREAMER)
    while True:
        #read the videocapture instance as a NumPy array
        image = cap.read()

        #split the b,g,r color channels
        b, g, r = cv2.split(image)

        #calculate NDVI

        #bottom of ndvi algorithim
        bottom = (r.astype(float) + b.astype(float))
        bottom[bottom == 0] = 0.01

        #perform ndvi algorithim
        ndvi = (r.astype(float) - b) / bottom
        ndvi = ndvi.astype(np.uint8)
        # Display
        cv2.imshow('image', ndvi)
        #take photo if button is pressed
        if if GPIO.wait_for_edge(but_pin, GPIO.FALLING):
            #save and label the image with the GPS coordinates
            cv2.imwrite(("/home/uiucagdrone/Desktop/output/ndvi.POS:{},{},{}/Date:{},{},{}/Time:{},{},{}".format(gps.latitude, gps.longitude, gps.altitude_m, gps.timestamp_utc.tm_mon, gps.timestamp_utc.tm_mday, gps.timestamp_utc.tm_year,  gps.timestamp_utc.tm_hour,  gps.timestamp_utc.tm_min, gps.timestamp_utc.tm_sec) + ".png", ndvi))
        else:
            continue
        # If we press ESC then break out of the loop
        c = cv2.waitKey(7) % 0x100
        if c == 27:
            break

#actual main code

#initialize gps
gps.initialize()
print('ready to go')
#give time for the system to set itself up
time.sleep(5)
# start the multiproccessing
if True:
    p1 = Process(target = display)
    p1.start() #to display constantly changing gps data for the used
    p2 = Process(target = run)
    p2.start() #to display the actual NDVI through the viewfinder
    p1.join()
    p2.join()

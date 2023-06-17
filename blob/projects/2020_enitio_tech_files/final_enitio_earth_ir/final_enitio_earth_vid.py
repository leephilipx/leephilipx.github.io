##  Use manual GPIO pins reading if serial method fails (See ##)

## import RPi.GPIO as GPIO
import cv2
import serial
from moviepy.editor import *
import pygame

## x = 0

# Video playing method using moviepy & pygame
def play_video():
    pygame.display.set_caption('Hologram')
    clip = VideoFileClip('Hologram Project by Kiste.mp4')
    clip.preview()
    if cv2.waitKey(25) & 0xFF == ord('e'):
        pygame.quit()
        ## x = 0


# Video playing method using opencv2
'''
def rescale_frame(frame, percent):
    width = int(frame.shape[1] * percent/ 100)
    height = int(frame.shape[0] * percent/ 100)
    dim = (width, height)
    return cv2.resize(frame, dim, interpolation =cv2.INTER_AREA)

def play_video():
    # Create a VideoCapture object and read from input file 
    cap = cv2.VideoCapture('Hologram Project by Kiste.mp4') 
    # Check if camera opened successfully 
    if (cap.isOpened()== False):
        print("Error opening video file") 
    # Read until video is completed
    
    while(cap.isOpened()): 
        # Capture frame-by-frame 
        ret, frame = cap.read()

        if ret == True: 
            # frame = rescale_frame(frame, 150)
            # Display the resulting frame 
            cv2.imshow('Hologram', frame) 
            # Press E on keyboard to exit 
            if cv2.waitKey(25) & 0xFF == ord('e'):
                break
        # Break the loop 
        else:  
            break
    
    # When everything done, release the video capture object 
    cap.release() 
    # Closes all the frames 
    cv2.destroyAllWindows()
    ## x = 0
'''


## GPIO.setmode(GPIO.BCM)
## GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
ser = serial.Serial('/dev/ttyUSB1', 9600)
s = [0]

while True:
    print("Run")
    read_serial = ser.readline()
    s[0] = str(int (ser.readline(), 16))
    print (s[0])
    print (read_serial)
    ##  if GPIO.input(17) == 1:
    ##      x = 1
    ##      play_video()
    if s[0] == '3960362407' or s[0] == '235820455' or s[0] == '4294967295': # HEX: EC0E55A7, E0E55A7, FFFFFFFF
        print ("Playing video")
        play_video()

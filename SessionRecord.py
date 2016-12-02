from picamera import PiCamera
from time import sleep

def camera():
    camera = PiCamera()
    camera.start_preview()
    camera.start_recording('/home/pi/video.h264')
    sleep(20)
    camera.stop_recording()
    camera.stop_preview
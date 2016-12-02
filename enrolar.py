import FPS, sys
from test_raw import *

if __name__ == '__main__':
    fps = FPS.FPS_GT511C3()
    fps.UseSerialDebug = True
    Enroll(fps,sys.argv[1])
    fps.Close()
    pass
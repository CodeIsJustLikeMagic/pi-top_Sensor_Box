from picamera import PiCamera
import time
import numpy as np
import cv2

def contrast(img_hsv):
    # michelson contrast
    # low contraast is ner zero
    # high contrast is near one
    # Y = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)[:,:,0]
    h, s, Y = cv2.split(img_hsv)
    min = int(np.min(Y))
    max = int(np.max(Y))
    contrast = (max - min) / (max + min)
    print("brightness (low, high): (", min, ", ", max, ")", sep="")
    print("contrast:", contrast)


def brightness(img_hsv):
    h, s, v = cv2.split(img_hsv)
    print("brightness:", np.mean(v))

with PiCamera() as camera:
    camera.start_preview()
    try:
        for i, filename in enumerate(camera.capture_continouous('image{counter:02d}.jpg')):
            print(filename)
            time.sleep(1)
            if i == 5:
                break
    finally:
        camera.stop_preview()

from picamera import PiCamera
from picamera.array import PiRGBArray
import time
import numpy as np
import cv2
from matplotlib import pyplot as plt


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


def color_distribution(img_hsv):
    pass
    # most common color values ?
    # do white and black count ?


def histogramms(img_hsv):
    print("hue")
    histr_hue1 = cv2.calcHist(img_hsv, [0], None, [256], [0, 256])
    plt.plot(histr_hue1)
    plt.show()

    print("saturation")
    histr_hue2 = cv2.calcHist(img_hsv, [1], None, [256], [0, 256])
    plt.plot(histr_hue2)
    plt.show()

    print("value")
    histr_hue3 = cv2.calcHist(img_hsv, [2], None, [256], [0, 256])
    plt.plot(histr_hue3)
    plt.show()


def do_the_thing(img):
    # create histogramm. should later be written in csv file
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    contrast(img_hsv)
    brightness(img_hsv)
    # histogramms(img_hsv)
    # threshholds(img_hsv)
    # colored_scatter_plot(img, img_hsv)
    # contrast
    # bightness
    # color distribution


camera = PiCamera()
camera.resolution = (640, 480)
rawCapture = PiRGBArray(camera, size=(640, 480))

time.sleep(0.1)
camera.capture(rawCapture, format="bgr")
img = rawCapture.array

do_the_thing(img)
camera.capture("foo.jpg")

cv2.imshow("image", img)
cv2.waitKey(0)
# capture 30 images in a row
import cv2
import numpy as np
from flirpy.camera.lepton import Lepton

matrix = None
with Lepton() as camera:
    r_image = camera.grab()
    r_image = (r_image - 27315) / 100

    matrix = np.expand_dims(r_image, -1)  # make it processable by TIPA

    for i in range(1, 30):
        print(i)
        r_image = camera.grab()
        r_image = (r_image - 27315) / 100
        r_image = np.expand_dims(r_image, -1)

        matrix = np.append(matrix, r_image, axis=-1)

print(matrix.shape)

# save data to file
np.save('test.npy', matrix)
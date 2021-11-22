import matplotlib.pyplot as plt
import numpy as np


frame_number = 29

matrix = np.load('test.npy')
print(matrix.shape)
print(matrix[:,:,frame_number])

def thermal_matrix_view(matrix):
    fig= plt.figure()
    ax = fig.add_subplot(1,1,1)
    plt.imshow(matrix)
    plt.savefig("thermal_matrix.png")

thermal_matrix_view(matrix[:,:,frame_number])
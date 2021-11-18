import cv2

# save an example iamge
camera = cv2.VideoCapture(1)
# camera 0 is the picamera. camera 1 is thermal camera
return_value,image = camera.read()
cv2.imwrite("example4.jpg",image) #save image
camera.release()
cv2.destroyAllWindows()
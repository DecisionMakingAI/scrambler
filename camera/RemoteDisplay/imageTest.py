import numpy as np
import cv2

#Load color image
img = cv2.imread('sample.jpg')
#print (img)

cv2.imshow('image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()



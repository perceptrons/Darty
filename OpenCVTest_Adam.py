import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

img2 = cv.imread('croppeddartboard.png',1)
edges = cv.Canny(img2,100,250)
blur = cv.GaussianBlur(edges,(5,5),0)
(thresh, binaried) = cv.threshold(blur, 128, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)
result = binaried

plt.subplot(121),plt.imshow(edges,cmap = 'gray')
plt.title('Original Image'), plt.xticks([]), plt.yticks([])
plt.subplot(122),plt.imshow(result,cmap='gray')
plt.title('Edge Image'), plt.xticks([]),plt.yticks([])
plt.show()
#cv.imshow('image', img2)

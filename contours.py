import cv2
import numpy as np
import imutils
from matplotlib import pyplot as plt

img = cv2.imread('dartboardtest_crop.png',1)
orig = img.copy()
#edges = cv2.Canny(img,100,400)
#imgray = cv2.cvtColor(edges, cv2.COLOR_BGR2GRAY)
imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
contrast = cv2.convertScaleAbs(imgray, alpha=1.2, beta=0)
edges = cv2.Canny(contrast,100,400)
edges = cv2.GaussianBlur(edges, (5,5), 0)
#print("\n\n\nEDGES\n\n\n")
#print(edges)

#ret, thresh = cv2.threshold(edges, 127, 255, 0)
#ret, thresh = cv2.threshold(imgray, 127, 255, 0)

#/plt.subplot(121),plt.imshow(img,cmap = 'gray')
#/plt.title('Original Image'), plt.xticks([]), plt.yticks([])
#/plt.subplot(122),plt.imshow(edges,cmap = 'gray')
#/plt.title('Edge Image'), plt.xticks([]), plt.yticks([])

#cv2.imwrite('edges.png', edges)

#print(cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE))
#im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cont = cv2.findContours(edges.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
contours = imutils.grab_contours(cont)
contours = sorted(contours, key = cv2.contourArea, reverse = True)


print(len(contours))
cv2.waitKey(0)
for i in range(0, len(contours)):
    print(contours[i], "\n\n")
    cv2.drawContours(img, contours, i, (0, 0, 255), 4)
    cv2.imshow('Contour', img)
    cv2.waitKey(0)
#print("\n\nCONTOURS\n", contours[20])

#cv2.drawContours(img, contours, 20, (0, 0, 255), 4)
#cv2.imshow('Contours', img)
#cv2.waitKey(0)

import cv2
import numpy as np
import imutils
import json
from matplotlib import pyplot as plt

img = cv2.imread('dartboardtest_crop.png',1)
orig = img.copy()
#edges = cv2.Canny(img,100,400)
#imgray = cv2.cvtColor(edges, cv2.COLOR_BGR2GRAY)
imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
contrast = cv2.convertScaleAbs(imgray, alpha=1.8, beta=0)
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
end = len(contours)
print(end)
for i in range(0, len(contours)):
    if cv2.contourArea(contours[i]) < 40: #change this to not hard coded number
        end = i - 1
        break

contours = contours[:end]



region_dict = {}
for region_number in range (0, len(contours)):
    string = ""
    for coordinate in contours[region_number]:
        string += str(coordinate[0][0])
        string += ','
        string += str(coordinate[0][1])
        string += ' '
    region_dict[region_number] = string 

with open("regions.json", "w") as write_file:
    json.dump(region_dict, write_file)
    
#print(len(contours))
#cv2.waitKey(0)
#for i in range(1, len(contours)):
#    print(contours[i], "\n\n")
#    cv2.drawContours(img, contours, i-1, (255, 0, 0), 4)
#    cv2.drawContours(img, contours, i, (0, 0, 255), 4)
#    cv2.imshow('Contour', img)
#    cv2.waitKey(0)
#print("\n\nCONTOURS\n", contours[20])

#cv2.drawContours(img, contours, 20, (0, 0, 255), 4)
#cv2.imshow('Contours', img)
#cv2.waitKey(0)

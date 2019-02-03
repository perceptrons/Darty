import cv2
import numpy as np
import imutils
import json
from matplotlib import pyplot as plt

img = cv2.imread('image0dartscropped.png',1)
orig = img.copy()
contrast = cv2.convertScaleAbs(img, alpha=3.8, beta=0)
edges = cv2.Canny(contrast,200,400)
edges = cv2.GaussianBlur(edges, (5,5), 0)
(thresh, edges) = cv2.threshold(edges, 125, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
#imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#contrast = cv2.convertScaleAbs(imgray, alpha=1.8, beta=0)

cv2.imshow('gaussian', edges)
cont = cv2.findContours(edges.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
contours = imutils.grab_contours(cont)
contours = sorted(contours, key = cv2.contourArea, reverse = True)
end = len(contours)
print(end)
for i in range(0, len(contours)):
    if cv2.contourArea(contours[i]) < 20: #change this to not hard coded number
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
    
print(len(contours))
cv2.waitKey(0)
for i in range(1, len(contours)):
    print(contours[i], "\n\n")
    cv2.drawContours(img, contours, i-1, (255, 0, 0), 3)
    cv2.drawContours(img, contours, i, (0, 0, 255), 3)
    cv2.imshow('Contour', img)
    cv2.waitKey(0)


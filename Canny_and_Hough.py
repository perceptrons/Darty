import cv2
import math
import numpy as np
from matplotlib import pyplot as plt

#img = cv2.imread('dartboardtest_crop.png',1)
img = cv2.imread('dart1.png',1)

# Canny filter for edge detection
filtered = cv2.Canny(img,100,400)
print("\n\nFiltered", filtered)
blur = cv2.GaussianBlur(filtered, (5,5), 0)
print("\n\nBlur", blur)
(thresh, binaried) = cv2.threshold(blur, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
print("\n\nBinaried", binaried)
edges = binaried

# Copy edges to the images that will display the results in BGR
cdst = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
cdstP = np.copy(cdst)

lines = cv2.HoughLines(edges, 1, np.pi / 180, 350, None, 0, 0)
if lines is not None:
    for i in range(0, len(lines)):
        rho = lines[i][0][0]
        theta = lines[i][0][1]
        a = math.cos(theta)
        b = math.sin(theta)
        x0 = a * rho
        y0 = b * rho
        pt1 = (int(x0 + 1000*(-b)), int(y0 + 1000*(a)))
        pt2 = (int(x0 - 1000*(-b)), int(y0 - 1000*(a)))
        cv2.line(cdst, pt1, pt2, (0,0,255), 3, cv2.LINE_AA)


#linesP = cv2.HoughLinesP(edges, 1, np.pi / 180, 50, None, 50, 10)

#if linesP is not None:
#    for i in range(0, len(linesP)):
#        l = linesP[i][0]
#        cv2.line(cdstP, (l[0], l[1]), (l[2], l[3]), (0,0,255), 3, cv2.LINE_AA)

partitions = 100
maxRad = 400
circles = []
for i in range(0, partitions):
    maxR = round(maxRad*(i+1)/partitions)
    minR = round(maxRad*(i)/partitions)
    print("max, min:" , maxR, minR)
    curr_circle = cv2.HoughCircles(edges,cv2.HOUGH_GRADIENT,1.5,1,
                            param1=100,param2=100,minRadius=minR ,maxRadius=maxR)
    if curr_circle is not None:
        curr_circle = np.uint16(np.around(curr_circle))
        curr = curr_circle.tolist()
        print("curr_circle:" , curr_circle, "i: ", i)
        circles.extend(curr[0])

#circles = np.uint16(np.around(circles))
print(circles)

for i in circles:
    print("\n\ni:", i)
    # draw the outer circle
    cv2.circle(cdst,(i[0],i[1]),i[2],(0,255,0),2)
    # draw the center of the circle
    cv2.circle(cdst,(i[0],i[1]),2,(0,0,255),3)

#cv2.imshow('detected circles',cimg)
#cv2.imshow("Source", img)
cv2.imshow("Detected Lines (in red) - Standard Hough Line Transform", cdst)
#cv2.imshow("Detected Lines (in red) - Probabilistic Line Transform", cdstP)

cv2.waitKey(0)

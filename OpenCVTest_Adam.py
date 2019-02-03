#adam benabbou's test file. messed with houghlines
import cv2 as cv
import numpy as np
import math
from matplotlib import pyplot as plt

img2 = cv.imread('croppeddartboard.png',1)
edges = cv.Canny(img2,100,250)
blur = cv.GaussianBlur(edges,(5,5),0)
(thresh, binaried) = cv.threshold(blur, 128, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)
#binaried = edges
result = binaried

cdst = cv.cvtColor(binaried, cv.COLOR_GRAY2BGR)
cdstP = np.copy(cdst)

width, height = img2.shape[:2] #img2 or whatever is smaller
minLineLength = min(width, height)*.75
#maxLineLength = max(width, height)
maxLineGap = minLineLength*.01 #dunno... aaaah

threshhold = max(width,height)*.5
lines = cv.HoughLines(binaried, 1, np.pi/180, 400, None, 0, 0)

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
            cv.line(cdst, pt1, pt2, (0,0,255), 3, cv.LINE_AA)

linesP = cv.HoughLinesP(binaried, 1, np.pi/180, 50, minLineLength, maxLineGap)
#for x1, y1, x2, y2 in lines[0]:
#    cv.line(img2,(x1,y1),(x2,y2),(0,255,0), 2)
if linesP is not None:
    for i in range(0,len(linesP)):
        l = linesP[i][0]
        cv.line(cdstP, (l[0], l[1]), (l[2], l[3]), (0, 0, 255), 3, cv.LINE_AA)

cv.imshow("Source", img2)
cv.imshow("Detected Lines (in red) - Standard Hough Line Transform", cdst)
cv.imshow("Detected Lines (in red) - Proablistic Hough Line Transform", cdstP)
cv.waitKey(0)

#cv.imwrite('houghlines5.png',img2)

#plt.subplot(121),plt.imshow(edges,cmap = 'gray')
#plt.title('Original Image'), plt.xticks([]), plt.yticks([])
#plt.subplot(122),plt.imshow(result,cmap='gray')
#plt.title('Edge Image'), plt.xticks([]),plt.yticks([])
#plt.show()
#cv.imshow('image', img2)

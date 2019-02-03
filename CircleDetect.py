import cv2
import math
import numpy as np
from matplotlib import pyplot as plt

def CircleDetect(image_file)
    #img = cv2.imread('dartboardtest_crop.png',1)
    img = cv2.imread(image_file,1)
    print(img)
    print(img.shape)
    
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
    
    circles = cv2.HoughCircles(edges,cv2.HOUGH_GRADIENT,1.5,len(img),
                                param1=20,param2=100,minRadius=40 ,maxRadius=500)
    circles = np.uint16(np.around(circles))
    for i in circles[0,:]:
        # draw the outer circle
        cv2.circle(cdst,(i[0],i[1]),i[2],(0,255,0),2)
        # draw the center of the circle
        cv2.circle(cdst,(i[0],i[1]),2,(0,0,255),3)
    
    
    #cv2.imshow("here", cdst)
    #cv2.waitKey(0)
    maxR = 0
    x = 0
    y = 0
    for i in circles[0,:]:
        if i[2] > maxR:
            maxR = (i[2])
            x = (i[0])
            y = (i[1])
    maxR = int(maxR * 1.5)
    
    xlow = max(int(x) - int(maxR), 0)
    
    xhigh = min(x + maxR, len(img))
    
    ylow = max(int(y) - int(maxR), 0)
    
    yhigh = min(y + maxR, len(img[0]))
    
    print(xlow, xhigh, ylow, yhigh)
    
    im = np.asarray(img)
    crop = im[ylow:yhigh, xlow:xhigh, :]
    print (crop)
    
    cv2.imwrite('cropped.png', crop)
    

import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('dartboardtest_crop.png',1)
print(img)
edges = cv2.Canny(img,100,400)
print("\n\n\nEDGES\n\n\n")
print(edges)

#/plt.subplot(121),plt.imshow(img,cmap = 'gray')
#/plt.title('Original Image'), plt.xticks([]), plt.yticks([])
#/plt.subplot(122),plt.imshow(edges,cmap = 'gray')
#/plt.title('Edge Image'), plt.xticks([]), plt.yticks([])

cv2.imwrite('edges.png', edges)

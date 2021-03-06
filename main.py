import cv2 as cv
import numpy as np
import time
from matplotlib import pyplot as plt
import json

from supportfunction import *
from crop import *

PiCamCapture('ImageStart.png')

print('Captured Template Image. Yay!')
#function where regions are sent to gui

crop_and_save('ImageStart.png', 'ImageStartCropped.png')

ScoreMonitoring = True
data = {
        "ScoreMonitoring": ScoreMonitoring
        }

with open("globalfile.json", "w") as write_file:
    json.dump(data, write_file)


PiCamCapture('CurrentPic1.png')

count = 0
while True:
    time.sleep(1) #pause loop for 5 seconds
    #updates picture if we are monitoring
    with open("globalfile.json", "r") as read_file:
        data = json.load(read_file)
    ScoreMonitoring = data["ScoreMonitoring"]
    print(ScoreMonitoring)

    if ScoreMonitoring== True:
        PiCamCapture('CurrentPic.png')
        crop_and_save('CurrentPic.png', 'CurrentPicCropped.png')
        count = count +1
        print("monitoring")

    print(count)

    if count >5:
        ScoreMonitoring=False
        data = {
            "ScoreMonitoring": ScoreMonitoring
        }
        with open("globalfile.json", "w") as write_file:
            json.dump(data, write_file)





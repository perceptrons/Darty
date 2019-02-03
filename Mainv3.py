import cv2 as cv
import numpy as np
import time
from matplotlib import pyplot as plt
import json
from time import sleep
import subprocess
from crop import *

import os

print('welcome')

#print(os.environ)
#print(os.environ["PATH"])

subprocess.run(["raspistill", "-o","ImageStart.jpg"])
print('Captured Template Image. Yay!')
#function where regions are sent to gui

crop_and_save('ImageStart.jpg', 'ImageStartCropped.jpg')

ScoreMonitoring = True
data = {
        "ScoreMonitoring": ScoreMonitoring
        }

with open("globalfile.json", "w") as write_file:
    json.dump(data, write_file)


subprocess.run(["raspistill", "-o","CurrentPic.jpg"])
crop_and_save('CurrentPic.jpg', 'CurrentPicCropped.jpg')
print("first current pic done")

count = 0
while True:
    time.sleep(2) #pause loop for 5 seconds
    #updates picture if we are monitoring
    with open("globalfile.json", "r") as read_file:
        data = json.load(read_file)
    ScoreMonitoring = data["ScoreMonitoring"]
    print(ScoreMonitoring)

    if ScoreMonitoring== True:
        subprocess.run(["raspistill", "-o","CurrentPic.jpg"])
        crop_and_save('CurrentPic.jpg', 'CurrentPicCropped.jpg')
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

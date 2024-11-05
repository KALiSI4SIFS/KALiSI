##!/usr/bin/python3

from picamera2 import Picamera2

from time import sleep
import numpy as np
import cv2
import glob
import os
from pathlib import Path

import datetime
import time
from sys import exit

from helper_file import is_dst
from helper_file import sunrise_sunset
from helper_file import img_fusion
from helper_file import outer_circle
from helper_file import trim_sky

from picamera2 import *
tuning = Picamera2.load_tuning_file("imx219.json")


#t1 = time.perf_counter()

folder_path = "/home/pi/Pictures/"
imgLoc="/home/pi/img2Comb/"
currentTime = datetime.datetime.now()
folder_name = currentTime.strftime("%Y-%m-%d")
output_folder = os.path.join(folder_path,folder_name)

if os.path.isdir(output_folder)==False:
    os.makedirs(output_folder)    

date_now=datetime.datetime.now()
sunrise, sunset = sunrise_sunset(date_now)

if date_now.time() < sunrise.time() or date_now.time() > sunset.time():
    exit(0)

else:
    # Get the current time
    currentTime = datetime.datetime.now()

    # Create file name for image
    picTime = currentTime.strftime("%Y-%m-%d-%H-%M")
 
    #set expore times 
    exposures = [1050, 1700, 2750]

    def exposure_images():
        with Picamera2(tuning=tuning) as camera: 
            config = camera.create_preview_configuration(main={"size": (2592, 1944),"format": "RGB888"})
            camera.configure(config)
            images=[]
            for exp in exposures:
                camera.set_controls({"ExposureTime": exp, "AnalogueGain": 1,"ColourGains": (1.0,1.7), "AwbEnable": 0})
                camera.start()
                image=camera.capture_array()
                camera.stop()
                images.append (image)
        return images
    
    images=exposure_images()
    fused_image=img_fusion(images)
    final_img = trim_sky(np.array(fused_image))
    cv2.imwrite(os.path.join(output_folder,picTime + '.jpg'),final_img )

#t2 = time.perf_counter()
#print(f"Finished in {t2-t1} seconds")

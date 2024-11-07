import numpy as np
import picamera.array
from time import sleep, time, localtime
from pathlib import Path
import subprocess
from pathlib import Path
import os 
import cv2

import pytz
import datetime
import time
from astral import LocationInfo
from astral.sun import sun
from sys import exit


def SDcard2ExtHD(SDcardPath, ExtHDpath):
    SDcardPath = SDcardPath.replace(' ', '\\ ')
    ExtHDpath = ExtHDpath.replace(' ', '\\ ')
    
    subprocess.call("rsync -aqr --remove-source-files "+SDcardPath+" "+ExtHDpath, shell=True)
    subprocess.call("find "+SDcardPath+" -type d -empty -delete", shell=True)


def is_dst(dt=None, timezone='UTC'):
    """Is daylight savings in effect?"""
    if dt is None:
        dt = datetime.datetime.utcnow()
    timezone = pytz.timezone(timezone)
    timezone_aware_date = timezone.localize(dt, is_dst=None)
    return timezone_aware_date.tzinfo._dst.seconds != 0


def sunrise_sunset(date):
    """Get the sunrise and sunset times adjusted for DST."""
    # 'date' is taken at midnight, but daylight savings starts/ends at 1am/2am
    # so move the time to midday to be accurate
    tdelta = datetime.timedelta(hours=12)
    date = date + tdelta
    # Get the unadjusted sunrise and sunset times
    city = LocationInfo('Karlsruhe', 'Germany', 'Europe/Ber', 49.098947, 8.437348) # Change this to suit your location 
    s = sun(city.observer, date=date)
    sunrise = s['sunrise']
    sunset = s['sunset']
    
    # Is daylight savings in effect?
    if is_dst(date, timezone='Europe/Berlin'): #change this to suit your location 
        tdelta = datetime.timedelta(hours=2)
        sunrise = sunrise + tdelta
        sunset = sunset + tdelta
   
    else:
        tdelta = datetime.timedelta(hours=1)
        sunrise = sunrise + tdelta
        sunset = sunset + tdelta  
      
      
    # To be conservative, round the time up to the nearest minute
    if sunrise.second > 0:
        sunrise = sunrise + datetime.timedelta(minutes=1)
    if sunrise.second > 13:
        sunset = sunset + datetime.timedelta(minutes=1)

    return sunrise, sunset


def HDR_fusion(images_array, FilePath):
    alignMTB = cv2.createAlignMTB()
    alignMTB.process(images_array, images_array)
    # Merge input images
    mergeMertens = cv2.createMergeMertens()
    exposureFusion = mergeMertens.process(images_array)
    # Save HDR image.
    Img_8bit = np.clip(exposureFusion*255, 0, 255).astype('uint8')
    
    def outer_circle(Img_8bit):
    
        width = sky.shape[0]
        height = sky.shape[1]
        center_on_width = int(width / 2)
        center_on_height = int(height / 2)
        circle_radius = 955

        sky_circle = np.zeros((width, height), dtype=np.uint8)
        rr, cc = draw.disk((center_on_width, center_on_height), circle_radius)
        sky_circle[rr, cc] = 1
        sky_trimmed = sky.copy()
        sky_trimmed[sky_circle == 0] = 0
        sky_trimmed[0:1946, 330:2274]

    return cv2.imwrite(FilePath, Img_8bit)


def HDR_fusion(images_array, FilePath):
        alignMTB = cv2.createAlignMTB()
        alignMTB.process(images_array, images_array)
        # Merge input images
        mergeMertens = cv2.createMergeMertens()
        exposureFusion = mergeMertens.process(images_array)
        # Save HDR image.
        Img_8bit = np.clip(exposureFusion*255, 0, 255).astype('uint8')
        return cv2.imwrite(FilePath, Img_8bit)

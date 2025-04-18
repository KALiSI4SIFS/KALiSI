# =========================================================
# How to run this script automatically using Cron:
#
# 1. Open crontab:
#    crontab -e
#
# 2. Add the following line to run the script every minute 
#    from 5:00 AM to 9:59 PM:
#
#    * 5-21 * * * /usr/bin/python3 /home/pi/your_script_name.py
#
#    - Replace /home/pi/your_script_name.py with the full path to this script.
#    - Adjust the python path if needed (find it with `which python3`).
#
# 3. (Optional) To log output for debugging, use:
#    * 5-21 * * * /usr/bin/python3 /home/pi/your_script_name.py >> /home/pi/cronlog.txt 2>&1
#
# =========================================================


import time
import datetime
import os
import csv
from utility_file import is_dst, sunrise_sunset
from sys import exit

import Adafruit_ADS1x15
adc = Adafruit_ADS1x15.ADS1115()
GAIN = 2  # +/-2.048V

folder_path = "/home/pi/Pictures"

# Get current date and time
now = datetime.datetime.now()
folder_name = now.strftime("%Y-%m-%d")
output_folder = os.path.join(folder_path, folder_name)
file_name_path = os.path.join(output_folder, folder_name) + ".csv"

# Create folder if it doesn't exist
if not os.path.isdir(output_folder):
    os.makedirs(output_folder)

# Create CSV file with headers if it doesn't exist
if not os.path.exists(file_name_path):
    with open(file_name_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Time", "GHI", "Cell_Temp"])

# Check if it's daytime
sunrise, sunset = sunrise_sunset(now)

if now.time() < sunrise.time() or now.time() > sunset.time():
    exit(0)

# If daytime, read sensor data and write to CSV
Solar_Irradiance_V = (adc.read_adc(0, GAIN) * (2.048 / 32768)) * 1000
Temperature_V = 65 * ((adc.read_adc(1, GAIN) * (2.048 / 32768)) - 0.6154)

data = [
    now.strftime("%Y-%m-%d"),
    now.strftime("%H:%M"),
    round(Solar_Irradiance_V, 2),
    round(Temperature_V, 2)
]

with open(file_name_path, 'a', newline='') as f:
    writer_object = csv.writer(f)
    writer_object.writerow(data)
  

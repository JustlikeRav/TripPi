import os
import glob
import pygame, sys
import time
from time import *
import serial
import urllib2, urllib

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

def print_data(lat,lng,temp):
    print "Latitude: " + lat + " | Longitude: " + lng + " | Temperature: " + temp
    
    #Save To Database
    mydata=[('lat',lat),('lon',lng),('temp',temp)]    #The first is the var name the second is the value
    mydata=urllib.urlencode(mydata)
    path='http://www.justlikerav.com/trippie/data.php'    #the url you want to POST to
    req=urllib2.Request(path, mydata)
    req.add_header("Content-type", "application/x-www-form-urlencoded")
    page=urllib2.urlopen(req).read()
    print page
	
def CoordinateToDouble(hours, minutes, seconds, NEWS):
    if NEWS == "W" or NEWS == "S": return (((minutes + ((seconds / 6000)%1))/60) + hours)*-1
    else: return ((minutes + ((seconds / 6000)%1))/60) + hours
 
def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp_raw():
	f = open(device_file, 'r')
	lines = f.readlines()
	f.close
	return lines

def read_temp():
	lines = read_temp_raw()
	while lines[0].strip()[-3:] != 'YES':
		time.sleep(0.2)
		lines = read_temp_raw()
	equals_pos = lines[1].find('t=')
	if equals_pos != -1:
		temp_string = lines[1][equals_pos+2:]
		temp_c = float(temp_string) / 1000.0
		return temp_c

ser = serial.Serial('/dev/ttyUSB0',4800,timeout = None)

fix = 1

x = 0
while x == 0:
   gps = ser.readline()

   if gps[1:6] == "GPGSA":
      fix = int(gps[9:10])
   if gps[1 : 6] == "GPGGA":

       if fix > 1:
          lat = CoordinateToDouble(float(gps[18:20]), float(gps[20:22]), float(gps[23:27]), gps[28:29])
          lon = CoordinateToDouble(float(gps[30:33]), float(gps[33:35]), float(gps[36:40]), gps[41:42])
	  print_data(str(lat),str(lon),str(read_temp()))
       else:
          lat = -1
          lon = -1
	  print_data(str(lat),str(lon),str(read_temp()))

#!/usr/bin/env python
import Image
import ImageStat
import math
import os
import time
import sys


def brightness(im_file):
   im = Image.open(im_file)
   stat = ImageStat.Stat(im)
   r,g,b = stat.mean
   return math.sqrt(0.241*(r**2) + 0.691*(g**2) + 0.068*(b**2))

def takeSample(tmpimg):
	import pygame.camera
	pygame.camera.init()
	cam = pygame.camera.Camera(pygame.camera.list_cameras()[0])
	cam.start()
	img = cam.get_image()
	import pygame.image
	pygame.image.save(img, tmpimg)
	pygame.camera.quit()
	cam.stop()
	
samplerate = 5.0
if len(sys.argv) >= 2:
	for arg in sys.argv:
		try:
                        samplerate = float(arg)
                        if samplerate < 0:
                        	print "Your sampling rate cannot be a negative number.  Resetting to default value of 5."
                        	samplerate = 5.0
                except:
                	if arg == "help" or arg == "--help" or arg == "-help":
	                	print "USAGE: autobrightness [TIME BETWEEN SAMPLES]... [CONFIG FILE]...\n Adjusts a laptop's brightness automatically, by using camera samples taken at a user definable interval."
	                	exit()
                	cfg_file = arg


while True:
	tmpimg = "/tmp/autobrightness-sample.bmp"
	takeSample(tmpimg)
	brightnessLevel = brightness(tmpimg)
	#os.remove(tmpimg)
	set = (brightnessLevel/255)*100
	os.system('xbacklight -set '+str(set))
	time.sleep(samplerate)


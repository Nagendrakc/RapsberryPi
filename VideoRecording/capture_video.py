#!/usr/bin/python

import os
import datetime as dt
import picamera
import time
import thread
import datetime

# Size in MB. Maximum space can be utilized for storing video files.  
max_size_of_storage = 300

# Length of the video capture in seconds
video_logth_to_capture = 120   

# Where the still photo captures are should be placed
still_path = '/var/www/html/pic.jpeg'

# Where the captured video files should be placed
video_path = '/var/www/html/captured_videos/'

cam_data = ['add_overlay', 'analog_gain', 'annotate_background', 'annotate_foreground', 'annotate_frame_num', 'annotate_text', 'annotate_text_size', 'awb_gains', 'awb_mode', 'brightness', 'capture', 'capture_continuous', 'capture_sequence', 'clock_mode', 'close', 'closed', 'color_effects', 'contrast', 'crop', 'digital_gain', 'drc_strength', 'exif_tags', 'exposure_compensation', 'exposure_mode', 'exposure_speed', 'flash_mode', 'frame', 'framerate', 'framerate_delta', 'hflip', 'image_denoise', 'image_effect', 'image_effect_params', 'iso', 'led', 'meter_mode', 'overlays', 'preview', 'preview_alpha', 'preview_fullscreen', 'preview_layer', 'preview_window', 'previewing', 'raw_format', 'record_sequence', 'recording', 'remove_overlay', 'request_key_frame', 'resolution', 'rotation', 'saturation', 'sensor_mode', 'sharpness', 'shutter_speed', 'split_recording', 'start_preview', 'start_recording', 'still_stats', 'stop_preview', 'stop_recording', 'timestamp', 'vflip', 'video_denoise', 'video_stabilization', 'wait_recording', 'zoom']

class MyCam:
	def __init__(self):
		self.cam = picamera.PiCamera()
		self.cam.annotate_text = "Video From Raspi Cam"

	def capture_still(self):
		#filename = dt.datetime.now().strftime("%d_%m_%Y_%H.%M.%S.jpeg")
		# 1280,960
		# 1024,768
		filename = still_path
		self.cam.resolution = (1024,768)
		self.cam.capture(filename)
    
	def start_video_capture(self):   
	        # filename fomat is "date_month_year_hour_.min.sec"
		# fileformat is *.h264
		videofilename = video_path + dt.datetime.now().strftime("%d_%m_%Y_%H.%M.%S.h264")
		# Available video resolution with camera
		# 720x480 --> 11mb per 60sec
		# 640X480 --> 8.3mb per 60sec
		# 160X120 --> 897K per 60sec
		# 320X240 --> 2.5mb per 60sec
		# 1024X768 --> 27mb per 60sec
		# 1920x1080
		# 2592x1944 (15fs)
		# 1296x972  (42fs)
		# 1296x730  (49fs)  --> 21MB per Min
		self.cam.resolution = (1296,730)
		self.cam.contrast = 25
		self.cam.sharpness = 25
		self.cam.meter_mode = 'matrix'
                print "Video Resolution : ",self.cam.resolution
                print "Video Brightness : ",self.cam.brightness
		self.cam.start_preview()
		time.sleep(2)
		print "Capturing on File {0}".format(videofilename)
		self.cam.start_recording(videofilename)

	def stop_video_capture(self):
		self.cam.stop_preview()
		time.sleep(2)
		self.cam.stop_recording()

	def monitor_video_store_space(self):
		# Monitor the storage space and make room for new video file. 
		# This makes sure that the video is captured always
		file_data = dict()
		l = os.listdir(video_path)
		total_size = sum(os.path.getsize(video_path+f) for f in l)/1024/1024
		print "Current Video Storage Size : {0} MB".format(total_size)
		print "Available Video Storage Size : {0} MB".format(max_size_of_storage-total_size)
		l.sort()
		for eachfile in l:
			file_stat = os.stat(video_path+eachfile)
			file_time = file_stat.st_mtime
			#print  file_time,'---',eachfile
			file_data[file_time] = eachfile
		if total_size >= max_size_of_storage:
			print 'removing file {0}'.format(l[0])
			os.remove(video_path+l[0])
			self.monitor_video_store_space()

	def get_camera_settings(self):
		print self.cam.contrast	
		print self.cam.awb_mode
		print self.cam.exif_tags
		print self.cam.framerate
		print self.cam.frame
		print self.cam.image_effect
		print self.cam.color_effects
		print self.cam.iso
		print self.cam.meter_mode
		print self.cam.saturation
		print self.cam.sensor_mode
		print self.cam.sharpness
		print self.cam.video_stabilization
		print self.cam.zoom

# Create camerapi instance
MC = MyCam()

# Go to infinete loop to capture video from CSI camera
# Below is the flow
# Step 1 -> Check the reserved video storage space
#           The max reserved space is defined in variable 'max_size_of_storage'
#           if the available space is reached max_size_of_storage, then delete the oldest video
#           file to make room for new video file
# Step 2 -> Start video capture, it is detached process
# Step 3 -> Go to sleep for till the defined video capture length 'video_logth_to_capture'
# Step 4 -> Stop video capture and repeate all steps again
# 
while 1 :
	MC.monitor_video_store_space()
	MC.start_video_capture()
	MC.get_camera_settings()
	time.sleep(video_logth_to_capture+2)
	MC.stop_video_capture()
	time.sleep(2)

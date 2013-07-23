#!/usr/bin/env python
"""
Demonstrates 

eg: ./015-archive.py --output triptych.avi "Washington"
"""
import argparse
from subprocess import call, STDOUT, check_output
import os
import re
import json
import requests
import glob
import math
import shutil
import datetime
import urllib
from urlparse import urlparse

def main():

	parser = argparse.ArgumentParser(description='Download some videos')
	parser.add_argument('--output', type=str, help='output name', default='triptych.avi')
	parser.add_argument('keyword', type=str, nargs=1, help='A keyword used to search YouTube')	
	args = parser.parse_args()

	base, ext = os.path.splitext( args.output )
	work_dir = "%s_tmp" % (base)
	if not os.path.exists(work_dir):
		os.makedirs(work_dir)

	width = 320
	height = 240

	now = datetime.datetime.now()
	time = '%d%02d%02d-%d%02d%02d' % (now.year, now.month, now.day-5, now.year, now.month, now.day)
	params = urllib.urlencode({'q': args.keyword[0], 'time': time, 'output': 'json'})
	url = "http://archive.org/details/tv?"+params
	r = requests.get(url)
	items = r.json()
	

	videos = []
	durations = []

	for item in items[0:3]:
		o = urlparse(item["video"])
		fname, ext = os.path.splitext( o.path )
		orig = '{0}/{1}{2}'.format(work_dir, item["identifier"], ext)
		avi = "{0}/{1}.avi".format(work_dir, item["identifier"])

		if os.path.exists(orig)==False:
			urllib.urlretrieve(item["video"], orig)

		#	Transcode
		cmd = 'ffmpeg -loglevel quiet -n -i {0} -q:v 1 -r 30 -s {1}x{2} {3}'.format(orig, width, height, avi)
		call(cmd, shell=True)

		videos.append(avi)

		#	Get duration
		cmd = 'ffprobe -i {0}'.format(avi)
		stderr = check_output(cmd, stderr=STDOUT, shell=True)
		match = re.search(r"Duration:\s+(?P<hours>\d+?):(?P<minutes>\d+?):(?P<seconds>\d+\.\d+?),", stderr)
		duration = (int(match.group("hours")) * 3600) + (int(match.group("minutes")) * 60) + float(match.group("seconds"))
		durations.append(duration)

	longest = max(durations)

	inputs = ""
	filter_complex ='color=duration={0}:size={1}x{2}:rate=30[canvas];'.format( math.ceil(longest), width*3, height )

	x = 0
	for i, video in enumerate(videos):
		inputs += "-i {0} ".format(video)

		if i==0: # Add the first video to the canvas generated in the first filter
			filter_complex += '[canvas][{0}:v]overlay=0:0[vid{1}];'.format(i, i)

		elif i==len(videos)-1: # Overlay this scaled video on top of the last output
			filter_complex += "[vid{0}][{1}:v]overlay={2}:0;".format( str(i-1), i, x )

		else: # Overlay this scaled video on top of the last output and create a new output (vidX)
			filter_complex += "[vid{0}][{1}:v]overlay={2}:0[vid{3}];".format(str(i-1), i, x, i )
		
		x += width

	filter_complex += "amix=inputs={0}".format(len(videos))

	cmd = 'ffmpeg -y {0} -filter_complex "{1}" -t {2} {3}'.format(inputs, filter_complex, math.ceil( longest ), args.output)
	call(cmd, shell=True)

	if os.path.exists(args.output):
		shutil.rmtree(work_dir)

	print "done!"


if __name__ == '__main__':
	main()
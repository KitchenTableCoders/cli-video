#!/usr/bin/env python
"""
Demonstrates 

Try these commands first:

ffmpeg -filter_complex "color=duration=5:color=0xFF0000" red.avi
ffmpeg -filter_complex "color=duration=233.0:size=960x240:rate=30" out.avi
ffmpeg -i small.mp4 -filter_complex "color=duration=233.0:size=960x240:rate=30[canvas];[canvas][0:v]overlay=20:20" out.avi


eg: ./014-triptych.py --output triptych.avi "brooklyn, NY"
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

	feed_url = "http://gdata.youtube.com/feeds/api/videos?q={0}&max-results=5&v=2&alt=json".format(args.keyword[0])
	r = requests.get(feed_url)
	feed = json.loads( r.text )
	videos = []
	durations = []

	for i, entry in enumerate(feed["feed"]["entry"]):

		url = entry["link"][0]["href"]
		mp4 = "{0}/{1}.mp4".format(work_dir, i)
		avi = "{0}/{1}.avi".format(work_dir, i)

		#	Download
		cmd = 'youtube-dl -f 18 -o "{0}" "{1}"'.format(mp4, url)
		call(cmd, shell=True)

		#	Transcode
		cmd = 'ffmpeg -loglevel quiet -n -i {0} -q:v 1 -r 30 -s {1}x{2} {3}'.format(mp4, width, height, avi)
		call(cmd, shell=True)

		videos.append(avi)

		#	Get duration
		cmd = 'ffprobe -i {0}/{1}.avi'.format(work_dir, i)
		stderr = check_output(cmd, stderr=STDOUT, shell=True)
		match = re.search(r"Duration:\s+(?P<hours>\d+?):(?P<minutes>\d+?):(?P<seconds>\d+\.\d+?),", stderr)
		duration = (int(match.group("hours")) * 3600) + (int(match.group("minutes")) * 60) + float(match.group("seconds"))
		durations.append(duration)

	longest = max(durations)

	inputs = ""
	filter_complex ='color=duration={0}:size={1}x{2}:rate=30[canvas];'.format( math.ceil(longest), width*len(videos), height )

	x = 0
	for i, video in enumerate(videos):
		inputs += "-i {0} ".format(video)

		if i==0: # Add the first video to the canvas generated in the first filter
			filter_complex += '[canvas][0:v]overlay=0:0[vid0];'

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
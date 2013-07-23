#!/usr/bin/env python
"""
Demonstrates getting the duration of a video

eg: 	./011-duration.py "skateboarding dog"
"""
import argparse
from subprocess import call, STDOUT, check_output
import os
import re
import json
import requests
import glob

def main():

	parser = argparse.ArgumentParser(description='Download some videos')
	parser.add_argument('--output', type=str, help='output name', default='triptych.mp4')
	parser.add_argument('keyword', type=str, nargs=1, help='A keyword used to search YouTube')	
	args = parser.parse_args()

	base, ext = os.path.splitext( args.output )
	work_dir = "%s_tmp" % (base)
	if not os.path.exists(work_dir):
		os.makedirs(work_dir)


	feed_url = "http://gdata.youtube.com/feeds/api/videos?q={0}&max-results=3&v=2&alt=json".format(args.keyword[0])
	r = requests.get(feed_url)
	feed = json.loads( r.text )

	for i, entry in enumerate(feed["feed"]["entry"]):
		#	Download
		cmd = 'youtube-dl -f 18 -o "{0}/{1}.mp4" "{2}"'.format(work_dir, i, entry["link"][0]["href"])
		call(cmd, shell=True)

		#	Transcode
		#	-n          do not overwrite output files
		#	-i 			input file
		#	-r rate     set frame rate (Hz value, fraction or abbreviation)
		#	-s 			resize video
		cmd = 'ffmpeg -loglevel quiet -n -i {0}/{1}.mp4 -r 30 -s 320x240 {0}/{1}.avi'.format(work_dir, i, work_dir, i)
		call(cmd, shell=True)

		#	Get duration
		cmd = 'ffprobe -i {0}/{1}.avi'.format(work_dir, i)
		stderr = check_output(cmd, stderr=STDOUT, shell=True)
		match = re.search(r"Duration:\s+(?P<hours>\d+?):(?P<minutes>\d+?):(?P<seconds>\d+\.\d+?),", stderr)
		duration = (int(match.group("hours")) * 3600) + (int(match.group("minutes")) * 60) + float(match.group("seconds"))

		print duration

	print "done!"


if __name__ == '__main__':
	main()
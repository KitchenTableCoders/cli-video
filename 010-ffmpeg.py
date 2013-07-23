#!/usr/bin/env python
"""
Demonstrates converting the videos to a uniform format after download

eg: 	./010-ffmpeg.py --output "dog.mp4" "skateboarding dog"
"""
import argparse
import subprocess
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
		url = entry["link"][0]["href"]
		cmd = 'youtube-dl -f 18 -o "{0}/{1}.mp4" "{2}"'.format(work_dir, i, url)
		subprocess.call(cmd, shell=True)
		cmd = 'ffmpeg -loglevel quiet -n -i {0}/{1}.mp4 -q:v 1 -r 30 {0}/{1}.avi'.format(work_dir, i, work_dir, i)
		subprocess.call(cmd, shell=True)
		

	print "done!"


if __name__ == '__main__':
	main()
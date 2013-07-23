#!/usr/bin/env python
"""
Demonstrates finding the name of the video from the output of youtube-dl (not recommended)

eg: 	./009-destination.py "skateboarding dog"
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

	for entry in feed["feed"]["entry"]:
		#title = entry["title"]["$t"]
		url = entry["link"][0]["href"]
		cmd = 'youtube-dl -o "{0}/%(title)s.%(ext)s" {1}'.format(work_dir, url)

		# Notice that we use subprocess.check_output instead of subprocess.call
		stdout = subprocess.check_output(cmd, shell=True)
		match = re.search(r'\[download\] Destination: (.+)', stdout)
		if match:                      
			print 'found', match.group(1)
		else:
			print 'did not find'	


if __name__ == '__main__':
	main()
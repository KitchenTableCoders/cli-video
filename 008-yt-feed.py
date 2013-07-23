#!/usr/bin/env python
"""
Demonstrates parsing a Youtube feed and passing the results to youtube-dl
https://developers.google.com/youtube/2.0/developers_guide_protocol_video_feeds#Videos_feed

note: you might need to do `sudo pip install requests' before running this script

eg: 	./008-yt-feed.py "skateboarding dog"
"""
import argparse
import subprocess
import os
import json
import requests

def main():

	parser = argparse.ArgumentParser(description='Download some videos')
	parser.add_argument('--dest', type=str, help='output destination', default='work')
	parser.add_argument('--num', type=int, help='number of videos', default=10)
	parser.add_argument('keyword', type=str, nargs=1, help='A keyword used to search YouTube')	
	args = parser.parse_args()

	if not os.path.exists(args.dest):
		os.makedirs(args.dest)

	feed_url = "http://gdata.youtube.com/feeds/api/videos?q={0}&max-results={1}&v=2&alt=json".format(args.keyword[0], args.num)
	r = requests.get(feed_url)
	feed = json.loads( r.text )

	for i, entry in enumerate(feed["feed"]["entry"]):
		#title = entry["title"]["$t"]
		url = entry["link"][0]["href"]
		cmd = 'youtube-dl -o "{0}/{1}.%(ext)s" {2}'.format(args.dest, i, url)
		subprocess.call(cmd, shell=True)


if __name__ == '__main__':
	main()
#!/usr/bin/env python
"""
Creates a video from a series of Google Street View API images

https://developers.google.com/maps/documentation/streetview

eg: ./026-hyperlapse.py --origin "274 Morgan Ave, 11211" --destination "Times Square, NYC" 
"""
import argparse 	# http://docs.python.org/2/library/argparse.html#module-argparse
import subprocess
import urllib
import os
import shutil
import requests
import json
import math

api_key = "AIzaSyBAtUbXjwQbKXulkh2HQWc5W2QOe5PIE40"


def bearing(lat1, lon1, lat2, lon2):
	lat1 = math.radians(lat1)
	lon1 = math.radians(lon1)
	lat2 = math.radians(lat2)
	lon2 = math.radians(lon2)
	dLat = lat2 - lat1
	dLon = lon2 - lon1
	y = math.sin(dLon) * math.cos(lat2);
	x = math.cos(lat1) * math.sin(lat2) - math.sin(lat1)* math.cos(lat2)*math.cos(dLon);
	brng = math.atan2(y, x)
	return math.degrees( brng )


def main():
	parser = argparse.ArgumentParser(description='Create a video using Google Streetview')
	parser.add_argument('--origin', type=str, help='a location', default="Times Square, NYC")	
	parser.add_argument('--destination', type=str, help='a location', default="Times Square, NYC")
	parser.add_argument('--output', type=str, help='output file', default="hyperlapse.avi")
	args = parser.parse_args()

	base, ext = os.path.splitext( args.output )
	work_dir = "%s_tmp" % (base)
	if not os.path.exists(work_dir):
		os.makedirs(work_dir)

	query = urllib.urlencode({"sensor": "false", "origin": args.origin, "destination": args.destination})
	url = "http://maps.googleapis.com/maps/api/directions/json?{0}".format(query)
	r = requests.get(url)
	json = r.json()
	distance = json["routes"][0]["legs"][0]["distance"]["value"]
	steps = json["routes"][0]["legs"][0]["steps"]
	n = 0
	cmd = "melt "
	for step in steps:
		start_lat = step["start_location"]["lat"]
		start_lng = step["start_location"]["lng"]
		end_lat = step["end_location"]["lat"]
		end_lng = step["end_location"]["lng"]
		delta_lat = end_lat - start_lat
		delta_lng = end_lng - start_lng
		distance = step["distance"]["value"]
		
		substeps =  int(math.ceil(distance/12))
		print "Plotting {5} points, distance of {4}, from {0},{1} to {2},{3}".format(start_lat, start_lng, end_lat, end_lng, distance, substeps)

		lat = start_lat
		lng = start_lng
		
		for substep in range(0, substeps):
			pct = float(substep) / float(substeps)
			new_lat = start_lat + (delta_lat * pct)
			new_lng = start_lng + (delta_lng * pct)
			heading = bearing(lat, lng, new_lat, new_lng)

			lat = new_lat
			lng = new_lng
			location = "{0},{1}".format(lat,lng)
			query = urllib.urlencode({"size": "320x240", "location": location, "heading": heading, "sensor": "false", "key": api_key})
			remote = 'http://maps.googleapis.com/maps/api/streetview?{0}'.format(query)
			local = "{0}/{1:03d}.png".format(work_dir, n)
			if os.path.exists(local)==False:
				urllib.urlretrieve(remote, local)
			cmd += "{0} out=5 -mix 4 -mixer luma ".format(local)
			n += 1


	cmd += "color:black out=50 -mix 50 -mixer luma "
	cmd += "-consumer avformat:{0} vcodec=libxvid vb=5000k r=30 s=320x240".format(args.output)
	subprocess.call(cmd, shell=True)

	if os.path.exists(args.output):
		shutil.rmtree(work_dir)

if __name__ == '__main__':
	main()
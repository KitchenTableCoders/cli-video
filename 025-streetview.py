#!/usr/bin/env python
"""
Creates a video from a series of Google Street View API images

https://developers.google.com/maps/documentation/streetview

eg: ./025-streetview.py --location "Offenbacher Landstrasse 473, Frankfurt, Germany" --output "Offenbacher.avi"
"""
import argparse 	# http://docs.python.org/2/library/argparse.html#module-argparse
import subprocess
import urllib
import os
import shutil

api_key = "AIzaSyBAtUbXjwQbKXulkh2HQWc5W2QOe5PIE40"

def main():

	parser = argparse.ArgumentParser(description='Create a video using Google Streetview')
	parser.add_argument('--location', type=str, help='a location', default="Times Square, NYC")	
	parser.add_argument('--output', type=str, help='output file', default="streetview.avi")
	args = parser.parse_args()

	base, ext = os.path.splitext( args.output )
	work_dir = "%s_tmp" % (base)
	if not os.path.exists(work_dir):
		os.makedirs(work_dir)

	cmd = "melt "
	n = 0
	for heading in range(0, 360, 2):
		query = urllib.urlencode({"size": "600x400", "location": args.location, "sensor": "false", "heading": heading, "key": api_key})
		remote = 'http://maps.googleapis.com/maps/api/streetview?{0}'.format(query)
		local = "{0}/{1:03d}.png".format(work_dir, n)
		n+=1
		if os.path.exists(local)==False:
			urllib.urlretrieve(remote, local)	
		cmd += "{0} out=5 -mix 4 -mixer luma ".format(local)

	cmd += "color:black out=50 -mix 50 -mixer luma "
	cmd += "-consumer avformat:{0} vcodec=libxvid vb=5000k r=30 s=600x400".format(args.output)
	subprocess.call(cmd, shell=True)

	if os.path.exists(args.output):
		shutil.rmtree(work_dir)

if __name__ == '__main__':
	main()
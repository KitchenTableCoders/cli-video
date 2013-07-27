#!/usr/bin/env python
"""
Demonstrate how to get frame information from a video

Try this command first: 
ffprobe -loglevel quiet -show_frames data/giant.mp4

eg: ./016-frames.py data/giant.mp4
"""
import argparse 	# http://docs.python.org/2/library/argparse.html#module-argparse
import subprocess
import re

def main():
	parser = argparse.ArgumentParser(description='Get frame information about a video')
	parser.add_argument('video', type=str, nargs=1, help='a videos')	# nargs='+' means "at least one"
	args = parser.parse_args()

	cmd = u'ffprobe -loglevel quiet -show_frames {0}'.format(args.video[0])
	stdout = subprocess.check_output(cmd, shell=True)
	pieces = stdout.split(u"[/FRAME]\n")
	frames = []
	for piece in pieces:
		if "media_type=video" in piece:
			frame = {}
			start = re.search(r"pkt_pts_time=([\d\.]+)", piece)
			if start: frame["start"] = float( start.group(1) )
			end = re.search(r"pkt_dts_time=([\d\.]+)", piece)
			if end: frame["end"] = float( end.group(1) )
			duration = re.search(r"pkt_duration_time=([\d\.]+)", piece)
			if duration: frame["duration"] = float( duration.group(1) )
			number = re.search(r"coded_picture_number=([\d\.]+)", piece)
			if number: 
				frame["number"] = int( number.group(1) )
				frames.append( frame )
	print frames


if __name__ == '__main__':
	main()
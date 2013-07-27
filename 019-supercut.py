#!/usr/bin/env python
"""
Introduces melt

eg: ./019-supercut.py data/giant.mp4 data/cows-big.flv data/puppets.mp4 data/nintendo-big.mp4
"""
import argparse 	# http://docs.python.org/2/library/argparse.html#module-argparse
import subprocess
import re
import os

def get_frames( video ):
	""" Basically parses the output of ffprobe"""
	cmd = u'ffprobe -loglevel quiet -show_frames {0}'.format(video)
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
	return frames


def main():

	parser = argparse.ArgumentParser(description='Mush together some videos')
	parser.add_argument('--frames', type=int, help='number of frames in video', default=5000)
	parser.add_argument('--output', type=str, help='output name')
	parser.add_argument('videos', type=str, nargs='+', help='some videos')	# nargs='+' means "at least one"
	args = parser.parse_args()

	# Construct some video objects
	videos = []
	for path in args.videos:
		video = {"pos": 500, "path": path, "nframes": len(get_frames(path))}
		videos.append( video )

	cmd = "melt color:black out=100 "
	inc = 60
	v = 0
	for i in range(0, args.frames, inc):
		cmd += '{0} in={1} out={2} -mix 10 -mixer luma '.format(videos[v]["path"], videos[v]["pos"], videos[v]["pos"]+inc)
		videos[v]["pos"] += inc
		if videos[v]["pos"] >= videos[v]["nframes"]:
			videos[v]["pos"] = 0

		v = (v+1) % len(videos)

	cmd += "color:black out=100 -mix 50 -mixer luma "
	if args.output != None:
		cmd += "-consumer avformat:{0} vcodec=libxvid acodec=aac ab=448000 vb=5000k r=30 s=640x480".format(args.output)
	
	# Check the command length on the host OS
	if len(cmd) > os.sysconf(os.sysconf_names['SC_ARG_MAX']):
		raise EnvironmentError("command is too long!")

	subprocess.call(cmd, shell=True)


if __name__ == '__main__':
	main()
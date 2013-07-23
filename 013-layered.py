#!/usr/bin/env python
"""
Introduces ffmpeg overlays

eg: ./013-layered.py data/cows-big.flv data/nintendo-big.mp4 data/nintendo-small.mp4 --output layered.avi
"""
import argparse 	# http://docs.python.org/2/library/argparse.html#module-argparse
import subprocess


def main():

	parser = argparse.ArgumentParser(description='stacks some videos')
	parser.add_argument('--output', type=str, help='the output video', default='layered.avi')
	parser.add_argument('videos', type=str, nargs=3, help='Three videos to stack')
	args = parser.parse_args()

	filters = '[0:v][1:v]overlay=20:20[firstTwo];[firstTwo][2:v]overlay=40:40;amix=inputs=3'

	#	http://www.ffmpeg.org/ffmpeg-filters.html#overlay-1
	#	main_w, overlay_w, main_h, overlay_h
	cmd = 'ffmpeg -i {0} -i {1} -i {2} -filter_complex "{3}" {4}'.format(args.videos[0], args.videos[1], args.videos[2], filters, args.output)
	subprocess.call(cmd, shell=True)


if __name__ == '__main__':
	main()



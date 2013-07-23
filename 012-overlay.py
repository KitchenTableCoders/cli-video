#!/usr/bin/env python
"""
Introduces ffmpeg overlays

eg: ./ssve012.py --video data/big.mp4 --watermark data/watermark.png watermarked.avi
"""
import argparse 	# http://docs.python.org/2/library/argparse.html#module-argparse
import subprocess


def main():

	parser = argparse.ArgumentParser(description='Watermarks a video using a transparent image')
	parser.add_argument('--video', type=str, help='a video')
	parser.add_argument('--watermark', type=str, help='a watermark image')
	parser.add_argument('output', type=str, nargs=1, help='The resulting image')
	args = parser.parse_args()

	#	http://www.ffmpeg.org/ffmpeg-filters.html#overlay-1
	#	main_w, overlay_w, main_h, overlay_h
	cmd = 'ffmpeg -i {0} -i {1} -filter_complex "[0:v][1:v]overlay=10:10" {2}'.format(args.video, args.watermark, args.output[0])
	subprocess.call(cmd, shell=True)


if __name__ == '__main__':
	main()



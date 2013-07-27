#!/usr/bin/env python
"""
Introduces crossfade via melt
http://www.mltframework.org/bin/view/MLT/MltMelt

eg: ./016-melt.py --output crossfade.mp4 data/giant.mp4 data/cows-big.flv 
"""
import argparse 	# http://docs.python.org/2/library/argparse.html#module-argparse
import subprocess

def main():

	parser = argparse.ArgumentParser(description='Mush together some videos')
	parser.add_argument('--output', type=str, help='output name', default="out.mp4")
	parser.add_argument('videos', type=str, nargs=2, help='some videos')	# nargs='+' means "at least one"
	args = parser.parse_args()

	cmd = "melt color:black out=120 "
	cmd += "{0} in=1000 out=2000 -mix 50 -mixer luma ".format(args.videos[0])
	cmd += "{0} in=1000 out=2000 -mix 200 -mixer luma ".format(args.videos[1])
	cmd += "color:black out=50 -mix 50 -mixer luma "
	cmd += "-consumer avformat:{0} vcodec=libxvid acodec=aac ab=448000 vb=5000k r=30 s=640x480".format(args.output)
	subprocess.call(cmd, shell=True)

if __name__ == '__main__':
	main()
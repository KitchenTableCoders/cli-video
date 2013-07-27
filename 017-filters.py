#!/usr/bin/env python
"""
Introduces melt filters

http://www.mltframework.org/bin/view/MLT/PluginsFilters
http://www.mltframework.org/bin/view/MLT/FilterFrei0r-cartoon

Frei0r
http://frei0r.dyne.org/

melt -query "filters"

Filters:

   Filters are frame modifiers - they can change the contents of the audio or
   the images associated to a frame.

   $ melt a.dv -filter greyscale

   As with producers, properties may be specified on filters too.
   
   Again, in and out properties are common to all, so to apply a filter to a
   range of frames, you would use something like:
   
   $ melt a.dv -filter greyscale in=0 out=50
   
   Again, filters have their own set of rules about properties and will
   silently ignore properties that do not apply.


eg: ./017-filters.py --output filters.mp4 data/giant.mp4 data/cows-big.flv 
"""
import argparse 	# http://docs.python.org/2/library/argparse.html#module-argparse
import subprocess
import os


def frange(x, y, jump):
	while x < y:
		yield x
		x += jump


def main():

	parser = argparse.ArgumentParser(description='Mush together some videos')
	parser.add_argument('--output', type=str, help='output name', default="out.mp4")
	parser.add_argument('videos', type=str, nargs=2, help='some videos')
	args = parser.parse_args()

	cmd = "melt "
	cmd += "{0} in=1000 out=2000 -mix 50 -mixer luma ".format(args.videos[0])
	cmd += "{0} in=1000 out=2000 -mix 200 -mixer luma ".format(args.videos[1])
	cmd += "color:black out=50 -mix 50 -mixer luma "
	
	cmd += "-filter frei0r.cartoon in=0 out=300 "
	cmd += "-filter burningtv in=300 out=600 "
	cmd += "-filter frei0r.sobel in=600 out=900 "
	
	_in = 900
	for _size in frange(0, 0.5, 0.005):
		cmd += "-filter frei0r.pixeliz0r 0={0} 1={0} in={1} out={2} ".format(_size, _in, _in+20)
		_in += 5
	
	cmd += "-consumer avformat:{0} vcodec=libxvid acodec=aac ab=448000 vb=5000k r=30 s=640x480".format(args.output)
	print cmd
	subprocess.call(cmd, shell=True)

if __name__ == '__main__':
	main()

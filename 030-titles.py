#!/usr/bin/env python
"""
Titles!

eg: ./030-titles.py --name Jeff 
"""
import argparse 	# http://docs.python.org/2/library/argparse.html#module-argparse
import subprocess
import os
from tempfile import mkstemp
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


def makeTextVideo( path, lines, y_start, width=640, height=480 ):
	global fontDir
	_, temp_path = mkstemp(suffix = '.png')
	image = Image.new("RGB", (width, height), (0, 0, 0))
	draw = ImageDraw.Draw(image)
	padding = 1.2
	y = y_start
	for line in lines:
		w = width+1
		h = 0
		while w > width-15:
			font = ImageFont.truetype(line["font"], line["size"])
			size = font.getsize( line["text"] )
			w = size[0]
			h = size[1]
			line["size"]-=1
		x = (width/2.0) - (w/2.0)
		draw.text((x, y), line["text"], (255, 0, 255), font=font)
		y += h * padding
	image.save(temp_path)
	cmd = u'ffmpeg -y -loglevel quiet -loop 1 -qscale 1 -f image2 -i %s -r 30 -t 10 -an %s' % (temp_path, path)
	subprocess.call(cmd, shell=True)
	os.remove( temp_path )
	return path


def main():

	parser = argparse.ArgumentParser(description='Say a sentence')
	parser.add_argument('--name', type=str, help='a name')
	args = parser.parse_args()

	introClip = "intro.avi"
	intro = [
			{"text": args.name, "size": 48, "font": "data/Railway.TTF"},
			{"text": "Description", "size": 24, "font": "data/Railway.ttf"},
			{"text": "  ", "size": 24, "font": "data/Railway.ttf"},
			{"text": "music:", "size": 24, "font": "data/Railway.ttf"},
			{"text": "song_text", "size": 18, "font": "data/Railway.ttf"} ]
	makeTextVideo( introClip, intro, 120 )

if __name__ == '__main__':
	main()
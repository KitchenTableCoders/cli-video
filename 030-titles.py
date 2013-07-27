#!/usr/bin/env python
"""
Demonstrates using PIL to create a single image, which is then turned into a video
http://www.pythonware.com/products/pil/

eg: ./030-titles.py --name Jeff 
"""
import argparse 	# http://docs.python.org/2/library/argparse.html#module-argparse
import subprocess
import os
from tempfile import mkstemp
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont




def main():

	parser = argparse.ArgumentParser(description='Say a sentence')
	parser.add_argument('--name', type=str, help='a name')
	parser.add_argument('--output', type=str, default='title.avi')
	args = parser.parse_args()

	width = 640
	height = 480

	# Create a list of dictionaries.  Each dict contains "text" and "size"
	lines = [
			{"text": args.name, "size": 48, "font": "data/Railway.TTF"},
			{"text": "Description", "size": 24, "font": "data/Railway.ttf"},
			{"text": "  ", "size": 24, "font": "data/Railway.ttf"},
			{"text": "music:", "size": 24, "font": "data/Railway.ttf"},
			{"text": "song_text", "size": 18, "font": "data/Railway.ttf"} ]

	_, temp_path = mkstemp(suffix = '.png')
	image = Image.new("RGB", (width, height), (0, 0, 0))
	draw = ImageDraw.Draw(image)
	padding = 1.2
	y = 120
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

	cmd = 'ffmpeg -y -loglevel quiet -loop 1 -qscale 1 -f image2 -i %s -r 30 -t 10 -an %s' % (temp_path, args.output)
	print cmd
	subprocess.call(cmd, shell=True)
	os.remove( temp_path )


if __name__ == '__main__':
	main()



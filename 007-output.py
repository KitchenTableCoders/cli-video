#!/usr/bin/env python
"""
Similar to ssve005, except that we are now using argparse and saving into a user-specified output folder
See the "output template" section of the youtube-dl documentation:
http://rg3.github.io/youtube-dl/documentation.html#d7

eg: 	./007-output.py http://www.youtube.com/watch?v=18-xvIjH8T4 \
	http://www.youtube.com/watch?v=2Syd_BUbl5A \
	http://www.youtube.com/watch?v=cU8HrO7XuiE
"""
import argparse
import subprocess
import os


def main():

	parser = argparse.ArgumentParser(description='Download some videos')
	parser.add_argument('--dest', type=str, help='output destination', default='work')
	parser.add_argument('videos', type=str, nargs='+', help='some youtube links')	# nargs='+' means "at least one"
	args = parser.parse_args()

	if not os.path.exists(args.dest):
		os.makedirs(args.dest)

	for i, url in enumerate(args.videos):
		cmd = 'youtube-dl -o "{0}/{1}.%(ext)s" {2}'.format(args.dest, i, url)
		subprocess.call(cmd, shell=True)


if __name__ == '__main__':
	main()
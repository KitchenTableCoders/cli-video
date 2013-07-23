#!/usr/bin/env python
"""
Demonstrates fetching id3 information for a song


Note: sudo pip install mutagen

eg: ./020-id3.py "data/06 Cliantro Vision.mp3"

"""
import argparse
from mutagen.easyid3 import EasyID3


def main():

	parser = argparse.ArgumentParser(description='Download some videos')
	parser.add_argument('song', type=str, nargs=1, help='The song to read id3 tags from')	
	args = parser.parse_args()

	audio = EasyID3(args.song[0])
	print "Album: "+audio["album"][0]
	print "Artist: "+audio["artist"][0]
	print "Title: "+audio["title"][0]


if __name__ == '__main__':
	main()
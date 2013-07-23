#!/usr/bin/env python
"""
Demonstrates fetching Echonest data for a song

Get a key!  https://developer.echonest.com/account/register

eg: ./021-echonest.py "data/06 Cliantro Vision.mp3"

"""
import argparse
import json
import requests
import hashlib
import time

api_key = "OHIGAA8TFWUEWMX6K"

def get_analysis( song ):
	"""Returns a json object that contains the echonest analysis for the supplied song"""
	
	md5 = hashlib.md5(open(song, 'rb').read()).hexdigest()
	url = "http://developer.echonest.com/api/v4/track/profile?api_key={0}&format=json&md5={1}&bucket=audio_summary".format(api_key, md5)
	r = requests.get(url)
	profile = json.loads( r.text )

	if profile["response"]["status"]["code"] == 5: # The Identifier specified does not exist
		url = 'http://developer.echonest.com/api/v4/track/upload'
		files = {'track': open(song, 'rb')}
		data = {'filetype': 'mp3', 'api_key': api_key}
		print "Uploading {0}...".format(song)
		r = requests.post(url, files=files, data=data)
		response = json.loads( r.text )
 		if response["response"]["status"]["code"]==0:	# Upload succeeded 
 			print "Waiting 2 seconds for analysis..."
 			time.sleep(2)
 			return get_analysis( song )

	elif profile["response"]["track"]["status"]=="pending":
		print "Analysis pending.  Waiting 2 more seconds..."
 		time.sleep(2)
 		return get_analysis( song )

	elif profile["response"]["track"]["status"]=="complete":
		url = profile["response"]["track"]["audio_summary"]["analysis_url"]
		r = requests.get(url)
		analysis = json.loads( r.text )
		return analysis



def main():
	parser = argparse.ArgumentParser(description='Download some videos')
	parser.add_argument('--key', type=str, help='Echonest developers key', default=api_key)
	parser.add_argument('song', type=str, nargs=1, help='The song to read id3 tags from')	
	args = parser.parse_args()
	
	analysis = get_analysis(args.song[0])
	print "Sections: {0}".format(len(analysis["sections"]))
	print "Bars: {0}".format(len(analysis["bars"]))
	print "Beats: {0}".format(len(analysis["beats"]))
	print "Tatums: {0}".format(len(analysis["tatums"]))
	print "Segments: {0}".format(len(analysis["segments"]))


if __name__ == '__main__':
	main()
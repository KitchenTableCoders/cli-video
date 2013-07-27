"""
Utils for dealing with video
"""
from subprocess import check_output, call, STDOUT
import json
import requests
import hashlib
import time
import re



def get_analysis( song, echo_api_key ):
	"""Returns a json object that contains the echonest analysis for the supplied song"""

	md5 = hashlib.md5(open(song, 'rb').read()).hexdigest()
	url = "http://developer.echonest.com/api/v4/track/profile?api_key={0}&format=json&md5={1}&bucket=audio_summary".format(echo_api_key, md5)
	r = requests.get(url)
	profile = json.loads( r.text )

	if profile["response"]["status"]["code"] == 5: # The Identifier specified does not exist
		url = 'http://developer.echonest.com/api/v4/track/upload'
		files = {'track': open(song, 'rb')}
		data = {'filetype': 'mp3', 'api_key': echo_api_key}
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


def get_frames(video):
	"""
	Get an array of dicts containing information about each frame of a video:
	
	{
		start: the start time of the frame
		end: the end time of the frame
		duration: end-start (?)
		number: the sequential number of the frame
	}
	""" 
	cmd = u'ffprobe -loglevel quiet -show_frames {0}'.format(video)
	stdout = check_output(cmd, shell=True)
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



def get_duration(video):
	""" Get the duration of a video (seconds) using ffprobe"""
	cmd = 'ffprobe -i {0}'.format(video)
	stderr = check_output(cmd, stderr=STDOUT, shell=True)
	match = re.search(r"Duration:\s+(?P<hours>\d+?):(?P<minutes>\d+?):(?P<seconds>\d+\.\d+?),", stderr)
	duration = (int(match.group("hours")) * 3600) + (int(match.group("minutes")) * 60) + float(match.group("seconds"))
	return duration


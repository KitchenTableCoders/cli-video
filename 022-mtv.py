#!/usr/bin/env python
"""
Demonstrates editing a video to the beat of a song

Get a key!  https://developer.echonest.com/account/register

eg: ./022-mtv.py --song "data/06 Cliantro Vision.mp3" data/cows-big.flv data/giant.mp4 data/nintendo-big.mp4 data/puppets.mp4

"""
import argparse
import subprocess
from videoutils import get_analysis, get_frames, get_duration


echo_api_key = "OHIGAA8TFWUEWMX6K"


def main():
	parser = argparse.ArgumentParser(description='Download some videos')
	parser.add_argument('--key', type=str, help='Echonest developers key', default=echo_api_key)
	parser.add_argument('--song', type=str, help='The song to read id3 tags from')	
	parser.add_argument('--output', type=str, help='The song to read id3 tags from')	
	parser.add_argument('videos', type=str, nargs='+', help='The videos to edit together')	
	args = parser.parse_args()
	

	# Step 1: collect information about videos
	videos = []
	for path in args.videos:
		nframes = len(get_frames(path))
		duration = get_duration(path)
		fps = nframes / duration
		videos.append({"path": path, "duration": duration, "nframes": nframes, "fps": fps, "position": 100}) 

	# Step 2: get song analysis
	analysis = get_analysis(args.song, echo_api_key)

	# Step 3: create melt command
	v = 0
	cmd = 'melt -audio-track "{0}" -video-track '.format(args.song)
	for beat in analysis["beats"]:
		video = videos[v]
		n_frames = int(beat["duration"] * video["fps"])

		cmd += '"{0}" in={1} out={2} '.format(video["path"], video["position"], video["position"]+n_frames)
		v = (v+1) % len(videos)
		video["position"] += n_frames
		if video["position"] > video["nframes"]:
			video["position"] = 100

	cmd += "color:black out=50 -mix 50 -mixer luma "
	if args.output != None:
		cmd += "-consumer avformat:{0} vcodec=libxvid acodec=aac ab=448000 vb=5000k r=30 s=640x480".format(args.output)
	subprocess.call(cmd, shell=True)


	# Step 4: Add audio to video


if __name__ == '__main__':
	main()
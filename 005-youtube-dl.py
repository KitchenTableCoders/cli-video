#!/usr/bin/env python
"""
Demonstrates using the subprocess command, "call" to invoke youtube-dl (http://rg3.github.io/youtube-dl/)
to download videos

youtube-dl --list-extractors

eg: 	./005-youtube-dl.py http://www.youtube.com/watch?v=18-xvIjH8T4 \
	http://www.youtube.com/watch?v=2Syd_BUbl5A \
	http://www.youtube.com/watch?v=cU8HrO7XuiE

"""
import sys
import subprocess


def main():

	for url in sys.argv[1:]:
		cmd = "youtube-dl -f 18 -t {0}".format(url)
		subprocess.call(cmd, shell=True)

if __name__ == '__main__':
	main()
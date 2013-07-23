#!/usr/bin/env python
"""
Demonstrates string formatting and very basic use of the subprocess module
http://docs.python.org/2/library/subprocess.html#using-the-subprocess-module

Note: AFAIK, the "say" command (used below) is only on Mac

eg: ./004-subprocess.py Jeff mauve
"""
import sys
import subprocess


def main():

	name = sys.argv[1]
	color = sys.argv[2]

	cmd = 'say "{0}\'s favorite color is {1}"'.format(name, color)
	subprocess.call(cmd, shell=True)

if __name__ == '__main__':
	main()
#!/usr/bin/env python
"""
Demonstrates main sentinel
http://stackoverflow.com/questions/4041238/python-why-use-def-main

eg: ./003-main-sentinel.py Jeff mauve
"""
import sys


def main():
	print sys.argv[1] + "'s favorite color is " + sys.argv[2];

if __name__ == '__main__':
	main()
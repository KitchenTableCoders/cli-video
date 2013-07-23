#!/usr/bin/env python
"""
Introduces the "argparse" module, which is used to parse more complex argument strings

eg: ./006-argparse.py --name Jeff mauve
"""
import argparse 	# http://docs.python.org/2/library/argparse.html#module-argparse
import subprocess


def main():

	parser = argparse.ArgumentParser(description='Say a sentence')
	parser.add_argument('--name', type=str, help='a name')
	parser.add_argument('color', type=str, nargs='+', help='a color')	# nargs='+' means "at least one"
	args = parser.parse_args()

	cmd = 'say {0} likes {1}'.format(args.name, args.color[0])
	subprocess.call(cmd, shell=True)


if __name__ == '__main__':
	main()
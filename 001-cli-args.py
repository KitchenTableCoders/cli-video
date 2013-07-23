import sys
"""
Demonstrates how to access command-line arguments.

Note:  ignore sys.argv[0] -- it's just the name of the script

eg: python 001-cli-args.py Jeff Mauve
"""

# ignore sys.argv[0] -- it's just the name of the script
print sys.argv[1] + "'s favorite color is " + sys.argv[2];


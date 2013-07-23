#!/usr/bin/env python
"""
Demonstrates the used of the hashbang line (above: #!/usr/bin/env python), which makes 
it possible to run the file as a script invoking the interpreter implicitly

python 002-hashbang.py Jeff Mauve
"""

import sys

print sys.argv[1] + "'s favorite color is " + sys.argv[2];


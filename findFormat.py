import csv
import json
import sys

import magic

# pip install python-magic
# https://github.com/ahupp/python-magic
print(magic.from_file(sys.argv[1]))




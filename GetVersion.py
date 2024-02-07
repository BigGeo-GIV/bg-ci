import distutils
import json
import sys

dev = distutils.util.strtobool(sys.argv[3])
if dev:
    name = sys.argv[2] + "-dev"
else:
    name = sys.argv[2]

print(json.load(open(sys.argv[1]))[name])

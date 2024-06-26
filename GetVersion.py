import json
import sys

def strtobool(value: str) -> bool:
    return value.lower() in ("y", "yes", "on", "1", "true", "t")

dev = strtobool(sys.argv[3])
if dev:
    name = sys.argv[2] + "-dev"
else:
    name = sys.argv[2]

print(json.load(open(sys.argv[1]))[name])

import json
import sys

def strtobool(value: str) -> bool:
    return value.lower() in ("y", "yes", "on", "1", "true", "t")

dev = strtobool(sys.argv[2])
if dev:
    name = "dev"
else:
    name = "rel"

print(json.load(open(sys.argv[1]))[name])

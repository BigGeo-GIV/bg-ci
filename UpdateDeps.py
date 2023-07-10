import subprocess
import json
import sys

from semantic_version import Version
from semantic_version import NpmSpec

if __name__ == "__main__":
    newDeps = {}

    f = open("dependencies.json")
    deps = json.load(f)

    for n, v in deps.items():
        curRange = v["range"]
        curVer = v["current"]
        result = subprocess.run(["conan", "search", n, f"-r={sys.argv[1]}", "--raw"], capture_output=True, text=True)

        packages = result.stdout.strip().split("\n")
        for package in packages:
            version = package.split("/")[1]
            try:
                if Version(version) > Version(curVer) and Version(version) in NpmSpec(curRange):
                    newDeps[n] = version
            except:
                pass

    if len(newDeps) == 0:
        exit(1)

    for n, v in newDeps.items():
        cur = deps[n]["current"]
        deps[n]["current"] = v
        print(f"{n}: {cur} -> {v}")

    json_object = json.dumps(deps, indent=4) + "\n"
    open("dependencies.json", "w").write(json_object)

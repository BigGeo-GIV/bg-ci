import subprocess
import json

from semantic_version import Version
from semantic_version import NpmSpec

if __name__ == "__main__":
    newDeps = {}

    f = open("dependencies.json")
    deps = json.load(f)

    for n, v in deps.items():
        curRange = v["range"]
        curVer = v["current"]
        result = subprocess.run(["conan", "search", n, "-r=conancenter", "--raw"], capture_output=True, text=True)

        packages = result.stdout.strip().split("\n")

        for package in packages:
            version = package.split("/")[1]
            if Version(version) > Version(curVer) and Version(version) in NpmSpec(curRange):
                newDeps[n] = version

    if len(newDeps) == 0:
        exit(0)

    for n, v in newDeps.items():
        cur = deps[n]["current"]
        deps[n]["current"] = v
        print(f"{n}: {cur} -> {v}")

    json_object = json.dumps(deps, indent=4)
    open("dependencies.json", "w").write(json_object)

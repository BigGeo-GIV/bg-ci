import distutils
import sys
import json

def commitJsonToIdx(commitJson, allowMajor):
    minFound = 10
    for commit in commitJson["commits"]:
        msg = commit["messageHeadline"]

        cType = msg.split(":")[0].lower()
        if cType[-1] == "!": # not really working right now: or "BREAKING CHANGE" in msg:
            if allowMajor:
                found = 0
            found = 1
        elif "feat" in cType:
            found = 1
        elif "fix" in cType:
            found = 2
        elif "infra" in cType or "deps" in cType:
            found = 10
        else:
            found = 1 # bump minor if commit didn't match a pattern just to be safe
        minFound = min(minFound, found)
    return minFound

def bumpSemVerList(semVer, idx):
    semVer[idx] += 1
    i = idx + 1
    while i < len(semVer):
        semVer[i] = 0
        i += 1

def bumpSemVerStr(semVerStr, idx):
    semVer = list(map(int, semVerStr.split(".")))
    bumpSemVerList(semVer, idx)
    return ".".join(list(map(str, semVer)))

if __name__ == "__main__":
    path = sys.argv[1]
    commitJsonPath = sys.argv[2]
    baseName = sys.argv[3]
    dev = distutils.util.strtobool(sys.argv[4])
    idx = commitJsonToIdx(json.load(open(commitJsonPath)), not dev)
    if idx == 10:
        print("no need to bump version")
        exit(-1)

    if dev:
        name = baseName + "-dev"
    else:
        name = baseName

    verJson = json.load(open(path))
    oldVer = verJson[name]
    newVer = bumpSemVerStr(oldVer, idx)
    verJson[name] = newVer

    out = open(path, "w")
    json.dump(verJson, out)
    out.write("\n")

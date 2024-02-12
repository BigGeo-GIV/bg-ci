import distutils
import sys
import json

def commitJsonToIdx(commitJson, allowMajor):
    minFound = 10
    for commit in commitJson["commits"]:
        found = commitTxtToIdx(commit["messageHeadline"])
        minFound = min(minFound, found)
    return minFound

def commitTxtToIdx(commitText, allowMajor):
    msg = commitText

    cType = msg.split(":")[0].lower()
    if cType[-1] == "!": # not really working right now: or "BREAKING CHANGE" in msg:
        if allowMajor:
            return  0
        return 1
    elif "feat" in cType:
        return 1
    elif "fix" in cType:
        return 2
    elif "infra" in cType or "deps" in cType:
        return 10
    else:
        return 1 # bump minor if commit didn't match a pattern just to be safe

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
    commitFilePath = sys.argv[2]
    baseName = sys.argv[3]
    dev = distutils.util.strtobool(sys.argv[4])

    ext = commitFilePath.split(".")[1].strip()

    if ext == "json":
        idx = commitJsonToIdx(json.load(open(commitFilePath)), not dev)
    elif ext == "txt":
        idx = commitTxtToIdx(''.join(open(commitFilePath).readlines()), not dev)
    else:
        print("unrecognized commit file extension")
        exit(1)

    if idx == 10:
        print("no need to bump version")
        exit(2)

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

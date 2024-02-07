import distutils
import sys
import json

def msgToIdx(msg, allowMajor):
    cType = msg.split(":")[0].lower()
    if cType[-1] == "!" or "BREAKING CHANGE" in msg:
        if allowMajor:
            return 0
        return 1
    elif "feat" in cType:
        return 1
    elif "fix" in cType:
        return 2
    elif "infra" in cType or "deps" in cType:
        return -1
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
    msg = sys.argv[2]
    baseName = sys.argv[3]
    dev = distutils.util.strtobool(sys.argv[4])
    idx = msgToIdx(msg, not dev)
    if idx < 0:
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

    json.dump(verJson, open(path, "w"))

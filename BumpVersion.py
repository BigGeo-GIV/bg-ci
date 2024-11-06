import sys
import json
import os

def strtobool(value: str) -> bool:
    return value.lower() in ("y", "yes", "on", "1", "true", "t")

def commitTxtToIdxKey(commitText, allowMajor, alwaysBump):
    msg = commitText
    cType = msg.split(":")[0].lower()

    idx = None

    if cType[-1] == "!":
        idx = 0 if allowMajor else 1
    elif "feat" in cType:
        idx = 1
    elif "fix" in cType:
        idx = 2
    elif "infra" in cType:
        idx = None
    elif "docs" in cType:
        idx = None;
    else:
        idx = 1 if alwaysBump else None # bump minor if commit didn't match a pattern just to be safe

    scope = "default"
    if "(" in cType and ")" in cType and "#" not in cType:
        scope = cType.split("(")[1][0:-1].lower()

    return (scope, idx)

def commitJsonToBumps(commitJson, allowMajor):
    bumps = {}

    for commit in commitJson["commits"]:
        (scope, idx) = commitTxtToIdxKey(commit["messageHeadline"], allowMajor, False)
        if idx is not None:
            if scope in bumps:
                bumps[scope] = min(bumps[scope], idx)
            else:
                bumps[scope] = idx

    return bumps

def bumpSemVerStr(semVerStr, idx):
    def bumpSemVerList(semVer, idx):
        semVer[idx] += 1
        i = idx + 1
        while i < len(semVer):
            semVer[i] = 0
            i += 1

    def intStrip(inNum):
        return int(inNum.split("-")[0])

    semVer = list(map(intStrip, semVerStr.split(".")))
    bumpSemVerList(semVer, idx)
    return ".".join(list(map(str, semVer)))

def performBumps(bumps, verJson, dev):
    baseName = "dev" if dev else "rel"

    first = True
    for (scope, idx) in bumps.items():
        if scope != "default":
            name = scope + "-" + baseName
        else:
            name = baseName
        oldVer = verJson[name]
        newVer = bumpSemVerStr(oldVer, idx)
        verJson[name] = newVer

        if dev:
            msg = name + "-" + str(newVer)
        else:
            msg = name + str(newVer)
        if (not first):
            print("; ", end="")

        print(msg, end="")
        first = False
    print("")

def main(jsonPath, commitFilePath, dev):
    ext = os.path.splitext(commitFilePath)[1]

    bumps = {}
    if ext == ".json":
        bumps = commitJsonToBumps(json.load(open(commitFilePath)), not dev)
    elif ext == ".txt":
        (scope, idx) = commitTxtToIdxKey(''.join(open(commitFilePath).readlines()), not dev, True)
        if idx is not None:
            bumps[scope] = idx
    else:
        print("unrecognized commit file extension")
        exit(1)

    verJson = json.load(open(jsonPath))
    performBumps(bumps, verJson, dev)
    out = open(jsonPath, "w")
    json.dump(verJson, out, indent=4)
    out.write("\n")

if __name__ == "__main__":
    jsonPath = sys.argv[1]
    commitFilePath = sys.argv[2]
    dev = strtobool(sys.argv[3])
    main(jsonPath, commitFilePath, dev)

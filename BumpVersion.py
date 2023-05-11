import sys

def msgToIdx(msg):
    cType = msg.split(":")[0].lower()
    if cType[-1] == "!" or "BREAKING CHANGE" in msg:
        return 1 # should be 0, but not doing major versions yet
    elif "feat" in cType:
        return 1
    elif "fix" in cType:
        return 2
    elif "infra" in cType or "deps" in cType:
        return -1
    else:
        return 2 # for now always bump if commit didn't match a pattern just to be safe

def bumpSemVer(semVer, idx):
    semVer[idx] += 1
    i = idx + 1
    while i < len(semVer):
        semVer[i] = 0
        i += 1

    return semVer

def bumpVer(fpath, idx):
    with open(fpath) as f:
        lines = f.readlines()

    semVer = list(map(int, lines[0].split(".")))
    semVer = bumpSemVer(semVer, idx)
    lines[0] = ".".join(list(map(str, semVer)))
    with open(fpath, "w") as f:
        f.writelines(lines[0] + "\n")

if __name__ == "__main__":
    msg = sys.argv[1]
    idx = msgToIdx(msg)
    if idx >= 0:
        bumpVer("version.txt", idx)
    else:
        print("no need to bump version")
        exit(1)

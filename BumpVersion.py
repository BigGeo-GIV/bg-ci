import sys

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
        f.writelines(lines)

if __name__ == "__main__":
    bumpVer("version.txt", int(sys.argv[1]))

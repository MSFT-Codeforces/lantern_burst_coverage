
import sys
import re

INT_LINE_RE = re.compile(r"-?\d+(?: -?\d+)*\Z")

def invalid():
    sys.stdout.write("False")
    sys.exit(0)

def check_sorted_non_decreasing(arr):
    for i in range(1, len(arr)):
        if arr[i] < arr[i - 1]:
            return False
    return True

def main():
    data = sys.stdin.read()
    if data == "":
        invalid()

    lines = data.splitlines()

    # Strict line-based format: no empty lines allowed anywhere.
    for line in lines:
        if line == "":
            invalid()
        # Strict spacing: only single spaces between integers; no leading/trailing spaces/tabs.
        if not INT_LINE_RE.fullmatch(line):
            invalid()

    # Each test case must be exactly 3 lines: header, a-array, b-array.
    if len(lines) % 3 != 0:
        invalid()

    tests = 0
    idx = 0
    while idx < len(lines):
        line1, line2, line3 = lines[idx], lines[idx + 1], lines[idx + 2]

        p1 = line1.split(" ")
        if len(p1) != 4:
            invalid()
        try:
            n, m, k, t = map(int, p1)
        except Exception:
            invalid()

        if not (1 <= n <= 100000):
            invalid()
        if not (1 <= m <= 100000):
            invalid()
        if not (1 <= k <= m):
            invalid()
        if not (1 <= t <= 30):
            invalid()

        p2 = line2.split(" ")
        if len(p2) != n:
            invalid()
        try:
            a = list(map(int, p2))
        except Exception:
            invalid()
        for x in a:
            if x < -10**9 or x > 10**9:
                invalid()
        if not check_sorted_non_decreasing(a):
            invalid()

        p3 = line3.split(" ")
        if len(p3) != m:
            invalid()
        try:
            b = list(map(int, p3))
        except Exception:
            invalid()
        for x in b:
            if x < -10**9 or x > 10**9:
                invalid()
        if not check_sorted_non_decreasing(b):
            invalid()

        tests += 1
        idx += 3

    if tests <= 0:
        invalid()
    sys.stdout.write("True")

if __name__ == "__main__":
    main()

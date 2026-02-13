
def fmt_case(n, m, k, t, a, b):
    return "\n".join([
        f"{n} {m} {k} {t}",
        " ".join(map(str, a)),
        " ".join(map(str, b)),
    ])

cases = []

# 1) Minimum sizes, answer can be s=0 (exact match)
cases.append(fmt_case(
    n=1, m=1, k=1, t=1,
    a=[0],
    b=[0]
))

# 2) Minimum sizes with extreme coordinates (huge radius), overflow-prone if using int
cases.append(fmt_case(
    n=1, m=1, k=1, t=1,
    a=[-10**9],
    b=[10**9]
))

# 3) Many duplicate outposts (all equal)
cases.append(fmt_case(
    n=5, m=3, k=1, t=1,
    a=[0, 0, 0, 0, 0],
    b=[-5, 0, 5]
))

# 4) Duplicate lanterns between distinct coordinates (breaks wrong coordinate-compression by index)
cases.append(fmt_case(
    n=2, m=5, k=2, t=1,
    a=[0, 100],
    b=[0, 0, 0, 0, 100]
))

# 5) Inclusive boundary check: outposts exactly at b ± s for minimal s
cases.append(fmt_case(
    n=2, m=1, k=1, t=1,
    a=[-5, 5],
    b=[0]
))

# 6) All outposts strictly left of all lanterns (one-sided coverage)
cases.append(fmt_case(
    n=3, m=2, k=1, t=1,
    a=[-10, -9, -8],
    b=[0, 100]
))

# 7) All outposts strictly right of all lanterns (one-sided coverage)
cases.append(fmt_case(
    n=3, m=2, k=1, t=1,
    a=[8, 9, 10],
    b=[-100, 0]
))

# 8) Tradeoff: k=1 forces using a single lantern; small s needs multiple lanterns
cases.append(fmt_case(
    n=3, m=3, k=1, t=1,
    a=[0, 100, 200],
    b=[0, 100, 200]
))

# 9) t=1 forces a single contiguous block; with k small you effectively must use one/two adjacent lanterns
cases.append(fmt_case(
    n=2, m=6, k=2, t=1,
    a=[0, 102],
    b=[0, 1, 2, 100, 101, 102]
))

# 10) Overflow test: b + s can exceed 2^31-1 (~3e9), must use 64-bit in computations
cases.append(fmt_case(
    n=2, m=2, k=1, t=1,
    a=[-10**9, 10**9],
    b=[999_999_999, 1_000_000_000]
))

# 11) Duplicates in outposts + tight boundary (one off-by-one point)
cases.append(fmt_case(
    n=6, m=2, k=1, t=1,
    a=[0, 0, 0, 0, 0, 1],
    b=[0, 2]
))

# 12) Max sizes stress: n=m=100000, large input (also tests O(n+m) feasibility)
n = m = 100000
a12 = range(0, n)          # 0..99999
b12 = range(1, m + 1)      # 1..100000
cases.append(fmt_case(
    n=n, m=m, k=m, t=30,
    a=a12,
    b=b12
))

# 13) Skewed sizes: very large n but tiny m
n13 = 100000
a13 = range(-50000, 50000)  # 100000 points
b13 = [-100000, -50000, 0, 50000, 100000]
cases.append(fmt_case(
    n=n13, m=5, k=5, t=2,
    a=a13,
    b=b13
))

# 14) k=1 with many lanterns, t large (t irrelevant); choose best single lantern among many
cases.append(fmt_case(
    n=7, m=10, k=1, t=30,
    a=[-90, -40, -10, 0, 10, 40, 90],
    b=[-100, -80, -60, -40, -20, 0, 20, 40, 60, 80]
))

# 15) Burst indexing edges: optimal uses burst starting at 1 and another ending at m
cases.append(fmt_case(
    n=3, m=5, k=4, t=2,
    a=[-10, -8, 51],
    b=[-10, -9, -8, 50, 51]
))

print("Test Cases:")
for i, tc in enumerate(cases, 1):
    print(f"Input {i}:\n{tc}\n")

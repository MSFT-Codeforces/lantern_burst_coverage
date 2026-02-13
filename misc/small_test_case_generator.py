
def tc(n, m, k, t, a, b):
    assert len(a) == n and len(b) == m
    assert 1 <= n <= 100000 and 1 <= m <= 100000
    assert 1 <= k <= m
    assert 1 <= t <= 30
    assert all(a[i] <= a[i + 1] for i in range(n - 1))
    assert all(b[i] <= b[i + 1] for i in range(m - 1))
    return "\n".join([
        f"{n} {m} {k} {t}",
        " ".join(map(str, a)),
        " ".join(map(str, b)),
    ])

cases = []

# 1) Minimum sizes, s=0 possible
cases.append(tc(
    n=1, m=1, k=1, t=1,
    a=[0],
    b=[0]
))

# 2) Minimum sizes, far apart (forces positive radius)
cases.append(tc(
    n=1, m=1, k=1, t=1,
    a=[5],
    b=[-5]
))

# 3) All outposts equal (many duplicates in a)
cases.append(tc(
    n=5, m=3, k=1, t=1,
    a=[2, 2, 2, 2, 2],
    b=[0, 2, 4]
))

# 4) Many duplicate lantern coordinates (compression-by-coordinate bug risk)
cases.append(tc(
    n=2, m=4, k=1, t=1,
    a=[1, 3],
    b=[1, 1, 1, 3]
))

# 5) Outposts entirely to the left of all lanterns
cases.append(tc(
    n=2, m=2, k=1, t=1,
    a=[-10, -9],
    b=[0, 5]
))

# 6) Tight boundary inclusion (outposts exactly at x ± s)
cases.append(tc(
    n=2, m=1, k=1, t=1,
    a=[-3, 3],
    b=[0]
))

# 7) Requires multiple bursts (k small, t enough); two single-lantern bursts
cases.append(tc(
    n=2, m=6, k=2, t=3,
    a=[-5, 5],
    b=[-5, 0, 0, 0, 5, 10]
))

# 8) t=1 and k=1: only one lantern can be activated
cases.append(tc(
    n=2, m=5, k=1, t=1,
    a=[-10, 10],
    b=[-10, -5, 0, 5, 10]
))

# 9) k=m and t=1: can activate all lanterns in one burst
cases.append(tc(
    n=5, m=6, k=6, t=1,
    a=[-6, -1, 0, 1, 6],
    b=[-5, -2, 0, 2, 5, 7]
))

# 10) t very large but k small: effort is the binding constraint
cases.append(tc(
    n=3, m=7, k=3, t=30,
    a=[-6, 0, 6],
    b=[-6, -3, 0, 3, 6, 9, 12]
))

# 11) Extreme coordinates to trigger overflow in b+s/a±s if using 32-bit int
cases.append(tc(
    n=2, m=1, k=1, t=1,
    a=[-10**9, 10**9],
    b=[0]
))

# 12) Dense outposts, sparse lanterns
cases.append(tc(
    n=8, m=2, k=2, t=2,
    a=[0, 1, 2, 3, 4, 5, 6, 7],
    b=[0, 7]
))

# 13) Sparse outposts, dense lanterns; one burst of length 3 suffices with s=0
cases.append(tc(
    n=2, m=8, k=3, t=1,
    a=[-1, 1],
    b=[-4, -3, -2, -1, 0, 1, 2, 3]
))

# 14) Duplicate outposts
cases.append(tc(
    n=4, m=2, k=1, t=1,
    a=[0, 0, 1, 1],
    b=[0, 2]
))

# 15) Alternating coverage; needs two separate bursts if s is small
cases.append(tc(
    n=4, m=3, k=2, t=2,
    a=[-3, -1, 1, 3],
    b=[-2, 0, 2]
))

print("Test Cases:")
for i, s in enumerate(cases, 1):
    print(f"Input {i}:")
    print(s)
    if i != len(cases):
        print()

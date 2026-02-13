
import sys

def print_list(arr):
    sys.stdout.write(" ".join(map(str, arr)) + "\n")

def emit_case(idx, n, m, k, t, a, b):
    sys.stdout.write(f"Input {idx}:\n")
    sys.stdout.write(f"{n} {m} {k} {t}\n")
    print_list(a)
    print_list(b)
    sys.stdout.write("\n")

def main():
    sys.stdout.write("Test Cases:\n")

    N = 100000
    M = 100000

    # 1) Coordinate extremes + overflow risk (b+s can exceed 2^31-1), k=1,t=1
    #    Lanterns all near -1e9, outposts all near +1e9 -> radius near 2e9
    n = N; m = M; k = 1; t = 1
    b = [-1_000_000_000 + i for i in range(m)]  # [-1e9 .. -999900001]
    a = [1_000_000_000 - (n - 1) + i for i in range(n)]  # [999900001 .. 1e9]
    emit_case(1, n, m, k, t, a, b)

    # 2) Heavy duplicates (a all equal, b has huge duplicate blocks), k=1
    n = N; m = M; k = 1; t = 30
    a = [0] * n
    b = [0] * (m // 2) + [1] * (m - m // 2)
    emit_case(2, n, m, k, t, a, b)

    # 3) All lanterns equal coordinate, outposts spread across full range (forces large s), duplicates in b
    n = N; m = M; k = 50000; t = 30
    b = [0] * m
    a = [-1_000_000_000 + (i * 2_000_000_000) // (n - 1) for i in range(n)]  # includes both extremes
    emit_case(3, n, m, k, t, a, b)

    # 4) t-limited, contiguity/effort interaction:
    #    Outposts in three far-apart clusters (-1e9, 0, +1e9).
    #    Lantern indices also form three big separated index blocks; to cover with small s you'd need 3 bursts,
    #    but t=2 disallows, and merging blocks exceeds small k -> forces large radius.
    n = N; m = M; k = 3; t = 2
    L, C, R = 40000, 20000, 40000  # sums to 100000
    b_left = [-1_000_000_000 + i for i in range(L)]                  # very negative
    b_center = [0 + i for i in range(C)]                              # near 0
    b_right = [1_000_000_000 - (R - 1) + i for i in range(R)]         # near +1e9 (within bounds)
    b = b_left + b_center + b_right

    # outposts: 3 clusters
    a = ([-1_000_000_000] * 33334) + ([0] * 33333) + ([1_000_000_000] * 33333)
    emit_case(4, n, m, k, t, a, b)

    # 5) Balanced minimax with k=1,t=1 (effectively choose one lantern index)
    n = N; m = M; k = 1; t = 1
    a = [-500_000_000 + (i * 1_000_000_000) // (n - 1) for i in range(n)]
    b = [-600_000_000 + (i * 1_200_000_000) // (m - 1) for i in range(m)]
    emit_case(5, n, m, k, t, a, b)

    # 6) All lanterns can be turned on (k=m,t=1): purely geometric nearest distance
    #    Make b evenly spaced, a placed at midpoints to maximize nearest distance.
    n = N; m = M; k = m; t = 1
    start = -1_000_000_000
    step = 20000  # m*step ~ 2e9 fits range
    b = [start + i * step for i in range(m)]  # ends at 999,980,000
    a = [start + i * step + (step // 2) for i in range(n)]  # offset by 10000
    emit_case(6, n, m, k, t, a, b)

    # 7) Needs close to t bursts: 30 clusters far apart, k=t=30 allows only 30 single-index activations
    n = N; m = M; k = 30; t = 30
    clusters = 30
    base = m // clusters
    rem = m % clusters
    sizes = [base + (1 if i < rem else 0) for i in range(clusters)]  # sums to 100000
    centers = [-725_000_000 + i * 50_000_000 for i in range(clusters)]  # within [-1e9,1e9]

    b = []
    for c in range(clusters):
        sz = sizes[c]
        center = centers[c]
        b.extend([center + j for j in range(sz)])

    base_n = n // clusters
    rem_n = n % clusters
    sizes_n = [base_n + (1 if i < rem_n else 0) for i in range(clusters)]
    a = []
    for c in range(clusters):
        a.extend([centers[c]] * sizes_n[c])
    emit_case(7, n, m, k, t, a, b)

    # 8) Boundary inclusion: many outposts exactly at distance 8 from nearest lantern
    #    uses k=m,t=1 so feasibility is purely geometric; catches < vs <= errors.
    n = N; m = M; k = m; t = 1
    start = -999_990_000
    step = 20
    b = [start + i * step for i in range(m)]  # within [-1e9, 1e9]
    half = n // 2
    a = [b[i] - 8 for i in range(half)] + [b[i] + 8 for i in range(half, n)]
    emit_case(8, n, m, k, t, a, b)

    # 9) Dense lanterns, highly duplicated outposts (10 unique coords repeated), moderate k,t
    n = N; m = M; k = 100; t = 30
    b = [-50000 + i for i in range(m)]  # dense, sorted
    uniques = [-40000, -30000, -20000, -10000, -1, 0, 1, 10000, 20000, 30000]
    reps = n // len(uniques)
    a = []
    for x in uniques:
        a.extend([x] * reps)
    a.extend([uniques[-1]] * (n - len(a)))
    emit_case(9, n, m, k, t, a, b)

    # 10) Contiguity/effort stress: interleaved grids (a odd, b even), k too small to activate all
    #     forces distributed activation under limited number of bursts.
    n = N; m = M; k = 50000; t = 30
    b = [-1_000_000 + 2 * i for i in range(m)]          # even coordinates
    a = [-1_000_000 + 2 * i + 1 for i in range(n)]      # odd coordinates
    emit_case(10, n, m, k, t, a, b)

if __name__ == "__main__":
    main()

#include <algorithm>
#include <cstdlib>
#include <iostream>
#include <limits>
#include <vector>

using namespace std;

static inline long long absll(long long x) {
    return x < 0 ? -x : x;
}

class BruteSolver {
public:
    int n, m, k, t;
    vector<long long> a;
    vector<long long> b;

    bool coversAllOutposts(const vector<int>& activeIndices, long long s) {
        // If there are no outposts, trivially covered (not expected by constraints, but safe).
        if (n == 0) {
            return true;
        }

        // No active lanterns cannot cover any outpost.
        if (activeIndices.empty()) {
            return false;
        }

        // Naively check each outpost against every active lantern.
        for (int i = 0; i < n; i++) {
            bool covered = false;
            for (int idx : activeIndices) {
                if (absll(a[i] - b[idx]) <= s) {
                    covered = true;
                    break;
                }
            }
            if (!covered) {
                return false;
            }
        }
        return true;
    }

    bool dfsEnumeratePlans(int startIndex,
                           int burstsUsed,
                           int effortUsed,
                           int maxBursts,
                           vector<int>& activeIndices,
                           long long s) {
        // Using fewer than maxBursts bursts is allowed, so check coverage at every state.
        if (coversAllOutposts(activeIndices, s)) {
            return true;
        }

        if (burstsUsed == maxBursts) {
            return false;
        }
        if (effortUsed == k) {
            return false;
        }
        if (startIndex >= m) {
            return false;
        }

        /*
            Enumerate the next (non-empty) burst interval [l..r] with l >= startIndex.
            This enumerates plans as a set of disjoint intervals in increasing order.
            This is sufficient for correctness because any feasible plan can be transformed
            into disjoint intervals covering the same activated indices with no more effort
            and no more bursts.
        */
        for (int l = startIndex; l < m; l++) {
            for (int r = l; r < m; r++) {
                int len = r - l + 1;
                if (effortUsed + len > k) {
                    break; // Increasing r only increases len.
                }

                int oldSize = (int)activeIndices.size();
                for (int idx = l; idx <= r; idx++) {
                    activeIndices.push_back(idx);
                }

                if (dfsEnumeratePlans(r + 1, burstsUsed + 1, effortUsed + len, maxBursts, activeIndices, s)) {
                    return true;
                }

                activeIndices.resize(oldSize);
            }
        }

        return false;
    }

    bool canCoverAllWithRadius(long long s) {
        if (n == 0) {
            return true;
        }
        if (m == 0) {
            return false;
        }
        if (k <= 0 || t <= 0) {
            return false;
        }

        // Maximum number of non-empty bursts can't exceed k (each burst costs at least 1 effort).
        int maxBursts = min(t, k);

        vector<int> activeIndices;
        return dfsEnumeratePlans(0, 0, 0, maxBursts, activeIndices, s);
    }

    long long solve() {
        // With coordinates in [-1e9, 1e9], radius 2e9 is enough for a single lantern
        // to cover all outposts (distance between any two points is <= 2e9).
        long long lo = -1;                  // infeasible
        long long hi = 2000000000LL;        // feasible under constraints (k>=1,t>=1,m>=1,n>=1)

        while (hi - lo > 1) {
            long long mid = lo + (hi - lo) / 2;
            if (canCoverAllWithRadius(mid)) {
                hi = mid;
            } else {
                lo = mid;
            }
        }

        return hi;
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    BruteSolver solver;
    cin >> solver.n >> solver.m >> solver.k >> solver.t;

    solver.a.resize(solver.n);
    solver.b.resize(solver.m);

    for (int i = 0; i < solver.n; i++) {
        cin >> solver.a[i];
    }
    for (int j = 0; j < solver.m; j++) {
        cin >> solver.b[j];
    }

    cout << solver.solve() << "\n";
    return 0;
}
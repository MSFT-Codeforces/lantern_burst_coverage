#include <algorithm>
#include <deque>
#include <iostream>
#include <vector>

namespace {
const long long kInfinity = (1LL << 60);

/**
 * @brief Computes coverage index intervals [leftIndex, rightIndex] for each outpost.
 *
 * For a given radius, an outpost can be illuminated by lanterns whose coordinates lie within
 * [outpost - radius, outpost + radius]. Because lanternCoordinates is sorted, this set is a
 * contiguous interval in lantern index space.
 *
 * Indices are produced in 1-based lantern index space, and outposts are treated as 1-based
 * in leftIndex/rightIndex to match the DP.
 *
 * @param radius The candidate illumination radius.
 * @param outpostCoordinates Sorted outpost coordinates.
 * @param lanternCoordinates Sorted lantern coordinates.
 * @param leftIndex Output vector (size outpostCount + 1), 1-based outpost indexing.
 * @param rightIndex Output vector (size outpostCount + 1), 1-based outpost indexing.
 * @return True if every outpost has a non-empty interval, false otherwise.
 */
bool computeCoverageIntervals(long long radius,
                              const std::vector<long long>& outpostCoordinates,
                              const std::vector<long long>& lanternCoordinates,
                              std::vector<int>& leftIndex,
                              std::vector<int>& rightIndex) {
    const int outpostCount = static_cast<int>(outpostCoordinates.size());
    const int lanternCount = static_cast<int>(lanternCoordinates.size());

    int leftLanternPointer = 0;   // First lantern with coordinate >= outpost - radius.
    int rightLanternPointer = 0;  // First lantern with coordinate > outpost + radius.

    for (int outpostIndex = 1; outpostIndex <= outpostCount; outpostIndex++) {
        const long long outpostCoordinate = outpostCoordinates[outpostIndex - 1];
        const long long leftCoordinate = outpostCoordinate - radius;
        const long long rightCoordinate = outpostCoordinate + radius;

        while (leftLanternPointer < lanternCount &&
               lanternCoordinates[leftLanternPointer] < leftCoordinate) {
            leftLanternPointer++;
        }

        if (rightLanternPointer < leftLanternPointer) {
            rightLanternPointer = leftLanternPointer;
        }
        while (rightLanternPointer < lanternCount &&
               lanternCoordinates[rightLanternPointer] <= rightCoordinate) {
            rightLanternPointer++;
        }

        leftIndex[outpostIndex] = leftLanternPointer + 1;  // Convert to 1-based lantern index.
        rightIndex[outpostIndex] = rightLanternPointer;    // Count of lanterns <= rightCoordinate.

        if (leftIndex[outpostIndex] > rightIndex[outpostIndex]) {
            return false;
        }
    }
    return true;
}

/**
 * @brief Checks if a given radius can illuminate all outposts within burst and effort limits.
 *
 * Steps:
 * 1) Compute leftIndex/outpostIndex and rightIndex/outpostIndex for the candidate radius.
 * 2) Run DP over up to maxBurstCount bursts to minimize total effort.
 * 3) Return whether the minimal effort to cover all outposts is <= maxEffort.
 *
 * @param radius Candidate radius to test.
 * @param outpostCoordinates Sorted outpost coordinates.
 * @param lanternCoordinates Sorted lantern coordinates.
 * @param maxEffort Maximum allowed total effort (sum of burst lengths).
 * @param maxBurstCount Maximum allowed number of bursts.
 * @return True if feasible, false otherwise.
 */
bool isFeasibleRadius(long long radius,
                      const std::vector<long long>& outpostCoordinates,
                      const std::vector<long long>& lanternCoordinates,
                      int maxEffort,
                      int maxBurstCount) {
    const int outpostCount = static_cast<int>(outpostCoordinates.size());

    std::vector<int> leftIndex(outpostCount + 1, 0);
    std::vector<int> rightIndex(outpostCount + 1, 0);

    if (!computeCoverageIntervals(radius, outpostCoordinates, lanternCoordinates, leftIndex, rightIndex)) {
        return false;
    }

    std::vector<long long> bestEffortAtMostBursts(outpostCount + 1, kInfinity);
    bestEffortAtMostBursts[0] = 0;

    for (int burstNumber = 1; burstNumber <= maxBurstCount; burstNumber++) {
        const std::vector<long long> previousBestEffort = bestEffortAtMostBursts;
        std::vector<long long> bestEffortWithExactlyThisBurstCount(outpostCount + 1, kInfinity);
        bestEffortWithExactlyThisBurstCount[0] = 0;

        int boundaryPointer = 0;
        int processedBadStarts = 0;
        long long bestBadValue = kInfinity;

        std::deque<int> goodDeque;

        for (int endOutpost = 1; endOutpost <= outpostCount; endOutpost++) {
            const int previousCoveredOutposts = endOutpost - 1;
            if (previousBestEffort[previousCoveredOutposts] < kInfinity) {
                while (!goodDeque.empty() &&
                       previousBestEffort[goodDeque.back()] >= previousBestEffort[previousCoveredOutposts]) {
                    goodDeque.pop_back();
                }
                goodDeque.push_back(previousCoveredOutposts);
            }

            while (boundaryPointer < outpostCount &&
                   rightIndex[boundaryPointer + 1] < leftIndex[endOutpost]) {
                boundaryPointer++;
            }

            const int badStartCount = std::min(boundaryPointer, endOutpost);

            while (processedBadStarts < badStartCount) {
                processedBadStarts++;
                const int startOutpost = processedBadStarts;
                const int previousIndex = startOutpost - 1;
                if (previousBestEffort[previousIndex] < kInfinity) {
                    bestBadValue = std::min(
                        bestBadValue,
                        previousBestEffort[previousIndex] - static_cast<long long>(rightIndex[startOutpost])
                    );
                }
            }

            while (!goodDeque.empty() && goodDeque.front() < badStartCount) {
                goodDeque.pop_front();
            }

            long long bestValueForCurrent = kInfinity;

            if (!goodDeque.empty()) {
                bestValueForCurrent = std::min(bestValueForCurrent, previousBestEffort[goodDeque.front()] + 1);
            }

            if (bestBadValue < kInfinity) {
                bestValueForCurrent = std::min(
                    bestValueForCurrent,
                    bestBadValue + static_cast<long long>(leftIndex[endOutpost]) + 1
                );
            }

            bestEffortWithExactlyThisBurstCount[endOutpost] = bestValueForCurrent;
        }

        for (int coveredOutposts = 0; coveredOutposts <= outpostCount; coveredOutposts++) {
            bestEffortAtMostBursts[coveredOutposts] = std::min(
                bestEffortAtMostBursts[coveredOutposts],
                bestEffortWithExactlyThisBurstCount[coveredOutposts]
            );
        }
    }

    return bestEffortAtMostBursts[outpostCount] <= static_cast<long long>(maxEffort);
}
}  // namespace

/**
 * @brief Reads input, binary searches the minimum feasible radius, and prints it.
 *
 * @return Exit code 0 on success.
 */
int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    int outpostCount = 0;
    int lanternCount = 0;
    int maxEffort = 0;
    int maxBurstCount = 0;

    std::cin >> outpostCount >> lanternCount >> maxEffort >> maxBurstCount;

    std::vector<long long> outpostCoordinates(outpostCount);
    std::vector<long long> lanternCoordinates(lanternCount);

    for (int outpostIndex = 0; outpostIndex < outpostCount; outpostIndex++) {
        std::cin >> outpostCoordinates[outpostIndex];
    }
    for (int lanternIndex = 0; lanternIndex < lanternCount; lanternIndex++) {
        std::cin >> lanternCoordinates[lanternIndex];
    }

    long long lowRadius = -1;
    long long highRadius = 2000000000LL;

    while (highRadius - lowRadius > 1) {
        const long long midRadius = lowRadius + (highRadius - lowRadius) / 2;
        if (isFeasibleRadius(midRadius, outpostCoordinates, lanternCoordinates, maxEffort, maxBurstCount)) {
            highRadius = midRadius;
        } else {
            lowRadius = midRadius;
        }
    }

    std::cout << highRadius << "\n";
    return 0;
}
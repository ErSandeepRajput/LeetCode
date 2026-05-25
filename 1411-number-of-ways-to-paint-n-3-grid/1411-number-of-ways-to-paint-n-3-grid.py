from itertools import product

def get_valid_patterns():
    """All 3-cell rows with no two adjacent cells same colour."""
    patterns = []
    for row in product(range(3), repeat=3):
        if row[0] != row[1] and row[1] != row[2]:
            patterns.append(row)
    return patterns  # exactly 12 patterns

def compatible(p1, p2):
    """Can row p2 follow row p1? No vertical adjacency conflicts."""
    return all(p1[col] != p2[col] for col in range(3))


class Solution:
    def numOfWays(self, n: int) -> int:
        MOD = 10**9 + 7

        # Step 1: enumerate valid patterns
        patterns = get_valid_patterns()  # 12 patterns
        k = len(patterns)  # k = 12

        # Step 2: build transition matrix (12×12)
        # trans[i][j] = 1 if pattern j can follow pattern i
        trans = [[0]*k for _ in range(k)]
        for i, p1 in enumerate(patterns):
            for j, p2 in enumerate(patterns):
                if compatible(p1, p2):
                    trans[i][j] = 1

        # Step 3: DP — dp[j] = ways to reach pattern j at current row
        dp = [1] * k  # row 0: all patterns valid, 1 way each

        for _ in range(n - 1):
            new_dp = [0] * k
            for j in range(k):
                for i in range(k):
                    if trans[i][j]:
                        new_dp[j] = (new_dp[j] + dp[i]) % MOD
            dp = new_dp

        return sum(dp) % MOD

# Synced seamlessly with LeetHub Pro
# Pro features: https://bit.ly/leethubpro | Free version: https://bit.ly/leethubv4
# Get it here: https://chromewebstore.google.com/detail/leethub-v4/bcilpkkbokcopmabingnndookdogmbna
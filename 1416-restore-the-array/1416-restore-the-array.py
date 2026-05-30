class Solution:
    def numberOfArrays(self, s: str, k: int) -> int:
        MOD = 10**9 + 7
        n = len(s)
        max_len = len(str(k))   # digits in k  ≤ 10

        # dp[i] = number of valid arrays using s[0..i-1]
        dp = [0] * (n + 1)
        dp[0] = 1              # empty prefix: one way

        for i in range(1, n + 1):
            for length in range(1, max_len + 1):
                j = i - length
                if j < 0:
                    break
                # no leading zeros
                if s[j] == '0':
                    continue
                num = int(s[j:i])
                if num > k:
                    continue
                dp[i] = (dp[i] + dp[j]) % MOD

        return dp[n]

# Synced seamlessly with LeetHub Pro
# Pro features: https://bit.ly/leethubpro | Free version: https://bit.ly/leethubv4
# Get it here: https://chromewebstore.google.com/detail/leethub-v4/bcilpkkbokcopmabingnndookdogmbna
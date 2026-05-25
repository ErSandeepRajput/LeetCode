from functools import lru_cache

def build_kmp_failure(evil):
    m = len(evil)
    fail = [0] * m
    j = 0
    for i in range(1, m):
        while j > 0 and evil[i] != evil[j]:
            j = fail[j-1]
        if evil[i] == evil[j]:
            j += 1
        fail[i] = j
    return fail

def kmp_next_state(state, char, evil, fail):
    """Given current KMP state and new char, return next state."""
    m = len(evil)
    while state > 0 and char != evil[state]:
        state = fail[state-1]
    if char == evil[state]:
        state += 1
    return state  # if state == m, evil is fully matched → invalid


class Solution:
    def findGoodStrings(self, n: int, s1: str, s2: str, evil: str) -> int:
        MOD = 10**9 + 7
        m = len(evil)

        # precompute KMP failure function
        fail = build_kmp_failure(evil)

        @lru_cache(maxsize=None)
        def dp(pos, kmp_state, tight_lo, tight_hi):
            """
            pos        : current position in string being built
            kmp_state  : chars of evil matched so far
            tight_lo   : still bounded below by s1
            tight_hi   : still bounded above by s2
            """
            if kmp_state == m:  # evil substring found — invalid
                return 0
            if pos == n:        # built full string — valid
                return 1

            # character range at this position
            lo = s1[pos] if tight_lo else 'a'
            hi = s2[pos] if tight_hi else 'z'

            count = 0
            for c in map(chr, range(ord(lo), ord(hi) + 1)):
                next_kmp = kmp_next_state(kmp_state, c, evil, fail)
                if next_kmp == m:   # this char completes evil — skip
                    continue
                count += dp(
                    pos + 1,
                    next_kmp,
                    tight_lo and (c == lo),
                    tight_hi and (c == hi)
                )

            return count % MOD

        result = dp(0, 0, True, True)
        dp.cache_clear()
        return result

# Synced seamlessly with LeetHub Pro
# Pro features: https://bit.ly/leethubpro | Free version: https://bit.ly/leethubv4
# Get it here: https://chromewebstore.google.com/detail/leethub-v4/bcilpkkbokcopmabingnndookdogmbna
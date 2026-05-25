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

from concurrent.futures import ThreadPoolExecutor
from itertools import product

class Solution:
    def findGoodStrings(self, n: int, s1: str, s2: str, evil: str) -> int:
        MOD = 10**9 + 7
        m = len(evil)
        fail = build_kmp_failure(evil)

        # dp_table[pos][kmp_state][tight_lo][tight_hi]
        # Build iteratively position by position
        # State: (kmp_state, tight_lo, tight_hi) → count
        from collections import defaultdict

        # current layer: maps state → count
        current = defaultdict(int)
        current[(0, True, True)] = 1  # start state

        WORKERS = 4

        def process_state(args):
            """Expand one state at current position."""
            state, count, pos = args
            kmp_state, tight_lo, tight_hi = state

            if kmp_state == m or count == 0:
                return []

            lo = s1[pos] if tight_lo else 'a'
            hi = s2[pos] if tight_hi else 'z'

            results = []
            for c in map(chr, range(ord(lo), ord(hi) + 1)):
                next_kmp = kmp_next_state(kmp_state, c, evil, fail)
                if next_kmp == m:
                    continue
                next_state = (
                    next_kmp,
                    tight_lo and (c == lo),
                    tight_hi and (c == hi)
                )
                results.append((next_state, count))
            return results

        for pos in range(n):
            # prepare tasks — all current states are independent
            tasks = [
                (state, count, pos)
                for state, count in current.items()
            ]

            # parallel expansion of all states at this position
            with ThreadPoolExecutor(max_workers=WORKERS) as ex:
                all_results = list(ex.map(process_state, tasks))

            # merge results — serial reduction (fast, just addition)
            next_layer = defaultdict(int)
            for results in all_results:
                for next_state, count in results:
                    next_layer[next_state] = (
                        next_layer[next_state] + count
                    ) % MOD

            current = next_layer

        # sum all valid final states (kmp_state != m already filtered)
        return sum(current.values()) % MOD

# Synced seamlessly with LeetHub Pro
# Pro features: https://bit.ly/leethubpro | Free version: https://bit.ly/leethubv4
# Get it here: https://chromewebstore.google.com/detail/leethub-v4/bcilpkkbokcopmabingnndookdogmbna
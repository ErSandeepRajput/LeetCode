from concurrent.futures import ThreadPoolExecutor
from threading import Lock

class Solution:
    def firstMissingPositive(self, nums: list[int]) -> int:
        n = len(nums)
        # O(n) auxiliary space — boolean presence array
        present = [False] * (n + 2)
        lock = Lock()
        WORKERS = 4

        def mark_chunk(chunk):
            local_marks = []
            for v in chunk:
                if 1 <= v <= n:
                    local_marks.append(v)
            # batch write under lock
            with lock:
                for v in local_marks:
                    present[v] = True

        def chunk(lst, w):
            size = -(-len(lst) // w)  # ceiling division
            return [lst[i:i+size] for i in range(0, len(lst), size)]

        # Phase 1: parallel marking — each thread marks its chunk
        with ThreadPoolExecutor(max_workers=WORKERS) as ex:
            list(ex.map(mark_chunk, chunk(nums, WORKERS)))

        # Phase 2: serial scan — inherently sequential, no parallelism possible
        for i in range(1, n + 2):
            if not present[i]:
                return i

# Synced seamlessly with LeetHub Pro
# Pro features: https://bit.ly/leethubpro | Free version: https://bit.ly/leethubv4
# Get it here: https://chromewebstore.google.com/detail/leethub-v4/bcilpkkbokcopmabingnndookdogmbna
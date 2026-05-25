from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock
from math import ceil

class Solution:
    def longestCommonPrefix(self, arr1: list[int], arr2: list[int]) -> int:

        def chunk(lst, n):
            size = ceil(len(lst) / n)
            return [lst[i:i+size] for i in range(0, len(lst), size)]

        seen = set()
        lock = Lock()

        def build_partial(nums):
            local = set()
            for num in nums:
                while num > 0:
                    local.add(num)
                    num //= 10
            with lock:
                seen.update(local)

        def check_partial(nums):
            result = 0
            for num in nums:
                digits = len(str(num))
                while num > 0:
                    if num in seen:
                        result = max(result, digits)
                        break
                    num //= 10
                    digits -= 1
            return result

        WORKERS = 4
        chunks1 = chunk(arr1, WORKERS)
        chunks2 = chunk(arr2, WORKERS)

        # Phase 1: build seen (write phase — needs lock)
        with ThreadPoolExecutor(max_workers=WORKERS) as ex:
            futures = [ex.submit(build_partial, c) for c in chunks1]
            for f in as_completed(futures):
                f.result()

        # Phase 2: check arr2 (read-only on seen — no lock needed)
        with ThreadPoolExecutor(max_workers=WORKERS) as ex:
            results = list(ex.map(check_partial, chunks2))

        return max(results)

# Synced seamlessly with LeetHub Pro
# Pro features: https://bit.ly/leethubpro | Free version: https://bit.ly/leethubv4
# Get it here: https://chromewebstore.google.com/detail/leethub-v4/bcilpkkbokcopmabingnndookdogmbna
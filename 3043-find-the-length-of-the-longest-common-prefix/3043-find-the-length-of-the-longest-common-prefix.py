class Solution:
    def longestCommonPrefix(self, arr1: List[int], arr2: List[int]) -> int:
        seen = set()

        for num in arr1:
            while num > 0:
                seen.add(num)
                num //= 10

        result = 0

        for num in arr2:
            while num > 0:
                if num in seen:
                    # len(str(num)) is expensive — use a precomputed length
                    l = len(str(num))
                    if l > result:
                        result = l
                    break  # no shorter prefix will beat this one
                num //= 10

        return result

# Synced seamlessly with LeetHub Pro
# Pro features: https://bit.ly/leethubpro | Free version: https://bit.ly/leethubv4
# Get it here: https://chromewebstore.google.com/detail/leethub-v4/bcilpkkbokcopmabingnndookdogmbna
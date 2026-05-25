class Solution:
    def firstMissingPositive(self, nums: list[int]) -> int:
        n = len(nums)

        # Phase 1: cyclic sort — place each value v at index v-1
        # Invariant: nums[i] == i+1 when correctly placed
        i = 0
        while i < n:
            j = nums[i] - 1                          # correct index for nums[i]
            if 1 <= nums[i] <= n and nums[j] != nums[i]:
                nums[i], nums[j] = nums[j], nums[i]  # swap into correct position
            else:
                i += 1                               # already correct, move on

        # Phase 2: first index where value != index+1 is the answer
        for i in range(n):
            if nums[i] != i + 1:
                return i + 1

        return n + 1  # all 1..n present, answer is n+1

# Synced seamlessly with LeetHub Pro
# Pro features: https://bit.ly/leethubpro | Free version: https://bit.ly/leethubv4
# Get it here: https://chromewebstore.google.com/detail/leethub-v4/bcilpkkbokcopmabingnndookdogmbna
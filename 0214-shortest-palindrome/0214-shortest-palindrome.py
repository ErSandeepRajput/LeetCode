class Solution:
    def shortestPalindrome(self, s: str) -> str:
        if not s:
            return s

        # build KMP string: s + sentinel + reverse(s)
        t = s + '#' + s[::-1]
        n = len(t)

        # build failure function — single linear scan, fully serial
        fail = [0] * n
        j = 0
        for i in range(1, n):
            while j > 0 and t[i] != t[j]:
                j = fail[j-1]       # follow failure links — serial dependency
            if t[i] == t[j]:
                j += 1
            fail[i] = j

        # fail[-1] = length of longest palindromic prefix
        longest_palindrome_prefix_len = fail[-1]

        # prepend the reversed suffix
        suffix = s[longest_palindrome_prefix_len:]
        return suffix[::-1] + s

# Synced seamlessly with LeetHub Pro
# Pro features: https://bit.ly/leethubpro | Free version: https://bit.ly/leethubv4
# Get it here: https://chromewebstore.google.com/detail/leethub-v4/bcilpkkbokcopmabingnndookdogmbna
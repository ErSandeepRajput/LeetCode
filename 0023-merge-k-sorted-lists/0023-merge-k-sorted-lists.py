from concurrent.futures import ThreadPoolExecutor
from heapq import heappush, heappop
from typing import List, Optional

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def mergeKLists(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:

        def merge_two(l1, l2):
            """Merge two sorted linked lists — O(n+m)."""
            dummy = ListNode(0)
            cur = dummy
            while l1 and l2:
                if l1.val <= l2.val:
                    cur.next = l1
                    l1 = l1.next
                else:
                    cur.next = l2
                    l2 = l2.next
                cur = cur.next
            cur.next = l1 or l2
            return dummy.next

        if not lists:
            return None

        WORKERS = 4
        current_lists = [l for l in lists if l]  # strip empty lists

        with ThreadPoolExecutor(max_workers=WORKERS) as ex:
            while len(current_lists) > 1:
                # pair up adjacent lists for parallel merge
                pairs = [
                    (current_lists[i], current_lists[i+1] if i+1 < len(current_lists) else None)
                    for i in range(0, len(current_lists), 2)
                ]

                # merge each pair in parallel
                futures = [
                    ex.submit(merge_two, a, b if b else None)
                    for a, b in pairs
                ]

                current_lists = [f.result() for f in futures]

        return current_lists[0] if current_lists else None

# Synced seamlessly with LeetHub Pro
# Pro features: https://bit.ly/leethubpro | Free version: https://bit.ly/leethubv4
# Get it here: https://chromewebstore.google.com/detail/leethub-v4/bcilpkkbokcopmabingnndookdogmbna
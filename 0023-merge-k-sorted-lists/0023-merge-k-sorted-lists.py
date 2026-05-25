class Solution:
    def mergeKLists(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
        if not lists:
            return None

        # STEP-1: number of sublists
        k = len(lists)

        # STEP-2: index pointers and master list
        pointers = list(lists)
        master = []

        # STEP-3: iterate until all pointers exhausted
        while any(p is not None for p in pointers):
            for i in range(k):
                if pointers[i] is None:
                    continue

                val = pointers[i].val
                pointers[i] = pointers[i].next

                # find correct position from end, insert
                j = len(master) - 1
                while j >= 0 and master[j] > val:
                    j -= 1
                master.insert(j + 1, val)

        # STEP-4: build and return linked list
        dummy = ListNode(0)
        curr = dummy
        for val in master:
            curr.next = ListNode(val)
            curr = curr.next

        return dummy.next

# Synced seamlessly with LeetHub Pro
# Pro features: https://bit.ly/leethubpro | Free version: https://bit.ly/leethubv4
# Get it here: https://chromewebstore.google.com/detail/leethub-v4/bcilpkkbokcopmabingnndookdogmbna
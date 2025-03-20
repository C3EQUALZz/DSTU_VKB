"""
You are given an integer array nums consisting of n elements, and an integer k.

Find a contiguous subarray whose length is equal to k that has the maximum average value and return this value.
Any answer with a calculation error less than 10-5 will be accepted.

https://leetcode.com/problems/maximum-average-subarray-i/description/
"""

class Solution:
    def findMaxAverage(self, nums: list[int], k: int) -> float:
        s = ans = sum(nums[:k])

        for i in range(k, len(nums)):
            s += nums[i] - nums[i - k]
            ans = max(ans, s)

        return ans / k
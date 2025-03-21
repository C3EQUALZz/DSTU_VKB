"""
You are given an integer array height of length n. There are n vertical lines drawn such that the two endpoints of the
ith line are (i, 0) and (i, height[i]).

Find two lines that together with the x-axis form a container, such that the container contains the most water.

Return the maximum amount of water a container can store.

Notice that you may not slant the container.

https://leetcode.com/problems/container-with-most-water/description/?envType=problem-list-v2&envId=two-pointers
"""


class Solution:
    def maxArea(self, height: list[int]) -> int:
        max_square: float = float("-inf")

        left: int = 0
        right: int = len(height) - 1

        while left != right:
            max_square = max(max_square, min(height[left], height[right]) * (right - left))

            if height[left] < height[right]:
                left += 1
            else:
                right -= 1

        return max_square
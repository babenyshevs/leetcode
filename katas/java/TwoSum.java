package com.babenyshev.leetcode;

import java.util.*;

/**
 * LeetCode #1 - Two Sum (Easy)
 *
 * Given an array of integers nums and an integer target,
 * return indices of the two numbers such that they add up to target.
 *
 * Hash map approach — O(n) time, O(n) space.
 */
public class TwoSum {

    public int[] twoSum(int[] nums, int target) {
        Map<Integer, Integer> seen = new HashMap<>();
        for (int i = 0; i < nums.length; i++) {
            int complement = target - nums[i];
            if (seen.containsKey(complement)) {
                return new int[]{seen.get(complement), i};
            }
            seen.put(nums[i], i);
        }
        throw new IllegalArgumentException("No solution exists");
    }

    // --- Tests ---

    public static void main(String[] args) {
        TwoSum sol = new TwoSum();

        // Example 1
        assert Arrays.equals(sol.twoSum(new int[]{2, 7, 11, 15}, 9),
                new int[]{0, 1}) : "Example 1 failed";

        // Example 2
        assert Arrays.equals(sol.twoSum(new int[]{3, 2, 4}, 6),
                new int[]{1, 2}) : "Example 2 failed";

        // Negative numbers
        assert Arrays.equals(sol.twoSum(new int[]{-1, -2, -3, -4, -5}, -8),
                new int[]{2, 4}) : "Negative numbers failed";

        // Duplicate values
        assert Arrays.equals(sol.twoSum(new int[]{0, 4, 3, 0}, 0),
                new int[]{0, 3}) : "Duplicate values failed";

        System.out.println("All tests passed! ✅");
    }
}

class Solution:
    def can_rob(self, nums, k, capability):
        n = len(nums)
        dp = [0] * (n + 1)  # dp[i] will store the max houses we can rob till index i-1
        
        for i in range(1, n + 1):
            if nums[i - 1] <= capability:
                if i > 1:
                    dp[i] = max(dp[i - 1], dp[i - 2] + 1)
                else:
                    dp[i] = 1
            else:
                dp[i] = dp[i - 1]

        return dp[-1] >= k

    def minCapability(self, nums, k):
        low, high = min(nums), max(nums)
        
        while low < high:
            mid = (low + high) // 2
            if self.can_rob(nums, k, mid):
                high = mid
            else:
                low = mid + 1
        
        return low        
    
nums = [2,7,9,3,1]
k = 2

solver = Solution()
print(solver.minCapability(nums, k))

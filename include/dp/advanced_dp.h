#pragma once

#include <algorithm>
#include <cstddef>
#include <cstdint>
#include <functional>
#include <map>
#include <vector>

namespace algorithm_x {
namespace dp {

// 数位 DP — 求 [1, n] 所有数字的数位和。
inline int64_t digit_dp_sum(int64_t n) {
    if (n <= 0) return 0;
    std::vector<int> digits;
    for (int64_t x = n; x > 0; x /= 10) {
        digits.push_back(static_cast<int>(x % 10));
    }
    std::reverse(digits.begin(), digits.end());

    int m = static_cast<int>(digits.size());
    // dp[pos][tight][started] — memo
    // State: (pos, tight, started) -> pair<count, sum>
    using State = std::tuple<int, bool, bool>;
    std::map<State, std::pair<int64_t, int64_t>> memo;

    std::function<std::pair<int64_t, int64_t>(int, bool, bool)> dfs =
        [&](int pos, bool tight, bool started) -> std::pair<int64_t, int64_t> {
            if (pos == m) return {1, 0};
            State key = {pos, tight, started};
            if (memo.count(key)) return memo[key];

            int64_t cnt = 0, sum = 0;
            int limit = tight ? digits[static_cast<std::size_t>(pos)] : 9;
            for (int d = 0; d <= limit; ++d) {
                bool ntight = tight && (d == limit);
                bool nstarted = started || (d > 0);
                auto [sub_cnt, sub_sum] = dfs(pos + 1, ntight, nstarted);
                cnt += sub_cnt;
                sum += sub_sum;
                if (nstarted) sum += d * sub_cnt;
            }
            return memo[key] = {cnt, sum};
        };

    return dfs(0, true, false).second;
}

// 树形 DP — 最大独立集（无权树）。
// adj: 无向邻接表。返回最大独立集大小。
inline int tree_dp_max_independent_set(
    const std::vector<std::vector<std::size_t>>& adj) {
    std::size_t n = adj.size();
    if (n == 0) return 0;

    // dp[u][0] = max if u NOT selected
    // dp[u][1] = max if u IS selected
    std::vector<std::vector<int>> dp(n, std::vector<int>(2, 0));
    std::vector<bool> visited(n, false);

    std::function<void(std::size_t)> dfs = [&](std::size_t u) {
        visited[u] = true;
        dp[u][0] = 0;
        dp[u][1] = 1;
        for (std::size_t v : adj[u]) {
            if (visited[v]) continue;
            dfs(v);
            dp[u][0] += std::max(dp[v][0], dp[v][1]);
            dp[u][1] += dp[v][0];
        }
    };

    dfs(0);
    return std::max(dp[0][0], dp[0][1]);
}

}  // namespace dp
}  // namespace algorithm_x

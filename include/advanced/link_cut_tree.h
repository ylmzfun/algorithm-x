#pragma once

#include <algorithm>
#include <array>
#include <cstddef>
#include <vector>

namespace algorithm_x {
namespace advanced {

// Link-Cut Tree（动态树）— O(log n) 维护森林上的路径信息（此处聚合为路径和）。
//
// 核心思想：把每棵树剖成"虚实链"。每条实链用一棵 Splay 维护（中序遍历
// 恰好是链上从上到下的顺序），虚链只保留父指针：辅助树根的 fa 指向它的
// "路径父"（代表树上的父节点），但不作为 Splay 的孩子。于是：
//   - access(x)：把代表树根到 x 的整条路径变成一条实链，并令 x 成为该
//     实链 Splay 的根（LCT 一切操作的基础）；
//   - makeroot(x)：access 后把 x 所在 Splay 整树打上翻转懒标记，
//     使 x 成为代表树的根（换根）；
//   - link / cut：借助 makeroot 与 access 拼接 / 断开路径；
//   - 路径查询：makeroot(x) + access(y) 后，路径 x→y 的每个点都聚在 y
//     的 Splay 子树中，直接取 y 的聚合值即可。
//
// 聚合取"路径和"：sum = 点权 + 左子树和 + 右子树和。翻转只交换左右子树，
// 不改变和，因此懒标记不会破坏聚合值。
class LinkCutTree {
public:
    // 构造 n 个孤立点（编号 0..n-1），每个点初始点权为 0，各自是一棵树的根。
    explicit LinkCutTree(int n) : n_(std::max(n, 0)) {
        std::size_t size = static_cast<std::size_t>(n_);
        fa_.assign(size, -1);
        ch_.assign(size, std::array<int, 2>{-1, -1});
        rev_.assign(size, false);
        val_.assign(size, 0);
        sum_.assign(size, 0);
    }

    // 把 x 的点权设为 v。makeroot(x) 后 x 是辅助树根，直接改权再 pushup 即可。
    void set_value(int x, long long v) {
        makeroot(x);
        val_[static_cast<std::size_t>(x)] = v;
        pushup(x);
    }

    // 查询 x 的当前点权（点权始终存在 val_[x]，与 Splay 结构无关）。
    long long value(int x) const {
        return val_[static_cast<std::size_t>(x)];
    }

    // x 与 y 是否连通（makeroot(x) 后用 findroot 判连通）。
    // 注意：findroot 会调整 LCT 内部的 Splay 结构（摊还 O(log n)），
    // 但不会改变森林的连通性，因此本查询在逻辑上是只读的；
    // 内部结构数组声明为 mutable 以允许 const 方法使用。
    bool connected(int x, int y) const {
        if (x == y) return true;
        makeroot(x);
        return findroot(y) == x;
    }

    // 把 x 所在树的根换为 x（换根）。
    void makeroot(int x) const {
        access(x);
        push_rev(x);
    }

    // 求 x 所在代表树的根（access 后沿左孩子下探到最深处）。
    int findroot(int x) const {
        access(x);
        int cur = x;
        pushdown(cur);
        while (ch_[static_cast<std::size_t>(cur)][0] != -1) {
            cur = ch_[static_cast<std::size_t>(cur)][0];
            pushdown(cur);
        }
        splay(cur);
        return cur;
    }

    // 连接 x 与 y：把 x 所在树连到 y 上（要求 x、y 不连通，否则忽略）。
    void link(int x, int y) {
        makeroot(x);
        if (findroot(y) != x) {
            fa_[static_cast<std::size_t>(x)] = y;
        }
    }

    // 断开边 x-y（要求 x、y 直接相连，否则忽略）。
    void cut(int x, int y) {
        makeroot(x);
        access(y);
        // 此时路径 x→y 的辅助树以 y 为根：x 必须是 y 的左孩子，
        // 且 x 没有右孩子（x、y 之间没有其他点）。
        if (ch_[static_cast<std::size_t>(y)][0] == x &&
            ch_[static_cast<std::size_t>(x)][1] == -1) {
            ch_[static_cast<std::size_t>(y)][0] = -1;
            fa_[static_cast<std::size_t>(x)] = -1;
            pushup(y);
        }
    }

    // 查询 x 到 y 路径上的点权和（split：makeroot + access）。
    long long path_query(int x, int y) {
        makeroot(x);
        access(y);
        return sum_[static_cast<std::size_t>(y)];
    }

private:
    // 维护 x 的聚合值：路径和 = 点权 + 左子树和 + 右子树和。
    void pushup(int x) const {
        long long s = val_[static_cast<std::size_t>(x)];
        if (ch_[static_cast<std::size_t>(x)][0] != -1) {
            s += sum_[static_cast<std::size_t>(ch_[static_cast<std::size_t>(x)][0])];
        }
        if (ch_[static_cast<std::size_t>(x)][1] != -1) {
            s += sum_[static_cast<std::size_t>(ch_[static_cast<std::size_t>(x)][1])];
        }
        sum_[static_cast<std::size_t>(x)] = s;
    }

    // 翻转懒标记：交换 x 的左右孩子并打上标记（配合 makeroot 的换根）。
    void push_rev(int x) const {
        if (x == -1) return;
        std::swap(ch_[static_cast<std::size_t>(x)][0],
                  ch_[static_cast<std::size_t>(x)][1]);
        rev_[static_cast<std::size_t>(x)] = !rev_[static_cast<std::size_t>(x)];
    }

    // 下传懒标记：翻转不影响路径和，这里只为保证下探 / 旋转时的树形正确。
    void pushdown(int x) const {
        if (rev_[static_cast<std::size_t>(x)]) {
            push_rev(ch_[static_cast<std::size_t>(x)][0]);
            push_rev(ch_[static_cast<std::size_t>(x)][1]);
            rev_[static_cast<std::size_t>(x)] = false;
        }
    }

    // x 是否为它所在 Splay 的根：辅助树根的 fa 是"路径父"而不是 Splay 父亲。
    bool is_root(int x) const {
        if (x == -1) return true;
        int f = fa_[static_cast<std::size_t>(x)];
        if (f == -1) return true;
        return ch_[static_cast<std::size_t>(f)][0] != x &&
               ch_[static_cast<std::size_t>(f)][1] != x;
    }

    // Splay 旋转：把 x 向上旋转一层（dir = 1 表示 x 是 p 的右孩子）。
    void rotate(int x) const {
        int p = fa_[static_cast<std::size_t>(x)];
        int g = fa_[static_cast<std::size_t>(p)];
        int dir = (ch_[static_cast<std::size_t>(p)][1] == x) ? 1 : 0;
        int b = ch_[static_cast<std::size_t>(x)][dir ^ 1];
        if (!is_root(p)) {
            if (ch_[static_cast<std::size_t>(g)][0] == p) {
                ch_[static_cast<std::size_t>(g)][0] = x;
            } else {
                ch_[static_cast<std::size_t>(g)][1] = x;
            }
        }
        fa_[static_cast<std::size_t>(x)] = g;
        ch_[static_cast<std::size_t>(x)][dir ^ 1] = p;
        fa_[static_cast<std::size_t>(p)] = x;
        ch_[static_cast<std::size_t>(p)][dir] = b;
        if (b != -1) {
            fa_[static_cast<std::size_t>(b)] = p;
        }
        pushup(p);
        pushup(x);
    }

    // 把 x 旋到它所在 Splay 的根：先自上而下下传懒标记，再双旋。
    void splay(int x) const {
        std::vector<int> stack;
        int cur = x;
        stack.push_back(cur);
        while (!is_root(cur)) {
            cur = fa_[static_cast<std::size_t>(cur)];
            stack.push_back(cur);
        }
        for (std::size_t i = stack.size(); i > 0; --i) {
            pushdown(stack[i - 1]);
        }
        while (!is_root(x)) {
            int p = fa_[static_cast<std::size_t>(x)];
            int g = fa_[static_cast<std::size_t>(p)];
            if (!is_root(p)) {
                if ((ch_[static_cast<std::size_t>(p)][0] == x) ==
                    (ch_[static_cast<std::size_t>(g)][0] == p)) {
                    rotate(p);  // zig-zig：先转父亲
                } else {
                    rotate(x);  // zig-zag：先转自己
                }
            }
            rotate(x);
        }
        pushup(x);
    }

    // access(x)：把代表树根到 x 的路径变为一条实链，并令 x 成为该链
    // Splay 的根。循环里每次把当前点 y 旋到其辅助树根，旧的右孩子
    // （下一段实链）被摘除，只保留 fa 指向 y 作为虚边；last 是刚处理完
    // 的下段链的链首，作为新的右孩子接上。
    void access(int x) const {
        int last = -1;
        for (int y = x; y != -1; y = fa_[static_cast<std::size_t>(y)]) {
            splay(y);
            ch_[static_cast<std::size_t>(y)][1] = last;
            pushup(y);
            last = y;
        }
        splay(x);
    }

    int n_;
    mutable std::vector<int> fa_;                       // 父亲（辅助树内）/ 路径父（辅助树根）
    mutable std::vector<std::array<int, 2>> ch_;        // 左右孩子（-1 表示无）
    mutable std::vector<bool> rev_;                     // 翻转懒标记
    mutable std::vector<long long> val_;                // 点权
    mutable std::vector<long long> sum_;                // 路径和（Splay 子树聚合值）
};

}  // namespace advanced
}  // namespace algorithm_x

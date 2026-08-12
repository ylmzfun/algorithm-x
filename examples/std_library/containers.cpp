#include <array>
#include <deque>
#include <iostream>
#include <list>
#include <map>
#include <set>
#include <unordered_map>
#include <vector>

// 核心库示例 —— 标准库容器（序列 / 关联 / 哈希）。
// 对应 README 第 13 章「核心库 · 容器」。
int main() {
    std::cout << "== vector（动态数组，随机访问最快）==\n";
    std::vector<int> v{3, 1, 4};
    v.push_back(1);
    std::cout << "  size=" << v.size() << " back=" << v.back() << "\n";

    std::cout << "== array（定长栈上数组）==\n";
    std::array<int, 3> a{1, 2, 3};
    std::cout << "  sum=" << a[0] + a[1] + a[2] << "\n";

    std::cout << "== deque（双端队列，两端 O(1)）==\n";
    std::deque<int> d{2};
    d.push_front(1);
    d.push_back(3);
    std::cout << "  front=" << d.front() << " back=" << d.back() << "\n";

    std::cout << "== list（双向链表，中间插入 O(1)）==\n";
    std::list<int> l{1, 2, 3};
    l.insert(std::next(l.begin()), 9);
    std::cout << "  size=" << l.size() << "\n";

    std::cout << "== set / map（有序，红黑树）==\n";
    std::set<int> s{3, 1, 3, 2};
    std::cout << "  set size=" << s.size() << " contains(2)=" << s.contains(2) << "\n";
    std::map<std::string, int> m{{"a", 1}, {"b", 2}};
    m["c"] = 3;  // operator[] 不存在则插入
    std::cout << "  map size=" << m.size() << " b=" << m["b"] << "\n";

    std::cout << "== unordered_map（哈希表，平均 O(1)）==\n";
    std::unordered_map<std::string, int> h{{"x", 10}};
    h["y"] = 20;
    std::cout << "  size=" << h.size() << " x=" << h.at("x") << "\n";
    return 0;
}

#include <iostream>
#include <memory>
#include <mutex>
#include <vector>

// C/C++ 关键知识示例 —— RAII、对象生命周期、三/五法则。
// 对应 README 第 13 章「C/C++ 关键知识 · 语言核心」。
namespace {

int g_live = 0;

struct Resource {
    Resource() { ++g_live; }
    ~Resource() { --g_live; }
    Resource(const Resource&) = delete;             // 三/五法则：不可拷贝
    Resource& operator=(const Resource&) = delete;
};

struct Counter {
    static inline int copies = 0;
    Counter() = default;
    Counter(const Counter&) { ++copies; }
    Counter(Counter&&) noexcept = default;
};

}  // namespace

int main() {
    std::cout << "== RAII：作用域结束自动析构 ==\n";
    {
        Resource a;
        std::cout << "  live=" << g_live << "\n";          // 1
        {
            Resource b;
            std::cout << "  live=" << g_live << "\n";      // 2
        }  // b 在此析构
        std::cout << "  live=" << g_live << "\n";          // 1
    }  // a 在此析构
    std::cout << "  live=" << g_live << "\n";              // 0

    std::cout << "== 智能指针（所有权管理）==\n";
    {
        auto u = std::make_unique<Resource>();
        auto s = std::make_shared<Resource>();
        std::cout << "  use_count=" << s.use_count() << " live=" << g_live << "\n";
        {
            auto s2 = s;  // 引用计数 +1
            std::cout << "  use_count=" << s.use_count() << "\n";
        }  // s2 析构，计数 -1
        std::cout << "  use_count=" << s.use_count() << "\n";
    }
    std::cout << "  live=" << g_live << "\n";

    std::cout << "== 拷贝 vs 移动（reserve 消除扩容拷贝）==\n";
    std::vector<Counter> v;
    v.reserve(2);
    v.push_back(Counter{});
    v.push_back(Counter{});
    std::cout << "  copies=" << Counter::copies << " size=" << v.size() << "\n";

    std::cout << "== lock_guard（RAII 锁）==\n";
    std::mutex m;
    {
        std::lock_guard<std::mutex> lock(m);  // 构造加锁，析构自动解锁
        std::cout << "  locked section\n";
    }
    std::cout << "  unlocked\n";
    return 0;
}

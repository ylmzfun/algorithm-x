#include <atomic>
#include <future>
#include <iostream>
#include <thread>
#include <vector>

// 核心库示例 —— 并发（<thread> / <atomic> / <future>）。
// 对应 README 第 13 章「核心库 · 并发」（详细算法见第 10 章）。
namespace {

std::atomic<int> g_counter{0};

void worker() {
    for (int i = 0; i < 1000; ++i) {
        g_counter.fetch_add(1);  // 原子自增，无数据竞争
    }
}

int square(int x) { return x * x; }

}  // namespace

int main() {
    std::cout << "== std::thread + std::atomic ==\n";
    std::vector<std::thread> threads;
    for (int i = 0; i < 4; ++i) threads.emplace_back(worker);
    for (auto& t : threads) t.join();
    std::cout << "  counter=" << g_counter.load() << "（期望 4000）\n";

    std::cout << "== std::async / future（异步任务）==\n";
    std::future<int> f = std::async(std::launch::async, square, 9);
    std::cout << "  square(9)=" << f.get() << "\n";
    return 0;
}

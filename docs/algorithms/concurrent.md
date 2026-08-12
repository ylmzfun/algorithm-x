# 算法文档：`algorithm_x::concurrent` — 并发编程模块

本模块（`include/algorithm_x/concurrent/`，7 个头文件）提供并发编程经典原语与数据结构的教学级实现：细粒度锁哈希表、哲学家就餐、SPSC 无锁队列（附单例与读写锁）、Treiber 无锁栈、RCU（读-拷贝-更新）、信号量/可复用屏障与线程池。全部为头文件实现、仅依赖标准库（`<thread>`、`<mutex>`、`<atomic>` 等），每个组件在 `tests/concurrent/` 下配有单元测试（含多线程并发验证）。文档中的 API 签名与源码一致，线程安全性说明基于源码实现给出。

---

### `concurrent/concurrent_hash_table.h` — 细粒度锁并发哈希表
**用途**：支持多线程并发插入、查找、删除的哈希表，用"每桶一把锁"的方式把锁竞争分散到各桶，替代单把大锁。
**原理**：哈希桶数量 `bucket_count` 固定（默认 16），每个桶一个 `std::shared_mutex`：`insert`/`erase` 取写锁（独占），`find` 取读锁（共享，多读者可并行）。冲突的键挂在桶内 `std::list` 上，线性探测式的遍历比较。
**主要 API**：
```cpp
template <typename K, typename V>
class ConcurrentHashTable {
public:
    explicit ConcurrentHashTable(std::size_t bucket_count = 16);
    void insert(const K& key, const V& value);   // 已存在则覆盖值
    V* find(const K& key);                       // 不存在返回 nullptr
    bool erase(const K& key);
};
```
**复杂度**：单次操作均摊 O(桶内元素数)（假设均匀哈希，即 O(1)）；空间 O(键值对数 + bucket_count)。**线程安全**：操作本身线程安全（桶级锁保证同一桶内互斥）；但 `find` 返回的是桶内元素的裸指针，锁释放后若其他线程删除/修改该元素，指针即悬垂——调用方需自行保证生命周期（教学简化，不做引用计数）。
**使用场景**：
- 多线程共享键值存储（配置表、缓存）；
- 对比"细粒度锁 vs 单锁/无锁"的伸缩性差异；
- 学习 `shared_mutex`（读共享 / 写独占）的用法。
**使用示例**：
```cpp
#include "concurrent/concurrent_hash_table.h"
using namespace algorithm_x::concurrent;

ConcurrentHashTable<int, std::string> ht;
ht.insert(1, "one");
ht.insert(2, "two");
std::string* p = ht.find(1);   // *p == "one"
ht.erase(2);                   // true
```

---

### `concurrent/dining.h` — 哲学家就餐（资源分级法）
**用途**：经典死锁教学问题——N 个哲学家围圆桌，每人需要左右两把叉子才能吃饭，演示如何通过加锁顺序避免死锁。
**原理**：每把叉子一个 `std::mutex`。哲学家先拿编号较小的叉子、再拿编号较大的（`first = min(left,right)`, `second = max(left,right)`），资源分级保证全局一致的加锁顺序，从而不可能出现环形等待（死锁）。吃一次饭计数器 `eat_count_` 原子自增。
**主要 API**：
```cpp
class DiningPhilosophers {
public:
    explicit DiningPhilosophers(int num = 5);
    ~DiningPhilosophers();
    void philosopher(int id);   // 哲学家 id 执行一次"思考-拿叉-吃饭-放叉"
    void run(int rounds = 1);   // 启动所有哲学家并发执行 n 轮
    int eat_count() const;      // 累计吃饭次数（原子）
};
```
**复杂度**：时间 O(1) 每次就餐（不含思考 sleep），空间 O(num)。**线程安全**：`philosopher` 可多线程并发调用，锁顺序保证不死锁；`eat_count_` 为 `std::atomic<int>` 可安全读取。注意每次 `philosopher` 调用只吃一次，多轮需用 `run`。
**使用场景**：
- 讲解死锁四大条件与"破坏循环等待"的解决思路；
- 并发测试框架中的线程同步演示；
- 学习原子计数（`fetch_add`）的简单用法。
**使用示例**：
```cpp
#include "concurrent/dining.h"
#include <thread>
using namespace algorithm_x::concurrent;

DiningPhilosophers dp;                       // 默认 5 个哲学家
std::vector<std::thread> ts;
for (int i = 0; i < 5; ++i)
    ts.emplace_back([&dp, i] { dp.philosopher(i); });
for (auto& t : ts) t.join();                 // 全部完成、无死锁
dp.eat_count();                              // 5
```

---

### `concurrent/lock_free_queue.h` — SPSC 无锁队列（+ 单例 + 读写锁）
**用途**：聚合三个并发原语——单生产者单消费者（SPSC）无锁环形队列、线程安全单例、写优先读写锁。
**原理**：
- **LockFreeQueue**：环形缓冲区，`head_`（消费者）与 `tail_`（生产者）各一个原子索引，容量内部 +1 以区分"空"与"满"；push 用 relaxed 读 tail + acquire 读 head、release 写 tail，pop 对称，全程无锁（SPSC 场景下不需要 CAS）；
- **Singleton**：函数局部静态变量（C++11 起构造天然线程安全），`instance()` 返回同一实例；
- **ReadWriteLock**：`std::mutex` + 两个条件变量，写者优先——写者等待时新读者被 `read_cv_` 拦在门外（`writers_waiting_ > 0` 即等待），避免写者饥饿。
**主要 API**：
```cpp
// SPSC 无锁队列（仅限单生产者 + 单消费者使用）
template <typename T>
class LockFreeQueue {
public:
    explicit LockFreeQueue(std::size_t capacity);   // 实际可用容量 = capacity
    ~LockFreeQueue();
    bool push(const T& item);   // 满则返回 false
    bool pop(T& item);          // 空则返回 false
    bool empty() const;
};

// 线程安全单例（函数局部静态）
template <typename T>
class Singleton {
public:
    static T& instance();
protected:
    Singleton() = default;
    ~Singleton() = default;
    Singleton(const Singleton&) = delete;
    Singleton& operator=(const Singleton&) = delete;
};

// 写优先读写锁
class ReadWriteLock {
public:
    void lock_read();
    void unlock_read();
    void lock_write();
    void unlock_write();
};
```
**复杂度**：队列 push/pop 均摊 O(1)；空间 O(capacity)。**线程安全**：队列仅支持 **单生产者 + 单消费者**（多生产者/多消费者需外部加锁，源码不保证），内存序用 release/acquire 配对保证缓冲区数据可见性；Singleton 构造线程安全；ReadWriteLock 允许多读者并发、写者独占且写优先。
**使用场景**：
- 生产-消费流水线中的无锁数据传递（单生产者单消费者）；
- 全局唯一资源（配置、连接池）的线程安全访问；
- 读多写少的共享数据保护（对比 `std::shared_mutex` 的教学实现）。
**使用示例**：
```cpp
#include "concurrent/lock_free_queue.h"
using namespace algorithm_x::concurrent;

LockFreeQueue<int> q(8);
q.push(42);
int v = 0;
q.pop(v);                    // v == 42

ReadWriteLock rw;
rw.lock_read();              // 多读者可并行
// ... 共享读 ...
rw.unlock_read();
rw.lock_write();             // 写者独占
rw.unlock_write();
```

---

### `concurrent/lock_free_stack.h` — Treiber 无锁栈
**用途**：多线程安全、无锁的栈（LIFO），基于 Treiber 算法——对栈顶指针做 CAS 循环，是并发无锁数据结构的基础范本。
**原理**：栈顶 `head_` 为 `std::atomic<Node*>`。push：新建节点把 `next` 指向当前 head，`compare_exchange_weak` 循环替换 head；pop：CAS 把 head 从 n 换成 `n->next` 成功后取数据并删除节点。释放/获取内存序分别配对 push（release）与 pop（acquire）。
**主要 API**：
```cpp
template <typename T>
class LockFreeStack {
public:
    LockFreeStack();
    ~LockFreeStack();                    // 释放剩余节点
    void push(const T& value);
    bool pop(T& result);                 // 空则返回 false
    bool empty() const;
};
```
**复杂度**：push/pop 均摊 O(1)（CAS 争用下重试）；空间 O(栈内节点数)。**线程安全**：多线程 push/pop 安全；但这是教学实现，**未做 ABA 防护**（无 hazard pointer / 引用计数），pop 删除节点时若其他线程恰好持有该节点指针，存在释放后使用风险，仅适合学习场景。
**使用场景**：
- 多线程任务/对象的 LIFO 池；
- 学习无锁编程核心原语 CAS（`compare_exchange_weak`）与内存序；
- 对比 Treiber 栈与互斥锁栈的并发性能。
**使用示例**：
```cpp
#include "concurrent/lock_free_stack.h"
using namespace algorithm_x::concurrent;

LockFreeStack<int> s;
s.push(1); s.push(2);
int v;
s.pop(v);                    // v == 2（LIFO）
s.pop(v);                    // v == 1
s.pop(v);                    // false（空）
```

---

### `concurrent/rcu.h` — RCU（读-拷贝-更新）教学实现
**用途**：读多写极少的共享数据场景下，让读者几乎无锁、写者不阻塞读者的并发更新机制（Linux 内核经典同步技术）。
**原理**：本实现基于 `std::shared_ptr` 快照：读者在互斥锁内"取快照"（一次短临界区），之后完全无锁地读取该快照；写者构造新副本后发布新指针，旧版本由 `shared_ptr` 引用计数延迟回收——当最后一个持有快照的读者释放后才真正析构，等价于真实 RCU 的宽限期（grace period）。源码注释明确说明：真实 RCU 连读者临界区的锁都没有（无锁指针交换 + 内存屏障），因目标编译器暂不支持 `std::atomic<std::shared_ptr<T>>` 而退化为"mutex 只保护指针发布"的教学版本。
**主要 API**：
```cpp
template <typename T>
class RcuValue {
public:
    explicit RcuValue(T init);
    T read() const;              // 读者：锁内取快照，锁外无锁读
    void update(T new_value);    // 写者：拷贝-修改-发布，旧版本延迟回收
};
```
**复杂度**：read O(1)（一次短临界区 + 一次 shared_ptr 拷贝），update O(1)（新分配副本）；空间随活跃快照数增长，由引用计数自动回收。**线程安全**：任意数量读者与写者可并发；读者只会看到"某个已发布版本"的完整一致值（测试断言观察值均属于已发布集合），不依赖线程调度时序。
**使用场景**：
- 读多写少、写不频繁的共享配置/状态（如路由表、全局参数）；
- 学习 RCU 核心思想"复制-发布-延迟回收"及与 `shared_ptr` 的对应关系；
- 对比"写者加锁更新 vs 全程加锁"的读者路径开销。
**使用示例**：
```cpp
#include "concurrent/rcu.h"
using namespace algorithm_x::concurrent;

RcuValue<int> rcu(0);
rcu.update(42);                  // 写者发布新值
int v = rcu.read();              // 读者无锁读快照：42
```

---

### `concurrent/sync.h` — 计数信号量与可复用屏障
**用途**：两个基础同步原语——信号量（限制并发访问数量）与屏障（多线程汇合点），是并发控制的"积木"。
**原理**：
- **Semaphore**：`count_` 受 mutex 保护，`acquire` 在 count>0 时减一并放行，否则在条件变量上等待；`release` 加一并唤醒一个等待者；
- **Barrier**：`wait` 使 count 递减，最后一个到达的线程把计数重置为阈值并 `notify_all`（同时递增代数 generation_），其余线程等待"代数变化"后放行——代数机制使屏障可跨轮复用，不会误放行下一轮的线程。
**主要 API**：
```cpp
// 计数信号量
class Semaphore {
public:
    explicit Semaphore(int count = 0);
    void acquire();
    void release();
    int available() const;
};

// 可复用屏障（每轮等待 count 个线程）
class Barrier {
public:
    explicit Barrier(std::size_t count);
    void wait();
};
```
**复杂度**：acquire/release/wait 均摊 O(1)；空间 O(1)。**线程安全**：两者均可多线程并发使用（内部 mutex + 条件变量），线程会阻塞等待而非忙等。
**使用场景**：
- 限制共享资源的同时访问数量（如连接池、限流）；
- 并行计算中的阶段同步（每轮计算后所有线程汇合再进入下一轮）；
- 学习条件变量"谓词等待 + notify"的规范写法。
**使用示例**：
```cpp
#include "concurrent/sync.h"
using namespace algorithm_x::concurrent;

Semaphore sem(2);                // 最多 2 个并发访问者
sem.acquire();
sem.release();

Barrier bar(3);                  // 3 个线程汇合
std::thread([&]{ bar.wait(); }).detach();
bar.wait();                      // 等到第 3 个线程到达才放行
```

---

### `concurrent/thread_pool.h` — 简易线程池
**用途**：固定数量工作线程的任务执行框架——把任务投递到队列，由工作线程异步执行，避免为每个任务新建线程的开销。
**原理**：构造时创建 num_threads 个工作线程，各自在条件变量上等待；`submit` 把可调用对象包进 `std::packaged_task`（保存 future 结果）放入任务队列并 notify；工作线程取出任务执行。析构时置 `stop_ = true`、notify 全部并 join。任务可返回任意类型（`std::future` 获取），支持 lambda、函数对象与带参调用。
**主要 API**：
```cpp
class ThreadPool {
public:
    explicit ThreadPool(std::size_t num_threads);
    ~ThreadPool();               // 置停止标志、唤醒并 join 所有工作线程
    // 提交任务，返回 future<返回类型>
    template <typename F, typename... Args>
    auto submit(F&& f, Args&&... args)
        -> std::future<typename std::invoke_result_t<F, Args...>>;
    std::size_t worker_count() const;
};
```
**复杂度**：submit O(1) 均摊（锁保护队列 + 一次 notify）；空间 O(排队任务数 + 工作线程数)。**线程安全**：任意线程可并发 submit；同一任务对象的返回类型任意（void 也可，通过 `std::future<void>` 同步）。析构时若队列仍有任务，将先执行完剩余任务再退出（`stop_ && tasks_.empty()` 才返回）。
**使用场景**：
- 并行执行一批独立计算任务（如测试中的 100 个平方任务）；
- 网络服务 / 后台任务的通用执行框架；
- 学习 `packaged_task` + `future` + 条件变量生产者-消费者模型。
**使用示例**：
```cpp
#include "concurrent/thread_pool.h"
using namespace algorithm_x::concurrent;

ThreadPool pool(4);
auto fut = pool.submit([] { return 42; });         // 返回 int
fut.get();                                          // 42

std::vector<std::future<int>> futs;
for (int i = 0; i < 100; ++i)
    futs.push_back(pool.submit([i] { return i * i; }));
for (int i = 0; i < 100; ++i)
    EXPECT_EQ(futs[static_cast<std::size_t>(i)].get(), i * i);
```

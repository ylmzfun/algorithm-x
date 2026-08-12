# 性能工具（perf）

本目录（`include/algorithm_x/perf/`）收录性能导向的底层工具：缓存友好的宏与函数
（分支预测提示、数据预取、原子加载/存储、缓存行对齐与伪共享防护）、C++20 Concepts
模板约束示范（concept / requires / SFINAE / if constexpr），以及定长块内存池。
全部为可直接嵌入项目的轻量工具。共 3 个头文件，以下为 3 个条目。

---

### `perf/cache.h` — 缓存友好工具（宏与函数集合）

**用途**：提供分支预测提示、数据预取、原子读写、缓存行对齐与伪共享防护等底层性能原语，减少缓存缺失与同步开销。

**原理**：这些工具直接映射到编译器内建指令：`LIKELY/UNLIKELY` 用 `__builtin_expect` 提示 CPU 分支预测；`prefetch_*` 用 `__builtin_prefetch` 提前把数据拉入缓存（locality=3 → L1）；`load_acquire/store_release` 用 `__atomic_*` 生成获取/释放语义的无锁读写；`CacheAligned` 通过 `alignas(缓存行)` 让对象独占缓存行，避免多线程写相邻变量时的伪共享（false sharing）。缓存行大小按平台取 128（Apple Silicon）/ 64。

**主要 API**（逐一列出）：

```cpp
// 分支预测提示：LIKELY(cond) 期望为真，UNLIKELY(cond) 期望为假。
#define LIKELY(cond)   __builtin_expect(static_cast<bool>(cond), 1)
#define UNLIKELY(cond) __builtin_expect(static_cast<bool>(cond), 0)

// 预取：locality 3 → 预取到 L1。
inline void prefetch_read(const void* addr);    // 读预取
inline void prefetch_write(const void* addr);   // 写预取

// 原子加载/存储：获取语义读、释放语义写（无锁共享变量的安全读写）。
template <typename T> inline T load_acquire(const T& var);
template <typename T> inline void store_release(T& var, T value);

// 缓存行大小：Apple Silicon 为 128，其余平台为 64。
constexpr std::size_t HARDWARE_CACHE_LINE;

// 伪共享防护：对象按缓存行对齐并填充到行边界。
template <typename T, std::size_t CacheLine = HARDWARE_CACHE_LINE>
struct alignas(CacheLine) CacheAligned { T value; };
```

**复杂度**：全部为 O(1) 常数开销（编译期内建指令），无额外空间；`CacheAligned<T>` 空间 = CacheLine（对齐后补齐）。

**使用场景**：
- 热路径分支的预测提示（错误预测惩罚高的循环条件）
- 遍历大数组前的批量预取（隐藏内存延迟）
- 多线程各自写独立变量的防伪共享布局
- 无锁标志位 / 状态共享的获取-释放语义读写

**使用示例**：

```cpp
if (LIKELY(ptr != nullptr)) { /* 高频路径 */ }

prefetch_read(data + i);              // 提前把下一批数据拉进 L1
store_release(flag, true);            // 释放写：此后可见
bool ready = load_acquire(flag);      // 获取读：读到最新值

struct alignas(HARDWARE_CACHE_LINE) Counter { int64_t v; };  // 防伪共享
CacheAligned<int> slot; slot.value = 7;
```

---

### `perf/concepts.h` — C++20 Concepts 与模板约束

**用途**：演示约束模板编程的三种主流写法（concept、SFINAE、requires 子句）以及"编译期类型分派"，在编译期约束模板参数、获得更友好的错误信息并消除运行期开销。

**原理**：`concept` 用 `requires` 表达式描述类型需满足的语法要求（如支持 `a + b`）；模板可用 `requires std::integral<T>` 子句或 `enable_if_t` 施加约束，两者作用等价但概念表达更清晰；多个受不同约束的重载在编译期按约束精确度分派（overload resolution）；`if constexpr` 则在函数体内按类型分支，未命中分支不实例化。

**主要 API**：

```cpp
// 概念：可相加（要求支持 a + b）与可流式输出（要求支持 os << a）。
template <typename T>
concept Addable = requires(T a, T b) { a + b; };
template <typename T>
concept Printable = requires(std::ostream& os, const T& a) { os << a; };

// SFINAE 版：仅接受整型（enable_if）。
template <typename T, typename = std::enable_if_t<std::is_integral_v<T>>>
inline T twice_sfinae(T x);

// requires 子句版：仅接受整型。
template <typename T>
    requires std::integral<T>
inline T twice_requires(T x);

// 受 Addable 概念约束：a + b。
template <typename T>
    requires Addable<T>
inline T sum(T a, T b);

// 按约束分派：整型 / 浮点 / 其他。
template <typename T> requires std::integral<T>     inline std::string classify();
template <typename T> requires std::floating_point<T> inline std::string classify();
template <typename T>
    requires(!std::integral<T> && !std::floating_point<T>)
inline std::string classify();

// 编译期 if：整型翻倍，浮点平方，其他返回默认构造。
template <typename T>
inline T transform(T x);
```

**复杂度**：全部约束在编译期求值，零运行期开销、零额外空间。

**使用场景**：
- 用概念约束模板参数（比 SFINAE 错误信息友好、代码可读）
- 按类型族自动选择实现（整型/浮点/字符串等）
- 学习 C++20 概念、requires、if constexpr 与约束重载

**使用示例**：

```cpp
static_assert(Addable<int> && !Addable<void>);
twice_requires(21);                            // 42
sum(std::string("a"), std::string("b"));       // "ab"（字符串可相加）
classify<int>();                               // "integral"
classify<double>();                            // "floating_point"
classify<std::string>();                       // "other"
transform(3.0);                                // 9.0（浮点平方）
```

---

### `perf/memory_pool.h` — 定长块内存池

**用途**：避免高频小对象分配/释放时反复调用堆分配器（malloc）的系统调用与元数据开销，用预分配的大块内存 + 自由链表提供 O(1) 的分配回收。

**原理**：构造时一次性 `new[]` 申请 BlockSize × BlockCount 字节，并把每块的前 8 字节串成单向自由链表（空闲块内存即链表指针存储处）；`allocate` 从链表头取块，`deallocate` 把块插回链表头——均只需 O(1) 指针操作。块大小相同，天然无外部碎片。

**主要 API**：

```cpp
// 定长块内存池：BlockSize 每块字节数，BlockCount 总块数。
template <std::size_t BlockSize, std::size_t BlockCount>
class MemoryPool {
public:
    MemoryPool();                 // 预分配整块内存并构建自由链表
    ~MemoryPool();                // 一次性释放整块内存
    void* allocate();             // 取一块；池耗尽返回 nullptr
    void deallocate(void* ptr);   // 归还一块到自由链表
    std::size_t block_size() const;
    std::size_t capacity() const;
};
```

**复杂度**：allocate/deallocate 时间 O(1)；空间 BlockSize × BlockCount（+ 少量指针）。

**使用场景**：
- 高频小对象（如网络包、节点对象）的分配回收
- 希望分配地址连续、减少 TLB 缺失的场景
- 学习自由链表内存池的实现原理

**使用示例**：

```cpp
MemoryPool<64, 10> pool;              // 10 块，每块 64 字节
void* p = pool.allocate();            // 取一块
// 使用 p（注意：块大小固定，需自己管理对象生命周期）
pool.deallocate(p);                   // 归还，O(1)
```

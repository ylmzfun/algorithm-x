# 分布式算法（distributed）

本目录（`include/algorithm_x/distributed/`）收录分布式系统核心算法的教学实现：Paxos 共识、
一致性哈希、CRDT（G-Counter / ORSet）、分布式锁、Gossip 传播、MapReduce、两阶段提交
与向量时钟。全部为单机模拟 / 教学简化版本（同步消息、无网络分区与节点故障），用于理解
协议本质而非生产使用。共 8 个头文件，以下为 8 个条目。

---

### `distributed/consensus.h` — Paxos 单值共识

**用途**：解决分布式系统中多个节点就"单个值"达成一致的问题，保证最终所有节点接受同一个值。

**原理**：两阶段协议（prepare → accept）。阶段一，提议者携带提案号 n 向所有接受者广播，接受者承诺不再接受更小的提案号并返回已接受的值；阶段二，收集到多数派承诺后，若承诺者中已有人接受过值则必须采纳其中提案号最高的值（保证一致性），否则使用自己的值，再向该多数派广播 accept(n, v)。任意两个多数派必有交集，因此不可能有两个不同的值同时被选中。本实现为教学简化：同步消息、无故障、只解决单值共识。

**主要 API**：

```cpp
class Paxos {
public:
    explicit Paxos(std::size_t num_acceptors);
    bool propose(std::size_t proposal_id, int value);  // 一轮 prepare+accept，达成共识返回 true
    int chosen_value() const;                          // 被选中的值，未达成时返回 -1
    std::size_t num_acceptors() const;
};
```

**复杂度**：时间 O(n)（n 为接受者数，一轮 propose 遍历全部接受者）/ 空间 O(n)。消息数为 2n（prepare + accept 各一轮）。

**使用场景**：
- 理解两阶段共识协议与多数派原理
- 教学演示"更高提案号必须采纳已选值"的一致性约束
- 作为多值共识（提案实例序列）的前置知识

**使用示例**：

```cpp
Paxos p(3);
p.propose(1, 7);          // 达成共识，选中值 7
p.propose(2, 8);          // 更高提案号：多数派已接受 7，必须采纳 7
// p.chosen_value() == 7；重复使用相同提案号则返回 false
```

---

### `distributed/consistent_hash.h` — 一致性哈希

**用途**：在分布式缓存 / 分片系统中，把 key 稳定映射到节点，使节点增删时只有少量 key 需要迁移。

**原理**：把节点哈希到环上（哈希空间按 std::size_t 排序成环），每个物理节点用 `node#i` 生成多个虚拟节点打散负载；查询 key 时在环上找第一个哈希值不小于 key 的虚拟节点（lower_bound），绕环一圈兜底。增删节点只影响环上相邻区间内的 key，负载通过虚拟节点均匀化。

**主要 API**：

```cpp
class ConsistentHash {
public:
    ConsistentHash(const std::vector<std::string>& nodes, int virtual_nodes = 150);
    void add_node(const std::string& node);     // 添加物理节点
    void remove_node(const std::string& node);  // 移除物理节点
    std::string get_node(const std::string& key) const;  // key 所属节点，空环返回 ""
    std::size_t node_count() const;             // 虚拟节点总数
};
```

**复杂度**：add/remove 时间 O(v)（v 为每节点虚拟节点数）/ get_node 时间 O(log V)（V 为环上虚拟节点总数，std::map lower_bound）；空间 O(V)。

**使用场景**：
- 分布式缓存节点扩缩容时最小化缓存失效
- 一致性哈希教学与负载打散演示
- 需要确定性映射（同一 key 恒落同一节点）的场景

**使用示例**：

```cpp
ConsistentHash ch({"nodeA", "nodeB"}, 50);
std::string node = ch.get_node("item42");   // 映射到 nodeA 或 nodeB
ch.add_node("nodeC");                        // 只迁移少量 key
ch.remove_node("nodeA");
```

---

### `distributed/crdt.h` — CRDT 无冲突复制数据类型（G-Counter 与 ORSet）

**用途**：解决多副本并发更新后如何收敛到一致状态的问题，无需中心协调即可实现最终一致性。

**原理**：CRDT 的合并运算满足交换律、结合律与幂等性。G-Counter 各副本维护其他副本的本地计数，合并逐副本取最大值（只增语义保证单调收敛），总值为各副本之和。ORSet 为每个元素维护 add 标签集合与删除标签集合，元素存在 ⇔ 存在未被删除的 add 标签；remove 只标记本副本已知的标签（"只标记删除"），对未见过的元素记录元素级墓碑，保证并发 add/remove 合并后语义正确。

**主要 API**：

```cpp
class GCounter {
public:
    explicit GCounter(std::size_t replicas);
    void increment(std::size_t replica, int64_t delta = 1);  // 副本本地计数 +delta
    int64_t value() const;                                   // 所有副本计数之和
    void merge(const GCounter& other);                       // 逐副本取最大值
    int64_t local(std::size_t replica) const;                // 某副本的本地计数
};

class ORSet {
public:
    ORSet();                                     // 自动分配全局唯一副本编号
    explicit ORSet(std::size_t replica_id);      // 显式指定副本编号（勿重复）
    void add(const std::string& elem);
    void remove(const std::string& elem);
    bool contains(const std::string& elem) const;
    std::vector<std::string> elements() const;   // 所有存在元素（字典序）
    void merge(const ORSet& other);
};
```

**复杂度**：GCounter：increment/value/merge 均 O(r)（r 为副本数），空间 O(r)。ORSet：add O(log s)，remove/contains O(标签数)，merge O(标签总数)，空间 O(标签总数)（s 为某元素的标签集合大小）。

**使用场景**：
- 无主复制（leaderless）系统的计数 / 集合同步
- 离线可编辑数据的并发合并（如分布式协作）
- 学习最终一致性收敛条件的教学示例

**使用示例**：

```cpp
GCounter a(2), b(2);
a.increment(0, 3); a.increment(1, 1);
b.increment(1, 2);
a.merge(b); b.merge(a);      // 双向合并后均收敛
// a.value() == b.value() == 5（副本 0: max(3,0)=3，副本 1: max(1,2)=2）

ORSet x, y;
x.add("k"); y.add("k");
x.remove("k");               // 只删除自己 add 的标签
x.merge(y); y.merge(x);
// x.contains("k") == true（y 的 add 标签仍然存活）
```

---

### `distributed/distributed_lock.h` — 分布式锁（Lamport 风格模拟）

**用途**：演示分布式互斥锁的基本形态——多节点竞争同一资源时保证同一时刻只有一个节点持锁。

**原理**：单机多线程模拟版本：每个节点一个独立的原子布尔标志，`acquire` 用 compare_exchange_strong 原子地"抢"锁（false→true 成功），`release` 原子写回 false。教学上对应 Lamport 互斥思想的最小可运行形态，未涉及真实分布式环境的消息往返与租约。

**主要 API**：

```cpp
class DistributedLock {
public:
    explicit DistributedLock(std::size_t num_nodes);
    bool acquire(std::size_t node_id);   // 尝试获取锁，成功返回 true
    void release(std::size_t node_id);   // 释放锁
    bool is_locked(std::size_t node_id) const;
};
```

**复杂度**：时间 O(1)（无锁原子操作）/ 空间 O(n)（n 为节点数）。

**使用场景**：
- 理解互斥锁的原子语义（CAS）与临界区保护
- 分布式锁协议教学的前置模拟
- 多线程共享资源互斥的轻量演示

**使用示例**：

```cpp
DistributedLock lock(2);
lock.acquire(0);        // true，节点 0 持锁
lock.acquire(0);        // false，已被占用
lock.release(0);        // 释放后可再次 acquire
```

---

### `distributed/gossip.h` — Gossip 协议传播

**用途**：模拟信息在节点网络中像"流言"一样扩散的过程，统计全部节点收到消息所需的轮数。

**原理**：初始仅节点 0 知道消息；每轮每个已通知的节点向 k 个随机节点传播消息（重复目标被跳过），直到全部节点知情。传播呈指数级扩散，轮数约为 O(log n) 量级。协议天然去中心化、对节点故障有弹性，是分布式系统传播/成员管理（如 Cassandra、BitTorrent）的基础。

**主要 API**：

```cpp
// 每轮每个节点向 k 个随机节点散播消息，返回所有节点收到消息所需的轮数。
inline int gossip_protocol(int nodes, int k = 2);
```

**复杂度**：时间 O(k · n · rounds)，rounds 期望 O(log n)；空间 O(n)。随机数发生器固定种子（42），结果可复现。

**使用场景**：
- 分布式系统无中心传播 / 成员发现的教学模拟
- 对比不同 fanout（k）对传播速度的影响
- 理解流行病学传播模型（SIR 简化版）

**使用示例**：

```cpp
int rounds = gossip_protocol(1000, 3);   // 1000 节点，每轮向 3 个随机节点传播
// rounds 约为 O(log n) 量级；k 越大传播越快
```

---

### `distributed/map_reduce.h` — MapReduce 教学框架

**用途**：解决"对大量数据先映射再按 key 归约"的批处理问题，演示 Map → Shuffle → Reduce 三阶段流水线。

**原理**：Map 阶段对每个输入元素调用 map_fn 产出若干 (Key, Value) 对；Shuffle 阶段按 Key 分组（std::map）；Reduce 阶段对每个 Key 的 value 列表以组内首元素为初值、从左到右两两折叠调用 reduce_fn。本实现单机顺序执行，未模拟分布式并行、分区与容错。

**主要 API**：

```cpp
template <typename In, typename Key, typename Value, typename ReduceFunc>
std::map<Key, Value> map_reduce(
    const std::vector<In>& input,
    std::function<std::vector<std::pair<Key, Value>>(const In&)> map_fn,
    ReduceFunc reduce_fn);               // Value(const Value& acc, const Value& v)

// 便捷函数：按空格分词统计单词出现次数。
inline std::map<std::string, int> word_count(const std::vector<std::string>& texts);
```

**复杂度**：时间 O(P log P)（P 为 Map 阶段产出的 pair 总数，shuffle 用 std::map 分组）/ 空间 O(P)。

**使用场景**：
- 理解 MapReduce 编程模型（词频统计是最经典入门例）
- 对分组-归约类问题（如平方和、求和、计数）的通用框架
- 分布式批处理（Hadoop/Spark 思想）的教学前置

**使用示例**：

```cpp
auto counts = word_count({"hello world", "hello algorithm"});
// counts["hello"] == 2

auto sq = map_reduce<int, int, int>(
    std::vector<int>{2, 2, 2},
    [](const int& x) { return std::vector<std::pair<int, int>>{{x, x * x}}; },
    [](const int& acc, const int& v) { return acc + v; });
// sq[2] == 12（三个 4 累加，即平方和）
```

---

### `distributed/two_phase_commit.h` — 两阶段提交（2PC）

**用途**：解决跨多个参与者（数据库/服务）的分布式事务原子性问题——要么全部提交，要么全部回滚。

**原理**：阶段一（准备/投票）协调者向所有参与者发"准备"请求，赞成者进入 PREPARED 并把投票返回；阶段二（决定）若全部赞成则广播"提交"（COMMITTED），否则广播"中止"（ABORTED，回滚）。本模拟假设消息同步可靠；与真实系统一致地存在阻塞问题（协调者在阶段二前故障会让参与者一直等待）与单点故障。

**主要 API**：

```cpp
class TwoPhaseCommit {
public:
    enum State { kInitial = 0, kPrepared = 1, kCommitted = 2, kAborted = 3 };
    explicit TwoPhaseCommit(std::size_t num_participants);
    bool commit(const std::vector<bool>& participant_votes);  // 全赞成 → true；缺失票视为反对
    int participant_state(std::size_t i) const;               // 越界返回 kInitial
    std::size_t num_participants() const;
};
```

**复杂度**：时间 O(n)（n 为参与者数，一轮 commit 遍历两次）/ 空间 O(n)。消息数为 2n。

**使用场景**：
- 分布式事务原子提交协议教学（对比 3PC、Paxos 的改进点）
- 理解"协调者故障导致阻塞"这一根本局限
- 数据库两阶段提交（如 XA 协议）的前置知识

**使用示例**：

```cpp
TwoPhaseCommit tpc(3);
tpc.commit({true, true, true});      // 全赞成 → 全部 kCommitted，返回 true
tpc.commit({true, false, true});     // 任一反对 → 全部 kAborted，返回 false
tpc.commit({true});                  // 票数不足（缺失视为反对）→ 中止
```

---

### `distributed/vector_clock.h` — 向量时钟

**用途**：解决分布式系统中事件的因果排序问题，比 Lamport 时钟更精确——能区分"因果先后"与"并发"。

**原理**：每个节点维护一个 n 维向量（每维对应一个节点的逻辑时钟）。本节点事件时递增自己那维；发送消息前 merge 对方时钟（逐维取最大值）并带上自己那维。判断规则：A 的每维都不大于 B 且至少一维严格小于 ⇒ A 发生在 B 之前（happens_before）；既存在小于又存在大于 ⇒ 两者并发（is_concurrent）。

**主要 API**：

```cpp
class VectorClock {
public:
    explicit VectorClock(std::size_t num_nodes);
    void increment(std::size_t node_id);              // 本节点事件，递增自己的时钟
    void merge(const VectorClock& other);             // 逐维取最大值
    bool is_concurrent(const VectorClock& other) const;
    bool happens_before(const VectorClock& other) const;  // 严格小于关系
    const std::vector<int>& clock() const;
    std::size_t size() const;
};
```

**复杂度**：increment O(1)，merge/happens_before/is_concurrent 均 O(n)；空间 O(n)（n 为节点数）。

**使用场景**：
- 分布式系统因果一致性（causal consistency）的实现基础
- 检测并发写冲突（如 DynamoDB 的版本向量）
- 理解 Lamport 时钟局限性的教学示例

**使用示例**：

```cpp
VectorClock a(3), b(3);
a.increment(0); b.increment(1);   // 两个不同节点的事件
a.is_concurrent(b);               // true：互不先后
a.merge(b);                       // 合并后 a 追平 b（a 已"看到"b 的事件）
```

#pragma once

#include <memory>
#include <mutex>
#include <utility>

namespace algorithm_x {
namespace concurrent {

// RCU（Read-Copy-Update）教学实现。
//
// 原理：
//   1. 读（Read）：读者在锁内原子取得当前版本的 shared_ptr 快照，
//      随后完全无锁地读取该快照——写者如何更新都影响不到它；
//   2. 拷贝（Copy）：写者不直接修改共享数据，而是构造一份新副本；
//   3. 更新（Update）：修改副本后发布新指针，读者下一次读即看到新版本；
//   4. 延迟回收：旧版本由 shared_ptr 引用计数回收——当最后一个持有快照的
//      读者释放后才真正析构，等价于真实 RCU 的宽限期（grace period）延迟回收。
//
// 教学简化：真实 RCU 使用无锁的指针交换与内存屏障（读路径连互斥锁都没有）。
// 由于目标编译器（Apple clang libc++）尚不支持 C++20 的
// std::atomic<std::shared_ptr<T>>（要求 T 平凡可复制），这里退化为
// "mutex 只保护指针的发布/替换" 的版本：读者取得快照后无锁读，语义等价。
template <typename T>
class RcuValue {
public:
    explicit RcuValue(T init) : data_(std::make_shared<T>(std::move(init))) {}

    // 读者：锁内取快照，锁外无锁读取（读路径只有一个短临界区）。
    T read() const {
        std::shared_ptr<T> snapshot;
        {
            std::lock_guard<std::mutex> lock(mutex_);
            snapshot = data_;
        }
        return *snapshot;
    }

    // 写者：构造新副本后发布新指针；旧版本由引用计数延迟回收。
    void update(T new_value) {
        std::shared_ptr<T> fresh = std::make_shared<T>(std::move(new_value));
        {
            std::lock_guard<std::mutex> lock(mutex_);
            data_ = std::move(fresh);
        }
    }

private:
    mutable std::mutex mutex_;
    std::shared_ptr<T> data_;
};

}  // namespace concurrent
}  // namespace algorithm_x

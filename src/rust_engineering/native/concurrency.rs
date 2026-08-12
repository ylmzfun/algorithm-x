//! 并发与同步（仅 std）
//!
//! 覆盖主题：
//! - `thread::scope`：借用非 `'static` 数据的线程作用域（无需 Arc 也能共享引用）
//! - `mpsc` 通道：线程间传递消息
//! - `Arc<Mutex<T>>`：互斥锁保护共享状态
//! - 原子操作：`AtomicUsize` + `Ordering::Relaxed`
//! - `LazyLock`：静态变量懒初始化，只计算一次

use std::sync::atomic::{AtomicUsize, Ordering};
use std::sync::{Arc, LazyLock, Mutex};

/// 多线程分块求和
///
/// `thread::scope` 允许子线程借用栈上的 `nums`（无需 `'static` 与 Arc）；
/// 用 `chunks` 把数组均分为 `threads` 份，每份一个线程求和，最后汇总。
/// 复杂度 O(n)，线程数取 `min(threads, len)`。
pub fn parallel_sum(nums: &[i32], threads: usize) -> i32 {
    let n = nums.len();
    if n == 0 {
        return 0;
    }
    let threads = threads.clamp(1, n);
    let chunk_size = n.div_ceil(threads);
    std::thread::scope(|scope| {
        let handles: Vec<_> = nums
            .chunks(chunk_size)
            .map(|chunk| scope.spawn(move || chunk.iter().sum::<i32>()))
            .collect();
        handles.into_iter().map(|h| h.join().unwrap()).sum()
    })
}

/// mpsc 通道往返：发送 0..5，接收方原样收集
///
/// `channel()` 返回 `(Sender, Receiver)`；发送端线程结束后通道关闭，
/// `rx.into_iter()` 在通道关闭时自然终止。
pub fn channel_roundtrip() -> Vec<i32> {
    let (tx, rx) = std::sync::mpsc::channel();
    std::thread::spawn(move || {
        for i in 0..5 {
            tx.send(i).unwrap();
        }
    });
    rx.into_iter().collect()
}

/// Arc<Mutex> 共享计数器
///
/// 每个线程对同一个 `Mutex<usize>` 加锁后自增 `per_thread` 次，
/// 返回最终计数。`Mutex` 保证写写互斥，结果确定。
pub fn shared_counter(threads: usize, per_thread: usize) -> usize {
    let counter = Arc::new(Mutex::new(0usize));
    std::thread::scope(|scope| {
        for _ in 0..threads {
            let counter = Arc::clone(&counter);
            scope.spawn(move || {
                for _ in 0..per_thread {
                    *counter.lock().unwrap() += 1;
                }
            });
        }
    });
    *counter.lock().unwrap()
}

/// 原子计数器
///
/// `fetch_add(1, Ordering::Relaxed)` 是原子的读-改-写，多个线程并发调用
/// 不会丢失增量。Relaxed 在此足够：我们不关心操作的全局顺序，只保证
/// "每次 fetch_add 都生效"，最终计数必定等于总增量。
pub fn atomic_counter(threads: usize, per_thread: usize) -> usize {
    let counter = Arc::new(AtomicUsize::new(0));
    std::thread::scope(|scope| {
        for _ in 0..threads {
            let counter = Arc::clone(&counter);
            scope.spawn(move || {
                for _ in 0..per_thread {
                    counter.fetch_add(1, Ordering::Relaxed);
                }
            });
        }
    });
    counter.load(Ordering::Relaxed)
}

/// 素数表（上限 100），LazyLock 静态缓存
///
/// `static CACHE: LazyLock<Vec<u64>> = LazyLock::new(|| ...)` 在首次访问时
/// 执行一次初始化闭包，此后所有线程共享同一份数据（内部用 Once 保证只算一次）。
/// 注意：初始化闭包无法引用函数参数，因此这里固定生成 100 以内的素数表。
static PRIME_CACHE: LazyLock<Vec<u64>> = LazyLock::new(|| {
    let mut primes = Vec::new();
    for n in 2..=100u64 {
        if primes.iter().all(|&p| n % p != 0) {
            primes.push(n);
        }
    }
    primes
});

/// 获取 100 以内素数表（懒初始化）
///
/// 返回静态缓存的引用，多次调用不会重复计算。
pub fn lazy_primes() -> &'static Vec<u64> {
    &PRIME_CACHE
}

/// 线程返回值的获取
///
/// `thread::spawn` 返回 `JoinHandle`，其 `join()` 返回
/// `Result<T, Box<dyn Any + Send>>`（线程 panic 时是 Err），`unwrap` 取值。
pub fn spawn_result() -> i32 {
    std::thread::spawn(|| 42).join().unwrap()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_parallel_sum() {
        let nums: Vec<i32> = (1..=100).collect();
        assert_eq!(parallel_sum(&nums, 4), 5050);
        assert_eq!(parallel_sum(&nums, 1), 5050);
        assert_eq!(parallel_sum(&[], 4), 0);
    }

    #[test]
    fn test_channel_roundtrip() {
        assert_eq!(channel_roundtrip(), vec![0, 1, 2, 3, 4]);
    }

    #[test]
    fn test_shared_counter() {
        assert_eq!(shared_counter(4, 100), 400);
    }

    #[test]
    fn test_atomic_counter() {
        assert_eq!(atomic_counter(4, 100), 400);
    }

    #[test]
    fn test_lazy_primes() {
        let primes = lazy_primes();
        for p in [2u64, 3, 5, 7] {
            assert!(primes.contains(&p));
        }
        assert!(!primes.contains(&4));
        // 多次调用返回同一缓存
        assert!(std::ptr::eq(lazy_primes(), primes));
    }

    #[test]
    fn test_spawn_result() {
        assert_eq!(spawn_result(), 42);
    }
}

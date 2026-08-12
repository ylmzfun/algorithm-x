//! tokio / futures 异步运行时
//!
//! 覆盖主题：async 函数、`tokio::spawn` 并发任务、`Runtime::block_on`
//! 同步驱动异步、mpsc 通道、`tokio::time::timeout` 超时、
//! `futures::future::join_all` 批量并发。
//!
//! 典型场景：网络 IO 密集任务用异步避免阻塞线程；在同步代码中通过
//! `Runtime::block_on` 进入异步世界；`#[tokio::test]` 提供测试用的
//! 异步运行时。

/// 计算平方的异步函数
///
/// 展示最简 async 函数写法：`async fn` 返回 Future，
/// 在 `.await` 或 `block_on` 时才真正执行。
pub async fn compute_square(x: i32) -> i32 {
    x * x
}

/// 同步包装：并发执行两个异步任务
///
/// `Runtime::block_on` 在当前线程驱动异步运行时；`tokio::spawn` 把
/// 任务提交到运行时线程池并发执行，`JoinHandle.await` 取回结果。
/// 3² 与 4² 并行计算，互不等待。
pub fn run_concurrent() -> Vec<i32> {
    tokio::runtime::Runtime::new().unwrap().block_on(async {
        let t1 = tokio::spawn(compute_square(3));
        let t2 = tokio::spawn(compute_square(4));
        vec![t1.await.unwrap(), t2.await.unwrap()]
    })
}

/// mpsc 通道：生产者 → 消费者流水线
///
/// `tokio::sync::mpsc::channel(4)` 建一个有界通道；spawn 的生产者
/// 发送 0..5 后随闭包结束 drop(tx)，接收端 `recv()` 返回 None 结束循环。
pub async fn channel_pipeline() -> Vec<i32> {
    let (tx, mut rx) = tokio::sync::mpsc::channel::<i32>(4);
    tokio::spawn(async move {
        for i in 0..5 {
            tx.send(i).await.unwrap();
        }
    });
    let mut out = Vec::new();
    while let Some(v) = rx.recv().await {
        out.push(v);
    }
    out
}

/// 超时演示：慢任务超过时限返回 Err
///
/// `tokio::time::timeout` 包住一个 sleep 200ms 的任务但只给 50ms，
/// 到时返回 `Elapsed` 错误，防止任务无限挂起。
pub async fn timeout_demo() -> Result<i32, tokio::time::error::Elapsed> {
    tokio::time::timeout(std::time::Duration::from_millis(50), async {
        tokio::time::sleep(std::time::Duration::from_millis(200)).await;
        42
    })
    .await
}

/// 同步包装：join_all 批量并发求平方
///
/// `futures::future::join_all` 接受一个 Future 迭代器，并发驱动全部，
/// 完成后按输入顺序返回结果向量（这里是 0..n 的平方）。
pub fn join_all_squares(n: i32) -> Vec<i32> {
    tokio::runtime::Runtime::new()
        .unwrap()
        .block_on(async { futures::future::join_all((0..n).map(compute_square)).await })
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_concurrent() {
        // run_concurrent 内部自行创建 Runtime，须在普通测试中调用
        assert_eq!(run_concurrent(), vec![9, 16]);
    }

    #[tokio::test]
    async fn test_channel() {
        assert_eq!(channel_pipeline().await, vec![0, 1, 2, 3, 4]);
    }

    #[tokio::test]
    async fn test_timeout() {
        assert!(timeout_demo().await.is_err());
    }

    #[test]
    fn test_join_all() {
        assert_eq!(join_all_squares(4), vec![0, 1, 4, 9]);
    }
}

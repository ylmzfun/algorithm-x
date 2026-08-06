/// 线性时间排序算法
///
/// 这些算法不基于比较，因此可以突破 Ω(n log n) 的下界。
/// 前提：数据满足特定约束（如范围有限）。
///
/// - 计数排序 O(n + k) — 适合小范围整数
/// - 桶排序 O(n) 平均 — 适合均匀分布数据
/// - 基数排序 O(d * (n + k)) — 适合固定长度的整数或字符串

/// 计数排序
///
/// 统计每个值的出现次数，然后依次输出。
/// 仅适用于非负整数且范围 k 较小的情况。
pub fn counting_sort(arr: &[usize], max_val: usize) -> Vec<usize> {
    let mut count = vec![0usize; max_val + 1];
    for &x in arr {
        count[x] += 1;
    }
    // 前缀和：count[i] 表示 ≤ i 的元素个数
    for i in 1..=max_val {
        count[i] += count[i - 1];
    }
    // 从后向前填充以保持稳定性
    let mut result = vec![0; arr.len()];
    for &x in arr.iter().rev() {
        count[x] -= 1;
        result[count[x]] = x;
    }
    result
}

/// 计数排序（泛型版本，支持负整数）
pub fn counting_sort_i32(arr: &[i32]) -> Vec<i32> {
    if arr.is_empty() {
        return vec![];
    }
    let min = *arr.iter().min().unwrap();
    let max = *arr.iter().max().unwrap();
    let range = (max - min + 1) as usize;

    let mut count = vec![0usize; range];
    for &x in arr {
        count[(x - min) as usize] += 1;
    }
    for i in 1..range {
        count[i] += count[i - 1];
    }
    let mut result = vec![0; arr.len()];
    for &x in arr.iter().rev() {
        let idx = (x - min) as usize;
        count[idx] -= 1;
        result[count[idx]] = x;
    }
    result
}

/// 桶排序
///
/// 将数据分配到若干个桶中，每个桶内部用插入排序，然后合并。
/// 适合数据均匀分布的情况。
pub fn bucket_sort(arr: &[f64]) -> Vec<f64> {
    if arr.is_empty() {
        return vec![];
    }
    let n = arr.len();
    let mut buckets: Vec<Vec<f64>> = (0..n).map(|_| Vec::new()).collect();

    // 分配到桶中
    for &x in arr {
        let idx = (x * n as f64) as usize;
        let idx = idx.min(n - 1);
        buckets[idx].push(x);
    }

    // 每个桶内排序
    for bucket in &mut buckets {
        bucket.sort_unstable_by(|a, b| a.partial_cmp(b).unwrap());
    }

    // 合并
    buckets.into_iter().flatten().collect()
}

/// 基数排序（LSD — 从最低位开始）
///
/// 按每个数位（个位、十位、百位...）依次做计数排序。
/// 因为是稳定排序，最终结果正确。
pub fn radix_sort(arr: &[u32]) -> Vec<u32> {
    if arr.is_empty() {
        return vec![];
    }
    let max = *arr.iter().max().unwrap();
    let mut result = arr.to_vec();
    let mut exp = 1;

    while max / exp > 0 {
        let mut count = [0usize; 10];
        let mut output = vec![0; result.len()];

        // 按当前位计数
        for &x in &result {
            let digit = ((x / exp) % 10) as usize;
            count[digit] += 1;
        }
        // 前缀和
        for i in 1..10 {
            count[i] += count[i - 1];
        }
        // 逆序填充（保持稳定性）
        for &x in result.iter().rev() {
            let digit = ((x / exp) % 10) as usize;
            count[digit] -= 1;
            output[count[digit]] = x;
        }

        result = output;
        exp *= 10;
    }
    result
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_counting_sort() {
        let arr = [4, 2, 2, 8, 3, 3, 1];
        assert_eq!(counting_sort(&arr, 8), vec![1, 2, 2, 3, 3, 4, 8]);
    }

    #[test]
    fn test_counting_sort_i32() {
        let arr = [-3, 1, -5, 2, 0, 4];
        assert_eq!(counting_sort_i32(&arr), vec![-5, -3, 0, 1, 2, 4]);
    }

    #[test]
    fn test_bucket_sort() {
        let arr = [0.42, 0.32, 0.23, 0.52, 0.25, 0.47];
        let sorted = bucket_sort(&arr);
        for i in 1..sorted.len() {
            assert!(sorted[i - 1] <= sorted[i]);
        }
    }

    #[test]
    fn test_radix_sort() {
        let arr = [170, 45, 75, 90, 802, 24, 2, 66];
        assert_eq!(radix_sort(&arr), vec![2, 24, 45, 66, 75, 90, 170, 802]);
    }
}

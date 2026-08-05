// 大整数乘法（Karatsuba 算法）—— 简化实现处理非负整数
export function karatsuba(x: number, y: number): number {
  if (x < 10 || y < 10) return x * y;
  const n = Math.max(String(x).length, String(y).length);
  const m = Math.floor(n / 2);
  const pow = 10 ** m;

  const a = Math.floor(x / pow);
  const b = x % pow;
  const c = Math.floor(y / pow);
  const d = y % pow;

  const ac = karatsuba(a, c);
  const bd = karatsuba(b, d);
  const ad_bc = karatsuba(a + b, c + d) - ac - bd;

  return ac * 10 ** (2 * m) + ad_bc * 10 ** m + bd;
}

// 快速幂
export function fastPow(base: number, exp: number): number {
  let result = 1;
  let b = base;
  let e = exp;
  while (e > 0) {
    if (e & 1) result *= b;
    b *= b;
    e >>= 1;
  }
  return result;
}

// 最大子数组和（Kadane）
export function maxSubArray(arr: number[]): number {
  let maxSoFar = arr[0];
  let maxEndingHere = arr[0];
  for (let i = 1; i < arr.length; i++) {
    maxEndingHere = Math.max(arr[i], maxEndingHere + arr[i]);
    maxSoFar = Math.max(maxSoFar, maxEndingHere);
  }
  return maxSoFar;
}

// 逆序对计数（归并分治）
export function countInversions(arr: number[]): number {
  function mergeCount(a: number[], temp: number[], left: number, right: number): number {
    if (left >= right) return 0;
    const mid = (left + right) >> 1;
    let inv = mergeCount(a, temp, left, mid) + mergeCount(a, temp, mid + 1, right);

    let i = left, j = mid + 1, k = left;
    while (i <= mid && j <= right) {
      if (a[i] <= a[j]) {
        temp[k++] = a[i++];
      } else {
        temp[k++] = a[j++];
        inv += mid - i + 1;
      }
    }
    while (i <= mid) temp[k++] = a[i++];
    while (j <= right) temp[k++] = a[j++];
    for (let p = left; p <= right; p++) a[p] = temp[p];
    return inv;
  }

  return mergeCount([...arr], new Array(arr.length), 0, arr.length - 1);
}

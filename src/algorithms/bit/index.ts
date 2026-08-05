// 是否为 2 的幂
export function isPowerOfTwo(n: number): boolean {
  return n > 0 && (n & (n - 1)) === 0;
}

// 统计二进制中 1 的个数（Brian Kernighan）
export function countSetBits(n: number): number {
  let count = 0;
  while (n) {
    n &= n - 1;
    count++;
  }
  return count;
}

// 翻转二进制位（32-bit）
export function reverseBits(n: number): number {
  let result = 0;
  for (let i = 0; i < 32; i++) {
    result = (result << 1) | (n & 1);
    n >>= 1;
  }
  return result >>> 0;
}

// 只出现一次的数字（其他出现两次）
export function singleNumber(nums: number[]): number {
  let result = 0;
  for (const n of nums) result ^= n;
  return result;
}

// 布隆过滤器
export class BloomFilter {
  private bits: Uint8Array;
  private hashCount: number;

  constructor(size: number, hashCount = 3) {
    this.bits = new Uint8Array(Math.ceil(size / 8));
    this.hashCount = hashCount;
  }

  add(item: string): void {
    const bitSize = this.bits.length * 8;
    for (let i = 0; i < this.hashCount; i++) {
      const idx = this.hash(item, i) % bitSize;
      this.bits[idx >> 3] |= 1 << (idx & 7);
    }
  }

  contains(item: string): boolean {
    const bitSize = this.bits.length * 8;
    for (let i = 0; i < this.hashCount; i++) {
      const idx = this.hash(item, i) % bitSize;
      if (!(this.bits[idx >> 3] & (1 << (idx & 7)))) return false;
    }
    return true;
  }

  private hash(item: string, seed: number): number {
    let h = seed;
    for (let i = 0; i < item.length; i++) {
      h = (h * 31 + item.charCodeAt(i)) | 0;
    }
    return Math.abs(h);
  }
}

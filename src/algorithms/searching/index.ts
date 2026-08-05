export function linearSearch<T>(arr: T[], target: T): number {
  for (let i = 0; i < arr.length; i++) {
    if (arr[i] === target) return i;
  }
  return -1;
}

export function binarySearch(arr: number[], target: number): number {
  let lo = 0;
  let hi = arr.length - 1;
  while (lo <= hi) {
    const mid = (lo + hi) >>> 1;
    if (arr[mid] === target) return mid;
    if (arr[mid] < target) lo = mid + 1;
    else hi = mid - 1;
  }
  return -1;
}

export function binarySearchRecursive(arr: number[], target: number): number {
  function recurse(lo: number, hi: number): number {
    if (lo > hi) return -1;
    const mid = (lo + hi) >>> 1;
    if (arr[mid] === target) return mid;
    return arr[mid] < target
      ? recurse(mid + 1, hi)
      : recurse(lo, mid - 1);
  }
  return recurse(0, arr.length - 1);
}

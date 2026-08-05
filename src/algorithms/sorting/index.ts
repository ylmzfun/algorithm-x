export function bubbleSort(arr: number[]): number[] {
  const a = [...arr];
  for (let i = 0; i < a.length - 1; i++) {
    let swapped = false;
    for (let j = 0; j < a.length - 1 - i; j++) {
      if (a[j] > a[j + 1]) {
        [a[j], a[j + 1]] = [a[j + 1], a[j]];
        swapped = true;
      }
    }
    if (!swapped) break;
  }
  return a;
}

export function selectionSort(arr: number[]): number[] {
  const a = [...arr];
  for (let i = 0; i < a.length - 1; i++) {
    let minIdx = i;
    for (let j = i + 1; j < a.length; j++) {
      if (a[j] < a[minIdx]) minIdx = j;
    }
    if (minIdx !== i) [a[i], a[minIdx]] = [a[minIdx], a[i]];
  }
  return a;
}

export function insertionSort(arr: number[]): number[] {
  const a = [...arr];
  for (let i = 1; i < a.length; i++) {
    const key = a[i];
    let j = i - 1;
    while (j >= 0 && a[j] > key) {
      a[j + 1] = a[j];
      j--;
    }
    a[j + 1] = key;
  }
  return a;
}

export function shellSort(arr: number[]): number[] {
  const a = [...arr];
  let gap = Math.floor(a.length / 2);
  while (gap > 0) {
    for (let i = gap; i < a.length; i++) {
      const key = a[i];
      let j = i;
      while (j >= gap && a[j - gap] > key) {
        a[j] = a[j - gap];
        j -= gap;
      }
      a[j] = key;
    }
    gap = Math.floor(gap / 2);
  }
  return a;
}

function merge(left: number[], right: number[]): number[] {
  const result: number[] = [];
  let i = 0, j = 0;
  while (i < left.length && j < right.length) {
    result.push(left[i] <= right[j] ? left[i++] : right[j++]);
  }
  return result.concat(left.slice(i), right.slice(j));
}

export function mergeSort(arr: number[]): number[] {
  if (arr.length <= 1) return [...arr];
  const mid = Math.floor(arr.length / 2);
  return merge(mergeSort(arr.slice(0, mid)), mergeSort(arr.slice(mid)));
}

function partition(a: number[], lo: number, hi: number): number {
  const pivot = a[hi];
  let i = lo - 1;
  for (let j = lo; j < hi; j++) {
    if (a[j] <= pivot) {
      i++;
      [a[i], a[j]] = [a[j], a[i]];
    }
  }
  [a[i + 1], a[hi]] = [a[hi], a[i + 1]];
  return i + 1;
}

function quickSortInPlace(a: number[], lo: number, hi: number): void {
  if (lo >= hi) return;
  const p = partition(a, lo, hi);
  quickSortInPlace(a, lo, p - 1);
  quickSortInPlace(a, p + 1, hi);
}

export function quickSort(arr: number[]): number[] {
  const a = [...arr];
  quickSortInPlace(a, 0, a.length - 1);
  return a;
}

export function countingSort(arr: number[]): number[] {
  if (arr.length === 0) return [];
  const max = Math.max(...arr);
  const min = Math.min(...arr);
  const range = max - min + 1;
  const count = new Array(range).fill(0);
  for (const v of arr) count[v - min]++;
  for (let i = 1; i < range; i++) count[i] += count[i - 1];
  const output = new Array(arr.length);
  for (let i = arr.length - 1; i >= 0; i--) {
    const v = arr[i];
    output[--count[v - min]] = v;
  }
  return output;
}

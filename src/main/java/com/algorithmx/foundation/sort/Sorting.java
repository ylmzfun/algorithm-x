package com.algorithmx.foundation.sort;

/**
 * 十大经典排序算法
 */
public class Sorting {

    // ==================== O(n²) ====================
    /**
     * 冒泡排序 — 稳定
     */
    public static void bubbleSort(int[] arr) {
        int n = arr.length;
        for (int i = 0; i < n - 1; i++) {
            boolean swapped = false;
            for (int j = 0; j < n - 1 - i; j++) {
                if (arr[j] > arr[j + 1]) {
                    swap(arr, j, j + 1);
                    swapped = true;
                }
            }
            if (!swapped) {
                break;
            }
        }
    }

    /**
     * 选择排序 — 不稳定
     */
    public static void selectionSort(int[] arr) {
        int n = arr.length;
        for (int i = 0; i < n - 1; i++) {
            int minIdx = i;
            for (int j = i + 1; j < n; j++) {
                if (arr[j] < arr[minIdx]) {
                    minIdx = j;
                }
            }
            swap(arr, i, minIdx);
        }
    }

    /**
     * 插入排序 — 稳定
     */
    public static void insertionSort(int[] arr) {
        for (int i = 1; i < arr.length; i++) {
            int key = arr[i], j = i - 1;
            while (j >= 0 && arr[j] > key) {
                arr[j + 1] = arr[j];
                j--;
            }
            arr[j + 1] = key;
        }
    }

    // ==================== O(n log n) ====================
    /**
     * 归并排序 — 稳定
     */
    public static void mergeSort(int[] arr) {
        mergeSort(arr, 0, arr.length - 1);
    }

    private static void mergeSort(int[] arr, int left, int right) {
        if (left >= right) {
            return;
        }
        int mid = left + (right - left) / 2;
        mergeSort(arr, left, mid);
        mergeSort(arr, mid + 1, right);
        merge(arr, left, mid, right);
    }

    private static void merge(int[] arr, int left, int mid, int right) {
        int[] tmp = new int[right - left + 1];
        int i = left, j = mid + 1, k = 0;
        while (i <= mid && j <= right) {
            tmp[k++] = arr[i] <= arr[j] ? arr[i++] : arr[j++];
        }
        while (i <= mid) {
            tmp[k++] = arr[i++];
        }
        while (j <= right) {
            tmp[k++] = arr[j++];
        }
        System.arraycopy(tmp, 0, arr, left, tmp.length);
    }

    /**
     * 快速排序 — 不稳定
     */
    public static void quickSort(int[] arr) {
        quickSort(arr, 0, arr.length - 1);
    }

    private static void quickSort(int[] arr, int left, int right) {
        if (left >= right) {
            return;
        }
        int pivot = partition(arr, left, right);
        quickSort(arr, left, pivot - 1);
        quickSort(arr, pivot + 1, right);
    }

    private static int partition(int[] arr, int left, int right) {
        int pivot = arr[right], i = left;
        for (int j = left; j < right; j++) {
            if (arr[j] < pivot) {
                swap(arr, i++, j);
            }
        }
        swap(arr, i, right);
        return i;
    }

    /**
     * 堆排序 — 不稳定
     */
    public static void heapSort(int[] arr) {
        int n = arr.length;
        // 建堆
        for (int i = n / 2 - 1; i >= 0; i--) {
            heapify(arr, n, i);
        }
        // 排序
        for (int i = n - 1; i > 0; i--) {
            swap(arr, 0, i);
            heapify(arr, i, 0);
        }
    }

    private static void heapify(int[] arr, int size, int i) {
        int largest = i, left = 2 * i + 1, right = 2 * i + 2;
        if (left < size && arr[left] > arr[largest]) {
            largest = left;
        }
        if (right < size && arr[right] > arr[largest]) {
            largest = right;
        }
        if (largest != i) {
            swap(arr, i, largest);
            heapify(arr, size, largest);
        }
    }

    // ==================== 线性排序 ====================
    /**
     * 计数排序
     */
    public static void countingSort(int[] arr) {
        if (arr.length == 0) {
            return;
        }
        int max = arr[0], min = arr[0];
        for (int v : arr) {
            if (v > max) {
                max = v;
            }
            if (v < min) {
                min = v;
            }
        }
        int range = max - min + 1;
        int[] count = new int[range];
        for (int v : arr) {
            count[v - min]++;
        }
        for (int i = 0, idx = 0; i < range; i++) {
            while (count[i]-- > 0) {
                arr[idx++] = i + min;
            }
        }
    }

    /**
     * 希尔排序 — 不稳定
     */
    public static void shellSort(int[] arr) {
        int n = arr.length;
        for (int gap = n / 2; gap > 0; gap /= 2) {
            for (int i = gap; i < n; i++) {
                int key = arr[i], j = i;
                while (j >= gap && arr[j - gap] > key) {
                    arr[j] = arr[j - gap];
                    j -= gap;
                }
                arr[j] = key;
            }
        }
    }

    /**
     * 桶排序
     */
    public static void bucketSort(int[] arr) {
        if (arr.length <= 1) {
            return;
        }
        int max = arr[0], min = arr[0];
        for (int v : arr) {
            if (v > max) {
                max = v;

            }
            if (v < min) {
                min = v;

            }
        }
        int bucketCount = Math.max(1, (max - min) / arr.length + 1);
        java.util.List<Integer>[] buckets = new java.util.ArrayList[bucketCount];
        for (int i = 0; i < bucketCount; i++) {
            buckets[i] = new java.util.ArrayList<>();
        }
        for (int v : arr) {
            buckets[(v - min) / arr.length].add(v);
        }
        int idx = 0;
        for (java.util.List<Integer> bucket : buckets) {
            java.util.Collections.sort(bucket);
            for (int v : bucket) {
                arr[idx++] = v;
            }
        }
    }

    /**
     * 基数排序（LSD）
     */
    public static void radixSort(int[] arr) {
        if (arr.length <= 1) {
            return;
        }
        int max = arr[0];
        for (int v : arr) {
            if (v > max) {
                max = v;
            }
        }
        for (int exp = 1; max / exp > 0; exp *= 10) {
            countingSortByDigit(arr, exp);
        }
    }

    private static void countingSortByDigit(int[] arr, int exp) {
        int n = arr.length;
        int[] output = new int[n], count = new int[10];
        for (int v : arr) {
            count[(v / exp) % 10]++;
        }
        for (int i = 1; i < 10; i++) {
            count[i] += count[i - 1];
        }
        for (int i = n - 1; i >= 0; i--) {
            int digit = (arr[i] / exp) % 10;
            output[--count[digit]] = arr[i];
        }
        System.arraycopy(output, 0, arr, 0, n);
    }

    // ==================== 工具 ====================
    private static void swap(int[] arr, int i, int j) {
        int tmp = arr[i];
        arr[i] = arr[j];
        arr[j] = tmp;
    }
}

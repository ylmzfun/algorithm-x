package com.algorithmx.datastructure.heap;

/**
 * 最大堆 — 数组实现
 */
public class MaxHeap {
    private final int[] heap;
    private int size;

    public MaxHeap(int capacity) {
        heap = new int[capacity];
    }

    public MaxHeap(int[] arr) {
        heap = arr;
        size = arr.length;
        for (int i = size / 2 - 1; i >= 0; i--) siftDown(i);
    }

    public void offer(int val) {
        heap[size] = val;
        siftUp(size);
        size++;
    }

    public int poll() {
        int top = heap[0];
        heap[0] = heap[--size];
        siftDown(0);
        return top;
    }

    public int peek() { return heap[0]; }
    public int size() { return size; }
    public boolean isEmpty() { return size == 0; }

    private void siftUp(int idx) {
        while (idx > 0) {
            int parent = (idx - 1) / 2;
            if (heap[parent] >= heap[idx]) break;
            swap(parent, idx);
            idx = parent;
        }
    }

    private void siftDown(int idx) {
        while (true) {
            int largest = idx, left = 2 * idx + 1, right = 2 * idx + 2;
            if (left < size && heap[left] > heap[largest]) largest = left;
            if (right < size && heap[right] > heap[largest]) largest = right;
            if (largest == idx) break;
            swap(idx, largest);
            idx = largest;
        }
    }

    private void swap(int i, int j) {
        int tmp = heap[i]; heap[i] = heap[j]; heap[j] = tmp;
    }
}

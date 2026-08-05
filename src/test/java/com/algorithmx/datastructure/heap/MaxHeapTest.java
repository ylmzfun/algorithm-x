package com.algorithmx.datastructure.heap;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class MaxHeapTest {

    @Test void basic() {
        MaxHeap heap = new MaxHeap(10);
        heap.offer(3);
        heap.offer(1);
        heap.offer(5);
        heap.offer(2);
        heap.offer(4);

        assertEquals(5, heap.poll());
        assertEquals(4, heap.poll());
        assertEquals(3, heap.poll());
        assertEquals(2, heap.poll());
        assertEquals(1, heap.poll());
        assertTrue(heap.isEmpty());
    }

    @Test void heapify() {
        int[] arr = {3, 1, 5, 2, 4};
        MaxHeap heap = new MaxHeap(arr);
        assertEquals(5, heap.poll());
        assertEquals(4, heap.poll());
        assertEquals(3, heap.poll());
        assertEquals(2, heap.poll());
        assertEquals(1, heap.poll());
    }
}

package com.algorithmx.foundation.sort;

import java.util.Arrays;
import java.util.Random;

import static org.junit.jupiter.api.Assertions.assertArrayEquals;
import static org.junit.jupiter.api.Assertions.assertEquals;
import org.junit.jupiter.api.Test;

class SortingTest {

    private static final Random RAND = new Random(42);

    private static int[] randomArray(int n) {
        return RAND.ints(n, 0, 1000).toArray();
    }

    private static void testSort(String name, java.util.function.Consumer<int[]> sortFn) {
        for (int i = 0; i < 20; i++) {
            int[] arr = randomArray(50);
            int[] expected = arr.clone();
            Arrays.sort(expected);
            sortFn.accept(arr);
            assertArrayEquals(expected, arr, name + " failed");
        }
    }

    @Test void bubbleSort() { testSort("bubbleSort", Sorting::bubbleSort); }
    @Test void selectionSort() { testSort("selectionSort", Sorting::selectionSort); }
    @Test void insertionSort() { testSort("insertionSort", Sorting::insertionSort); }
    @Test void mergeSort() { testSort("mergeSort", Sorting::mergeSort); }
    @Test void quickSort() { testSort("quickSort", Sorting::quickSort); }
    @Test void heapSort() { testSort("heapSort", Sorting::heapSort); }
    @Test void countingSort() { testSort("countingSort", Sorting::countingSort); }
    @Test void shellSort() { testSort("shellSort", Sorting::shellSort); }
    @Test void bucketSort() { testSort("bucketSort", Sorting::bucketSort); }
    @Test void radixSort() { testSort("radixSort", Sorting::radixSort); }

    @Test void emptyArray() {
        int[] arr = {};
        Sorting.quickSort(arr);
        assertEquals(0, arr.length);
    }

    @Test void singleElement() {
        int[] arr = {5};
        Sorting.quickSort(arr);
        assertArrayEquals(new int[]{5}, arr);
    }
}

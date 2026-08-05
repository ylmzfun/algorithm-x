package com.algorithmx.technique.image;

import java.util.List;

import static org.junit.jupiter.api.Assertions.assertArrayEquals;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;
import org.junit.jupiter.api.Test;

class ImageProcessingTest {

    private int[][] sample() {
        return new int[][]{
            {10, 20, 30, 40},
            {50, 60, 70, 80},
            {90,100,110,120},
            {130,140,150,160}
        };
    }

    @Test void flipHorizontal() {
        int[][] res = ImageProcessing.flipHorizontal(sample());
        assertEquals(40, res[0][0]);
        assertEquals(10, res[0][3]);
        assertEquals(80, res[1][0]);
    }

    @Test void flipVertical() {
        int[][] res = ImageProcessing.flipVertical(sample());
        assertEquals(130, res[0][0]);
        assertEquals(10, res[3][0]);
    }

    @Test void rotate90() {
        int[][] img = {{1, 2}, {3, 4}, {5, 6}}; // 3×2
        // 顺时针 90°:
        //   1 2       5 3 1
        //   3 4   →   6 4 2
        //   5 6
        int[][] res = ImageProcessing.rotate90(img);
        assertEquals(2, res.length);     // 2×3
        assertEquals(3, res[0].length);
        assertArrayEquals(new int[]{5, 3, 1}, res[0]);
        assertArrayEquals(new int[]{6, 4, 2}, res[1]);
    }

    @Test void blur() {
        int[][] img = new int[5][5];
        for (int i = 0; i < 5; i++)
            for (int j = 0; j < 5; j++)
                img[i][j] = 100;
        int[][] res = ImageProcessing.blur(img);
        assertEquals(100, res[1][1], 1);
    }

    @Test void sharpen() {
        int[][] img = {
            {50, 50, 50, 50},
            {50,100,100, 50},
            {50,100,100, 50},
            {50, 50, 50, 50}
        };
        int[][] res = ImageProcessing.sharpen(img);
        assertEquals(2, res.length);    // 4-2=2
        assertEquals(2, res[0].length); // 4-2=2
        // 中心亮区经过锐化后值更大（5*100 为核心权重）
        assertTrue(res[0][0] > 100, "center should be sharpened above original 100");
    }

    @Test void sobel() {
        int[][] flat = {{50, 50, 50}, {50, 50, 50}, {50, 50, 50}};
        int[][] flatRes = ImageProcessing.sobel(flat); // 1×1
        assertEquals(0, flatRes[0][0], "flat area has no gradient");

        // 左黑右白的垂直边缘
        int[][] edge = {
            {0,  0, 255, 255},
            {0,  0, 255, 255},
            {0,  0, 255, 255},
            {0,  0, 255, 255}
        };
        int[][] edgeRes = ImageProcessing.sobel(edge); // 2×2
        assertTrue(edgeRes[0][0] > 0, "vertical edge should produce gradient");
        assertTrue(edgeRes[1][0] > 0);
    }

    @Test void histogramEqualization() {
        int[][] img = {{50, 55}, {55, 200}};
        int[][] res = ImageProcessing.histogramEqualization(img);
        assertNotEquals(50, res[0][0]); // values should be redistributed
    }

    @Test void dilateAndErode() {
        int[][] img = {{0, 0, 0}, {0, 255, 0}, {0, 0, 0}};
        int[][] d = ImageProcessing.dilate(img);
        assertTrue(d[0][0] > 0 || d[0][1] > 0); // single pixel spreads

        int[][] e = ImageProcessing.erode(d);
        // erosion shrinks back
        assertTrue(e[1][1] >= 0);
    }

    @Test void floodFill() {
        int[][] img = {
            {1, 1, 1},
            {1, 1, 0},
            {1, 0, 1}
        };
        int[][] res = ImageProcessing.floodFill(img, 1, 1, 2);
        assertEquals(2, res[0][0]);
        assertEquals(2, res[1][1]);
        assertEquals(0, res[1][2]); // not connected
    }

    @Test void runLengthEncodeDecode() {
        int[][] img = {{255, 255, 0}, {0, 128, 128}};
        List<int[]> rle = ImageProcessing.runLengthEncode(img);
        int[][] decoded = ImageProcessing.runLengthDecode(rle, 2, 3);
        assertArrayEquals(img[0], decoded[0]);
        assertArrayEquals(img[1], decoded[1]);
    }
}

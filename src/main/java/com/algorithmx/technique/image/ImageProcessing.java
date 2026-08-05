package com.algorithmx.technique.image;

import java.util.*;

/**
 * 图像处理算法 — 基于二维数组的纯 Java 实现
 *
 * 约定：图像为 int[][]，值范围 [0, 255] 表示灰度。
 * 不依赖任何第三方图像库。
 */
public class ImageProcessing {

    // ==================== 翻转与旋转 ====================

    /** 水平翻转 */
    public static int[][] flipHorizontal(int[][] img) {
        int h = img.length, w = img[0].length;
        int[][] res = new int[h][w];
        for (int i = 0; i < h; i++)
            for (int j = 0; j < w; j++)
                res[i][j] = img[i][w - 1 - j];
        return res;
    }

    /** 垂直翻转 */
    public static int[][] flipVertical(int[][] img) {
        int h = img.length, w = img[0].length;
        int[][] res = new int[h][w];
        for (int i = 0; i < h; i++)
            res[i] = img[h - 1 - i];
        return res;
    }

    /** 顺时针旋转 90° */
    public static int[][] rotate90(int[][] img) {
        int h = img.length, w = img[0].length;
        int[][] res = new int[w][h];
        for (int i = 0; i < h; i++)
            for (int j = 0; j < w; j++)
                res[j][h - 1 - i] = img[i][j];
        return res;
    }

    /** 旋转 180° */
    public static int[][] rotate180(int[][] img) {
        return rotate90(rotate90(img));
    }

    // ==================== 卷积滤波 ====================

    /** 通用卷积（valid 模式，不补边） */
    public static int[][] convolve(int[][] img, double[][] kernel) {
        int h = img.length, w = img[0].length;
        int kh = kernel.length, kw = kernel[0].length;
        int outH = h - kh + 1, outW = w - kw + 1;
        int[][] res = new int[outH][outW];
        int r0 = kh / 2, c0 = kw / 2;
        for (int i = 0; i < outH; i++) {
            for (int j = 0; j < outW; j++) {
                double sum = 0;
                for (int ki = 0; ki < kh; ki++)
                    for (int kj = 0; kj < kw; kj++)
                        sum += img[i + ki][j + kj] * kernel[ki][kj];
                res[i][j] = clamp((int) Math.round(sum));
            }
        }
        return res;
    }

    /** 高斯模糊 3×3 */
    public static int[][] blur(int[][] img) {
        double[][] kernel = {
            {1/16.0, 2/16.0, 1/16.0},
            {2/16.0, 4/16.0, 2/16.0},
            {1/16.0, 2/16.0, 1/16.0}
        };
        return convolve(img, kernel);
    }

    /** 锐化 */
    public static int[][] sharpen(int[][] img) {
        double[][] kernel = {
            { 0, -1,  0},
            {-1,  5, -1},
            { 0, -1,  0}
        };
        return convolve(img, kernel);
    }

    /** Sobel 边缘检测 — 返回梯度幅值 */
    public static int[][] sobel(int[][] img) {
        double[][] gx = {{-1, 0, 1}, {-2, 0, 2}, {-1, 0, 1}};
        double[][] gy = {{-1, -2, -1}, {0, 0, 0}, {1, 2, 1}};
        int h = img.length, w = img[0].length;
        int[][] res = new int[h - 2][w - 2];
        for (int i = 1; i < h - 1; i++) {
            for (int j = 1; j < w - 1; j++) {
                double sx = 0, sy = 0;
                for (int ki = -1; ki <= 1; ki++) {
                    for (int kj = -1; kj <= 1; kj++) {
                        sx += img[i + ki][j + kj] * gx[ki + 1][kj + 1];
                        sy += img[i + ki][j + kj] * gy[ki + 1][kj + 1];
                    }
                }
                res[i - 1][j - 1] = clamp((int) Math.sqrt(sx * sx + sy * sy));
            }
        }
        return res;
    }

    // ==================== 直方图 ====================

    /** 直方图均衡化 */
    public static int[][] histogramEqualization(int[][] img) {
        int h = img.length, w = img[0].length;
        int total = h * w;
        int[] hist = new int[256];
        for (int[] row : img) for (int p : row) hist[p]++;

        int[] cdf = new int[256]; // 累积分布
        cdf[0] = hist[0];
        for (int i = 1; i < 256; i++) cdf[i] = cdf[i - 1] + hist[i];

        int minCdf = 0;
        for (int v : cdf) { if (v > 0) { minCdf = v; break; } }

        int[][] res = new int[h][w];
        for (int i = 0; i < h; i++)
            for (int j = 0; j < w; j++)
                res[i][j] = clamp(Math.round((cdf[img[i][j]] - minCdf) * 255f / (total - minCdf)));
        return res;
    }

    // ==================== 形态学 ====================

    /** 膨胀（3×3 结构元素） */
    public static int[][] dilate(int[][] img) {
        int h = img.length, w = img[0].length;
        int[][] res = new int[h][w];
        for (int i = 0; i < h; i++) {
            for (int j = 0; j < w; j++) {
                int max = 0;
                for (int di = -1; di <= 1; di++)
                    for (int dj = -1; dj <= 1; dj++)
                        max = Math.max(max, getSafe(img, i + di, j + dj, 0));
                res[i][j] = max;
            }
        }
        return res;
    }

    /** 腐蚀（3×3 结构元素） */
    public static int[][] erode(int[][] img) {
        int h = img.length, w = img[0].length;
        int[][] res = new int[h][w];
        for (int i = 0; i < h; i++) {
            for (int j = 0; j < w; j++) {
                int min = 255;
                for (int di = -1; di <= 1; di++)
                    for (int dj = -1; dj <= 1; dj++)
                        min = Math.min(min, getSafe(img, i + di, j + dj, 255));
                res[i][j] = min;
            }
        }
        return res;
    }

    // ==================== 填充 ====================

    /** 泛洪填充（BFS）— 将与 (sr, sc) 连通的 oldColor 替换为 newColor */
    public static int[][] floodFill(int[][] img, int sr, int sc, int newColor) {
        int h = img.length, w = img[0].length;
        int oldColor = img[sr][sc];
        if (oldColor == newColor) return img;
        int[][] res = deepCopy(img);
        Queue<int[]> q = new LinkedList<>();
        q.offer(new int[]{sr, sc});
        res[sr][sc] = newColor;
        int[][] dirs = {{1, 0}, {-1, 0}, {0, 1}, {0, -1}};
        while (!q.isEmpty()) {
            int[] p = q.poll();
            for (int[] d : dirs) {
                int r = p[0] + d[0], c = p[1] + d[1];
                if (r >= 0 && r < h && c >= 0 && c < w && res[r][c] == oldColor) {
                    res[r][c] = newColor;
                    q.offer(new int[]{r, c});
                }
            }
        }
        return res;
    }

    // ==================== 压缩 ====================

    /** 游程编码（Run-Length Encoding） */
    public static List<int[]> runLengthEncode(int[][] img) {
        List<int[]> rle = new ArrayList<>();
        int last = -1, count = 0;
        for (int[] row : img) {
            for (int p : row) {
                if (p == last) { count++; }
                else {
                    if (last != -1) rle.add(new int[]{last, count});
                    last = p;
                    count = 1;
                }
            }
        }
        if (last != -1) rle.add(new int[]{last, count});
        return rle;
    }

    /** 游程解码（需要知道原始尺寸） */
    public static int[][] runLengthDecode(List<int[]> rle, int h, int w) {
        int[][] res = new int[h][w];
        int idx = 0;
        for (int[] pair : rle) {
            for (int k = 0; k < pair[1]; k++) {
                res[idx / w][idx % w] = pair[0];
                idx++;
            }
        }
        return res;
    }

    // ==================== 工具 ====================

    private static int clamp(int v) { return Math.max(0, Math.min(255, v)); }

    private static int getSafe(int[][] img, int r, int c, int def) {
        return (r >= 0 && r < img.length && c >= 0 && c < img[0].length) ? img[r][c] : def;
    }

    private static int[][] deepCopy(int[][] img) {
        int[][] copy = new int[img.length][];
        for (int i = 0; i < img.length; i++) copy[i] = img[i].clone();
        return copy;
    }
}

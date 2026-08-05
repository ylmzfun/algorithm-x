package com.algorithmx.technique.ml;

import java.util.*;

/**
 * AI 经典 — 决策树 (CART) + PCA 降维
 */
public class MLAdvanced {

    // ==================== 决策树（CART 分类树） ====================

    public static class DecisionTree {
        static class Node {
            int feature = -1;
            double threshold;
            int label = -1;          // 叶节点标签
            Node left, right;
            boolean isLeaf() { return left == null && right == null; }
        }

        private Node root;
        private final int maxDepth, minSamples;

        public DecisionTree(int maxDepth, int minSamples) { this.maxDepth = maxDepth; this.minSamples = minSamples; }

        public void fit(double[][] X, int[] y) { root = build(X, y, 0); }

        private Node build(double[][] X, int[] y, int depth) {
            int m = X.length;
            Node node = new Node();
            // 叶节点条件
            if (depth >= maxDepth || m < minSamples || allSame(y)) {
                node.label = majority(y);
                return node;
            }
            // 找最佳分裂
            int bestFeature = -1;
            double bestThresh = 0, bestGini = Double.MAX_VALUE;
            for (int f = 0; f < X[0].length; f++) {
                double[] vals = uniqueSorted(X, f);
                for (int i = 0; i < vals.length - 1; i++) {
                    double thresh = (vals[i] + vals[i + 1]) / 2.0;
                    double gini = giniSplit(X, y, f, thresh);
                    if (gini < bestGini) { bestGini = gini; bestFeature = f; bestThresh = thresh; }
                }
            }
            if (bestFeature == -1) { node.label = majority(y); return node; }

            node.feature = bestFeature;
            node.threshold = bestThresh;
            // 分裂
            List<double[]> leftX = new ArrayList<>(), rightX = new ArrayList<>();
            List<Integer> leftY = new ArrayList<>(), rightY = new ArrayList<>();
            for (int i = 0; i < m; i++) {
                if (X[i][bestFeature] <= bestThresh) { leftX.add(X[i]); leftY.add(y[i]); }
                else { rightX.add(X[i]); rightY.add(y[i]); }
            }
            node.left = build(leftX.toArray(new double[0][]), leftY.stream().mapToInt(v -> v).toArray(), depth + 1);
            node.right = build(rightX.toArray(new double[0][]), rightY.stream().mapToInt(v -> v).toArray(), depth + 1);
            return node;
        }

        public int predict(double[] x) {
            Node cur = root;
            while (!cur.isLeaf()) {
                cur = x[cur.feature] <= cur.threshold ? cur.left : cur.right;
            }
            return cur.label;
        }

        private double giniSplit(double[][] X, int[] y, int f, double t) {
            List<Integer> leftY = new ArrayList<>(), rightY = new ArrayList<>();
            for (int i = 0; i < X.length; i++) {
                if (X[i][f] <= t) leftY.add(y[i]); else rightY.add(y[i]);
            }
            double gL = leftY.isEmpty() ? 0 : gini(leftY) * leftY.size() / X.length;
            double gR = rightY.isEmpty() ? 0 : gini(rightY) * rightY.size() / X.length;
            return gL + gR;
        }

        private double gini(List<Integer> labels) {
            Map<Integer, Integer> cnt = new HashMap<>();
            for (int v : labels) cnt.merge(v, 1, Integer::sum);
            double sum = 0;
            for (int c : cnt.values()) { double p = (double) c / labels.size(); sum += p * p; }
            return 1 - sum;
        }

        private int majority(int[] y) {
            Map<Integer, Integer> cnt = new HashMap<>();
            for (int v : y) cnt.merge(v, 1, Integer::sum);
            return cnt.entrySet().stream().max(Map.Entry.comparingByValue()).get().getKey();
        }

        private boolean allSame(int[] y) { for (int v : y) if (v != y[0]) return false; return true; }

        private double[] uniqueSorted(double[][] X, int f) {
            return Arrays.stream(X).mapToDouble(row -> row[f]).distinct().sorted().toArray();
        }
    }

    // ==================== PCA 降维 ====================

    /** 将数据降到 targetDim 维 */
    public static double[][] pca(double[][] X, int targetDim) {
        int m = X.length, n = X[0].length;
        // 1. 去均值
        double[][] centered = new double[m][n];
        double[] mean = new double[n];
        for (double[] row : X) for (int j = 0; j < n; j++) mean[j] += row[j];
        for (int j = 0; j < n; j++) mean[j] /= m;
        for (int i = 0; i < m; i++) for (int j = 0; j < n; j++) centered[i][j] = X[i][j] - mean[j];

        // 2. 协方差矩阵 C = (1/m) * X^T X
        double[][] cov = new double[n][n];
        for (int i = 0; i < n; i++)
            for (int j = 0; j < n; j++)
                for (int k = 0; k < m; k++)
                    cov[i][j] += centered[k][i] * centered[k][j];

        // 3. 用幂迭代依次求前 targetDim 个特征向量
        double[][] components = new double[targetDim][n];
        for (int k = 0; k < targetDim; k++) {
            double[] v = LinearAlgebra.powerIteration(cov, 100);
            System.arraycopy(v, 0, components[k], 0, n);
            // 收缩：从协方差矩阵中减去已找到的分量
            for (int i = 0; i < n; i++)
                for (int j = 0; j < n; j++)
                    cov[i][j] -= dot(v, v) * v[i] * v[j]; // 近似收缩
        }

        // 4. 投影
        double[][] reduced = new double[m][targetDim];
        for (int i = 0; i < m; i++)
            for (int k = 0; k < targetDim; k++)
                reduced[i][k] = LinearAlgebra.dot(components[k], centered[i]);
        return reduced;
    }

    private static double dot(double[] a, double[] b) {
        double s = 0; for (int i = 0; i < a.length; i++) s += a[i] * b[i]; return s;
    }
}

package com.algorithmx.technique.ml;

import java.util.*;

/**
 * AI/ML — 聚类、KNN、朴素贝叶斯
 */
public class MLClassifiers {

    // ==================== K-Means 聚类 ====================

    public static class KMeans {
        private final int k, maxIter;
        private double[][] centroids;

        public KMeans(int k, int maxIter) { this.k = k; this.maxIter = maxIter; }

        /** @return 每个样本的簇标签 [0..k-1] */
        public int[] fit(double[][] data) {
            int m = data.length, n = data[0].length;
            centroids = new double[k][n];
            // 随机初始化：选前 k 个样本
            for (int i = 0; i < k; i++) centroids[i] = data[i].clone();
            int[] labels = new int[m];

            for (int iter = 0; iter < maxIter; iter++) {
                boolean changed = false;
                // 分配
                for (int i = 0; i < m; i++) {
                    int best = 0;
                    double minDist = Double.MAX_VALUE;
                    for (int j = 0; j < k; j++) {
                        double d = LinearAlgebra.euclidean(data[i], centroids[j]);
                        if (d < minDist) { minDist = d; best = j; }
                    }
                    if (labels[i] != best) { labels[i] = best; changed = true; }
                }
                if (!changed) break;
                // 更新
                double[][] sums = new double[k][n];
                int[] counts = new int[k];
                for (int i = 0; i < m; i++) {
                    for (int j = 0; j < n; j++) sums[labels[i]][j] += data[i][j];
                    counts[labels[i]]++;
                }
                for (int j = 0; j < k; j++)
                    for (int d = 0; d < n; d++)
                        centroids[j][d] = sums[j][d] / Math.max(counts[j], 1);
            }
            return labels;
        }

        public double[][] getCentroids() { return centroids; }
    }

    // ==================== KNN ====================

    /** K 近邻分类 */
    public static class KNN {
        private double[][] trainX;
        private int[] trainY;
        private final int k;

        public KNN(int k) { this.k = k; }

        public void fit(double[][] X, int[] y) { this.trainX = X; this.trainY = y; }

        public int predict(double[] x) {
            int m = trainX.length;
            // 距离 + 标签对，按距离排序取 Top-K
            double[][] dists = new double[m][2];
            for (int i = 0; i < m; i++) {
                dists[i][0] = LinearAlgebra.euclidean(x, trainX[i]);
                dists[i][1] = trainY[i];
            }
            Arrays.sort(dists, Comparator.comparingDouble(a -> a[0]));
            // 投票
            Map<Integer, Integer> votes = new HashMap<>();
            for (int i = 0; i < k; i++) {
                int label = (int) dists[i][1];
                votes.merge(label, 1, Integer::sum);
            }
            return votes.entrySet().stream().max(Map.Entry.comparingByValue()).get().getKey();
        }
    }

    // ==================== 朴素贝叶斯 ====================

    /** 朴素贝叶斯（高斯分布假设，适用于连续特征） */
    public static class NaiveBayes {
        private double[][] means;    // [class][feature]
        private double[][] stds;     // [class][feature]
        private double[] priors;     // [class]
        private int numClasses;

        public void fit(double[][] X, int[] y) {
            int m = X.length, n = X[0].length;
            Set<Integer> classSet = new HashSet<>();
            for (int v : y) classSet.add(v);
            numClasses = classSet.size();
            means = new double[numClasses][n];
            stds = new double[numClasses][n];
            priors = new double[numClasses];
            int[] counts = new int[numClasses];

            // 按类别汇总
            for (int i = 0; i < m; i++) {
                int c = y[i];
                for (int j = 0; j < n; j++) means[c][j] += X[i][j];
                counts[c]++;
            }
            for (int c = 0; c < numClasses; c++) {
                priors[c] = (double) counts[c] / m;
                for (int j = 0; j < n; j++) means[c][j] /= counts[c];
            }
            // 方差
            for (int i = 0; i < m; i++) {
                int c = y[i];
                for (int j = 0; j < n; j++)
                    stds[c][j] += (X[i][j] - means[c][j]) * (X[i][j] - means[c][j]);
            }
            for (int c = 0; c < numClasses; c++)
                for (int j = 0; j < n; j++)
                    stds[c][j] = Math.sqrt(stds[c][j] / counts[c] + 1e-9);
        }

        public int predict(double[] x) {
            double bestLogProb = Double.NEGATIVE_INFINITY;
            int bestClass = 0;
            for (int c = 0; c < numClasses; c++) {
                double logProb = Math.log(priors[c]);
                for (int j = 0; j < x.length; j++)
                    logProb += logGaussian(x[j], means[c][j], stds[c][j]);
                if (logProb > bestLogProb) { bestLogProb = logProb; bestClass = c; }
            }
            return bestClass;
        }

        private double logGaussian(double x, double mean, double std) {
            double z = (x - mean) / std;
            return -0.5 * z * z - Math.log(std) - 0.5 * Math.log(2 * Math.PI);
        }
    }
}

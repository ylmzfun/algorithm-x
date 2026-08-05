package com.algorithmx.technique.ml;

import java.util.Random;

/**
 * AI/ML 经典算法 — 回归与分类
 *
 * 纯 Java 实现，无第三方依赖。
 */
public class MLAlgorithms {

    // ==================== 梯度下降 ====================

    /**
     * 批量梯度下降（BGD）
     * @param X 特征矩阵 [m × n]，每行一个样本
     * @param y 标签 [m]
     * @param lr 学习率
     * @param epochs 迭代次数
     * @return 权重向量 [n]
     */
    public static double[] gradientDescent(double[][] X, double[] y, double lr, int epochs) {
        int m = X.length, n = X[0].length;
        double[] w = new double[n];
        for (int e = 0; e < epochs; e++) {
            double[] grad = new double[n];
            for (int i = 0; i < m; i++) {
                double err = LinearAlgebra.dot(X[i], w) - y[i];
                for (int j = 0; j < n; j++) grad[j] += err * X[i][j];
            }
            for (int j = 0; j < n; j++) w[j] -= lr * grad[j] / m;
        }
        return w;
    }

    /**
     * 随机梯度下降（SGD）
     */
    public static double[] sgd(double[][] X, double[] y, double lr, int epochs) {
        int m = X.length, n = X[0].length;
        double[] w = new double[n];
        Random rand = new Random(42);
        for (int e = 0; e < epochs; e++) {
            for (int i = 0; i < m; i++) {
                int idx = rand.nextInt(m);
                double err = LinearAlgebra.dot(X[idx], w) - y[idx];
                for (int j = 0; j < n; j++) w[j] -= lr * err * X[idx][j];
            }
        }
        return w;
    }

    // ==================== 线性回归 ====================

    /**
     * 最小二乘法（正规方程）：w = (X^T X)^(-1) X^T y
     */
    public static double[] linearRegression(double[][] X, double[] y) {
        double[][] xtx = LinearAlgebra.xTx(X);
        double[] xty = LinearAlgebra.xTy(X, y);
        return LinearAlgebra.solve(xtx, xty);
    }

    /** 预测 */
    public static double predictLinear(double[] w, double[] x) {
        return LinearAlgebra.dot(w, x);
    }

    // ==================== 逻辑回归 ====================

    /** 二分类逻辑回归，使用 SGD 训练。y[i] ∈ {0, 1} */
    public static double[] logisticRegression(double[][] X, int[] y, double lr, int epochs) {
        int m = X.length, n = X[0].length;
        double[] w = new double[n];
        Random rand = new Random(42);
        for (int e = 0; e < epochs; e++) {
            for (int i = 0; i < m; i++) {
                int idx = rand.nextInt(m);
                double z = LinearAlgebra.dot(X[idx], w);
                double p = sigmoid(z);
                double err = p - y[idx];
                for (int j = 0; j < n; j++) w[j] -= lr * err * X[idx][j];
            }
        }
        return w;
    }

    private static double sigmoid(double z) { return 1.0 / (1.0 + Math.exp(-z)); }

    /** 返回预测概率 */
    public static double predictLogistic(double[] w, double[] x) {
        return sigmoid(LinearAlgebra.dot(w, x));
    }

    // ==================== 感知机 ====================

    /** 原始感知机算法，y[i] ∈ {-1, +1} */
    public static double[] perceptron(double[][] X, int[] y, double lr, int epochs) {
        int m = X.length, n = X[0].length;
        double[] w = new double[n];
        for (int e = 0; e < epochs; e++) {
            boolean allCorrect = true;
            for (int i = 0; i < m; i++) {
                if (y[i] * LinearAlgebra.dot(w, X[i]) <= 0) {
                    for (int j = 0; j < n; j++) w[j] += lr * y[i] * X[i][j];
                    allCorrect = false;
                }
            }
            if (allCorrect) break;
        }
        return w;
    }

    public static int predictPerceptron(double[] w, double[] x) {
        return LinearAlgebra.dot(w, x) >= 0 ? 1 : -1;
    }
}

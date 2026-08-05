package com.algorithmx.technique.ml;

/**
 * 线性代数基础工具（纯 Java，无第三方依赖）
 */
public class LinearAlgebra {

    // ==================== 向量 ====================

    public static double dot(double[] a, double[] b) {
        double sum = 0;
        for (int i = 0; i < a.length; i++) sum += a[i] * b[i];
        return sum;
    }

    public static double[] add(double[] a, double[] b) {
        double[] r = new double[a.length];
        for (int i = 0; i < a.length; i++) r[i] = a[i] + b[i];
        return r;
    }

    public static double[] subtract(double[] a, double[] b) {
        double[] r = new double[a.length];
        for (int i = 0; i < a.length; i++) r[i] = a[i] - b[i];
        return r;
    }

    public static double[] scale(double[] v, double s) {
        double[] r = new double[v.length];
        for (int i = 0; i < v.length; i++) r[i] = v[i] * s;
        return r;
    }

    public static double norm(double[] v) {
        return Math.sqrt(dot(v, v));
    }

    public static double[] normalize(double[] v) {
        return scale(v, 1.0 / norm(v));
    }

    public static double mean(double[] v) {
        double sum = 0;
        for (double x : v) sum += x;
        return sum / v.length;
    }

    public static double std(double[] v) {
        double m = mean(v), sum = 0;
        for (double x : v) sum += (x - m) * (x - m);
        return Math.sqrt(sum / v.length);
    }

    // ==================== 矩阵 ====================

    /** 矩阵 × 向量 */
    public static double[] matMul(double[][] mat, double[] vec) {
        int m = mat.length, n = mat[0].length;
        double[] r = new double[m];
        for (int i = 0; i < m; i++)
            for (int j = 0; j < n; j++)
                r[i] += mat[i][j] * vec[j];
        return r;
    }

    /** 转置 */
    public static double[][] transpose(double[][] mat) {
        int m = mat.length, n = mat[0].length;
        double[][] t = new double[n][m];
        for (int i = 0; i < m; i++)
            for (int j = 0; j < n; j++)
                t[j][i] = mat[i][j];
        return t;
    }

    /** X^T × X */
    public static double[][] xTx(double[][] X) {
        int m = X.length, n = X[0].length;
        double[][] r = new double[n][n];
        for (int i = 0; i < n; i++)
            for (int j = 0; j < n; j++)
                for (int k = 0; k < m; k++)
                    r[i][j] += X[k][i] * X[k][j];
        return r;
    }

    /** X^T × y */
    public static double[] xTy(double[][] X, double[] y) {
        int m = X.length, n = X[0].length;
        double[] r = new double[n];
        for (int j = 0; j < n; j++)
            for (int i = 0; i < m; i++)
                r[j] += X[i][j] * y[i];
        return r;
    }

    /** 解线性方程组 (Gauss-Jordan 消元)，小规模适用 */
    public static double[] solve(double[][] A, double[] b) {
        int n = A.length;
        double[][] aug = new double[n][n + 1];
        for (int i = 0; i < n; i++) {
            System.arraycopy(A[i], 0, aug[i], 0, n);
            aug[i][n] = b[i];
        }
        for (int col = 0; col < n; col++) {
            int pivot = col;
            for (int i = col + 1; i < n; i++)
                if (Math.abs(aug[i][col]) > Math.abs(aug[pivot][col])) pivot = i;
            double[] tmp = aug[col]; aug[col] = aug[pivot]; aug[pivot] = tmp;
            double div = aug[col][col];
            for (int j = col; j <= n; j++) aug[col][j] /= div;
            for (int i = 0; i < n; i++) {
                if (i == col) continue;
                double factor = aug[i][col];
                for (int j = col; j <= n; j++) aug[i][j] -= factor * aug[col][j];
            }
        }
        double[] x = new double[n];
        for (int i = 0; i < n; i++) x[i] = aug[i][n];
        return x;
    }

    // ==================== 特征值（幂迭代） ====================

    /** 幂迭代求最大特征值和对应特征向量 */
    public static double[] powerIteration(double[][] A, int maxIter) {
        int n = A.length;
        double[] v = new double[n];
        java.util.Arrays.fill(v, 1.0 / Math.sqrt(n));
        for (int iter = 0; iter < maxIter; iter++) {
            double[] Av = matMul(A, v);
            v = normalize(Av);
        }
        return v;
    }

    // ==================== 距离 ====================

    public static double euclidean(double[] a, double[] b) {
        double sum = 0;
        for (int i = 0; i < a.length; i++) sum += (a[i] - b[i]) * (a[i] - b[i]);
        return Math.sqrt(sum);
    }
}

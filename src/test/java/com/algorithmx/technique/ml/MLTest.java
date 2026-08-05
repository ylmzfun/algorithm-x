package com.algorithmx.technique.ml;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;
import org.junit.jupiter.api.Test;

class MLTest {

    // ==================== 线性代数 ====================
    @Test
    void dot() {
        assertEquals(9, LinearAlgebra.dot(new double[]{1, 2, 3}, new double[]{4, 1, 1}), 0.01);
    }

    @Test
    void solve() {
        // 2x + y = 5, x + 3y = 8 → x=1.4, y=2.2
        double[][] A = {{2, 1}, {1, 3}};
        double[] b = {5, 8};
        double[] x = LinearAlgebra.solve(A, b);
        assertEquals(1.4, x[0], 0.01);
        assertEquals(2.2, x[1], 0.01);
    }

    @Test
    void solve_correct() {
        double[][] A = {{3, 2}, {1, -1}};
        double[] b = {8, 1};
        double[] x = LinearAlgebra.solve(A, b);
        assertEquals(2.0, x[0], 0.01);
        assertEquals(1.0, x[1], 0.01); // 3*2+2*1=8 ✓, 2-1=1 ✓
    }

    // ==================== 线性回归 ====================
    @Test
    void linearRegression() {
        // y = 3*x1 + 2*x2 + 1  （含截距列）
        double[][] X = {
            {1, 1, 0}, {1, 2, 0}, {1, 3, 1}, {1, 0, 2}
        };
        double[] y = {4, 7, 12, 5}; // 3*1+2*0+1=4, 3*2+0+1=7, 3*3+2*1+1=12, 3*0+2*2+1=5
        double[] w = MLAlgorithms.linearRegression(X, y);
        assertEquals(1.0, w[0], 0.01);  // intercept
        assertEquals(3.0, w[1], 0.01);  // x1 coeff
        assertEquals(2.0, w[2], 0.01);  // x2 coeff
    }

    @Test
    void gradientDescent() {
        double[][] X = {{1, 1}, {1, 2}, {1, 3}};
        double[] y = {3, 5, 7}; // y = 2*x + 1
        double[] w = MLAlgorithms.gradientDescent(X, y, 0.01, 5000);
        assertEquals(1.0, w[0], 0.1);
        assertEquals(2.0, w[1], 0.1);
    }

    // ==================== 逻辑回归 ====================
    @Test
    void logisticRegression() {
        double[][] X = {{1, 1}, {1, 2}, {1, 3}, {1, 4}, {1, 5}};
        int[] y = {0, 0, 1, 1, 1}; // 线性可分
        double[] w = MLAlgorithms.logisticRegression(X, y, 0.1, 2000);
        double p1 = MLAlgorithms.predictLogistic(w, new double[]{1, 1});
        double p5 = MLAlgorithms.predictLogistic(w, new double[]{1, 5});
        assertTrue(p1 < 0.5, "p1=" + p1);
        assertTrue(p5 > 0.5, "p5=" + p5);
    }

    // ==================== KNN ====================
    @Test
    void knn() {
        double[][] X = {{0, 0}, {1, 0}, {0, 1}, {5, 5}, {6, 5}, {5, 6}};
        int[] y = {0, 0, 0, 1, 1, 1};
        MLClassifiers.KNN knn = new MLClassifiers.KNN(3);
        knn.fit(X, y);
        assertEquals(0, knn.predict(new double[]{1, 1}));
        assertEquals(1, knn.predict(new double[]{5, 5}));
    }

    // ==================== K-Means ====================
    @Test
    void kmeans() {
        double[][] data = {{0, 0}, {0.5, 0}, {0, 0.5}, {5, 5}, {5.5, 5}, {5, 5.5}};
        MLClassifiers.KMeans km = new MLClassifiers.KMeans(2, 100);
        int[] labels = km.fit(data);
        assertEquals(labels[0], labels[1]);
        assertEquals(labels[0], labels[2]);
        assertEquals(labels[3], labels[4]);
        assertEquals(labels[3], labels[5]);
        assertNotEquals(labels[0], labels[3]);
    }

    // ==================== 朴素贝叶斯 ====================
    @Test
    void naiveBayes() {
        double[][] X = {{1, 0}, {2, 0}, {1, 1}, {8, 8}, {9, 9}, {8, 9}};
        int[] y = {0, 0, 0, 1, 1, 1};
        MLClassifiers.NaiveBayes nb = new MLClassifiers.NaiveBayes();
        nb.fit(X, y);
        assertEquals(0, nb.predict(new double[]{2, 1}));
        assertEquals(1, nb.predict(new double[]{8, 8}));
    }

    // ==================== 决策树 ====================
    @Test
    void decisionTree() {
        double[][] X = {{1, 1}, {2, 2}, {1, 2}, {9, 9}, {8, 8}, {9, 8}};
        int[] y = {0, 0, 0, 1, 1, 1};
        MLAdvanced.DecisionTree dt = new MLAdvanced.DecisionTree(3, 1);
        dt.fit(X, y);
        assertEquals(0, dt.predict(new double[]{2, 2}));
        assertEquals(1, dt.predict(new double[]{8, 8}));
    }

    // ==================== 感知机 ====================
    @Test
    void perceptron() {
        double[][] X = {{1, 1}, {1, 2}, {1, 3}, {1, 4}, {1, 5}}; // bias + feature
        int[] y = {-1, -1, 1, 1, 1};
        double[] w = MLAlgorithms.perceptron(X, y, 0.1, 100);
        assertEquals(-1, MLAlgorithms.predictPerceptron(w, new double[]{1, 1}));
        assertEquals(1, MLAlgorithms.predictPerceptron(w, new double[]{1, 5}));
    }
}

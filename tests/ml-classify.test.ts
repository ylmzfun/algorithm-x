import { describe, it, expect } from 'vitest';
import { KNN, KMeans } from '../src/algorithms/ml/classification';
import { DecisionTreeClassifier, GaussianNaiveBayes } from '../src/algorithms/ml/tree-bayes';
import { NeuralNetwork } from '../src/algorithms/ml/neural-network';

describe('KNN', () => {
  it('classifies based on neighbors', () => {
    const knn = new KNN(3);
    const X = [[1, 1], [2, 2], [3, 3], [8, 8], [9, 9], [10, 10]];
    const y = [0, 0, 0, 1, 1, 1];
    knn.fit(X, y);
    expect(knn.predict([2, 2])).toBe(0);
    expect(knn.predict([9, 9])).toBe(1);
  });
});

describe('KMeans', () => {
  it('clusters into groups', () => {
    const km = new KMeans(2);
    const X = [[1, 2], [1, 3], [2, 2], [8, 9], [8, 8], [9, 9]];
    const labels = km.fit(X);
    expect(labels[0]).toBe(labels[1]);
    expect(labels[3]).toBe(labels[4]);
    expect(labels[0]).not.toBe(labels[3]);
  });

  it('predict assigns to nearest centroid', () => {
    const km = new KMeans(2);
    const X = [[0, 0], [10, 10]];
    km.fit(X);
    expect(km.predict([0, 1])).toBe(km.predict([1, 0]));
    expect(km.predict([9, 10])).toBe(km.predict([10, 9]));
    expect(km.predict([0, 1])).not.toBe(km.predict([9, 9]));
  });
});

describe('DecisionTreeClassifier', () => {
  it('fits and predicts', () => {
    const dt = new DecisionTreeClassifier(3);
    const X = [[1], [2], [3], [7], [8], [9]];
    const y = [0, 0, 0, 1, 1, 1];
    dt.fit(X, y);
    expect(dt.predict([2])).toBe(0);
    expect(dt.predict([8])).toBe(1);
  });
});

describe('GaussianNaiveBayes', () => {
  it('classifies based on probabilities', () => {
    const nb = new GaussianNaiveBayes();
    const X = [[1], [2], [3], [7], [8], [9]];
    const y = [0, 0, 0, 1, 1, 1];
    nb.fit(X, y);
    expect(nb.predict([2])).toBe(0);
    expect(nb.predict([8])).toBe(1);
  });
});

describe('NeuralNetwork', () => {
  it('learns XOR', () => {
    const nn = new NeuralNetwork([2, 4, 1]);
    const X = [[0, 0], [0, 1], [1, 0], [1, 1]];
    const y = [[0], [1], [1], [0]];
    nn.fit(X, y, 5000, 0.5);
    const p00 = nn.predict([0, 0])[0];
    const p11 = nn.predict([1, 1])[0];
    const p01 = nn.predict([0, 1])[0];
    const p10 = nn.predict([1, 0])[0];
    expect(p00).toBeLessThan(0.5);
    expect(p11).toBeLessThan(0.5);
    expect(p01).toBeGreaterThan(0.5);
    expect(p10).toBeGreaterThan(0.5);
  });
});

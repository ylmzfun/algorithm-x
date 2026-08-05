import { describe, it, expect } from 'vitest';
import { LinearRegression, LogisticRegression } from '../src/algorithms/ml/regression';

describe('LinearRegression', () => {
  it('fits a simple linear relationship', () => {
    const model = new LinearRegression();
    // y = 2 * x0 + 3 * x1
    const X = [[1, 2], [2, 4], [3, 6], [4, 8]];
    const y = [8, 16, 24, 32]; // 2*x0 + 3*x1 = 2*1+3*2=8, 2*2+3*4=16 ... 
    model.fit(X, y);
    const pred = model.predict([5, 10]); // expect ~35
    expect(pred).toBeCloseTo(35, -1); // 1 decimal place
  });
});

describe('LogisticRegression', () => {
  it('classifies linearly separable data', () => {
    const model = new LogisticRegression();
    // x > 5 => 1, else 0
    const X = [[2], [3], [4], [6], [7], [8]];
    const y = [0, 0, 0, 1, 1, 1];
    model.fit(X, y, 0.1, 5000);
    expect(model.predict([3])).toBe(0);
    expect(model.predict([7])).toBe(1);
  });
});

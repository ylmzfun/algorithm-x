// 向量工具
export function dot(a: number[], b: number[]): number {
  let sum = 0;
  for (let i = 0; i < a.length; i++) sum += a[i] * b[i];
  return sum;
}

// 线性回归（最小二乘法解析解）—— y = w · x + b
export class LinearRegression {
  private weights: number[] = [];
  private bias = 0;

  fit(X: number[][], y: number[]): void {
    const n = X.length;
    const d = X[0].length;
    // 正规方程: (X^T X + I λ)^(-1) X^T y
    // 使用梯度下降以简化实现
    this.weights = new Array(d).fill(0);
    this.bias = 0;
    const lr = 0.001;
    const epochs = 5000;

    for (let e = 0; e < epochs; e++) {
      let gradW = new Array(d).fill(0);
      let gradB = 0;
      for (let i = 0; i < n; i++) {
        const pred = dot(this.weights, X[i]) + this.bias;
        const err = pred - y[i];
        for (let j = 0; j < d; j++) gradW[j] += err * X[i][j];
        gradB += err;
      }
      for (let j = 0; j < d; j++) this.weights[j] -= (lr * gradW[j]) / n;
      this.bias -= (lr * gradB) / n;
    }
  }

  predict(x: number[]): number {
    return dot(this.weights, x) + this.bias;
  }
}

// 逻辑回归（二分类，梯度下降）
export class LogisticRegression {
  private weights: number[] = [];
  private bias = 0;

  fit(X: number[][], y: number[], lr = 0.01, epochs = 3000): void {
    const n = X.length;
    const d = X[0].length;
    this.weights = new Array(d).fill(0);
    this.bias = 0;

    for (let e = 0; e < epochs; e++) {
      let gradW = new Array(d).fill(0);
      let gradB = 0;
      for (let i = 0; i < n; i++) {
        const z = sigmoid(dot(this.weights, X[i]) + this.bias);
        const err = z - y[i];
        for (let j = 0; j < d; j++) gradW[j] += err * X[i][j];
        gradB += err;
      }
      for (let j = 0; j < d; j++) this.weights[j] -= (lr * gradW[j]) / n;
      this.bias -= (lr * gradB) / n;
    }
  }

  predictProb(x: number[]): number {
    return sigmoid(dot(this.weights, x) + this.bias);
  }

  predict(x: number[]): number {
    return this.predictProb(x) >= 0.5 ? 1 : 0;
  }
}

export function sigmoid(z: number): number {
  return 1 / (1 + Math.exp(-z));
}

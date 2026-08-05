import { sigmoid } from './regression';

// 简单的全连接神经网络
export class NeuralNetwork {
  private layers: number[];
  private weights: number[][][] = []; // [layer][from][to]
  private biases: number[][] = [];

  constructor(layers: number[]) {
    this.layers = layers;
    for (let l = 1; l < layers.length; l++) {
      const w: number[][] = [];
      for (let i = 0; i < layers[l - 1]; i++) {
        const row: number[] = [];
        for (let j = 0; j < layers[l]; j++) {
          row.push((Math.random() - 0.5) * 0.3);
        }
        w.push(row);
      }
      this.weights.push(w);
      this.biases.push(new Array(layers[l]).fill(0));
    }
  }

  forward(input: number[]): number[] {
    let activations = input;
    for (let l = 0; l < this.weights.length; l++) {
      const next: number[] = new Array(this.layers[l + 1]).fill(0);
      for (let j = 0; j < this.layers[l + 1]; j++) {
        let sum = this.biases[l][j];
        for (let i = 0; i < activations.length; i++) {
          sum += activations[i] * this.weights[l][i][j];
        }
        next[j] = sigmoid(sum);
      }
      activations = next;
    }
    return activations;
  }

  // 反向传播（一个样本）
  train(input: number[], target: number[], lr = 0.1): void {
    // Forward pass with caches
    const activations: number[][] = [input];
    const zs: number[][] = [];

    for (let l = 0; l < this.weights.length; l++) {
      const z: number[] = new Array(this.layers[l + 1]).fill(0);
      for (let j = 0; j < this.layers[l + 1]; j++) {
        z[j] = this.biases[l][j];
        for (let i = 0; i < activations[l].length; i++) {
          z[j] += activations[l][i] * this.weights[l][i][j];
        }
      }
      zs.push(z);
      activations.push(z.map(sigmoid));
    }

    // Backward pass
    const L = this.weights.length;
    const deltas: number[][] = new Array(L);

    // 输出层 delta
    deltas[L - 1] = activations[L].map(
      (a, j) => (a - target[j]) * a * (1 - a),
    );

    // 隐藏层 delta
    for (let l = L - 2; l >= 0; l--) {
      deltas[l] = new Array(this.layers[l + 1]).fill(0);
      for (let i = 0; i < this.layers[l + 1]; i++) {
        let err = 0;
        for (let j = 0; j < this.layers[l + 2]; j++) {
          err += deltas[l + 1][j] * this.weights[l + 1][i][j];
        }
        const a = activations[l + 1][i];
        deltas[l][i] = err * a * (1 - a);
      }
    }

    // 更新参数
    for (let l = 0; l < L; l++) {
      for (let i = 0; i < this.layers[l]; i++) {
        for (let j = 0; j < this.layers[l + 1]; j++) {
          this.weights[l][i][j] -= lr * activations[l][i] * deltas[l][j];
        }
      }
      for (let j = 0; j < this.layers[l + 1]; j++) {
        this.biases[l][j] -= lr * deltas[l][j];
      }
    }
  }

  // 批量训练
  fit(X: number[][], y: number[][], epochs = 1000, lr = 0.1): void {
    for (let e = 0; e < epochs; e++) {
      for (let i = 0; i < X.length; i++) {
        this.train(X[i], y[i], lr);
      }
    }
  }

  predict(input: number[]): number[] {
    return this.forward(input);
  }
}

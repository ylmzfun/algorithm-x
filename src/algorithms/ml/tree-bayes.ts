// 决策树节点
interface DTNode {
  feature?: number;
  threshold?: number;
  left?: DTNode;
  right?: DTNode;
  label?: number; // 叶节点
}

// ID3/C4.5 决策树（仅连续特征，使用信息增益）
export class DecisionTreeClassifier {
  private root: DTNode | null = null;
  private maxDepth: number;

  constructor(maxDepth = 5) {
    this.maxDepth = maxDepth;
  }

  fit(X: number[][], y: number[]): void {
    const features = Array.from({ length: X[0].length }, (_, i) => i);
    this.root = this._build(X, y, features, 0);
  }

  predict(x: number[]): number {
    return this._predictNode(this.root!, x);
  }

  private _predictNode(node: DTNode, x: number[]): number {
    if (node.label !== undefined) return node.label;
    if (x[node.feature!] <= node.threshold!) {
      return this._predictNode(node.left!, x);
    }
    return this._predictNode(node.right!, x);
  }

  private _build(X: number[][], y: number[], features: number[], depth: number): DTNode {
    // 所有标签相同
    if (new Set(y).size === 1) return { label: y[0] };
    // 达到最大深度
    if (depth >= this.maxDepth) return { label: this._majority(y) };

    // 选择最优分裂点
    let bestGain = -Infinity;
    let bestFeature = -1;
    let bestThreshold = 0;
    let bestLeftX: number[][] = [];
    let bestLeftY: number[] = [];
    let bestRightX: number[][] = [];
    let bestRightY: number[] = [];

    for (const f of features) {
      const values = X.map((row) => row[f]).sort((a, b) => a - b);
      for (let i = 0; i < values.length - 1; i++) {
        const threshold = (values[i] + values[i + 1]) / 2;
        const { leftX, leftY, rightX, rightY } = this._split(X, y, f, threshold);
        if (leftX.length === 0 || rightX.length === 0) continue;
        const gain = this._infoGain(y, leftY, rightY);
        if (gain > bestGain) {
          bestGain = gain;
          bestFeature = f;
          bestThreshold = threshold;
          bestLeftX = leftX;
          bestLeftY = leftY;
          bestRightX = rightX;
          bestRightY = rightY;
        }
      }
    }

    if (bestFeature === -1) return { label: this._majority(y) };

    return {
      feature: bestFeature,
      threshold: bestThreshold,
      left: this._build(bestLeftX, bestLeftY, features, depth + 1),
      right: this._build(bestRightX, bestRightY, features, depth + 1),
    };
  }

  private _split(X: number[][], y: number[], f: number, t: number) {
    const leftX: number[][] = [], leftY: number[] = [];
    const rightX: number[][] = [], rightY: number[] = [];
    for (let i = 0; i < X.length; i++) {
      if (X[i][f] <= t) {
        leftX.push(X[i]);
        leftY.push(y[i]);
      } else {
        rightX.push(X[i]);
        rightY.push(y[i]);
      }
    }
    return { leftX, leftY, rightX, rightY };
  }

  private _entropy(y: number[]): number {
    const counts = new Map<number, number>();
    for (const lbl of y) counts.set(lbl, (counts.get(lbl) ?? 0) + 1);
    let e = 0;
    for (const cnt of counts.values()) {
      const p = cnt / y.length;
      e -= p * Math.log2(p);
    }
    return e;
  }

  private _infoGain(parent: number[], left: number[], right: number[]): number {
    const n = parent.length;
    return (
      this._entropy(parent) -
      (left.length / n) * this._entropy(left) -
      (right.length / n) * this._entropy(right)
    );
  }

  private _majority(y: number[]): number {
    const cnt = new Map<number, number>();
    for (const lbl of y) cnt.set(lbl, (cnt.get(lbl) ?? 0) + 1);
    let best = y[0], max = 0;
    for (const [l, c] of cnt) if (c > max) { max = c; best = l; }
    return best;
  }
}

// 朴素贝叶斯（高斯分布）
export class GaussianNaiveBayes {
  private means: number[][] = [];
  private vars: number[][] = [];
  private priors: number[] = [];
  private classes: number[] = [];

  fit(X: number[][], y: number[]): void {
    this.classes = [...new Set(y)].sort();
    const d = X[0].length;

    for (const c of this.classes) {
      const cX = X.filter((_, i) => y[i] === c);
      const mean = new Array(d).fill(0);
      const vars = new Array(d).fill(0);
      for (const row of cX) for (let j = 0; j < d; j++) mean[j] += row[j];
      for (let j = 0; j < d; j++) mean[j] /= cX.length;
      for (const row of cX) for (let j = 0; j < d; j++) vars[j] += (row[j] - mean[j]) ** 2;
      for (let j = 0; j < d; j++) vars[j] = Math.max(vars[j] / cX.length, 1e-9);
      this.means.push(mean);
      this.vars.push(vars);
      this.priors.push(cX.length / X.length);
    }
  }

  predict(x: number[]): number {
    let bestClass = this.classes[0];
    let bestScore = -Infinity;
    for (let i = 0; i < this.classes.length; i++) {
      let score = Math.log(this.priors[i]);
      for (let j = 0; j < x.length; j++) {
        const mu = this.means[i][j];
        const v = this.vars[i][j];
        score += -0.5 * Math.log(2 * Math.PI * v) - (x[j] - mu) ** 2 / (2 * v);
      }
      if (score > bestScore) {
        bestScore = score;
        bestClass = this.classes[i];
      }
    }
    return bestClass;
  }
}

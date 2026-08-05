// K 近邻（分类）
export class KNN {
  private X: number[][] = [];
  private y: number[] = [];
  private k: number;

  constructor(k = 3) {
    this.k = k;
  }

  fit(X: number[][], y: number[]): void {
    this.X = X.map((row) => [...row]);
    this.y = [...y];
  }

  predict(x: number[]): number {
    const distances = this.X.map((xi, i) => ({
      dist: euclidean(xi, x),
      label: this.y[i],
    }));
    distances.sort((a, b) => a.dist - b.dist);

    // 多数投票
    const votes = new Map<number, number>();
    for (let i = 0; i < this.k && i < distances.length; i++) {
      const lbl = distances[i].label;
      votes.set(lbl, (votes.get(lbl) ?? 0) + 1);
    }
    let bestLabel = distances[0].label;
    let bestCount = 0;
    for (const [lbl, cnt] of votes) {
      if (cnt > bestCount) {
        bestCount = cnt;
        bestLabel = lbl;
      }
    }
    return bestLabel;
  }
}

// 距离度量
export function euclidean(a: number[], b: number[]): number {
  let sum = 0;
  for (let i = 0; i < a.length; i++) sum += (a[i] - b[i]) ** 2;
  return Math.sqrt(sum);
}

export function manhattan(a: number[], b: number[]): number {
  let sum = 0;
  for (let i = 0; i < a.length; i++) sum += Math.abs(a[i] - b[i]);
  return sum;
}

// K-Means 聚类
export class KMeans {
  private centroids: number[][] = [];
  private k: number;

  constructor(k: number) {
    this.k = k;
  }

  fit(X: number[][], maxIter = 100): number[] {
    const n = X.length;
    const d = X[0].length;

    // 随机初始化质心
    this.centroids = [];
    const used = new Set<number>();
    while (this.centroids.length < this.k) {
      const idx = Math.floor(Math.random() * n);
      if (!used.has(idx)) {
        used.add(idx);
        this.centroids.push([...X[idx]]);
      }
    }

    let labels = new Array(n).fill(0);

    for (let iter = 0; iter < maxIter; iter++) {
      // 分配簇
      let changed = false;
      for (let i = 0; i < n; i++) {
        let minDist = Infinity;
        let bestC = 0;
        for (let c = 0; c < this.k; c++) {
          const dist = euclidean(X[i], this.centroids[c]);
          if (dist < minDist) {
            minDist = dist;
            bestC = c;
          }
        }
        if (labels[i] !== bestC) changed = true;
        labels[i] = bestC;
      }
      if (!changed) break;

      // 更新质心
      const sums = Array.from({ length: this.k }, () => new Array(d).fill(0));
      const counts = new Array(this.k).fill(0);
      for (let i = 0; i < n; i++) {
        const c = labels[i];
        counts[c]++;
        for (let j = 0; j < d; j++) sums[c][j] += X[i][j];
      }
      for (let c = 0; c < this.k; c++) {
        for (let j = 0; j < d; j++) {
          this.centroids[c][j] = counts[c] > 0 ? sums[c][j] / counts[c] : this.centroids[c][j];
        }
      }
    }

    return labels;
  }

  predict(x: number[]): number {
    let minDist = Infinity;
    let bestC = 0;
    for (let c = 0; c < this.k; c++) {
      const dist = euclidean(x, this.centroids[c]);
      if (dist < minDist) {
        minDist = dist;
        bestC = c;
      }
    }
    return bestC;
  }
}

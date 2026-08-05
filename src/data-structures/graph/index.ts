export class Graph {
  private adj: Map<number, number[]> = new Map();
  private directed: boolean;

  constructor(directed = false) {
    this.directed = directed;
  }

  addVertex(v: number): void {
    if (!this.adj.has(v)) this.adj.set(v, []);
  }

  addEdge(u: number, v: number): void {
    this.addVertex(u);
    this.addVertex(v);
    this.adj.get(u)!.push(v);
    if (!this.directed) this.adj.get(v)!.push(u);
  }

  getVertices(): number[] {
    return [...this.adj.keys()];
  }

  getEdges(): [number, number][] {
    const edges: [number, number][] = [];
    const seen = new Set<string>();
    for (const [u, neighbors] of this.adj) {
      for (const v of neighbors) {
        if (this.directed || !seen.has(`${Math.min(u, v)}-${Math.max(u, v)}`)) {
          edges.push([u, v]);
          seen.add(`${u}-${v}`);
        }
      }
    }
    return edges;
  }

  getNeighbors(v: number): number[] {
    return [...(this.adj.get(v) ?? [])];
  }

  get vertexCount(): number {
    return this.adj.size;
  }

  get edgeCount(): number {
    return this.getEdges().length;
  }
}

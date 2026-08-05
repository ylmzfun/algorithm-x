// 活动选择 —— 返回最多不相交活动的下标
export function activitySelection(start: number[], finish: number[]): number[] {
  const n = start.length;
  const acts = Array.from({ length: n }, (_, i) => ({ s: start[i], f: finish[i], idx: i }));
  acts.sort((a, b) => a.f - b.f);

  const selected = [acts[0].idx];
  let lastFinish = acts[0].f;
  for (let i = 1; i < n; i++) {
    if (acts[i].s >= lastFinish) {
      selected.push(acts[i].idx);
      lastFinish = acts[i].f;
    }
  }
  return selected;
}

// Huffman 编码 —— 返回字符到编码的映射
export function huffmanEncode(freq: Map<string, number>): Map<string, string> {
  if (freq.size === 0) return new Map();

  interface HuffNode {
    ch?: string;
    freq: number;
    left?: HuffNode;
    right?: HuffNode;
  }

  const heap: HuffNode[] = [];
  for (const [ch, f] of freq) heap.push({ ch, freq: f });
  heap.sort((a, b) => b.freq - a.freq); // max heap by freq

  while (heap.length > 1) {
    const a = heap.pop()!;
    const b = heap.pop()!;
    const merged: HuffNode = { freq: a.freq + b.freq, left: a, right: b };
    // 插入并保持有序
    let i = heap.length - 1;
    while (i >= 0 && heap[i].freq < merged.freq) i--;
    heap.splice(i + 1, 0, merged);
  }

  const codes = new Map<string, string>();
  function dfs(node: HuffNode, code: string) {
    if (node.ch !== undefined) {
      codes.set(node.ch, code);
    } else {
      if (node.left) dfs(node.left, code + '0');
      if (node.right) dfs(node.right, code + '1');
    }
  }

  dfs(heap[0], '');
  return codes;
}

// 跳跃游戏 —— 能否从 0 跳到末尾
export function canJump(nums: number[]): boolean {
  let reach = 0;
  for (let i = 0; i < nums.length; i++) {
    if (i > reach) return false;
    reach = Math.max(reach, i + nums[i]);
    if (reach >= nums.length - 1) return true;
  }
  return false;
}

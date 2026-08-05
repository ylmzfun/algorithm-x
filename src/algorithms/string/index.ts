// KMP 字符串匹配 —— 返回所有匹配位置
export function kmpSearch(text: string, pattern: string): number[] {
  if (pattern.length === 0) return [];

  const lps = buildLPS(pattern);
  const result: number[] = [];
  let i = 0; // text index
  let j = 0; // pattern index

  while (i < text.length) {
    if (text[i] === pattern[j]) {
      i++;
      j++;
    }
    if (j === pattern.length) {
      result.push(i - j);
      j = lps[j - 1];
    } else if (i < text.length && text[i] !== pattern[j]) {
      if (j > 0) j = lps[j - 1];
      else i++;
    }
  }
  return result;
}

// Longest Proper Prefix which is also Suffix
function buildLPS(pattern: string): number[] {
  const lps = new Array(pattern.length).fill(0);
  let len = 0;
  let i = 1;
  while (i < pattern.length) {
    if (pattern[i] === pattern[len]) {
      lps[i++] = ++len;
    } else if (len > 0) {
      len = lps[len - 1];
    } else {
      lps[i++] = 0;
    }
  }
  return lps;
}

// Rabin-Karp 字符串匹配
export function rabinKarp(text: string, pattern: string): number[] {
  const result: number[] = [];
  const n = text.length;
  const m = pattern.length;
  if (m === 0 || m > n) return result;

  const base = 256;
  const mod = 101; // 质数

  let patternHash = 0;
  let textHash = 0;
  let h = 1; // base^(m-1) % mod

  for (let i = 0; i < m - 1; i++) h = (h * base) % mod;
  for (let i = 0; i < m; i++) {
    patternHash = (base * patternHash + pattern.charCodeAt(i)) % mod;
    textHash = (base * textHash + text.charCodeAt(i)) % mod;
  }

  for (let i = 0; i <= n - m; i++) {
    if (patternHash === textHash) {
      if (text.slice(i, i + m) === pattern) result.push(i);
    }
    if (i < n - m) {
      textHash = (base * (textHash - text.charCodeAt(i) * h) + text.charCodeAt(i + m)) % mod;
      if (textHash < 0) textHash += mod;
    }
  }
  return result;
}

// 最长回文子串（中心扩展法）
export function longestPalindrome(s: string): string {
  if (s.length === 0) return '';
  let start = 0, maxLen = 1;

  function expand(l: number, r: number) {
    while (l >= 0 && r < s.length && s[l] === s[r]) {
      l--;
      r++;
    }
    return r - l - 1;
  }

  for (let i = 0; i < s.length; i++) {
    const len1 = expand(i, i);
    const len2 = expand(i, i + 1);
    const len = Math.max(len1, len2);
    if (len > maxLen) {
      start = i - Math.floor((len - 1) / 2);
      maxLen = len;
    }
  }
  return s.slice(start, start + maxLen);
}

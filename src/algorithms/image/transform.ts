import { createImage } from './convolution';
import type { GrayImage } from './convolution';

// 最近邻缩放
export function resizeNearest(img: GrayImage, newH: number, newW: number): GrayImage {
  const h = img.length;
  const w = img[0].length;
  const result = createImage(newH, newW);
  for (let r = 0; r < newH; r++) {
    for (let c = 0; c < newW; c++) {
      const sr = Math.floor((r / newH) * h);
      const sc = Math.floor((c / newW) * w);
      result[r][c] = img[Math.min(sr, h - 1)][Math.min(sc, w - 1)];
    }
  }
  return result;
}

// 双线性插值缩放
export function resizeBilinear(img: GrayImage, newH: number, newW: number): GrayImage {
  const h = img.length;
  const w = img[0].length;
  const result = createImage(newH, newW);
  for (let r = 0; r < newH; r++) {
    for (let c = 0; c < newW; c++) {
      const sr = (r / newH) * (h - 1);
      const sc = (c / newW) * (w - 1);
      const r0 = Math.floor(sr);
      const c0 = Math.floor(sc);
      const r1 = Math.min(r0 + 1, h - 1);
      const c1 = Math.min(c0 + 1, w - 1);
      const dr = sr - r0;
      const dc = sc - c0;
      result[r][c] = Math.round(
        img[r0][c0] * (1 - dr) * (1 - dc) +
        img[r0][c1] * (1 - dr) * dc +
        img[r1][c0] * dr * (1 - dc) +
        img[r1][c1] * dr * dc,
      );
    }
  }
  return result;
}

// 旋转 90° 的倍数
export function rotate90(img: GrayImage, times = 1): GrayImage {
  times = ((times % 4) + 4) % 4;
  let result = img;
  for (let t = 0; t < times; t++) {
    const h = result.length;
    const w = result[0].length;
    const rotated = createImage(w, h);
    for (let r = 0; r < h; r++) {
      for (let c = 0; c < w; c++) {
        rotated[c][h - 1 - r] = result[r][c];
      }
    }
    result = rotated;
  }
  return result;
}

// 水平翻转
export function flipHorizontal(img: GrayImage): GrayImage {
  return img.map((row) => [...row].reverse());
}

// 垂直翻转
export function flipVertical(img: GrayImage): GrayImage {
  return [...img].reverse();
}

// 平移（空区域填 0）
export function translate(img: GrayImage, dx: number, dy: number): GrayImage {
  const h = img.length;
  const w = img[0].length;
  const result = createImage(h, w);
  for (let r = 0; r < h; r++) {
    for (let c = 0; c < w; c++) {
      const sr = r - dy;
      const sc = c - dx;
      if (sr >= 0 && sr < h && sc >= 0 && sc < w) {
        result[r][c] = img[sr][sc];
      }
    }
  }
  return result;
}

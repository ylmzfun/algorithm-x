import { createImage } from './convolution';
import type { GrayImage } from './convolution';

// 计算直方图
export function histogram(img: GrayImage): number[] {
  const hist = new Array(256).fill(0);
  for (const row of img) {
    for (const pix of row) {
      hist[pix]++;
    }
  }
  return hist;
}

// 直方图均衡化
export function equalizeHistogram(img: GrayImage): GrayImage {
  const hist = histogram(img);
  const n = img.length * img[0].length;
  const cdf = new Array(256).fill(0);
  let acc = 0;
  for (let i = 0; i < 256; i++) {
    acc += hist[i];
    cdf[i] = Math.round((acc / n) * 255);
  }
  const result = createImage(img.length, img[0].length);
  for (let r = 0; r < img.length; r++) {
    for (let c = 0; c < img[0].length; c++) {
      result[r][c] = cdf[img[r][c]];
    }
  }
  return result;
}

// 二值化（阈值处理）
export function threshold(img: GrayImage, t: number): GrayImage {
  const result = createImage(img.length, img[0].length);
  for (let r = 0; r < img.length; r++) {
    for (let c = 0; c < img[0].length; c++) {
      result[r][c] = img[r][c] > t ? 255 : 0;
    }
  }
  return result;
}

// Otsu 自动阈值
export function otsuThreshold(img: GrayImage): number {
  const hist = histogram(img);
  const n = img.length * img[0].length;
  let bestT = 0;
  let maxVariance = 0;
  let sumAll = 0;
  for (let i = 0; i < 256; i++) sumAll += i * hist[i];

  let sumB = 0;
  let wB = 0;

  for (let t = 0; t < 256; t++) {
    wB += hist[t];
    if (wB === 0) continue;
    const wF = n - wB;
    if (wF === 0) break;
    sumB += t * hist[t];
    const mB = sumB / wB;
    const mF = (sumAll - sumB) / wF;
    const variance = wB * wF * (mB - mF) ** 2;
    if (variance > maxVariance) {
      maxVariance = variance;
      bestT = t;
    }
  }
  return bestT;
}

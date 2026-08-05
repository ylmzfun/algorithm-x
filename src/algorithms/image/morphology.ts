import type { GrayImage } from './convolution';
import { cloneImage } from './convolution';

// 膨胀
export function dilate(img: GrayImage, kernelSize = 3): GrayImage {
  const h = img.length;
  const w = img[0].length;
  const pad = Math.floor(kernelSize / 2);
  const result = cloneImage(img);

  for (let r = 0; r < h; r++) {
    for (let c = 0; c < w; c++) {
      let maxVal = 0;
      for (let dr = -pad; dr <= pad; dr++) {
        for (let dc = -pad; dc <= pad; dc++) {
          const rr = r + dr;
          const cc = c + dc;
          if (rr >= 0 && rr < h && cc >= 0 && cc < w) {
            maxVal = Math.max(maxVal, img[rr][cc]);
          }
        }
      }
      result[r][c] = maxVal;
    }
  }
  return result;
}

// 腐蚀
export function erode(img: GrayImage, kernelSize = 3): GrayImage {
  const h = img.length;
  const w = img[0].length;
  const pad = Math.floor(kernelSize / 2);
  const result = cloneImage(img);

  for (let r = 0; r < h; r++) {
    for (let c = 0; c < w; c++) {
      let minVal = 255;
      for (let dr = -pad; dr <= pad; dr++) {
        for (let dc = -pad; dc <= pad; dc++) {
          const rr = r + dr;
          const cc = c + dc;
          if (rr >= 0 && rr < h && cc >= 0 && cc < w) {
            minVal = Math.min(minVal, img[rr][cc]);
          }
        }
      }
      result[r][c] = minVal;
    }
  }
  return result;
}

// 开运算 = 先腐蚀后膨胀
export function open(img: GrayImage, kernelSize = 3): GrayImage {
  return dilate(erode(img, kernelSize), kernelSize);
}

// 闭运算 = 先膨胀后腐蚀
export function close(img: GrayImage, kernelSize = 3): GrayImage {
  return erode(dilate(img, kernelSize), kernelSize);
}

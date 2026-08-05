// 灰度图 = 2D 像素数组，值范围 [0, 255]
export type GrayImage = number[][];

export function createImage(h: number, w: number, fill = 0): GrayImage {
  return Array.from({ length: h }, () => new Array(w).fill(fill));
}

export function cloneImage(img: GrayImage): GrayImage {
  return img.map((row) => [...row]);
}

// 常用卷积核
export const KERNELS = {
  blur3: [
    [1 / 9, 1 / 9, 1 / 9],
    [1 / 9, 1 / 9, 1 / 9],
    [1 / 9, 1 / 9, 1 / 9],
  ],
  sharpen: [
    [0, -1, 0],
    [-1, 5, -1],
    [0, -1, 0],
  ],
  sobelX: [
    [-1, 0, 1],
    [-2, 0, 2],
    [-1, 0, 1],
  ],
  sobelY: [
    [-1, -2, -1],
    [0, 0, 0],
    [1, 2, 1],
  ],
  laplacian: [
    [0, 1, 0],
    [1, -4, 1],
    [0, 1, 0],
  ],
  emboss: [
    [-2, -1, 0],
    [-1, 1, 1],
    [0, 1, 2],
  ],
};

// 2D 卷积
export function convolve2D(img: GrayImage, kernel: number[][]): GrayImage {
  const h = img.length;
  const w = img[0].length;
  const kh = kernel.length;
  const kw = kernel[0].length;
  const padR = Math.floor(kh / 2);
  const padC = Math.floor(kw / 2);

  const result = createImage(h, w);

  for (let r = 0; r < h; r++) {
    for (let c = 0; c < w; c++) {
      let sum = 0;
      for (let kr = 0; kr < kh; kr++) {
        for (let kc = 0; kc < kw; kc++) {
          const rr = r + kr - padR;
          const cc = c + kc - padC;
          if (rr >= 0 && rr < h && cc >= 0 && cc < w) {
            sum += img[rr][cc] * kernel[kr][kc];
          }
        }
      }
      result[r][c] = Math.max(0, Math.min(255, Math.round(sum)));
    }
  }
  return result;
}

// Sobel 边缘检测
export function sobelEdge(img: GrayImage): GrayImage {
  const gx = convolve2D(img, KERNELS.sobelX);
  const gy = convolve2D(img, KERNELS.sobelY);
  const result = createImage(img.length, img[0].length);
  for (let r = 0; r < img.length; r++) {
    for (let c = 0; c < img[0].length; c++) {
      result[r][c] = Math.min(255, Math.round(Math.sqrt(gx[r][c] ** 2 + gy[r][c] ** 2)));
    }
  }
  return result;
}

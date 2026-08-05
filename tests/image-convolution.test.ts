import { describe, it, expect } from 'vitest';
import {
  createImage,
  convolve2D,
  KERNELS,
  sobelEdge,
} from '../src/algorithms/image/convolution';

describe('convolve2D', () => {
  it('applies blur kernel', () => {
    const img = createImage(3, 3, 0);
    img[1][1] = 255; // center pixel
    const result = convolve2D(img, KERNELS.blur3);
    expect(result[1][1]).toBeLessThan(255); // center should be smoothed
    expect(result[1][1]).toBeGreaterThan(0);
  });

  it('applies sharpen kernel', () => {
    const img = createImage(3, 3, 100);
    img[1][1] = 200;
    const result = convolve2D(img, KERNELS.sharpen);
    expect(result[1][1]).toBeGreaterThan(200); // center enhanced
  });
});

describe('sobelEdge', () => {
  it('detects edges', () => {
    const img = createImage(5, 5, 0);
    for (let i = 2; i < 5; i++) for (let c = 0; c < 5; c++) img[i][c] = 255;
    const edges = sobelEdge(img);
    // edge at row 1-2 boundary
    expect(edges[1][2]).toBeGreaterThan(0);
  });
});

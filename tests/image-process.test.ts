import { describe, it, expect } from 'vitest';
import { histogram, equalizeHistogram, threshold, otsuThreshold } from '../src/algorithms/image/histogram';
import { floodFill, bresenhamLine, bezierCurve } from '../src/algorithms/image/draw';
import { createImage } from '../src/algorithms/image/convolution';

describe('histogram', () => {
  it('counts pixel values', () => {
    const img = [[0, 0, 255], [128, 255, 0]];
    const hist = histogram(img);
    expect(hist[0]).toBe(3);
    expect(hist[128]).toBe(1);
    expect(hist[255]).toBe(2);
  });
});

describe('equalizeHistogram', () => {
  it('enhances contrast', () => {
    const img = createImage(2, 3, 50);
    img[0][0] = 200;
    img[0][1] = 200;
    const result = equalizeHistogram(img);
    // min should be 0, max should be 255
    expect(result.some((row) => row.some((p) => p === 255))).toBe(true);
  });
});

describe('threshold', () => {
  it('binarizes image', () => {
    const img = [[100, 150], [200, 50]];
    const result = threshold(img, 125);
    expect(result).toEqual([[0, 255], [255, 0]]);
  });
});

describe('otsuThreshold', () => {
  it('finds optimal threshold', () => {
    const img = [[10, 12, 200, 210]]; // two clusters
    const t = otsuThreshold(img);
    expect(t).toBeGreaterThanOrEqual(12);
    expect(t).toBeLessThan(200);
  });
});

describe('floodFill', () => {
  it('fills connected region', () => {
    const img = [
      [1, 1, 1],
      [1, 0, 1],
      [1, 1, 1],
    ];
    const result = floodFill(img, 0, 0, 2);
    // center (0) is not connected to border (1)
    expect(result[1][1]).toBe(0);
    expect(result[0][0]).toBe(2);
    expect(result[2][2]).toBe(2);
  });
});

describe('bresenhamLine', () => {
  it('draws straight line', () => {
    const points = bresenhamLine(0, 0, 2, 2);
    expect(points[0]).toEqual([0, 0]);
    expect(points[points.length - 1]).toEqual([2, 2]);
    expect(points.length).toBe(3);
  });

  it('draws horizontal line', () => {
    const points = bresenhamLine(0, 5, 3, 5);
    expect(points.every(([, y]) => y === 5)).toBe(true);
  });
});

describe('bezierCurve', () => {
  it('generates curve points', () => {
    const points = bezierCurve([0, 0], [10, 20], [30, 30], [40, 0], 10);
    expect(points.length).toBe(11);
    expect(points[0]).toEqual([0, 0]);
    expect(points[10]).toEqual([40, 0]);
  });
});

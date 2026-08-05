import { describe, it, expect } from 'vitest';
import { createImage } from '../src/algorithms/image/convolution';
import {
  resizeNearest,
  resizeBilinear,
  rotate90,
  flipHorizontal,
  flipVertical,
  translate,
} from '../src/algorithms/image/transform';

describe('resizeNearest', () => {
  it('resizes image', () => {
    const img = createImage(2, 2, 100);
    img[0][0] = 255;
    const result = resizeNearest(img, 4, 4);
    expect(result.length).toBe(4);
    expect(result[0].length).toBe(4);
    expect(result[0][0]).toBe(255); // top-left preserved
  });
});

describe('resizeBilinear', () => {
  it('smooths on upscale', () => {
    const img = createImage(2, 2, 100);
    const result = resizeBilinear(img, 4, 4);
    expect(result.length).toBe(4);
  });
});

describe('rotate90', () => {
  it('rotates 1 time', () => {
    const img = [[1, 2], [3, 4]];
    const result = rotate90(img, 1);
    expect(result).toEqual([[3, 1], [4, 2]]);
  });

  it('4 rotations returns original', () => {
    const img = [[1, 2], [3, 4]];
    expect(rotate90(img, 4)).toEqual(img);
  });
});

describe('flipHorizontal', () => {
  it('mirrors left-right', () => {
    const img = [[1, 2, 3]];
    expect(flipHorizontal(img)).toEqual([[3, 2, 1]]);
  });
});

describe('flipVertical', () => {
  it('mirrors top-bottom', () => {
    const img = [[1], [2], [3]];
    expect(flipVertical(img)).toEqual([[3], [2], [1]]);
  });
});

describe('translate', () => {
  it('shifts image', () => {
    const img = [[1, 2], [3, 4]];
    const result = translate(img, 1, 1);
    expect(result[1][1]).toBe(1);
    expect(result[0][0]).toBe(0);
  });
});

import { describe, it, expect } from 'vitest';
import { createImage } from '../src/algorithms/image/convolution';
import { dilate, erode, open, close } from '../src/algorithms/image/morphology';

describe('morphology', () => {
  const img = createImage(5, 5, 0);
  img[2][2] = 255;

  it('dilate expands bright areas', () => {
    const result = dilate(img, 3);
    expect(result[2][2]).toBe(255);
    // neighbors should also become bright
    expect(result[2][1]).toBe(255);
    expect(result[1][2]).toBe(255);
  });

  it('erode shrinks bright areas', () => {
    const big = createImage(5, 5, 255);
    big[0][0] = 0;
    const result = erode(big, 3);
    // border pixels become 0
    expect(result[0][0]).toBe(0);
    expect(result[0][1]).toBe(0);
    expect(result[2][2]).toBe(255); // center still 255
  });

  it('open removes small noise', () => {
    const img = createImage(5, 5, 0);
    img[2][2] = 255;
    const result = open(img, 3);
    expect(result[2][2]).toBe(0); // isolated pixel removed
  });

  it('close fills small holes', () => {
    const img = createImage(5, 5, 255);
    img[2][2] = 0;
    const result = close(img, 3);
    expect(result[2][2]).toBe(255); // hole filled
  });
});

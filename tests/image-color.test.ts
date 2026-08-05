import { describe, it, expect } from 'vitest';
import { rgbToGray, rgbToHSL, hslToRGB, rgbToYUV, yuvToRGB } from '../src/algorithms/image/color';

describe('rgbToGray', () => {
  it('converts to grayscale', () => {
    expect(rgbToGray({ r: 255, g: 255, b: 255 })).toBe(255);
    expect(rgbToGray({ r: 0, g: 0, b: 0 })).toBe(0);
  });
});

describe('rgbToHSL / hslToRGB round trip', () => {
  it('converts there and back', () => {
    const rgb = { r: 128, g: 64, b: 192 };
    const hsl = rgbToHSL(rgb);
    const back = hslToRGB(hsl);
    expect(back.r).toBeCloseTo(rgb.r, -1);
    expect(back.g).toBeCloseTo(rgb.g, -1);
    expect(back.b).toBeCloseTo(rgb.b, -1);
  });
});

describe('rgbToYUV / yuvToRGB round trip', () => {
  it('converts there and back', () => {
    const rgb = { r: 200, g: 100, b: 50 };
    const yuv = rgbToYUV(rgb);
    const back = yuvToRGB(yuv);
    expect(back.r).toBeCloseTo(rgb.r, 0);
    expect(back.g).toBeCloseTo(rgb.g, 0);
    expect(back.b).toBeCloseTo(rgb.b, 0);
  });
});

// RGB 颜色
export interface RGB {
  r: number; // 0-255
  g: number;
  b: number;
}

export interface HSL {
  h: number; // 0-360
  s: number; // 0-1
  l: number; // 0-1
}

export interface YUV {
  y: number;
  u: number;
  v: number;
}

// RGB → 灰度
export function rgbToGray(rgb: RGB): number {
  return Math.round(0.299 * rgb.r + 0.587 * rgb.g + 0.114 * rgb.b);
}

// RGB → HSL
export function rgbToHSL(rgb: RGB): HSL {
  const r = rgb.r / 255;
  const g = rgb.g / 255;
  const b = rgb.b / 255;
  const max = Math.max(r, g, b);
  const min = Math.min(r, g, b);
  const delta = max - min;

  const l = (max + min) / 2;
  let h = 0;
  let s = 0;

  if (delta !== 0) {
    s = l > 0.5 ? delta / (2 - max - min) : delta / (max + min);
    if (max === r) h = ((g - b) / delta + (g < b ? 6 : 0)) / 6;
    else if (max === g) h = ((b - r) / delta + 2) / 6;
    else h = ((r - g) / delta + 4) / 6;
  }

  return { h: Math.round(h * 360), s, l };
}

// HSL → RGB
export function hslToRGB(hsl: HSL): RGB {
  const { h, s, l } = hsl;
  const hue = ((h % 360) + 360) % 360;

  const c = (1 - Math.abs(2 * l - 1)) * s;
  const x = c * (1 - Math.abs(((hue / 60) % 2) - 1));
  const m = l - c / 2;

  let rp = 0, gp = 0, bp = 0;
  if (hue < 60)       { rp = c; gp = x; }
  else if (hue < 120) { rp = x; gp = c; }
  else if (hue < 180) { gp = c; bp = x; }
  else if (hue < 240) { gp = x; bp = c; }
  else if (hue < 300) { rp = x; bp = c; }
  else                { rp = c; bp = x; }

  return {
    r: Math.round((rp + m) * 255),
    g: Math.round((gp + m) * 255),
    b: Math.round((bp + m) * 255),
  };
}

// RGB → YUV (BT.601)
export function rgbToYUV(rgb: RGB): YUV {
  return {
    y: 0.299 * rgb.r + 0.587 * rgb.g + 0.114 * rgb.b,
    u: -0.14713 * rgb.r - 0.28886 * rgb.g + 0.436 * rgb.b + 128,
    v: 0.615 * rgb.r - 0.51499 * rgb.g - 0.10001 * rgb.b + 128,
  };
}

// YUV → RGB
export function yuvToRGB(yuv: YUV): RGB {
  const y = yuv.y;
  const u = yuv.u - 128;
  const v = yuv.v - 128;
  return {
    r: clamp(Math.round(y + 1.13983 * v), 0, 255),
    g: clamp(Math.round(y - 0.39465 * u - 0.5806 * v), 0, 255),
    b: clamp(Math.round(y + 2.03211 * u), 0, 255),
  };
}

function clamp(v: number, lo: number, hi: number): number {
  return Math.max(lo, Math.min(hi, v));
}

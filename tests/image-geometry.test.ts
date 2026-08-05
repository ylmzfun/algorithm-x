import { describe, it, expect } from 'vitest';
import {
  segmentsIntersect,
  convexHull,
  pointToSegmentDist,
  polygonArea,
  pointInPolygon,
} from '../src/algorithms/image/geometry';

describe('segmentsIntersect', () => {
  it('detects intersection', () => {
    expect(segmentsIntersect([0, 0], [2, 2], [0, 2], [2, 0])).toBe(true);
  });

  it('detects non-intersection', () => {
    expect(segmentsIntersect([0, 0], [1, 1], [3, 3], [4, 4])).toBe(false);
  });
});

describe('convexHull', () => {
  it('computes convex hull', () => {
    const hull = convexHull([[0, 0], [1, 1], [2, 0], [1, 2], [3, 1]]);
    // hull should contain extreme points
    expect(hull.length).toBeLessThan(5);
    expect(hull).toEqual(expect.arrayContaining([[0, 0]]));
  });
});

describe('pointToSegmentDist', () => {
  it('returns 0 for point on segment', () => {
    expect(pointToSegmentDist([1, 1], [0, 0], [2, 2])).toBeCloseTo(0);
  });
});

describe('polygonArea', () => {
  it('computes area', () => {
    // Unit square
    expect(polygonArea([[0, 0], [1, 0], [1, 1], [0, 1]])).toBe(1);
  });
});

describe('pointInPolygon', () => {
  it('detects point inside square', () => {
    const sq: [number, number][] = [[0, 0], [4, 0], [4, 4], [0, 4]];
    expect(pointInPolygon([2, 2], sq)).toBe(true);
    expect(pointInPolygon([5, 5], sq)).toBe(false);
  });
});

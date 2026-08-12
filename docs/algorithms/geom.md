# 计算几何（`include/algorithm_x/geom/`）

本文档覆盖计算几何模块的 **5 个头文件**：点 / 向量基础运算（`point.h`）、凸包（`convex_hull.h`）、线段相交与最近点对（`intersection.h`）、半平面交（`half_plane.h`）、扫描线求矩形面积并（`sweep_line.h`）。

所有 API 均位于 `namespace algorithm_x::geom`，坐标使用 `double`。核心概念：`orient(a, b, c)`（叉积方向）与 `on_segment` 被多个算法共用，`point.h` 是其余四个头文件的公共依赖（`convex_hull.h`、`intersection.h`、`half_plane.h` 均 `#include "point.h"`）。

---

### `geom/point.h` — 二维点 / 向量基础运算
**用途**：定义二维平面上的点（向量）类型及最常用的几何原语：加减、数乘、点积、叉积、距离、多边形有向面积、点在线段上的判定、三点转向判定。
**原理**：`Point` 用 `double x, y` 表示，重载运算符使向量写法与数学一致；`cross(a, b) = a.x*b.y - a.y*b.x` 的符号表示两向量转向，`orient(a,b,c) = cross(b-a, c-a)` 表示三点 a→b→c 的转向（>0 逆时针，<0 顺时针，==0 共线）；多边形面积用鞋带公式（shoelace）求有向面积。
**主要 API**：
```cpp
// 二维点 / 向量。
struct Point {
    double x, y;
    Point operator+(const Point& o) const;   // 向量加
    Point operator-(const Point& o) const;   // 向量减
    Point operator*(double k) const;         // 数乘
    double operator*(const Point& o) const;  // 点积（dot）
    bool operator==(const Point& o) const;
};

// 叉积：a × b = |a||b| sin θ。正值表示 b 在 a 的逆时针方向。
double cross(const Point& a, const Point& b);

// 两点间欧氏距离。
double dist(const Point& a, const Point& b);

// 两点间距离的平方（避免开方）。
double dist2(const Point& a, const Point& b);

// 多边形面积（顶点按逆时针或顺时针给出，返回有向面积）。
// 逆时针为正，绝对值 / 2 为实际面积。
double polygon_area(const std::vector<Point>& poly);

// 判断点 c 是否在线段 ab 上（假设共线已判定）。
bool on_segment(const Point& a, const Point& b, const Point& c);

// 叉积方向：>0 逆时针，<0 顺时针，==0 共线。
double orient(const Point& a, const Point& b, const Point& c);
```
**复杂度**：全部为 O(1)；`polygon_area` 为 O(n)（n 为顶点数）
**使用场景**：所有几何算法的基础设施；凸性判定、点在多边形内外判定、碰撞检测前的转向判断。
**使用示例**：
```cpp
using namespace algorithm_x::geom;
Point a{1, 2}, b{3, 4};
auto c = a + b;                 // {4, 6}；a * b == 11（点积）
double o = orient({0, 0}, {1, 0}, {0, 1});   // > 0，逆时针
double area = polygon_area({{0, 0}, {2, 0}, {2, 2}, {0, 2}});  // 4.0
bool on = on_segment({0, 0}, {4, 0}, {2, 0});  // true
```

---

### `geom/convex_hull.h` — 凸包（Andrew 单调链）
**用途**：求平面点集的凸包——包含所有点的最小凸多边形顶点序列（逆时针，不含共线中间点）。
**原理**：Andrew 单调链算法：先按 (x, y) 字典序排序；从左到右构造下凸壳、从右到左构造上凸壳，维护单调栈时用 `orient <= 0` 弹出（即保持严格逆时针转向，剔除共线中间点与内部点）；最后去掉首尾重复点。
**主要 API**：
```cpp
// Andrew 单调链算法 — O(n log n)。
// 返回凸包顶点（逆时针，不含共线中间点）。
std::vector<Point> convex_hull(std::vector<Point> pts);
```
**复杂度**：时间 O(n log n)（排序主导）/ 空间 O(n)
**使用场景**：点集外包形状；作为旋转卡壳（最远点对、最小面积外接矩形）的前置；碰撞检测与点集简化。
**使用示例**：
```cpp
using namespace algorithm_x::geom;
std::vector<Point> pts = {{0, 0}, {2, 0}, {2, 2}, {1, 1}, {0, 2}};
auto hull = convex_hull(pts);   // 4 个顶点 {0,0},{2,0},{2,2},{0,2}（逆时针）
// 点数 ≤ 2 时原样返回；全共线时返回两端点
```

---

### `geom/intersection.h` — 线段相交判定与最近点对
**用途**：两个经典问题：判断两条线段是否相交（含端点接触），以及平面点集最近点对距离。
**原理**：线段相交用「跨立实验」——`orient(a,b,c)` 与 `orient(a,b,d)` 异号且 `orient(c,d,a)` 与 `orient(c,d,b)` 异号则严格相交；共线时退化为 `on_segment` 端点检测。最近点对用分治法：按 x 排序后递归左右两半，合并时只检查中线两侧带状区域内按 y 排序的点（每个点只需与后面几个 y 差小于当前最优值的点比较）。
**主要 API**：
```cpp
// 判断线段 ab 和 cd 是否相交（包括端点接触）。
bool segment_intersect(const Point& a, const Point& b,
                       const Point& c, const Point& d);

// 最近点对（分治法）— O(n log n)。
// 返回 {点1索引, 点2索引, 距离}。
// 调用者传入点数组（会被排序），返回原始点的距离。
double closest_pair(std::vector<Point>& pts);
```
**复杂度**：`segment_intersect` O(1)；`closest_pair` 时间 O(n log n) / 空间 O(n)
**使用场景**：地图 / CAD 中的线段碰撞检测；几何覆盖问题的相交判定；平面最近点对（聚类、最邻近搜索的预处理）。注意 `closest_pair` 会原地修改 `pts`（按 x 排序）。
**使用示例**：
```cpp
using namespace algorithm_x::geom;
bool hit = segment_intersect({0, 0}, {2, 2}, {0, 2}, {2, 0});  // true（X 形相交）
std::vector<Point> pts = {{0, 0}, {1, 0}, {10, 10}, {11, 10}};
double d = closest_pair(pts);   // 1.0（{0,0} 与 {1,0}）
```

---

### `geom/half_plane.h` — 半平面交
**用途**：求若干半平面（每条半平面为直线一侧的闭区域）的交集区域，输出该凸多边形区域的顶点（逆时针）；交为空时返回空。
**原理**：增量式算法：从「足够大的矩形」开始（边界取 ±1e9），对每条半平面用直线裁剪当前多边形——保留在 `a*x + b*y + c <= EPS` 一侧的顶点，线段穿过边界时插入交点。O(n²)，实现简单直观。
**主要 API**：
```cpp
// 半平面交 — 每条半平面表示为 a·x + b·y + c ≤ 0。
// 返回交区域的多边形顶点（逆时针）。使用增量式 O(n²) 算法。
struct HalfPlane {
    double a, b, c;  // a*x + b*y + c <= 0
};

std::vector<Point> half_plane_intersection(
    const std::vector<HalfPlane>& planes);
```
**复杂度**：时间 O(n²)（n 为半平面数）/ 空间 O(n)
**使用场景**：求线性规划可行域（二维 LP 的可行区域）；求多边形内核（每个顶点内侧半平面的交）；可见区域 / 安全区域问题。
**使用示例**：
```cpp
using namespace algorithm_x::geom;
// 四条边围成 [-1,1] × [-1,1] 的正方形
std::vector<HalfPlane> planes = {
    {1.0, 0.0, -1.0},   // x <= 1
    {-1.0, 0.0, -1.0},  // x >= -1
    {0.0, 1.0, -1.0},   // y <= 1
    {0.0, -1.0, -1.0},  // y >= -1
};
auto poly = half_plane_intersection(planes);  // 面积为 4 的正方形
```

---

### `geom/sweep_line.h` — 扫描线：矩形面积并
**用途**：求多个（可相互重叠的）轴对齐矩形的并集面积，是扫描线 + 线段树的经典应用。
**原理**：将 y 坐标离散化，把每个矩形拆成「左边界进入 (+1) / 右边界离开 (-1)」两个事件；按 x 扫描事件，线段树维护当前被覆盖的 y 区间总长度 `len[1]`，相邻两个事件之间的面积增量 = `len[1] × Δx`，累加即得总面积。
**主要 API**：
```cpp
// 矩形 {x1, y1, x2, y2} 其中 x1 < x2, y1 < y2。
struct Rect {
    double x1, y1, x2, y2;
};

// 矩形面积并（扫描线算法）。
// 离散化 y 坐标，扫描线从左到右。
double rectangle_union_area(const std::vector<Rect>& rects);
```
**复杂度**：时间 O(n log n)（排序 + 线段树操作）/ 空间 O(n)
**使用场景**：多个矩形区域的并集面积（电子设计自动化中的版图面积、城市地块合并）；推广可求矩形周长并、矩形覆盖层数最大值。
**使用示例**：
```cpp
using namespace algorithm_x::geom;
std::vector<Rect> rects = {{0, 0, 2, 2}, {1, 1, 3, 3}};
double area = rectangle_union_area(rects);   // 7.0（重叠区只算一次）
```

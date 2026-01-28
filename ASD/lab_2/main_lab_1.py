from dataclasses import dataclass
from itertools import combinations
import math

EPS = 1e-9


@dataclass
class Point:
    x: float
    y: float

    def __str__(self) -> str:
        return f"({self.x:.2f}, {self.y:.2f})"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Point):
            return False
        return abs(self.x - other.x) < EPS and abs(self.y - other.y) < EPS

    def __hash__(self):
        return hash((round(self.x, 6), round(self.y, 6)))


@dataclass
class Line:
    p1: Point
    p2: Point

    def __str__(self) -> str:
        return f"Line({self.p1} -> {self.p2})"


@dataclass
class Segment:
    p1: Point
    p2: Point

    def __str__(self) -> str:
        return f"Segment[{self.p1} -> {self.p2}]"


@dataclass
class Circle:
    center: Point
    radius: float

    def __str__(self) -> str:
        return f"Circle(center={self.center}, r={self.radius:.2f})"


@dataclass
class Triangle:
    vertices: list[Point]

    def __str__(self) -> str:
        v = self.vertices
        return f"Triangle({v[0]}, {v[1]}, {v[2]})"

    def get_edges(self) -> list:
        v = self.vertices
        return [Segment(v[0], v[1]), Segment(v[1], v[2]), Segment(v[2], v[0])]


def cross_product(o: Point, a: Point, b: Point) -> float:
    return (a.x - o.x) * (b.y - o.y) - (a.y - o.y) * (b.x - o.x)


def distance(p1: Point, p2: Point) -> float:
    return math.sqrt((p2.x - p1.x) ** 2 + (p2.y - p1.y) ** 2)


def sign(x: float) -> int:
    if x > EPS:
        return 1
    if x < -EPS:
        return -1
    return 0


def is_collinear(p1: Point, p2: Point, p3: Point) -> bool:
    return abs(cross_product(p1, p2, p3)) < EPS


def point_on_segment(p: Point, seg_start: Point, seg_end: Point) -> bool:
    if not is_collinear(p, seg_start, seg_end):
        return False
    return (
        min(seg_start.x, seg_end.x) - EPS <= p.x <= max(seg_start.x, seg_end.x) + EPS
        and min(seg_start.y, seg_end.y) - EPS
        <= p.y
        <= max(seg_start.y, seg_end.y) + EPS
    )


def line_line_intersection(line1: Line, line2: Line) -> list[Point]:
    p1, p2 = line1.p1, line1.p2
    p3, p4 = line2.p1, line2.p2

    # уравнение прямой ax + by + c = 0
    a1 = p2.y - p1.y
    b1 = p1.x - p2.x
    c1 = p2.x * p1.y - p1.x * p2.y

    a2 = p4.y - p3.y
    b2 = p3.x - p4.x
    c2 = p4.x * p3.y - p3.x * p4.y

    det = a1 * b2 - a2 * b1

    if abs(det) < EPS:
        return []  # прямые параллельны или совпадают

    x = (b1 * c2 - b2 * c1) / det
    y = (a2 * c1 - a1 * c2) / det

    return [Point(x, y)]


def line_segment_intersection(line: Line, segment: Segment) -> list[Point]:
    segment_as_line = Line(segment.p1, segment.p2)
    intersection = line_line_intersection(line, segment_as_line)

    if not intersection:
        return []

    point = intersection[0]
    if point_on_segment(point, segment.p1, segment.p2):
        return [point]
    return []


def segment_segment_intersection(seg1: Segment, seg2: Segment) -> list[Point]:
    if is_collinear(seg1.p1, seg1.p2, seg2.p1) and is_collinear(
        seg1.p1, seg1.p2, seg2.p2
    ):
        points = []

        if point_on_segment(seg2.p1, seg1.p1, seg1.p2):
            points.append(seg2.p1)
        if point_on_segment(seg2.p2, seg1.p1, seg1.p2):
            points.append(seg2.p2)

        if point_on_segment(seg1.p1, seg2.p1, seg2.p2):
            points.append(seg1.p1)
        if point_on_segment(seg1.p2, seg2.p1, seg2.p2):
            points.append(seg1.p2)

        return list(set(points))

    line1 = Line(seg1.p1, seg1.p2)
    line2 = Line(seg2.p1, seg2.p2)
    intersection = line_line_intersection(line1, line2)

    if not intersection:
        return []

    point = intersection[0]
    if point_on_segment(point, seg1.p1, seg1.p2) and point_on_segment(
        point, seg2.p1, seg2.p2
    ):
        return [point]
    return []


def line_circle_intersection(line: Line, circle: Circle) -> list[Point]:
    """
    Пересечение прямой и окружности.

    Прямая параметрически: P(t) = P1 + t · (P2 - P1), где t ∈ ℝ
    Окружность: (x - cx)² + (y - cy)² = r²

    Подставляем прямую в окружность → квадратное уравнение at² + bt + c = 0
    """
    # Исходные данные
    P1 = line.p1
    P2 = line.p2
    C = circle.center
    r = circle.radius

    # Направляющий вектор прямой: d = P2 - P1
    dx = P2.x - P1.x
    dy = P2.y - P1.y

    # Вектор от центра окружности к началу прямой: f = P1 - C
    fx = P1.x - C.x
    fy = P1.y - C.y

    # Коэффициенты квадратного уравнения at² + bt + c = 0
    # Получаются подстановкой P(t) в уравнение окружности
    a = dx * dx + dy * dy  # |d|²
    b = 2 * (fx * dx + fy * dy)  # 2(f · d)
    c = fx * fx + fy * fy - r * r  # |f|² - r²

    # Дискриминант
    discriminant = b * b - 4 * a * c

    # Анализ дискриминанта
    if discriminant < -EPS:
        # D < 0: прямая не пересекает окружность
        return []

    if abs(discriminant) < EPS:
        # D = 0: прямая касается окружности (одна точка)
        t = -b / (2 * a)
        x = P1.x + t * dx
        y = P1.y + t * dy
        return [Point(x, y)]

    # D > 0: прямая пересекает окружность (две точки)
    sqrt_D = math.sqrt(discriminant)

    t1 = (-b - sqrt_D) / (2 * a)
    t2 = (-b + sqrt_D) / (2 * a)

    point1 = Point(P1.x + t1 * dx, P1.y + t1 * dy)
    point2 = Point(P1.x + t2 * dx, P1.y + t2 * dy)

    return [point1, point2]


def segment_circle_intersection(segment: Segment, circle: Circle) -> list[Point]:
    line = Line(segment.p1, segment.p2)
    points = line_circle_intersection(line, circle)
    return [p for p in points if point_on_segment(p, segment.p1, segment.p2)]


def circle_circle_intersection(circle1: Circle, circle2: Circle) -> list[Point]:
    C1 = circle1.center
    C2 = circle2.center
    r1 = circle1.radius
    r2 = circle2.radius

    d = distance(C1, C2)

    if d < EPS:
        return []

    if d > r1 + r2 + EPS:
        return []

    if d < abs(r1 - r2) - EPS:
        return []

    # a — расстояние от c1 до линии пересечения
    a = (r1 * r1 - r2 * r2 + d * d) / (2 * d)

    # h — расстояние от линии центров до точек пересечения
    h_squared = r1 * r1 - a * a

    if h_squared < -EPS:
        return []

    h = math.sqrt(max(0, h_squared))

    # точка P на линии между центрами
    Px = C1.x + a * (C2.x - C1.x) / d
    Py = C1.y + a * (C2.y - C1.y) / d

    if abs(h) < EPS:
        return [Point(Px, Py)]

    # перпендикуляр к (dx, dy) это (-dy, dx) или (dy, -dx)
    perpendicular_x = h * (C2.y - C1.y) / d
    perpendicular_y = h * (C2.x - C1.x) / d

    point1 = Point(Px + perpendicular_x, Py - perpendicular_y)
    point2 = Point(Px - perpendicular_x, Py + perpendicular_y)

    return [point1, point2]


def is_valid_triangle(t: Triangle) -> bool:
    if len(t.vertices) != 3:
        return False
    v = t.vertices
    return not is_collinear(v[0], v[1], v[2])


def triangle_area(t: Triangle) -> float:
    v = t.vertices
    return abs(cross_product(v[0], v[1], v[2])) / 2


def point_in_triangle(p: Point, t: Triangle, inclusive: bool = False) -> bool:
    a, b, c = t.vertices

    d1 = cross_product(a, b, p)
    d2 = cross_product(b, c, p)
    d3 = cross_product(c, a, p)

    s1, s2, s3 = sign(d1), sign(d2), sign(d3)

    if not inclusive:
        return s1 == s2 == s3 != 0
    else:
        has_neg = s1 < 0 or s2 < 0 or s3 < 0
        has_pos = s1 > 0 or s2 > 0 or s3 > 0
        return not (has_neg and has_pos)


def point_in_triangle_raycast(p: Point, t: Triangle) -> bool:
    ray_end = Point(p.x + 1e9, p.y + 0.1)
    ray = Line(p, ray_end)

    intersection_count = 0

    for edge in t.get_edges():
        intersections = line_segment_intersection(ray, edge)

        for point in intersections:
            if point.x > p.x + EPS:
                intersection_count += 1

    return intersection_count % 2 == 1


def triangles_edges_intersect(t1: Triangle, t2: Triangle) -> bool:
    for edge1 in t1.get_edges():
        for edge2 in t2.get_edges():
            intersections = segment_segment_intersection(edge1, edge2)

            if intersections:
                point = intersections[0]
                is_vertex_t1 = any(
                    abs(point.x - v.x) < EPS and abs(point.y - v.y) < EPS
                    for v in t1.vertices
                )
                is_vertex_t2 = any(
                    abs(point.x - v.x) < EPS and abs(point.y - v.y) < EPS
                    for v in t2.vertices
                )

                if not (is_vertex_t1 and is_vertex_t2):
                    return True

    return False


def triangle_contains_triangle(outer: Triangle, inner: Triangle) -> bool:
    for vertex in inner.vertices:
        if not point_in_triangle_raycast(vertex, outer):
            return False

    if triangles_edges_intersect(outer, inner):
        return False

    return True


def find_nested_pair(points: list[Point]) -> tuple[Triangle, Triangle] | None:
    triangles = []
    for combo in combinations(points, 3):
        t = Triangle(list(combo))
        if is_valid_triangle(t):
            triangles.append(t)

    for i, outer in enumerate(triangles):
        for j, inner in enumerate(triangles):
            if i != j and triangle_contains_triangle(outer, inner):
                return (outer, inner)
    return None


def parse_input(filepath: str) -> list[Point]:
    points = []
    with open(filepath, "r") as f:
        for line in f:
            line = line.strip()
            parts = line.split()
            if len(parts) >= 2:
                x, y = float(parts[0]), float(parts[1])
                points.append(Point(x, y))
    return points


def main(filepath: str):
    try:
        points = parse_input(filepath)
    except FileNotFoundError:
        print(f"Ошибка: файл '{filepath}' не найден")
        return

    if len(points) < 6:
        print("Нужно минимум 6 точек для двух треугольников")
        return

    result = find_nested_pair(points)

    if result:
        outer, inner = result
        print("\nЕсть вложенные треугольники:\n")
        print(f"Внешний: {outer}")
        print(f"Внутренний: {inner}")
    else:
        print("\nВложенных треугольников не найдено")


if __name__ == "__main__":
    filepath = "lab_2/points.txt"
    main(filepath)

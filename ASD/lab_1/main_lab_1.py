from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class Point:
    x: float
    y: float

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"


def cross_product(origin: Point, point_a: Point, point_b: Point) -> float:
    return (point_a.x - origin.x) * (point_b.y - origin.y) - (point_a.y - origin.y) * (
        point_b.x - origin.x
    )


def distance_squared(point_a: Point, point_b: Point) -> float:
    return (point_b.x - point_a.x) ** 2 + (point_b.y - point_a.y) ** 2


def parse_points_from_file(filepath: str) -> list[Point]:
    points = []
    path = Path(filepath)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {filepath}")

    with open(path, "r", encoding="utf-8") as file:
        for line_num, line in enumerate(file, start=1):
            line: str = line.strip()

            if not line:
                continue

            try:
                parts: list[str] = line.split()
                if len(parts) != 2:
                    print(
                        f"Line {line_num} - expected 2 values, "
                        f"got {len(parts)}: '{line}'"
                    )
                    continue

                x, y = float(parts[0]), float(parts[1])
                points.append(Point(x, y))

            except ValueError:
                print(f"Line {line_num} - invalid values: '{line}'")

    return points


def find_starting_point_index(points: list[Point]) -> int:
    best_index = 0

    for i, point in enumerate(points):
        if (point.y, point.x) < (points[best_index].y, points[best_index].x):
            best_index = i

    return best_index

def remove_duplicates(points: list[Point]) -> list[Point]:
    unique_points = []
    
    for point in points:
        if point not in unique_points:
            unique_points.append(point)
    
    return unique_points

def jarvis_algorithm(points: list[Point]) -> Optional[list[Point]]:
    unique_points: list[Point] = remove_duplicates(points)
    n = len(unique_points)

    if n < 3:
        return None

    start_idx = find_starting_point_index(unique_points)

    hull_indices = []
    current_idx = start_idx

    while True:
        hull_indices.append(current_idx)
        next_idx = 0 if current_idx != 0 else 1

        for candidate_idx in range(n):
            if candidate_idx == current_idx:
                continue

            cross = cross_product(
                unique_points[current_idx],
                unique_points[next_idx],
                unique_points[candidate_idx],
            )

            if cross < 0:
                next_idx = candidate_idx
            elif cross == 0:
                if distance_squared(
                    unique_points[current_idx], unique_points[candidate_idx]
                ) > distance_squared(
                    unique_points[current_idx], unique_points[next_idx]
                ):
                    next_idx = candidate_idx

        if next_idx == start_idx:
            break

        current_idx = next_idx

        if len(hull_indices) > n:
            return None

    hull = [unique_points[i] for i in hull_indices]

    if len(hull) < 3:
        return None

    return hull


def format_result(hull: Optional[list[Point]]) -> str:
    if hull is None:
        return (
            "Convex hull exists: No\n"
            "Reason: Insufficient points or all points are collinear"
        )

    lines = [
        "Convex hull exists: Yes",
        f"Number of hull vertices: {len(hull)}",
        "Hull vertices (counterclockwise order):",
    ]

    for idx, point in enumerate(hull, start=1):
        lines.append(f"  {idx}. {point}")

    return "\n".join(lines)


def main():
    filepath = "points.txt"
    try:
        points = parse_points_from_file(filepath)
        if not points:
            print("Error: No valid points found in the file.")
            return

        print(f"Successfully loaded {len(points)} point(s).\n")

        hull: Optional[list[Point]] = jarvis_algorithm(points)
        print(format_result(hull))

    except FileNotFoundError as error:
        print(f"Error: {error}")
    except Exception as error:
        print(f"Unexpected error: {error}")


if __name__ == "__main__":
    main()

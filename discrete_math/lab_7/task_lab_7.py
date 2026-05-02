"""
ВАРИАНТ 4. Дискретная математика. Кратчайшие пути на графах.

Требования:
1) Случайно задать простые связные разреженные неориентированные графы для N:
   1500, 3300, 7700, 22000, 35000.
2) Граф должен содержать два непересекающихся (по вершинам) подграфа: K6 и K3,5.
3) A) Флойд–Уоршелл: расстояние от каждой вершины до каждой.
4) Б) Дейкстра: расстояния от вершины 0 до всех. Восстановить путь 0 -> (N-1).
5) Найти число итераций. Сравнить с асимптотической сложностью.

Пояснение по практике:
- Флойд–Уоршелл имеет сложность O(n^3) и память O(n^2) (в оптимизированной форме),
  поэтому для больших N его запуск обычно невозможен по времени.
  В программе это сделано через ограничение FLOYD_MAX_N (можно менять параметром).
"""

import math
import random
import time
import heapq
from collections import deque
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional

import numpy as np


GRAPH_SIZES: List[int] = [1500, 3300, 7700, 22000, 35000]

RANDOM_SEED: int = 20260422

# "разреженность": средняя степень ~ sqrt(n)
# Тогда число рёбер m ≈ n * sqrt(n) / 2.
SPARSITY_DEGREE_FORMULA = "sqrt(n)"

# Диапазоны весов
CHAIN_EDGE_WEIGHT: int = 1
WEIGHT_K6: Tuple[int, int] = (1, 5)
WEIGHT_K3_5: Tuple[int, int] = (1, 5)
WEIGHT_RANDOM_EDGES: Tuple[int, int] = (1, 10)

# Подграфы (непересекающиеся)
K6_SIZE: int = 6
K3_5_LEFT_SIZE: int = 3
K3_5_RIGHT_SIZE: int = 5

# Ограничение на запуск Флойда
FLOYD_MAX_N: int = 1500

# Вывод пути (чтобы консоль не засорять)
PATH_PRINT_LIMIT: int = 18

# Для проверки корректности на малых N: сравнивать Дейкстру с Флойдом полностью
COMPARE_DIJKSTRA_WITH_FLOYD_IF_AVAILABLE: bool = True


@dataclass
class GraphInfo:
    n: int
    m: int
    avg_degree: float
    is_connected: bool


@dataclass
class DijkstraStats:
    pop_count: int  # сколько раз извлекали из кучи
    relax_count: int  # сколько раз улучшали метки (релаксаций)
    settled_count: int  # сколько вершин "зафиксировали" (visited=True)
    time_sec: float


@dataclass
class FloydStats:
    time_sec: float
    used: bool
    reason: str


def _add_undirected_edge(adj: List[Dict[int, int]], u: int, v: int, w: int) -> bool:
    """Добавить ребро (u, v) веса w, если его ещё нет. Граф простой: петель и кратных рёбер нет."""
    if u == v:
        return False
    if v in adj[u]:
        return False
    adj[u][v] = w
    adj[v][u] = w
    return True


def _target_edge_count_for_sparse_graph(n: int) -> int:
    """m ≈ n * sqrt(n) / 2 (средняя степень ≈ sqrt(n))."""
    return int(n * math.sqrt(n) / 2)


def _choose_subgraph_vertices() -> Tuple[List[int], List[int], List[int]]:
    """
    Вершины:
    - K6: 0..5
    - K3,5: 6..13, где левая доля: 6,7,8; правая: 9..13
    """
    k6_vertices = list(range(0, K6_SIZE))
    left = list(range(K6_SIZE, K6_SIZE + K3_5_LEFT_SIZE))
    right = list(
        range(K6_SIZE + K3_5_LEFT_SIZE, K6_SIZE + K3_5_LEFT_SIZE + K3_5_RIGHT_SIZE)
    )
    return k6_vertices, left, right


def build_random_sparse_connected_graph(
    n: int, rng: random.Random
) -> List[Dict[int, int]]:
    """
    Генерация связного разреженного неориентированного простого графа:
    - обеспечиваем связность "цепью" (0-1-2-...-(n-1));
    - внедряем K6 и K3,5 на непересекающихся вершинах;
    - добавляем случайные ребра, чтобы средняя степень стала ~ sqrt(n).

    Представление: список словарей adj[u][v] = weight.
    """
    if n < (K6_SIZE + K3_5_LEFT_SIZE + K3_5_RIGHT_SIZE):
        raise ValueError(
            "N слишком маленькое, невозможно разместить K6 и K3,5 без пересечения."
        )

    adj: List[Dict[int, int]] = [dict() for _ in range(n)]

    k6_vertices, K3_5_left, K3_5_right = _choose_subgraph_vertices()
    K3_5_left_set = set(K3_5_left)
    K3_5_right_set = set(K3_5_right)

    # Запрещаем добавлять "лишние" рёбра внутри долей K3,5 (чтобы подграф был именно K3,5 в явном виде)
    def forbidden_extra_edge(u: int, v: int) -> bool:
        return (u in K3_5_left_set and v in K3_5_left_set) or (
            u in K3_5_right_set and v in K3_5_right_set
        )

    edge_count = 0

    # 1) Связность: цепь
    for i in range(n - 1):
        if _add_undirected_edge(adj, i, i + 1, CHAIN_EDGE_WEIGHT):
            edge_count += 1

    # 2) Подграф K6: полный граф на 6 вершинах
    w_min, w_max = WEIGHT_K6
    for i in range(len(k6_vertices)):
        for j in range(i + 1, len(k6_vertices)):
            u, v = k6_vertices[i], k6_vertices[j]
            if _add_undirected_edge(adj, u, v, rng.randint(w_min, w_max)):
                edge_count += 1

    # 3) Подграф K3,5: полный двудольный граф
    w_min, w_max = WEIGHT_K3_5
    for u in K3_5_left:
        for v in K3_5_right:
            if _add_undirected_edge(adj, u, v, rng.randint(w_min, w_max)):
                edge_count += 1

    # 4) Добавляем случайные ребра до нужной разреженности
    target_m = _target_edge_count_for_sparse_graph(n)
    degree_goal = max(2, int(math.sqrt(n)))  # примерно sqrt(n)

    w_min, w_max = WEIGHT_RANDOM_EDGES

    # Идея: для каждой вершины добиваем степень до degree_goal (пока не достигнем target_m)
    order = list(range(n))
    rng.shuffle(order)

    for u in order:
        while edge_count < target_m and len(adj[u]) < degree_goal:
            v = rng.randrange(n)
            if v == u:
                continue
            if forbidden_extra_edge(u, v):
                continue
            if _add_undirected_edge(adj, u, v, rng.randint(w_min, w_max)):
                edge_count += 1

        if edge_count >= target_m:
            break

    # Если вдруг не добрали рёбер (редко), добиваем простым циклом попыток
    # (держим запрет внутри долей K3,5)
    while edge_count < target_m:
        u = rng.randrange(n)
        v = rng.randrange(n)
        if u == v:
            continue
        if forbidden_extra_edge(u, v):
            continue
        if _add_undirected_edge(adj, u, v, rng.randint(w_min, w_max)):
            edge_count += 1

    return adj


# ============================================================
#                 ПРОВЕРКИ СВОЙСТВ (ОТЧЁТ)
# ============================================================


def count_edges(adj: List[Dict[int, int]]) -> int:
    return sum(len(nei) for nei in adj) // 2


def bfs_connected_component_size(adj: List[Dict[int, int]], start: int = 0) -> int:
    n = len(adj)
    visited = [False] * n
    q = deque([start])
    visited[start] = True
    seen = 1

    while q:
        u = q.popleft()
        for v in adj[u].keys():
            if not visited[v]:
                visited[v] = True
                seen += 1
                q.append(v)

    return seen


def describe_graph(adj: List[Dict[int, int]]) -> GraphInfo:
    n = len(adj)
    m = count_edges(adj)
    avg_degree = (2.0 * m) / n if n > 0 else 0.0
    comp_size = bfs_connected_component_size(adj, start=0)
    return GraphInfo(n=n, m=m, avg_degree=avg_degree, is_connected=(comp_size == n))


def check_k6_present(
    adj: List[Dict[int, int]], vertices: List[int]
) -> Tuple[bool, int, int]:
    """Проверка, что между каждой парой вершин из vertices есть ребро."""
    need = len(vertices) * (len(vertices) - 1) // 2
    have = 0
    missing = 0
    for i in range(len(vertices)):
        for j in range(i + 1, len(vertices)):
            u, v = vertices[i], vertices[j]
            if v in adj[u]:
                have += 1
            else:
                missing += 1
    return (missing == 0, have, need)


def check_K3_5_present(
    adj: List[Dict[int, int]], left: List[int], right: List[int]
) -> Tuple[bool, int, int, int]:
    """
    Проверка K3,5: все ребра между левыми и правыми должны существовать.
    Дополнительно считаем, есть ли рёбра внутри долей (это НЕ мешает как подграфу,
    но мы в генерации стараемся их не добавлять).
    """
    need_cross = len(left) * len(right)
    have_cross = 0
    for u in left:
        for v in right:
            if v in adj[u]:
                have_cross += 1

    # рёбра внутри долей:
    inside = 0
    for part in (left, right):
        for i in range(len(part)):
            for j in range(i + 1, len(part)):
                u, v = part[i], part[j]
                if v in adj[u]:
                    inside += 1

    return (have_cross == need_cross, have_cross, need_cross, inside)


def format_path(path: List[int], limit: int = PATH_PRINT_LIMIT) -> str:
    if not path:
        return "[]"
    if len(path) <= limit:
        return str(path)
    head = path[: limit // 2]
    tail = path[-(limit // 2) :]
    return f"{head} ... {tail} (всего вершин в пути: {len(path)})"


# ============================================================
#                 АЛГОРИТМ ДЕЙКСТРЫ
# ============================================================


def dijkstra_from_source(
    adj: List[Dict[int, int]], source: int = 0
) -> Tuple[List[float], List[int], DijkstraStats]:
    """
    Алгоритм Дейкстры для неориентированного графа с неотрицательными весами.
    Хранит:
    - dist[v] = длина кратчайшего пути от source до v
    - parent[v] = предшественник v на кратчайшем пути (для восстановления)
    """
    n = len(adj)
    inf = float("inf")

    dist = [inf] * n
    parent = [-1] * n
    fixed = [False] * n  # "путь уже известен"

    dist[source] = 0.0
    heap: List[Tuple[float, int]] = [(0.0, source)]

    pop_count = (
        0  # сколько раз извлекали вершину с минимальной меткой из кучи (heap pop)
    )
    relax_count = (
        0  # сколько раз выполнялась успешная релаксация (улучшение метки dist[v])
    )
    settled_count = 0  # сколько вершин окончательно помечено как просмотренные (метка уже минимальна)

    t0 = time.perf_counter()

    while heap:
        cur_dist, u = heapq.heappop(heap)  # достаём элемент с минимальным расстоянием
        pop_count += 1

        if fixed[u]:
            continue

        fixed[u] = True
        settled_count += 1

        # Если достали неактуальное значение — пропускаем
        if cur_dist != dist[u]:
            continue

        for v, w in adj[u].items():
            if fixed[v]:
                continue
            cand = cur_dist + w
            if cand < dist[v]:
                dist[v] = cand
                parent[v] = u
                relax_count += 1
                heapq.heappush(heap, (cand, v))

    t1 = time.perf_counter()

    stats = DijkstraStats(
        pop_count=pop_count,
        relax_count=relax_count,
        settled_count=settled_count,
        time_sec=(t1 - t0),
    )
    return dist, parent, stats


def restore_path_by_parent(parent: List[int], start: int, finish: int) -> List[int]:
    """Восстановление пути по массиву parent."""
    path: List[int] = []
    v = finish
    while v != -1:
        path.append(v)
        if v == start:
            break
        v = parent[v]
    path.reverse()
    if path and path[0] == start:
        return path
    return []


# ============================================================
#              АЛГОРИТМ ФЛОЙДА–УОРШЕЛЛА
# ============================================================


def floyd_warshall_all_pairs(
    adj: List[Dict[int, int]],
) -> Tuple[Optional[np.ndarray], FloydStats]:
    """
    Алгоритм Флойда–Уоршелла: матрица S[n,n], динамическое программирование.
    Используем оптимизацию памяти: храним только одну матрицу dist (O(n^2)).

    Сложность: O(n^3). Для больших n не запускаем (см. FLOYD_MAX_N).
    """
    n = len(adj)
    if n > FLOYD_MAX_N:
        return None, FloydStats(
            time_sec=0.0,
            used=False,
            reason=f"N={n} слишком большое для практического запуска алгоритма Флойда (O(n^3), память O(n^2)). "
            f"Увеличьте FLOYD_MAX_N, если нужно.",
        )

    INF = 10**15
    dist = np.full((n, n), INF, dtype=np.int64)
    np.fill_diagonal(dist, 0)  # путь из вершины в саму себя имеет длину 0

    # заполняем по списку смежности
    for u in range(n):
        for v, w in adj[u].items():
            if w < dist[u, v]:
                dist[u, v] = w

    # Основной цикл Флойда: S[i,j] = min(S[i,j], S[i,k] + S[k,j])
    # Чтобы меньше выделять память, используем временный буфер на строку.
    temp = np.empty(n, dtype=np.int64)

    t0 = time.perf_counter()
    for k in range(n):
        row_k = dist[k]
        for i in range(n):
            dik = dist[i, k]
            if dik >= INF:
                continue

            # temp[j] = dist[i,k] + dist[k,j]
            np.add(row_k, dik, out=temp)

            # dist[i,j] = min(dist[i,j], temp[j])
            np.minimum(dist[i], temp, out=dist[i])
    t1 = time.perf_counter()

    stats = FloydStats(time_sec=(t1 - t0), used=True, reason="OK")
    return dist, stats


# ============================================================
#                  СРАВНЕНИЕ СЛОЖНОСТИ (ОЦЕНКИ)
# ============================================================


def estimate_ops_floyd(n: int) -> int:
    return n**3


def estimate_ops_dijkstra_heap(n: int, m: int) -> float:
    # для разреженного графа: O(m log2 n) (как в лекции: релаксаций не больше m, высота кучи ~ log n)
    if n <= 1:
        return float(m)
    return float(m) * math.log2(n)


# ============================================================
#                          ЗАПУСК
# ============================================================


def run_for_one_n(n: int, base_seed: int) -> None:
    print("\n" + "=" * 110)
    print(f"ГРАФ N = {n}")
    print("=" * 110)

    rng = random.Random(base_seed + n)

    # 1) Строим граф
    t0 = time.perf_counter()
    adj = build_random_sparse_connected_graph(n, rng)
    t1 = time.perf_counter()
    build_time = t1 - t0

    info = describe_graph(adj)

    # 2) Иллюстрация свойств графа
    k6_vertices, K3_5_left, K3_5_right = _choose_subgraph_vertices()
    ok_k6, have_k6, need_k6 = check_k6_present(adj, k6_vertices)
    ok_K3_5, have_cross, need_cross, inside_edges = check_K3_5_present(
        adj, K3_5_left, K3_5_right
    )

    print("Свойства построенного графа:")
    print(f"- Построение заняло: {build_time:.4f} c")
    print(f"- Число вершин n(G) = {info.n}")
    print(f"- Число рёбер m(G) = {info.m}")
    print(
        f"- Средняя степень вершин = {info.avg_degree:.3f} (цель: sqrt(n) = {math.sqrt(n):.3f})"
    )
    print(f"- Связность: {'ГРАФ СВЯЗЕН' if info.is_connected else 'ГРАФ НЕСВЯЗЕН'}")

    print("\nПроверка наличия требуемых подграфов:")
    print(
        f"- K6 на вершинах {k6_vertices}: рёбер {have_k6} из {need_k6} -> {'OK' if ok_k6 else 'НЕТ'}"
    )
    print(
        f"- K3,5 на вершинах {K3_5_left} и {K3_5_right}: перекрёстных рёбер {have_cross} из {need_cross} -> "
        f"{'OK' if ok_K3_5 else 'НЕТ'}"
    )
    print(f"  (для наглядности) рёбер внутри долей K3,5: {inside_edges} (в идеале 0)")

    # 3) A) Алгоритм Флойда–Уоршелла
    print("\nA) Алгоритм Флойда–Уоршелла (все пары вершин):")
    dist_fw, fw_stats = floyd_warshall_all_pairs(adj)
    if fw_stats.used:
        # В связном графе все расстояния конечны (кроме INF, не должно быть)
        finite_count = int(np.sum(dist_fw < 10**15))
        print(f"- Выполнено: ДА")
        print(f"- Время: {fw_stats.time_sec:.4f} c")
        print(f"- Размер матрицы S: {dist_fw.shape[0]} x {dist_fw.shape[1]}")
        print(f"- Число ячеек с конечным расстоянием: {finite_count} из {n*n}")
        print(f"- Итерации: ~ n^3 = {estimate_ops_floyd(n):.3e}")
        print(
            f"- Пример: S[0, 0] = {int(dist_fw[0, 0])}, S[0, n-1] = {int(dist_fw[0, n-1])}"
        )
    else:
        print(f"- Выполнено: НЕТ")
        print(f"- Причина: {fw_stats.reason}")
        print(f"- Итерации: ~ n^3 = {estimate_ops_floyd(n):.3e}")

    # 4) B) Алгоритм Дейкстры
    print("\nB) Алгоритм Дейкстры (от вершины 0 до всех):")
    dist_dij, parent, dij_stats = dijkstra_from_source(adj, source=0)

    print(f"- Время: {dij_stats.time_sec:.4f} c")
    print(f"- Итерации (практические счётчики):")
    print(f"  * извлечений из очереди (heap pop): {dij_stats.pop_count}")
    print(f"  * релаксаций (улучшений меток): {dij_stats.relax_count}")
    print(
        f"  * зафиксировано вершин (visited/fixed): {dij_stats.settled_count} (в идеале n={n})"
    )

    target = n - 1
    path = restore_path_by_parent(parent, 0, target)
    if path:
        print("\nВосстановление кратчайшего пути (по массиву parent):")
        print(f"- Путь 0 -> {target}: {format_path(path)}")
        print(f"- Длина пути (число рёбер): {len(path) - 1}")
        print(f"- Вес кратчайшего пути (сумма весов): {dist_dij[target]}")
    else:
        print("\nВосстановление пути:")
        print(f"- Пути 0 -> {target} НЕТ (что странно для связного графа)")

    # 5) Сравнение алгоритмов Дейкстры и Флойда (если Флойд считали)
    if dist_fw is not None and COMPARE_DIJKSTRA_WITH_FLOYD_IF_AVAILABLE:
        fw_row0 = dist_fw[0].astype(np.float64)
        dij_vec = np.array(dist_dij, dtype=np.float64)
        diff = np.max(np.abs(fw_row0 - dij_vec))
        print("\nПроверка корректности (сравнение с Флойдом для источника 0):")
        print(f"- max |S_Floyd[0, v] - S_Dijkstra[v]| = {diff}")
        print(f"- Итог: {'OK' if diff == 0 else 'ЕСТЬ РАСХОЖДЕНИЕ'}")

    # 6) Сравнение асимптотик
    print("\nСравнение асимптотической сложности (оценка количества операций):")
    ops_fw = estimate_ops_floyd(n)
    ops_dij = estimate_ops_dijkstra_heap(n, info.m)
    ratio = (ops_fw / ops_dij) if ops_dij > 0 else float("inf")
    print(f"- Алгоритм Флойда:  O(n^3)  ~ {ops_fw:.3e}")
    print(
        f"- Алгоритм Дейкстры (куча): O(m log n) ~ {ops_dij:.3e}, где m={info.m}, log2(n)={math.log2(n):.3f}"
    )
    print(f"- Отношение (Флойда / Дейкстры) ~ {ratio:.3e}")


def main() -> None:
    print("=" * 110)
    print("ЛАБОРАТОРНАЯ РАБОТА № 7, ВАРИАНТ 4")
    print("=" * 110)
    print("Параметры:")
    print(f"- Размеры графов: {GRAPH_SIZES}")
    print(f"- Seed: {RANDOM_SEED}")
    print(f"- Разреженность: средняя степень ~ {SPARSITY_DEGREE_FORMULA}")
    print(f"- Подграфы: K6 и K3,5 (непересекающиеся)")
    print(
        f"- Запуск алгоритма Флойда только для N <= {FLOYD_MAX_N} (иначе печатается причина)"
    )

    for n in GRAPH_SIZES:
        run_for_one_n(n, RANDOM_SEED)


if __name__ == "__main__":
    main()

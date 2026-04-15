import json
import random
from collections import deque

class Network:
    """
    Класс для представления сети и вычисления максимального потока.
    Использует алгоритм Форда-Фалкерсона с поиском увеличивающего пути через BFS (алгоритм Эдмондса-Карпа).
    """

    def __init__(self, graph_data):
        """
        Инициализация сети из словаря, полученного из JSON.
        """
        self.nodes = graph_data['nodes']
        self.source_name = graph_data['source']
        self.sink_name = graph_data['sink']
        self.num_nodes = len(self.nodes)

        # Создаем удобные сопоставления между именами вершин и их индексами
        self.node_to_idx = {name: i for i, name in enumerate(self.nodes)}
        self.idx_to_node = {i: name for i, name in enumerate(self.nodes)}

        self.source_idx = self.node_to_idx[self.source_name]
        self.sink_idx = self.node_to_idx[self.sink_name]

        # Матрица пропускных способностей (capacity matrix)
        self.capacity_matrix = [[0] * self.num_nodes for _ in range(self.num_nodes)]
        for edge in graph_data['edges']:
            u = self.node_to_idx[edge['from']]
            v = self.node_to_idx[edge['to']]
            capacity = edge['capacity']
            self.capacity_matrix[u][v] = capacity
    
    def find_augmenting_path_bfs(self, residual_graph, source, sink, parent):
        """
        Поиск увеличивающего пути в остаточной сети.
        """
        visited = [False] * self.num_nodes
        queue = deque()

        # Начинаем с источника
        queue.append(source)
        visited[source] = True
        parent[source] = -1

        while queue:
            u = queue.popleft()
            # Проверяем все смежные вершины
            for v in range(self.num_nodes):
                # Если вершина не посещена и есть остаточная пропускная способность
                if not visited[v] and residual_graph[u][v] > 0:
                    print(f"    Найдено допустимое ребро "
                          f"{self.idx_to_node[u]} -> {self.idx_to_node[v]} "
                          f"(остаток = {residual_graph[u][v]})")
                    queue.append(v)
                    visited[v] = True
                    parent[v] = u # Запоминаем предка для восстановления пути
                    if v == sink:
                        print("    Сток достигнут!")
                        return True
        
        # Сток недостижим
        return False

    def ford_fulkerson(self):
        """
        Основная реализация алгоритма Форда-Фалкерсона.
        """
        # Создаем остаточную сеть, которая в начале равна исходной сети
        residual_graph = [row[:] for row in self.capacity_matrix]
        
        # Массив для хранения найденного пути (используется для "пометки вершин")
        parent = [None] * self.num_nodes
        max_flow = 0
        
        iteration = 1
        print("Начало работы алгоритма Форда-Фалкерсона.")
        
        # Ищем увеличивающие пути, пока они существуют
        while self.find_augmenting_path_bfs(residual_graph, self.source_idx, self.sink_idx, parent):
            print(f"\n--- Итерация {iteration} ---")
            
            # Находим минимальную остаточную пропускную способность на найденном пути
            path_flow = float('Inf')
            s = self.sink_idx
            path_nodes_idx = []
            while s != self.source_idx:
                path_nodes_idx.append(s)

                u = parent[s]
                print(f"    {self.idx_to_node[u]} -> {self.idx_to_node[s]} "
                      f"(остаток = {residual_graph[u][s]})")
                path_flow = min(path_flow, residual_graph[parent[s]][s])
                s = parent[s]
            path_nodes_idx.append(self.source_idx)
            path_nodes_idx.reverse()

            path_nodes_names = [self.idx_to_node[i] for i in path_nodes_idx]
            print(f"Найден увеличивающий путь: {' -> '.join(path_nodes_names)}")
            print(f"Пропускная способность пути: {path_flow}")

            # Обновляем остаточную сеть:
            # - Уменьшаем пропускную способность вдоль пути
            # - Увеличиваем пропускную способность в обратном направлении
            print("  Обновляем остаточную сеть:")
            v = self.sink_idx
            while v != self.source_idx:
                u = parent[v]
                print(f"    Уменьшаем {self.idx_to_node[u]} -> {self.idx_to_node[v]} на {path_flow}")
                print(f"    Увеличиваем {self.idx_to_node[v]} -> {self.idx_to_node[u]} на {path_flow}")
                residual_graph[u][v] -= path_flow
                residual_graph[v][u] += path_flow
                v = parent[v]

            # Добавляем найденный поток к общему
            max_flow += path_flow
            print(f"Текущий общий поток: {max_flow}")
            iteration += 1

        print("\nУвеличивающих путей больше не найдено. Алгоритм завершен.")
        
        # --- Находим минимальный разрез ---
        # Множество A: все вершины, достижимые из источника в КОНЕЧНОЙ остаточной сети
        # Множество B: все остальные вершины
        
        source_side_nodes_idx = []
        queue = deque([self.source_idx])
        visited_for_cut = {self.source_idx}
        
        while queue:
            u = queue.popleft()
            source_side_nodes_idx.append(u)
            for v in range(self.num_nodes):
                if v not in visited_for_cut and residual_graph[u][v] > 0:
                    visited_for_cut.add(v)
                    queue.append(v)
                    
        source_side_nodes = {self.idx_to_node[i] for i in source_side_nodes_idx}
        sink_side_nodes = set(self.nodes) - source_side_nodes
        
        return max_flow, source_side_nodes, sink_side_nodes

    def print_results(self, max_flow, source_side_nodes, sink_side_nodes):
        """
        Красиво выводит результаты.
        """
        print(f"\n==================== РЕЗУЛЬТАТ ====================")
        print(f"Максимальный поток из '{self.source_name}' в '{self.sink_name}': {max_flow}")
        
        print("\nМинимальный разрез (согласно теореме Форда-Фалкерсона):")
        
        print(f"  - Формальное описание: вершины разделены на два множества:")
        print(f"    - Множество A (сторона источника): {sorted(list(source_side_nodes))}")
        print(f"    - Множество B (сторона стока):     {sorted(list(sink_side_nodes))}")

        print("\n  - Графическое описание (дуги, идущие из множества A во множество B):")
        cut_capacity = 0
        cut_edges = []
        for u_idx in range(self.num_nodes):
            for v_idx in range(self.num_nodes):
                u_name = self.idx_to_node[u_idx]
                v_name = self.idx_to_node[v_idx]
                # Если дуга идет из A в B и имеет пропускную способность
                if u_name in source_side_nodes and v_name in sink_side_nodes and self.capacity_matrix[u_idx][v_idx] > 0:
                    capacity = self.capacity_matrix[u_idx][v_idx]
                    cut_edges.append(f"    - Дуга {u_name} -> {v_name} с пропускной способностью {capacity}")
                    cut_capacity += capacity
        
        for edge_str in cut_edges:
            print(edge_str)
            
        print(f"\nПропускная способность разреза (сумма способностей дуг): {cut_capacity}")
        print(f"Проверка по теореме: Макс.поток ({max_flow}) == Пропускная способность мин.разреза ({cut_capacity})")


def main():
    json_data_string = """
    {
      "nodes": ["A", "B", "C", "D", "E", "F", "G", "H", "I"],
      "edges": [
        {"from": "A", "to": "B", "capacity": 22},
        {"from": "A", "to": "C", "capacity": 9},
        {"from": "A", "to": "I", "capacity": 37},
        {"from": "B", "to": "C", "capacity": 6},
        {"from": "B", "to": "I", "capacity": 6},
        {"from": "B", "to": "G", "capacity": 43},
        {"from": "I", "to": "C", "capacity": 41},
        {"from": "I", "to": "H", "capacity": 7},
        {"from": "I", "to": "G", "capacity": 6},
        {"from": "H", "to": "C", "capacity": 7},
        {"from": "H", "to": "G", "capacity": 7},
        {"from": "H", "to": "F", "capacity": 7},
        {"from": "G", "to": "C", "capacity": 7},
        {"from": "G", "to": "F", "capacity": 3},
        {"from": "G", "to": "E", "capacity": 3},
        {"from": "F", "to": "C", "capacity": 6},
        {"from": "F", "to": "D", "capacity": 7},
        {"from": "F", "to": "E", "capacity": 33},
        {"from": "D", "to": "C", "capacity": 42},
        {"from": "E", "to": "D", "capacity": 7}
      ],
      "source": "A",
      "sink": "C"
    }
    """
    network_data = json.loads(json_data_string)

    print("ЗАДАНИЕ 1: Максимальный поток для исходной сети")

    net1 = Network(network_data)
    max_flow1, source_side1, sink_side1 = net1.ford_fulkerson()
    net1.print_results(max_flow1, source_side1, sink_side1)

    print("ЗАДАНИЕ 2: Сеть со случайными пропускными способностями")
    
    # Модифицируем пропускные способности
    random_network_data = json.loads(json_data_string) # Создаем копию
    
    print("Генерация случайных пропускных способностей в диапазоне [100, 1000]...")
    for edge in random_network_data['edges']:
        edge['capacity'] = random.randint(100, 1000)
        
    net2 = Network(random_network_data)
    max_flow2, source_side2, sink_side2 = net2.ford_fulkerson()
    net2.print_results(max_flow2, source_side2, sink_side2)

if __name__ == "__main__":
    main()

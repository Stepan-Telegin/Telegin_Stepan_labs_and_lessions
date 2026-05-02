import itertools
import networkx as nx
import matplotlib.pyplot as plt
import itertools

def check_isomorphism_by_bruteforce(edges1, vertices1, edges2, vertices2):
    """
    Проверяет изоморфизм графов G1 и G2 методом полного перебора биекций.
    ВНИМАНИЕ: Очень медленно для графов с > 8-9 вершинами.
    """
    
    # Ребра храним в отсортированном виде, т.к. граф неориентированный.
    # Например, (1, 3) и (3, 1) — это одно и то же ребро.
    set_edges1 = {tuple(sorted(e)) for e in edges1}
    # Еще нам понадобится множество ребер G2.
    set_edges2 = {tuple(sorted(e)) for e in edges2}
    
    # `vertices1` у нас отсортированы (0, 1, 2, ...), `vertices2` тоже.
    # Мы будем сопоставлять i-ю вершину из `vertices1` с i-й вершиной из `permuted_v2`.
    for permuted_v2 in itertools.permutations(vertices2):
        
        mapping = {vertices1[i]: permuted_v2[i] for i in range(len(vertices1))}
        
        # Теперь нужно проверить, сохраняет ли это отображение ребра.
        # Для этого создадим "новый" граф G1_mapped, применив наше отображение к G1.
        # И сравним его с G2.
        
        is_mapping_valid = True
        
        # Проверяем каждое ребро из G1
        for edge1 in set_edges1:
            u1, v1 = edge1
            
            # Применяем отображение
            u2_mapped = mapping[u1]
            v2_mapped = mapping[v1]
            
            # Создаем соответствующее ребро в пространстве G2
            mapped_edge = tuple(sorted((u2_mapped, v2_mapped)))
            
            # Проверяем, существует ли такое ребро в G2.
            if mapped_edge not in set_edges2:
                # Если хотя бы одно ребро не нашлось, эта биекция неверная.
                is_mapping_valid = False
                break # Прерываем проверку текущей биекции, переходим к следующей.
        
        if is_mapping_valid:
            # Если мы прошли весь цикл и все ребра G1 были успешно отображены в ребра G2,
            # то мы нашли изоморфизм!
            # (Поскольку число ребер одинаково, обратная проверка не нужна)
            return True, mapping # Возвращаем True и само отображение

    # Если мы перебрали все 3.6 миллиона перестановок и ни одна не подошла
    return False, None # Возвращаем False, изоморфизма нет

# --- Исходные данные из задания ---

# Два простых графа заданы списками ребер:
edges_g1 = [
    (0, 1), (0, 2), (0, 8), (1, 2), (1, 3), (1, 9),
    (2, 3), (2, 5), (2, 6), (2, 8), (2, 9), (3, 4),
    (3, 7), (3, 8), (3, 9), (4, 5), (4, 8), (5, 6),
    (5, 8), (6, 7), (6, 9), (7, 8), (7, 9), (8, 9)
]

edges_g2 = [
    (0, 1), (0, 3), (0, 5), (0, 6), (0, 7), (0, 8),
    (0, 9), (1, 3), (1, 4), (1, 6), (1, 7), (1, 9),
    (2, 3), (2, 6), (2, 8), (3, 4), (3, 5), (3, 6),
    (3, 8), (4, 6), (4, 9), (5, 7), (6, 7), (8, 9)
]

# --- Вспомогательные функции ---

def get_vertices_from_edges(edges):
    """Получает отсортированный список уникальных вершин из списка ребер."""
    vertices = set()
    for u, v in edges:
        vertices.add(u)
        vertices.add(v)
    return sorted(list(vertices))

def build_adjacency_list(edges, vertices):
    """Строит список смежности по списку ребер."""
    adj_list = {v: [] for v in vertices}
    for u, v in edges:
        adj_list[u].append(v)
        adj_list[v].append(u)
    # Сортируем списки соседей
    for v in adj_list:
        adj_list[v].sort()
    return adj_list

def calculate_degrees(adj_list):
    """Вычисляет степени вершин."""
    degrees = {v: len(adj_list[v]) for v in adj_list}
    return degrees

def draw_graph(edges, vertices, title, layout_func=nx.spring_layout):
    """Строит чертеж графа с помощью networkx и matplotlib."""
    G = nx.Graph()
    G.add_nodes_from(vertices)
    G.add_edges_from(edges)
    
    plt.figure(figsize=(8, 8))
    pos = layout_func(G)
    nx.draw_networkx_nodes(G, pos, node_size=700, node_color='skyblue')
    nx.draw_networkx_edges(G, pos, width=1.5, alpha=0.8)
    nx.draw_networkx_labels(G, pos, font_size=12, font_family='sans-serif')
    plt.title(title, size=15)
    plt.axis('off') # Отключаем оси

# --- Функции для выполнения заданий ---

def task_isomorphism(edges1, edges2):
    """
    Для изоморфизма необходимо, чтобы инварианты графов совпадали.
    Проверим основные инварианты: число вершин, число ребер и последовательность степеней.
    """
    print("--- 1. Проверка на изоморфизм графов G1 и G2 ---")
    
    vertices1 = get_vertices_from_edges(edges1)
    vertices2 = get_vertices_from_edges(edges2)
    
    # 1. Проверка числа вершин
    num_vertices1 = len(vertices1)
    num_vertices2 = len(vertices2)
    print(f"Число вершин G1: {num_vertices1}")
    print(f"Число вершин G2: {num_vertices2}")
    if num_vertices1 != num_vertices2:
        print("\nРезультат: Графы не изоморфны, так как число вершин не совпадает.")
        return

    # 2. Проверка числа ребер
    num_edges1 = len(edges1)
    num_edges2 = len(edges2)
    print(f"Число ребер G1: {num_edges1}")
    print(f"Число ребер G2: {num_edges2}")
    if num_edges1 != num_edges2:
        print("\nРезультат: Графы не изоморфны, так как число ребер не совпадает.")
        return

    # 3. Проверка последовательности степеней
    adj_list1 = build_adjacency_list(edges1, vertices1)
    adj_list2 = build_adjacency_list(edges2, vertices2)
    degrees1 = calculate_degrees(adj_list1)
    degrees2 = calculate_degrees(adj_list2)
    
    degree_sequence1 = sorted(degrees1.values())
    degree_sequence2 = sorted(degrees2.values())
    
    print(f"Последовательность степеней G1: {degree_sequence1}")
    print(f"Последовательность степеней G2: {degree_sequence2}")
    
    if degree_sequence1 != degree_sequence2:
        print("\nРезультат: Графы не изоморфны, так как их последовательности степеней не совпадают.")
        return
        
    print("\nИнварианты (число вершин, ребер, последовательности степеней) совпадают.")
    print("Это необходимое, но не достаточное условие. Продолжаем проверку перебором биекций.")

    print("Но для 10 вершин это займет очень много времени (10! = 3628800 итераций).")
    print("Вместо этого мы используем эффективную библиотечную реализацию.")
    
    # --- Закомментированный вызов медленной функции ---
    # Если раскомментировать следующую строку, запустится полный перебор.
    # Но делать этого не стоит, можно ждать несколько минут или даже дольше.
    
    # is_isomorphic, mapping = check_isomorphism_by_bruteforce(edges1, vertices1, edges2, vertices2)
    # if is_isomorphic:
    #     print("\nРезультат (полный перебор): Графы ИЗОМОРФНЫ.")
    #     print("Найденное отображение:", mapping)
    # else:
    #     print("\nРезультат (полный перебор): Графы НЕ ИЗОМОРФНЫ.")

    # Используем NetworkX для проверки изоморфизма, так как полный перебор (10! = 3628800) очень долог.
    # Это эффективная реализация того же принципа.
    G1_nx = nx.Graph(edges1)
    G2_nx = nx.Graph(edges2)
    
    isomorphic_checker = nx.isomorphism.GraphMatcher(G1_nx, G2_nx)
    
    if isomorphic_checker.is_isomorphic():
        isomorphism_map = isomorphic_checker.mapping
        print("\nРезультат: Графы G1 и G2 ИЗОМОРФНЫ.")
        print("Изоморфизм (одно из возможных отображений вершин G1 в G2):")

        print("f: V(G1) -> V(G2)")
        for v1, v2 in sorted(isomorphism_map.items()):
            print(f"  {v1} -> {v2}")
    else:
        print("\nРезультат: Графы G1 и G2 НЕ ИЗОМОРФНЫ после полной проверки.")

def tasks_for_g1(edges, vertices):
    """Выполняет все задания для графа G1."""
    adj_list = build_adjacency_list(edges, vertices)
    
    print("\n--- 2. Задания для графа G1 ---")
    
    # 2.1 Чертеж
    print("\n2.1. Построение чертежа графа G1...")
    draw_graph(edges, vertices, "Чертеж графа G1")
    print(" -> Чертеж G1 будет показан в отдельном окне.")
    
    # 2.2 Список смежности
    print("\n2.2. Список смежности графа G1:")
    for vertex, neighbors in adj_list.items():
        print(f"  {vertex}: {neighbors}")

    # 2.3 Матрица смежности
    print("\n2.3. Матрица смежности графа G1:")
    num_vertices = len(vertices)
    adj_matrix = [[0] * num_vertices for _ in range(num_vertices)]
    for u, v in edges:
        adj_matrix[u][v] = 1
        adj_matrix[v][u] = 1
    # Вывод шапки
    print("    " + " ".join(map(str, vertices)))
    print("   " + "-" * (2 * num_vertices))
    for i, row in enumerate(adj_matrix):
        print(f"{i} | " + " ".join(map(str, row)))

        # 2.4 Матрица инцидентности
    print("\n2.4. Матрица инцидентности графа G1:")
    num_edges = len(edges)
    inc_matrix = [[0] * num_edges for _ in range(num_vertices)]
    # Создаем обозначения для ребер
    edge_names = {i: f"e{i+1}" for i in range(num_edges)} 
    
    # Заполнение матрицы
    for j, edge in enumerate(edges):
        u, v = edge
        inc_matrix[u][j] = 1
        inc_matrix[v][j] = 1
        
    print(f"(матрица {num_vertices} вершин x {num_edges} ребер)")
    
    header = "   "
    for i in range(num_edges):
        header += f" {edge_names[i]:>3}"
    print(header)
    
    print("   " + "-" * (len(header) - 3))
    
    for i, row in enumerate(inc_matrix):
        row_str = f"{i:<2} |"
        for val in row:
            row_str += f" {val:^3}"
        print(row_str)


    # 2.5 Вектор степеней вершин
    print("\n2.5. Вектор степеней вершин графа G1:")
    degrees = calculate_degrees(adj_list)
    sorted_degrees = sorted(degrees.items())
    for vertex, degree in sorted_degrees:
        print(f"  Степень вершины {vertex}: {degree}")

    # 2.6 Дополнение графа
    print("\n2.6. Дополнение графа G1:")
    # Согласно определению, дополнение G_bar содержит те ребра, которых нет в G
    all_possible_edges = set(itertools.combinations(vertices, 2))
    existing_edges_set = {tuple(sorted(e)) for e in edges}
    complement_edges = list(all_possible_edges - existing_edges_set)
    
    print("Список ребер дополнения графа G1_bar:")
    # Выводим ребра порциями для читаемости
    line_break = 8
    for i in range(0, len(complement_edges), line_break):
        print("  " + ", ".join(map(str, complement_edges[i:i+line_break])))
    
    print("\nПостроение чертежа дополнения графа G1...")
    draw_graph(complement_edges, vertices, "Чертеж дополнения графа G1_bar")
    print(" -> Чертеж дополнения G1 будет показан в отдельном окне.")
    
    # 2.7 Два длинных цикла
    print("\n2.7. Поиск двух длинных циклов в G1:")
    # Будем искать простые циклы с помощью DFS ("Обход в глубину", Depth-First Search)
    all_cycles = []
    
    def find_all_cycles_util(u, visited, path):
        visited[u] = True
        path.append(u)
        
        for v in adj_list[u]:
            if not visited[v]:
                find_all_cycles_util(v, visited, path)

            # Если соседняя вершина посещена и не является родителем в пути DFS (т.е. не предпоследняя)
            # и является начальной вершиной, и длина цикла > 2, то это простой цикл
            elif v == path[0] and len(path) > 2:
                # Нормализуем цикл, чтобы избежать дубликатов (1-2-3-1 и 2-3-1-2)
                # путем сортировки, начиная с минимального элемента
                start_index = path.index(min(path))
                normalized_cycle = path[start_index:] + path[:start_index]
                if normalized_cycle not in all_cycles:
                    all_cycles.append(normalized_cycle)
        
        path.pop()
        visited[u] = False

    # Ищем циклы, начиная с каждой вершины
    for start_node in vertices:
        visited = {v: False for v in vertices}
        find_all_cycles_util(start_node, visited, [])
    
    if all_cycles:
        # Сортируем циклы по убыванию длины
        all_cycles.sort(key=len, reverse=True)
        print("Найденные циклы отсортированы по длине.")
        print(f"Самый длинный цикл: {all_cycles[0]} (длина {len(all_cycles[0])})")
        if len(all_cycles) > 1:
            print(f"Второй по длине цикл: {all_cycles[1]} (длина {len(all_cycles[1])})")
        else:
            print("Найден только один цикл.")
    else:
        print("В графе не найдено циклов.")

    # 2.8 Подграф K4
    print("\n2.8. Поиск подграфа K4 (полный граф на 4 вершинах):")
    # Полный граф K4 - это полный граф на 4 вершинах
    # Проверим все комбинации из 4 вершин
    found_k4 = None
    for combo in itertools.combinations(vertices, 4):
        is_full = True
        # Проверяем, что каждая пара вершин в комбинации соединена ребром
        for u, v in itertools.combinations(combo, 2):
            if v not in adj_list[u]:
                is_full = False
                break
        if is_full:
            found_k4 = combo
            break
            
    if found_k4:
        print(f"Результат: В графе G1 НАЙДЕН подграф K4 на вершинах: {list(found_k4)}")
    else:
        print("Результат: В графе G1 подграф K4 НЕ НАЙДЕН.")
        
    # 2.9 Реберный граф
    print("\n2.9. Построение реберного графа для G1:")
    # Согласно определению, вершины реберного графа - это ребра исходного графа.
    # Две вершины в реберном графе соединены, если их соответствующие ребра в G1 имеют общую вершину.
    
    line_graph_edges = []
    # Ребра G1 становятся вершинами L(G1)
    original_edges_list = [tuple(sorted(e)) for e in edges]

    # Перебираем все уникальные пары ребер из G1
    for i in range(len(original_edges_list)):
        for j in range(i + 1, len(original_edges_list)):
            edge1 = original_edges_list[i]
            edge2 = original_edges_list[j]
            
            # Проверяем, есть ли общая вершина
            if len(set(edge1) & set(edge2)) > 0:
                # Новые вершины - это сами ребра (представленные в виде строк для networkx)
                line_graph_edges.append((str(edge1), str(edge2)))

    line_graph_vertices = [str(e) for e in original_edges_list]
    print(f"Реберный граф L(G1) имеет {len(line_graph_vertices)} вершин и {len(line_graph_edges)} ребер.")
    print("Построение чертежа реберного графа L(G1)...")
    # Чертеж реберного графа может быть очень плотным, используем circular_layout
    draw_graph(line_graph_edges, line_graph_vertices, "Чертеж реберного графа L(G1)", layout_func=nx.circular_layout)
    print(" -> Чертеж реберного графа L(G1) будет показан в отдельном окне.")


if __name__ == "__main__":
    
    # Задание на изоморфизм
    task_isomorphism(edges_g1, edges_g2)
    
    print("-" * 50)

    # Задания для графа G1
    g1_vertices = get_vertices_from_edges(edges_g1)
    tasks_for_g1(edges_g1, g1_vertices)
    
    # Показать все созданные чертежи
    plt.show()
class GraphColoring:
    def __init__(self, num_vertices):
        self.num_vertices = num_vertices
        self.graph_matrix = [
            [0 for _ in range(num_vertices)] for _ in range(num_vertices)
        ]

    def is_safe(self, vertex_index, color, colors_solution):
        for i in range(self.num_vertices):
            if self.graph_matrix[vertex_index][i] == 1 and colors_solution[i] == color:
                return False
        return True

    def solve_recursive(self, max_colors, colors_solution, vertex_index):
        if vertex_index == self.num_vertices:
            return True

        for color in range(1, max_colors + 1):

            if self.is_safe(vertex_index, color, colors_solution):

                colors_solution[vertex_index] = color

                if self.solve_recursive(max_colors, colors_solution, vertex_index + 1):
                    return True

                colors_solution[vertex_index] = 0

        return False

    def start_coloring(self, m_colors):
        colors_solution = [0] * self.num_vertices

        if not self.solve_recursive(m_colors, colors_solution, 0):
            print(f"Решения с {m_colors} цветами не существует.")
            return False

        print("Решение найдено. Раскраска вершин:")
        for idx, color in enumerate(colors_solution):
            print(f"Vertex {idx}: Color {color}")
        return True


if __name__ == "__main__":
    g = GraphColoring(4)

    g.graph_matrix = [
        [0, 1, 1, 1], 
        [1, 0, 1, 0], 
        [1, 1, 0, 1], 
        [1, 0, 1, 0]
    ]

    num_colors = 3
    g.start_coloring(num_colors)

# Проверить является ли граф деревом или нет

from typing import TypeVar

from programming_methods.lections.first_doc.fifth_block.core.base import \
    BaseUnWeightedGraph
from programming_methods.lections.first_doc.fifth_block.core.unweighted.nonoriented import \
    NonOrientedGraph

T = TypeVar("T")


def is_tree(graph: BaseUnWeightedGraph[T]) -> bool:
    visited: set[T] = set()

    # Получаем список всех вершин
    vertices: list[T] = graph.vertices

    # Если граф пустой, это не дерево
    if not vertices:
        return False

    # DFS для проверки на циклы и связность
    def dfs(v: T, parent: T) -> bool:
        visited.add(v)
        for neighbor in graph.get_neighbors(v):
            if neighbor == parent:
                continue  # Не возвращаемся по ребру, по которому пришли
            if neighbor in visited:
                return False  # Найден цикл
            if not dfs(neighbor, v):
                return False
        return True

    # Стартуем DFS с первой вершины
    start_vertex = vertices[0]
    if not dfs(start_vertex, None):
        return False  # Есть цикл

    # Проверяем связность: все вершины должны быть посещены
    if len(visited) != len(vertices):
        return False

    # Проверяем количество рёбер
    edge_count = sum(len(graph.get_neighbors(v)) for v in vertices) // 2
    if edge_count != len(vertices) - 1:
        return False

    return True


def main() -> None:
    tree_graph = NonOrientedGraph[str]()
    tree_graph.add_edge("A", "B")
    tree_graph.add_edge("A", "C")
    tree_graph.add_edge("B", "D")
    tree_graph.add_edge("B", "E")

    # Пример графа с циклом (не дерево)
    cyclic_graph = NonOrientedGraph[str]()
    cyclic_graph.add_edge("A", "B")
    cyclic_graph.add_edge("B", "C")
    cyclic_graph.add_edge("C", "A")

    # Пример несвязного графа (не дерево)
    disconnected_graph = NonOrientedGraph[str]()
    disconnected_graph.add_edge("A", "B")
    disconnected_graph.add_edge("C", "D")

    # Проверка деревьев
    print("Tree Graph is tree:", is_tree(tree_graph))  # True
    print("Cyclic Graph is tree:", is_tree(cyclic_graph))  # False
    print("Disconnected Graph is tree:", is_tree(disconnected_graph))  # False


if __name__ == "__main__":
    main()

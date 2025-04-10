# Посчитать количество ребер в графе
from typing import TypeVar

from programming_methods.lections.first_doc.fifth_block.core.base import \
    BaseGraph
from programming_methods.lections.first_doc.fifth_block.core.unweighted.nonoriented import \
    NonOrientedGraph as UnWeightedNonOrientedGraph
from programming_methods.lections.first_doc.fifth_block.core.unweighted.oriented import \
    OrientedGraph as UnWeightedOrientedGraph
from programming_methods.lections.first_doc.fifth_block.core.weighted.nonoriented import \
    NonOrientedGraph as WeightedNonOrientedGraph
from programming_methods.lections.first_doc.fifth_block.core.weighted.oriented import \
    OrientedGraph as WeightedOrientedGraph

T = TypeVar("T")


def count_graph_edges(graph: BaseGraph[T]) -> int:
    vertices = list(graph.vertices)
    total_edges = sum(len(graph.get_neighbors(v)) for v in vertices)

    # Проверяем по типу графа — ориентированный или неориентированный
    if isinstance(graph, (UnWeightedNonOrientedGraph, WeightedNonOrientedGraph)):
        # В неориентированном графе каждое ребро считается дважды
        return total_edges // 2
    elif isinstance(graph, (UnWeightedOrientedGraph, WeightedOrientedGraph)):
        # В ориентированном графе рёбра считаются один раз
        return total_edges
    raise TypeError("Граф должен быть либо ориентированным, либо неориентированным.")


def main() -> None:
    # Неориентированный граф
    non_oriented_graph = UnWeightedNonOrientedGraph[str]()
    non_oriented_graph.add_edge("A", "B")
    non_oriented_graph.add_edge("A", "C")
    non_oriented_graph.add_edge("B", "D")

    print("NonOrientedGraph edges:", count_graph_edges(non_oriented_graph))
    # Должно быть 3 (A-B, A-C, B-D)

    # Ориентированный граф
    oriented_graph = UnWeightedOrientedGraph[str]()
    oriented_graph.add_edge("A", "B")
    oriented_graph.add_edge("B", "C")
    oriented_graph.add_edge("C", "A")
    oriented_graph.add_edge("A", "D")
    oriented_graph.add_edge("D", "A")

    print("OrientedGraph edges:", count_graph_edges(oriented_graph))
    # Должно быть 5

    # Доп. тесты
    empty_graph = UnWeightedNonOrientedGraph[str]()
    print("Empty NonOrientedGraph edges:", count_graph_edges(empty_graph))  # 0

    empty_oriented_graph = UnWeightedOrientedGraph[str]()
    print("Empty OrientedGraph edges:", count_graph_edges(empty_oriented_graph))  # 0


if __name__ == "__main__":
    main()

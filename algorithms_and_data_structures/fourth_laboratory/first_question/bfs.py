from queue import Queue
from typing import TypeVar, List

from algorithms_and_data_structures.fourth_laboratory.first_question.core.base import BaseGraph

T = TypeVar('T')


def bfs(graph: BaseGraph[T], start_node: T, target_node: T) -> List[T]:
    # Set of visited nodes to prevent loops
    visited: set[T] = set()
    queue: Queue[T] = Queue()

    # Add the start_node to the queue and visited list
    queue.put(start_node)
    visited.add(start_node)

    # start_node has no parents
    parent: dict[T, T] = {start_node: None}

    # Perform BFS
    path_found = False
    while not queue.empty():
        current_node = queue.get()
        if current_node == target_node:
            path_found = True
            break

        for next_node in graph.get_neighbors(current_node):
            if next_node not in visited:
                queue.put(next_node)
                parent[next_node] = current_node
                visited.add(next_node)

    # Path reconstruction
    path: List[T] = []
    if path_found:
        path.append(target_node)
        while parent[target_node] is not None:
            path.append(parent[target_node])
            target_node = parent[target_node]
        path.reverse()
    return path

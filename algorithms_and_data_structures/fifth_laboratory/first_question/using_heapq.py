import heapq
from typing import List

from algorithms_and_data_structures.core.types import CT


def heap_sort(list_for_sort: List[CT]) -> List[CT]:
    heapq.heapify(list_for_sort)
    return [heapq.heappop(list_for_sort) for i in range(len(list_for_sort))]

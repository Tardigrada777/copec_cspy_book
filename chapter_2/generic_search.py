from __future__ import annotations
from typing import TypeVar, Iterable, Sequence, Generic, List, Callable, Set, Deque, Dict, Any, Optional
from typing_extensions import Protocol
from heapq import heappush, heappop

T = TypeVar('T')

# обощенная функция линейного поиска
def linear_contains(iterable: Iterable[T], key: T) -> bool:
    for item in iterable:
        if item == key:
            return True
    return False

C = TypeVar('C', bound='Comparable')
class Comparable(Protocol):
    def __eq__(self, other: Any) -> bool:
        return self == other

    def __lt__(self: C, other: Any) -> bool:
        return self < other

    # больше чем
    def __gt__(self: C, other: C) -> bool:
        return (not self < other) and self != other

    # больше или равно
    def __ge__(self: C, other: C) -> bool:
        return not self < other

# обощенная функция бинарного поиска
def binary_contains(sequence: Sequence[C], key: C) -> bool:
    low: int = 0
    high: int = len(sequence) - 1
    while low <= high:
        mid: int = (low + high) // 2
        if sequence[mid] < key:
            low = mid + 1
        elif sequence[mid] > key:
            high = mid - 1
        else:
            return True
    return False

# обобщенный стек
class Stack(Generic[T]):
    def __init__(self) -> None:
        self._container: List[T] = []

    @property
    def empty(self) -> bool:
        return not self._container

    def push(self, item: T) -> None:
        self._container.append(item)

    def pop(self) -> T:
        self._container.pop()

    def __repr__(self) -> str:
        return repr(self._container)

if __name__ == '__main__':
    print(linear_contains([1, 5, 15, 15, 15, 15, 20], 5)) # True
    print(binary_contains(['a', 'c', 'e', 'x'], 'x')) # True
    print(binary_contains(['john', 'mark', 'sarah'], 'bob')) # False


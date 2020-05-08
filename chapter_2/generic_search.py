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
        return self._container.pop()

    def __repr__(self) -> str:
        return repr(self._container)

# очередь
class Queue(Generic[T]):
    def __init__(self):
        self._container: Deque[T] = Deque()

    @property
    def empty(self) -> bool:
        return not self._container

    def push(self, item: T) -> None:
        self._container.append(item) # добавляем новые элементы в конец (справа)

    def pop(self) -> T:
        self._container.popleft() # красивый способ извлечь первый (левый) элемент

    def __repr__(self) -> str:
        return repr(self._container)


class Node(Generic[T]):
    def __init__(self, state: T, parent: Optional[Node], cost: float = 0.0, heuristic: float = 0.0) -> None:
        self.state: T = state
        self.parent: Optional[Node] = parent
        self.cost: float = cost
        self.heuristic: float = heuristic
    
    def __lt__(self, other: Node) -> bool:
        return (self.cost + self.heuristic) < (other.cost + other.heuristic)

# функция, которая извлечет из Node путь по лабиринту
def node_to_path(node: Node[T]) -> List[T]:
    path: List[T] = [node.state]
    # двигаемся от конца к началу
    while node.parent is not None:
        node = node.parent
        path.append(node.state)
    path.reverse()
    return path

# поиск в глубину
def dfs(initial: T, goal_test: Callable[[T], bool], successors: Callable[[T], List[T]]) -> Optional[Node[T]]:
    # frontier - то, что нужно проверить
    frontier: Stack[Node[T]] = Stack()
    frontier.push(Node(initial, None))

    # explored - где мы уже побывали
    explored: Set[T] = {initial}

    # пока есть что просматривать, просматриваем frontier
    while not frontier.empty:
        current_node: Node[T] = frontier.pop()
        current_state: T = current_node.state
        # если мы нашли искомое, то заканчиваем
        if goal_test(current_state):
            return current_node
        # проверяем куда можно идти дальше
        for child in successors(current_state):
            if child in explored: # пропускаем состояния, которые уже исследовали
                continue
            explored.add(child)
            frontier.push(Node(child, current_node))
    return None # все состояния проверили, пути к цели не нашли

# поиск в ширину
def bfs(initial: T, goal_test: Callable[[T], bool], successors: Callable[[T], List[T]]) -> Optional[Node[T]]:
    # frontier - то, что нужно проверить
    frontier: Queue[Node[T]] = Queue()
    frontier.push(Node(initial, None))

    # explored - где мы уже побывали
    explored: Set[T] = {initial}

    # пока есть что просматривать, просматриваем frontier
    while not frontier.empty:
        current_node: Node[T] = frontier.pop()
        current_state: T = current_node.state
        # если мы нашли искомое, то заканчиваем
        if goal_test(current_state):
            return current_node
        # проверяем куда можно идти дальше
        for child in successors(current_state):
            if child in explored: # пропускаем состояния, которые уже исследовали
                continue
            explored.add(child)
            frontier.push(Node(child, current_node))
    return None # все состояния проверили, пути к цели не нашли
        


if __name__ == '__main__':
    print(linear_contains([1, 5, 15, 15, 15, 15, 20], 5)) # True
    print(binary_contains(['a', 'c', 'e', 'x'], 'x')) # True
    print(binary_contains(['john', 'mark', 'sarah'], 'bob')) # False


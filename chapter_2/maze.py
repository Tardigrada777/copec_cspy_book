from enum import Enum
from typing import List, NamedTuple, Callable, Optional
import random
from math import sqrt
from generic_search import dfs, bfs, astar, node_to_path, Node


# одна конкретная ячейка лабиринта
class Cell(str, Enum):
    EMPTY = '.'
    BLOCKED = 'X'
    START = 'S'
    GOAL = 'G'
    PATH = '*'

# координаты ячейки в лабиринте
class MazeLocation(NamedTuple):
    row: int
    column: int


# лабиринт
class Maze:
    def __init__(self, rows: int = 10, columns: int = 10, sparseness: float = 0.2,
                 start: MazeLocation = MazeLocation(0, 0), goal: MazeLocation = MazeLocation(9, 9)) -> None:
        self._rows: int = rows
        self._columns: int = columns
        self.start: MazeLocation = start
        self.goal: MazeLocation = goal
        # заполнение сетки пустыми ячейками
        self._grid: List[List[Cell]] = [[Cell.EMPTY for c in range(columns)] for r in range(rows)]
        # заполнение сетки заблокированными ячейками
        self._randomly_fill(rows, columns, sparseness)
        # заполнение начальной и конечной позиций в лабиринте
        self._grid[start.row][start.column] = Cell.START
        self._grid[goal.row][goal.column] = Cell.GOAL

    def _randomly_fill(self, rows: int, columns: int, sparseness: float):
        for row in range(rows):
            for column in range(columns):
                if random.uniform(0, 1.0) < sparseness:
                    self._grid[row][column] = Cell.BLOCKED

    def successors(self, ml: MazeLocation):
        locations: List[MazeLocation] = []

        # проверяем ячейку сверху от текущей
        if ml.row + 1 < self._rows and self._grid[ml.row + 1][ml.column] != Cell.BLOCKED:
            locations.append(MazeLocation(ml.row + 1, ml.column))

        # проверяем ячейку снизу от текущей
        if ml.row - 1 >= 0 and self._grid[ml.row - 1][ml.column] != Cell.BLOCKED:
            locations.append(MazeLocation(ml.row - 1, ml.column))

        # проверяем ячейку справа от текущей
        if ml.column + 1 < self._columns and self._grid[ml.row][ml.column + 1] != Cell.BLOCKED:
            locations.append(MazeLocation(ml.row, ml.column + 1))

        # проверяем ячейку слева от текущей
        if ml.column - 1 >= 0 and self._grid[ml.row][ml.column - 1] != Cell.BLOCKED:
            locations.append(MazeLocation(ml.row, ml.column - 1))

        return locations # возвращаем все возможные ходы из текущей ячейки

    # разметка лабиринта для красивого вывода
    def mark(self, path: List[MazeLocation], clear: bool = False) -> None:
        for maze_location in path:
            self._grid[maze_location.row][maze_location.column] = Cell.EMPTY if clear else Cell.PATH
            self._grid[self.start.row][self.start.column] = Cell.START
            self._grid[self.goal.row][self.goal.column] = Cell.GOAL

    def goal_test(self, ml: MazeLocation) -> bool:
        return ml == self.goal

    def __str__(self) -> str:
        output: str = ''
        for row in self._grid:
            output += ''.join([c.value for c in row]) + '\n'
        return output

# возвращает функцию вычисляющую расстояние по прямой до цели
def euclidean_distance(goal: MazeLocation) -> Callable[[MazeLocation], float]:
    def distance(ml: MazeLocation) -> float:
        xdist: int = ml.column - goal.column
        ydist: int = ml.row - goal.row
        return sqrt(xdist ** 2 + ydist ** 2)
    return distance

# возвращает функцию вычисляющую расстояние до цели в "ячеечном" пространстве
def manhattan_distance(goal: MazeLocation) -> Callable[[MazeLocation], float]:
    def distance(ml: MazeLocation) -> float:
        xdist: int = abs(ml.column - goal.column)
        ydist: int = abs(ml.row - goal.row)
        return (xdist + ydist)
    return distance

# тестирование лабиринта
if __name__ == '__main__':
    # DFS
    m: Maze = Maze()
    print('===== Original ======')
    print(m)

    # Тестирование DFS алгоритма
    solution1: Optional[Node[MazeLocation]] = dfs(m.start, m.goal_test, m.successors)
    if solution1 is None:
        print('No solution found using DFS!')
    else:
        path1: List[MazeLocation] = node_to_path(solution1)
        m.mark(path1)
        print('===== DFS ======')
        print(m)
        m.mark(path1, clear=True)

    # Тестирование BFS алгоритма
    solution2: Optional[Node[MazeLocation]] = dfs(m.start, m.goal_test, m.successors)
    if solution2 is None:
        print('No solution found using BFS!')
    else:
        path2: List[MazeLocation] = node_to_path(solution2)
        m.mark(path2)
        print('===== BFS ======')
        print(m)
        m.mark(path2, clear=True)

    # Тестирование A*
    distance: Callable[[MazeLocation], float] = manhattan_distance(m.goal)
    solution3: Optional[Node[MazeLocation]] = astar(m.start, m.goal_test, m.successors, distance)
    if solution3 is None:
        print('No solution found using A*!')
    else:
        path3: List[MazeLocation] = node_to_path(solution3)
        m.mark(path3)
        print('===== A* ======')
        print(m)
        m.mark(path3, clear=True)
from enum import Enum
from typing import List, NamedTuple, Callable, Optional
import random
from math import sqrt
# from generic_search import dfs, bfs, node_to_path, astar, Node


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

    def __str__(self) -> str:
        output: str = ''
        for row in self._grid:
            output += ''.join([c.value for c in row]) + '\n'
        return output


if __name__ == '__main__':
    maze: Maze = Maze()
    print(maze)

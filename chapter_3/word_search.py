from typing import NamedTuple, List, Dict, Optional
from random import choice
from string import ascii_uppercase
from csp import CSP, Constraint

Grid = List[List[str]] # псевдоним типа сетки

class GridLocation(NamedTuple):
    row: int
    column: int

def generate_grid(rows: int, columns: int) -> Grid:
    # инициализируем сетку случайными буквами
    return [[choice(ascii_uppercase) for c in range(columns)] for r in range(rows)]

def display_grid(grid: Grid) -> None:
    for row in grid:
        print(''.join(row))

def generate_domain(word: str, grid: Grid) -> List[List[GridLocation]]:
    domain: List[List[GridLocation]] = []
    height: int = len(grid)
    width: int = len(grid[0])
    length: int = len(word)

    for row in range(height):
        for col in range(width):
            columns: range = range(col, col + length + 1)
            rows: range = range(row, row + length + 1)
            if col + length <= width:
                # слева направо
                domain.append([GridLocation(row, c) for c in columns])
                # по диагонали снизу направо
                if row + length <= height:
                    domain.append([GridLocation(r, col + (r - row)) for r in rows])
            if row + length <= height:
                # сверху вниз
                domain.append([GridLocation(r, col) for r in rows])
                # по диагонали снизу налево
                if col - length >= 0:
                    domain.append([GridLocation(r, col - (r - row)) for r in rows])
    return domain


class WordSearchConstraint(Constraint[str, List[GridLocation]]):
    def __init__(self, words: List[str]):
        super().__init__(words)
        self.words: List[str] = words

    def satisfied(self, assignment: Dict[str, List[GridLocation]]) -> bool:
        # наличие дубликатов положений сетки означает наличие совпадения
        all_locations = [locs for values in assignment.values() for locs in values]
        return len(set(all_locations)) == len(all_locations)


if __name__ == '__main__':
    grid: Grid = generate_grid(9, 9)
    words: List[str] = ['MATTHEW', 'JOE', 'MARY', 'SARAH', 'SALLY']
    locations: Dict[str, List[List[GridLocation]]] = {}
    for word in words:
        locations[word] = generate_domain(word, grid)

    csp: CSP[str, List[GridLocation]] = CSP(words, locations)
    csp.add_constraint(WordSearchConstraint(words))
    solution: Optional[Dict[str, List[GridLocation]]] = csp.backtracking_search()
    if solution is None:
        print('No solution found!')
    else:
        for word, grid_locations in solution.items():
            # в половине случаев случайным выбором задом наперед
            if choice([True, False]):
                grid_locations.reverse()
            for index, letter in enumerate(word):
                (row, col) = (grid_locations[index].row, grid_locations[index].column)
                grid[row][col] = letter
        display_grid(grid)
from typing import List, Dict, Optional
from csp import CSP, Constraint

class QueensConstraint(Constraint[int, int]):
    def __init__(self, columns: List[int]):
        super().__init__(columns)
        self.columns: List[int] = columns

    def satisfied(self, assignment: Dict[int, int]) -> bool:
        # q1c - ферзь на первой вертикали
        # q1r - ферзь на первой горизонтали
        for q1c, q1r in assignment.items():
            # q2c - ферзь на второй вертикали
            for q2c in range(q1c + 1, len(self.columns) + 1):
                if q2c in assignment:
                    q2r: int = assignment[q2c] # ферзь на второй горизонтали
                    if q1r == q2r: # тот же ряд?
                        return False
                    if abs(q1r - q2r) == abs(q1c - q2c): # одна диагональ?
                        return False
        return True # нет конфликтов

if __name__ == '__main__':
    columns: List[int] = [1, 2, 3, 4, 5, 6, 7, 8]
    rows: Dict[int, List[int]] = {}
    for column in columns:
        rows[column] = [1, 2, 3, 4, 5, 6, 7, 8]
    csp: CSP[int, int] = CSP(columns, rows)
    csp.add_constraint(QueensConstraint(columns))
    solution: Optional[Dict[int, int]] = csp.backtracking_search()
    if solution is None:
        print('No solution found!')
    else:
        print(solution)
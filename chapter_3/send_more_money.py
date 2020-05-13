from csp import CSP, Constraint
from typing import Dict, List, Optional


class SendMoreMoneyConstraint(Constraint[str, int]):
    def __init__(self, letters: List[str]) -> None:
        super().__init__(letters)
        self.letters: List[str] = letters

    def satisfied(self, assignment: Dict[str, int]) -> bool:
        # если есть повторяющиеся значения, то решение не подходит
        # это красивый способ проверить есть ли повторяющиеся значения
        # set() вернет set в котором будут только уникальные значения из исходного листа
        # следовательно, если длина set меньше длины исходного листа
        # это значит, что в исходном листе есть повторяющиеся значения,
        # которые были проигнорированы при преобразовании листа в set
        if len(set(assignment.values())) < len(assignment):
            return False

        # если все переменные назначены, проверяем правильна ли сумма
        if len(assignment) == len(self.letters):
            s: int = assignment['S']
            e: int = assignment['E']
            n: int = assignment['N']
            d: int = assignment['D']
            m: int = assignment['M']
            o: int = assignment['O']
            r: int = assignment['R']
            y: int = assignment['Y']
            send: int = s * 1000 + e * 100 + n * 10 + d
            more: int = m * 1000 + o * 100 + r * 10 + e
            money: int = m * 10000 + o * 1000 + n * 100 + e * 10 + y
            return send + more == money
        return True


if __name__ == '__main__':
    letters: List[str] = ['S', 'E', 'N', 'D', 'M', 'O', 'R', 'Y']
    possible_digits: Dict[str, List[int]] = {}
    for letter in letters:
        possible_digits[letter] = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    possible_digits['M'] = [1] # мы не принимает ответы, начинающиеся с нуля
    csp: CSP[str, int] = CSP(letters, possible_digits)
    csp.add_constraint(SendMoreMoneyConstraint(letters))
    solution: Optional[Dict[str, int]] = csp.backtracking_search()
    if solution is None:
        print('No solution found!')
    else:
        print(solution)
        
            



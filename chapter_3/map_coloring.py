from csp import Constraint, CSP
from typing import Dict, List, Optional

class MapColoringConstraint(Constraint[str, str]):
    def __init__(self, place1: str, place2: str):
        super().__init__([place1, place2])
        self.place1: str = place1
        self.place2: str = place2

    def satisfied(self, assignment: Dict[str, str]) -> bool:
        # если какой-то регион placeN отсутствует в присваивании
        # то его цвета не могут привести к конфликту
        if self.place1 not in assignment or self.place2 not in assignment:
            return True
        # проверяем, совпадает ли цвет присвоенный place1 цвету place2
        return assignment[self.place1] != assignment[self.place2]

if __name__ == '__main__':
    # переменные в нашей задаче
    variables: List[str] = [
        'Western Australia',
        'Northern Territory',
        'South Australia',
        'Queensland',
        'New South Wales',
        'Victoria',
        'Tasmania'
    ]

    # области определения
    domains: Dict[str, List[str]] = {}
    for variable in variables:
        domains[variable] = ['red', 'green', 'blue']
    
    # описываем ограничения для нашей задачи
    csp: CSP[str, str] = CSP(variables, domains)
    csp.add_constraint(MapColoringConstraint('Western Australia', 'Northern Territory'))
    csp.add_constraint(MapColoringConstraint('Western Australia', 'South Australia'))
    csp.add_constraint(MapColoringConstraint('South Australia', 'Northern Territory'))
    csp.add_constraint(MapColoringConstraint('Queensland', 'Northern Territory'))
    csp.add_constraint(MapColoringConstraint('Queensland', 'South Australia'))
    csp.add_constraint(MapColoringConstraint('Queensland', 'New South Wales'))
    csp.add_constraint(MapColoringConstraint('New South Wales', 'South Australia'))
    csp.add_constraint(MapColoringConstraint('Victoria', 'South Australia'))
    csp.add_constraint(MapColoringConstraint('Victoria', 'New South Wales'))
    csp.add_constraint(MapColoringConstraint('Victoria', 'Tasmania'))

    # выполняем поиск решения
    solution: Optional[Dict[str, str]] = csp.backtracking_search()
    if solution is None:
        print('No solution found!')
    else:
        print(solution)